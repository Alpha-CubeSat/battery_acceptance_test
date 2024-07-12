#include <Adafruit_INA219.h>
#include <Wire.h>

Adafruit_INA219 ina219;

// TMP36 Pin Variables
int sensorPin = A0; // The analog pin the TMP36's Vout (sense) pin is connected to
                    // The resolution is 10 mV / degree centigrade with a
                    // 500 mV offset to allow for negative temperatures

void setup()
{
  Serial.begin(115200);  // Start the serial connection with the computer
                         // To view the result, open the serial monitor

  // Initialize TMP36 sensor
  pinMode(sensorPin, INPUT);

  // Initialize INA219 sensor
  if (!ina219.begin()) {
    Serial.println("Failed to find INA219 chip");
    while (1) { delay(10); }
  }

  Serial.println("Measuring voltage and current with INA219 ...");
}

void loop() 
{
  // TMP36 temperature sensor reading
  int reading = analogRead(sensorPin);  
  float voltage = reading * 5.0;
  voltage /= 1024.0; 

  float temperatureC = (voltage - 0.5) * 100;  // Converting from 10 mV per degree with 500 mV offset
                                               // to degrees ((voltage - 500mV) times 100)
  Serial.print("Temperature: "); Serial.print(temperatureC); Serial.println(" C");

  // INA219 sensor reading
  float busvoltage = 0;
  float current_mA = 0;

  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  
  Serial.print("Bus Voltage: "); Serial.print(busvoltage); Serial.println(" V");
 
  Serial.print("Current: "); Serial.print(current_mA); Serial.println(" mA");

  Serial.println("");

  delay(2000);  // Waiting 2 seconds before the next loop
}
