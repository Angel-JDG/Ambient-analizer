# Ambient-analizer

The ambient analyser system uses sensors, an Arduino controller, Python scripts in VScode and a MySQL database. The system's objective is to take data from the Arduino IDE and send it to a Python script to connect and upload the data to the SQL database. After that, another Python script creates the graphics, performs the data analysis and generates the PDF file to display in HTML.

**Sensors:**
- DHT22 (temperature and humidity).
- MQ-7 (CO carbon Monoxide).
  
**Microcontroller**
- Arduino UNO R3.
  
**Softwares**
- VSCode.
- Arduino IDE.
- MySQL Workbench.
- MySQL Server.

**Programming lenguages**
- Python.
- C++ (Arduino IDE coding)

The SQL  database only work withe the personal database configurations, with ur own database.
database tables structure:
primary key: star in number 1
first column: date
second column: humidity
thirt column: temperature
fourth column: carbon monoxide (gas ppms)
