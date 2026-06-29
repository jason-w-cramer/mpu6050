# MPU6050 Position Data Driver
This is a driver I am writing to learn about the MPU6050 and about filters for getting position data. There will be 4 or 5 different methods using the mpu6050 to calculate the position of the sensor with varying amounts of complexity. The core of this driver is copied from leech001's driver.

## Method 1: Rotational Matricies
The first few methods will be using this guide: https://www.nxp.com/docs/en/application-note/AN3461.pdf

In the link above it explains much better than I can how to get the functions to calculate pitch and roll from the accelerometers alone. 

Roll = atan2(Ay/Az)
Pitch = atan2(-Ax/sqrt(Ay^2 + Az^2))

Pros:
- Doesn't drift over time
  
Cons:
- Noisy
- Prone to large errors in roll when pitch is close to 90 degrees
- Only accurate when sensor is stationary

## Method 2: Method 1 with Approximation
To fix the roll error when both Ay and Az are very close to 0 (pitch~=90), we can add in an Ax term. This gives us a very good approximation of the angle while fixing the large errors when pitch is close to 90. The error graph for u=0.01 can be seen in the article linked in Method 1. In my own testing of this method I found it to be an unreliable approximation due to rapidly changing signs when Az was close to 0.

Roll = atan2(Ay/Az_sign * sqrt(Az^2+u*Ax^2))

Pros:
- Fixes error around pitch = 90 degrees in theory
  
Cons:
- Same cons as method one (except errors around 90 degree pitch)
- In my testing I found it to be just as if not even more unreliable due to the sign of Az flipping rapidly when Az was close to 0

## Method 3: Gyroscope Integration
Given that gyroscopes return angular acceleration, it is easy to calculate angular position by taking the double integral of this data.

Pros:
- Fast angle calculation
- Less error from accelerating and decelerating sensor
- Accurate over short periods of time
  
Cons:
- Has drift

## Method 4: Complementary Filter (Gyroscope + Accelerometer)
Explained really well here: https://www.youtube.com/watch?v=whSw42XddsU

Pros:
- Fast angle calculation
- Low noise
- Accurate over long and short periods of time

Cons: 
- Harder to implement
- Requires 2x ammount of sensors as previous method
