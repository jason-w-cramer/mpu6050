import serial
import csv
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from datetime import datetime
from collections import deque
import threading

PORT = 'COM10'
BAUD = 115200
OUTPUT_FILE = 'imu_log.csv'
MAX_POINTS = 200

times = deque(maxlen=MAX_POINTS)
Ax_buf = deque(maxlen=MAX_POINTS)
Ay_buf = deque(maxlen=MAX_POINTS)
Az_buf = deque(maxlen=MAX_POINTS)
Gx_buf = deque(maxlen=MAX_POINTS)
Gy_buf = deque(maxlen=MAX_POINTS)
Gz_buf = deque(maxlen=MAX_POINTS)
AngleX_buf = deque(maxlen=MAX_POINTS)
AngleY_buf = deque(maxlen=MAX_POINTS)

ser = serial.Serial(PORT, BAUD, timeout=1)
import time
time.sleep(2)

csvfile = open(OUTPUT_FILE, 'w', newline='')
writer = csv.writer(csvfile)
writer.writerow(['timestamp', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz', 'AngleX', 'AngleY'])

def serial_reader():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue
            values = {}
            for part in line.split():
                key, val = part.split(':')
                values[key] = float(val)
            times.append(datetime.now().timestamp())
            Ax_buf.append(values['Ax'])
            Ay_buf.append(values['Ay'])
            Az_buf.append(values['Az'])
            Gx_buf.append(values['Gx'])
            Gy_buf.append(values['Gy'])
            Gz_buf.append(values['Gz'])
            AngleX_buf.append(values['AngleX'])
            AngleY_buf.append(values['AngleY'])
            writer.writerow([datetime.now().isoformat(),
                             values['Ax'], values['Ay'], values['Az'],
                             values['Gx'], values['Gy'], values['Gz'],
                             values['AngleX'], values['AngleY']])
            csvfile.flush()
        except (ValueError, KeyError):
            continue
        except Exception as e:
            print(f"Serial error: {e}")
            break

thread = threading.Thread(target=serial_reader, daemon=True)
thread.start()

app = QtWidgets.QApplication([])

win = pg.GraphicsLayoutWidget(title="IMU Live Plot")
win.resize(1000, 900)

p1 = win.addPlot(title="Accelerometer (g)")
win.nextRow()
p2 = win.addPlot(title="Gyroscope (deg/s)")
win.nextRow()
p3 = win.addPlot(title="Angles (deg)")

p1.setYRange(-2, 2)
p2.setYRange(-250, 250)
p3.setYRange(-180, 180)
p1.addLegend()
p2.addLegend()
p3.addLegend()

curve_ax = p1.plot(pen='r', name='Ax')
curve_ay = p1.plot(pen='g', name='Ay')
curve_az = p1.plot(pen='b', name='Az')
curve_gx = p2.plot(pen='r', name='Gx')
curve_gy = p2.plot(pen='g', name='Gy')
curve_gz = p2.plot(pen='b', name='Gz')
curve_anglex = p3.plot(pen='c', name='AngleX')
curve_angley = p3.plot(pen='m', name='AngleY')

def update():
    t = list(times)
    ax = list(Ax_buf)
    ay = list(Ay_buf)
    az = list(Az_buf)
    gx = list(Gx_buf)
    gy = list(Gy_buf)
    gz = list(Gz_buf)
    anglex = list(AngleX_buf)
    angley = list(AngleY_buf)

    n = min(len(t), len(ax), len(ay), len(az),
            len(gx), len(gy), len(gz),
            len(anglex), len(angley))
    if n < 2:
        return

    t = t[:n]
    t0 = t[0]
    t_rel = [x - t0 for x in t]

    curve_ax.setData(t_rel, ax[:n])
    curve_ay.setData(t_rel, ay[:n])
    curve_az.setData(t_rel, az[:n])
    curve_gx.setData(t_rel, gx[:n])
    curve_gy.setData(t_rel, gy[:n])
    curve_gz.setData(t_rel, gz[:n])
    curve_anglex.setData(t_rel, anglex[:n])
    curve_angley.setData(t_rel, angley[:n])

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

win.show()

try:
    app.exec()
except KeyboardInterrupt:
    pass
finally:
    ser.close()
    csvfile.close()
    print("Closed.")