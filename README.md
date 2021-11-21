# ves-pi
Telemetry collection and MQTT signaling for vintage vespa scooters
Data captured:
* Engine RPM's
* Cylinder Head Temperature (CHT), degrees F
* Exhaust Gas Temperature (EGT), degress F
* Throttle Position (0-100%)
* Current Gear (1-0-2-3-4)
* Clutch status (in/out of gear)
* GPS:
    * Speed (MPH)
    * Postion (Lat/Long)
* Acceleration


Pinout (Incomplete)

|   |     |Pin|Pin|   |     |      |
|---|---:|---:|---|---|-----|------|
|BUS     |          3v3 |1 |2 |5v |       |    |
|A2D SDA |GPIO2/I2C1 SDA|3 |4 |5v               |    |
|A2D SCL |GPIO3/I2C1 SCL|5 |6 |Ground           | |
|        |GPIO4 (GPCLK0)|7 |8 |GPIO 14 (UART TX)|GPS TXD|
|        |GROUND        |9 |10*|GPIO 15 (UART RX)|GPS RXD|
| |GPIO17|11|12*|GPIO18 (PCM Clk)||
| |GPIO27|13|14|Ground||
| |GPIO22|15|16|GPIO23||
| |3v3|17|18*|GPIO24||
| |GPIO10 (SPI0 MOSI)|19|20|Ground||
|Thermal DO |GPIO9 (SPI0 MISO) |21*|22|GPIO25||
|Thermal CLK |GPIO11 (SPI0 SCLK)|23|24|GPIO8 (SPI0 CE0)||
| |Ground            |25|26|GPIO7 (SPI0 CE1)||
| |GPIO0 (EEPROM SDA)|27|28|GPIO1 (EEPROM SCL)||
|Thermal CS |GPIO5             |29|30|Ground||
| |GPIO6             |31|22|GPIO12 (PWM0)||
| |GPIO13 (PWM1)     |33|22|Ground| BUS|
| |GPIO19 (PCM FS)   |35|22|GPIO16|Tach Trigger (Generic GPIO)|
| |GPIO26            |37|22|GPIO20 (PCM DIN) ||
| |Ground            |39|22|GPIO21 (PCM DOUT)||
