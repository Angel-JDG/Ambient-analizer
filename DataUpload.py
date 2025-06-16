import serial
import time
import mysql.connector


print("Intentando abrir el puerto serial...")

try:
    ser = serial.Serial('COM3', 115200)
    time.sleep(2)
    print("Puerto abierto correctamente. Escuchando datos...\n")
    db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Akyra1102.",
    database="Datos"
    )
    cursor = db.cursor()


    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Datos recibidos:", line)
            try:
                datos = dict(item.split(":") for item in line.split(";"))
                humedad = float(datos["H"])
                temperatura = float(datos["T"])
                co = int(datos["CO"])
                print(f"Humedad: {humedad} %, Temperatura: {temperatura} °C, CO (monóxido de carbono): {co}")
                # Insertar en la base de datos
                query = "INSERT INTO datos_sensores (humedad, temperatura, co) VALUES (%s, %s, %s)"
                valores = (humedad, temperatura, co)
                cursor.execute(query, valores)
                db.commit()
                print("Datos guardados en la base de datos.")
            except Exception as e:
                print("Error al procesar datos:", e)

except Exception as e:
    print("Error al abrir el puerto serial:", e)