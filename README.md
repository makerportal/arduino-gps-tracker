# arduino-gps-datalogger
Arduino GPS datalogger with ATGM336H module, SD card module, and ATSAMD21 microcontroller.

Get an ATGM336H GPS module here: [ATGM336H Module](https://makersportal.com/shop/) <br>
See full tutorial here: [Mini GPS Datalogger with Arduino](https://makersportal.com/blog/) <br>

# 
### JUMP TO:
<a href="#wiring">- Wiring Diagram</a><br>
<a href="#arduino">- Arduino Codes</a><br>
<a href="#python">- Python Scripts</a><br>

The arduino-gps-datalogger library can be downloaded using git:

    git clone https://github.com/makerportal/arduino-gps-datalogger

<a id="wiring"></a>
# - Wiring Diagram -
Here, we are wiring the ATGM336H GPS module via SPI to the Arduino Xiao (ATSAMD21) board:

![ATGM336H wiring to ATSAMD21](/images/atgm336h_datalogger_wiring.jpg)

![ATGM336H wiring to ATSAMD21 - table](/images/atgm336h_datalogger_wiring_table.jpg)

<a id="arduino"></a>
# - Arduino Code -
The Arduino code used to log GPS data is found at:

- [gps_datalogger.ino](/arduino/gps_datalogger.ino)

<a id="python"></a>
# - Python Scripts -
The Python scripts used to parse the GPS coordinates from the .csv log file and plot them atop a street map can be found at:

- [gps_mapper.py](/python/gps_mapper.py)
