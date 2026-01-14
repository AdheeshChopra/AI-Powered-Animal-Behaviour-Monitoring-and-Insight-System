// arduino/imu_temp_sensor.ino
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 sensor!");
    while (1) { delay(10); }
  }
  // Configure ranges (optional)
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("MPU6050 initialized.");
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  // Print in CSV format: ax,ay,az,gx,gy,gz,temperature
  Serial.print(a.acceleration.x); Serial.print(',');
  Serial.print(a.acceleration.y); Serial.print(',');
  Serial.print(a.acceleration.z); Serial.print(',');
  Serial.print(g.gyro.x); Serial.print(',');
  Serial.print(g.gyro.y); Serial.print(',');
  Serial.print(g.gyro.z); Serial.print(',');
  Serial.println(temp.temperature);
  delay(100); // 10 Hz output
}
