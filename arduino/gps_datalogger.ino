/***************************************************************************
* Arduino Xiao GPS Datalogger 
* -- using ATGM336H + SD Module
*
* 
*  by Josh Hrisko | Maker Portal LLC (c) 2021
* 
* 
***************************************************************************/
#include <SPI.h>
#include <SD.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

const int chipSelect = 6; // chip select for SD module
String filename = "gpsLog.csv"; // filename for saving to SD card

static const int RXPin = 2, TXPin = 1; // pins for ATGM336H GPS device
static const uint32_t GPSBaud = 9600; // default baudrate of ATGM336H GPS device

TinyGPSPlus gps;
SoftwareSerial ss(TXPin, RXPin);

void setup() {
  Serial.begin(9600); // start serial monitor for debugging
  ss.begin(GPSBaud);
  
  if (!SD.begin(chipSelect)) { // verify SD card and module are working
    Serial.println("SD Card not found"); 
    while (1);
  }

  if (SD.exists(filename)) {
    SD.remove(filename); // delete file if it already exists
  }
 
  data_saver("Date [mm/dd/yyyy], Time [HH:MM:SS.ZZ], Latitude [deg], Longitude [deg]"); // save data header
  
}

void loop() {
  while (ss.available() > 0){
    if (gps.encode(ss.read()) && gps.location.isValid() && gps.date.isValid() && gps.time.isValid()){
      String data_to_save = ""; // data string for saving
      data_to_save += String(gps.date.month())+"/"+String(gps.date.day())+"/"+
                      String(gps.date.year())+",";
      data_to_save += String(gps.time.hour())+":"+String(gps.time.minute())+":"+
                      String(gps.time.second())+"."+String(gps.time.centisecond())+",";
      data_to_save += String(gps.location.lat(),8)+","; // latitude
      data_to_save += String(gps.location.lng(),8); // longitude
      
      data_saver(data_to_save); // save new data points

//      Serial.println(data_to_save); // uncomment to print GPS data
    }
  }

}

void data_saver(String WriteData){ // data saver function
  File dataFile = SD.open(filename, FILE_WRITE); // open/create file
  if (dataFile) {
    dataFile.println(WriteData); // write data to file
    dataFile.close(); // close file before continuing
  } else {
    delay(50); // prevents cluttering
    Serial.println("SD Error"); // print error if SD card issue
  }

}
