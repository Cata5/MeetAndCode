
//Libraies: DHT11,Adafruit SSD1306!!!!!!!!
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
 // Change this to the pin where your DHT11 sensor is connected
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define gasSensorPin1 A0
#define gasSensorPin2 7
// #define  dustSensorPin A5
int UVOUT = A1; //Output from the sensor
int REF_3V3 = A2; //3.3V power on the Arduino board

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
DHT dht(3, DHT11); //Temp/Humid module
SoftwareSerial bluetooth(0,1);
void setup() {
  Serial.begin(115200);
  //bluetooth.begin(9600);
  display.clearDisplay();
  display.setTextColor(WHITE);
  dht.begin();
  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }

 
}

int gasSensor(){
  int gasSensorValueAnalog = analogRead(gasSensorPin1);
  int gasSensorValueDigital = digitalRead(gasSensorPin2);
  display.setCursor(0, 10);
  display.print("Gas Detect:  ");
  display.println(gasSensorValueAnalog,DEC);
  display.display();
}
// int UVsensor(){
//   int uvLevel = analogRead(UVOUT);
//   int refLevel = analogRead(REF_3V3);
//   float outputVoltage = 3.3 / refLevel * uvLevel;
//   float uvIntensity = map(outputVoltage, 0.99, 2.8, 0.0, 15.0);
//   display.setCursor(0, 29);
//   display.print(uvLevel);
//   display.println("mW/m^2");
//   display.display();
// }

// int Dust(){
//   int dustValue = analogRead(dustPin);
//   Serial.print("Dust Value: ");
//   Serial.println(dustValue);

// }
int Temp_Humid(){
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

   if (isnan(humidity) || isnan(temperature)) {
    display.println("Failed to read from DHT sensor!");
  } else {
    
    display.setCursor(0, 19);
    display.print("Hum: ");
    display.print(humidity);
    display.println("%");
    display.print("Temp: ");
    display.print(temperature);
    display.println("C");
    display.display();

    Serial.println("");
    Serial.print("Hum: ");
    Serial.print(humidity);
    Serial.print("%, ");
    Serial.print("Temp: ");
    Serial.print(temperature);
    Serial.println("C");
  }
}

void loop() {
  Temp_Humid();
  delay(250);
  display.clearDisplay();
}


