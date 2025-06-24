import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

def generar_estadisticas(df):
    resumen = {
        "promedio": df.mean(),
        "maximo": df.max(),
        "minimo": df.min()
    }

    recomendaciones = []

    temperatura = resumen["promedio"]["temperatura"]
    humedad = resumen["promedio"]["humedad"]
    co = resumen["promedio"]["co"]

    if temperatura > 30:
        recomendaciones.append("Temperatura elevada. Evita actividades físicas intensas y mantente hidratado.")
    elif temperatura < 18:
        recomendaciones.append("Temperatura baja. Usa ropa adecuada para evitar hipotermia.")

    if humedad > 70:
        recomendaciones.append("Alta humedad. Aumenta el riesgo de hongos. Ventila el ambiente.")
    elif humedad < 30:
        recomendaciones.append("Humedad baja. Puede causar resequedad en piel y mucosas. Usa humidificadores.")

    if co > 800:
        recomendaciones.append("Nivel muy alto de CO. Riesgo severo de intoxicación. Evacuar inmediatamente.")
        recomendaciones.append("No exponerse más de 10 minutos.")
    elif co > 400:
        recomendaciones.append("CO peligrosamente alto. Puede causar síntomas severos en poco tiempo.")
        recomendaciones.append("No exponerse más de 30 minutos. Ventila el área y usa protección respiratoria.")
    elif co > 200:
        recomendaciones.append("Nivel alto de monóxido de carbono. Causa dolor de cabeza tras 2–3 horas.")
        recomendaciones.append("No exponerse más de 1 hora. Verifica fuentes de combustión.")
    elif co > 100:
        recomendaciones.append("Nivel moderado de CO. Riesgo leve tras exposición prolongada.")
        recomendaciones.append("Limitar exposición a menos de 2 horas. Asegurar ventilación.")
    elif co > 50:
        recomendaciones.append("CO levemente elevado. Puede afectar a personas sensibles.")
        recomendaciones.append("Evitar exposición prolongada (>8 horas). Mantén buena ventilación.")
    else:
        recomendaciones.append("Nivel de CO en rango aceptable.")
        recomendaciones.append("Seguro para exposición continua en interiores bien ventilados.")

    return resumen, recomendaciones

def agregar_fechas_pdf(pdf, df):
    fecha_inicio = df["fecha"].iloc[0]
    fecha_fin = df["fecha"].iloc[-1]
    fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    pdf.cell(0, 10, f"Datos del {fecha_inicio} al {fecha_fin}", ln=True, align="C")
    pdf.cell(0, 10, f"Reporte generado: {fecha_generacion}", ln=True, align="C")
    pdf.ln(5)

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Akyra1102.",
    database="Datos"
)

df_general = pd.read_sql("SELECT fecha, humedad, temperatura, co FROM Datos_sensores ORDER BY fecha", conexion)

resumen_general, recomendaciones_general = generar_estadisticas(df_general)

plt.figure(figsize=(12, 6))
plt.plot(df_general["fecha"], df_general["humedad"], label="Humedad")
plt.plot(df_general["fecha"], df_general["temperatura"], label="Temperatura")
plt.plot(df_general["fecha"], df_general["co"], label="CO")
plt.legend()
plt.title("Reporte General")
plt.xlabel("Fecha")
plt.ylabel("Valores")
plt.tight_layout()
plt.savefig("grafica_general.png")
plt.close()

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Reporte General de Sensores", ln=True, align="C")
pdf.ln(5)

agregar_fechas_pdf(pdf, df_general)

pdf.image("grafica_general.png", x=10, y=50, w=190)
pdf.ln(110)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, f"Temperatura promedio: {resumen_general['promedio']['temperatura']:.2f} °C", ln=True)
pdf.cell(0, 10, f"Humedad promedio: {resumen_general['promedio']['humedad']:.2f} %", ln=True)
pdf.cell(0, 10, f"CO promedio: {resumen_general['promedio']['co']:.2f}", ln=True)

pdf.cell(0, 10, f"Temperatura máxima: {resumen_general['maximo']['temperatura']:.2f} °C", ln=True)
pdf.cell(0, 10, f"Humedad máxima: {resumen_general['maximo']['humedad']:.2f} %", ln=True)
pdf.cell(0, 10, f"CO máximo: {resumen_general['maximo']['co']}", ln=True)

pdf.cell(0, 10, f"Temperatura mínima: {resumen_general['minimo']['temperatura']:.2f} °C", ln=True)
pdf.cell(0, 10, f"Humedad mínima: {resumen_general['minimo']['humedad']:.2f} %", ln=True)
pdf.cell(0, 10, f"CO mínimo: {resumen_general['minimo']['co']}", ln=True)

pdf.ln(10)
pdf.cell(0, 10, "Recomendaciones:", ln=True)
for rec in recomendaciones_general:
    pdf.multi_cell(0, 10, f"- {rec}")

pdf.output("reporte_general.pdf")

inicio = int(input("¿Desde qué registro deseas empezar el reporte personalizado? (Ej: 50): "))
fin = int(input("¿Hasta qué registro deseas finalizar el reporte personalizado? (Ej: 150): "))
cantidad = fin - inicio
query_personalizado = f"""
    SELECT fecha, humedad, temperatura, co 
    FROM Datos_sensores 
    ORDER BY fecha 
    LIMIT {cantidad} OFFSET {inicio}
"""
df_personal = pd.read_sql(query_personalizado, conexion) 
resumen_personal, recomendaciones_personal = generar_estadisticas(df_personal)

plt.figure(figsize=(12, 6))
plt.plot(df_personal["fecha"], df_personal["humedad"], label="Humedad")
plt.plot(df_personal["fecha"], df_personal["temperatura"], label="Temperatura")
plt.plot(df_personal["fecha"], df_personal["co"], label="CO")
plt.legend()
plt.title("Reporte Personalizado")
plt.xlabel("Fecha")
plt.ylabel("Valores")
plt.tight_layout()
plt.savefig("grafica_personalizada.png")
plt.close()

pdf2 = FPDF()
pdf2.add_page()
pdf2.set_font("Arial", "B", 16)
pdf2.cell(0, 10, f"Reporte Personalizado de los registros {inicio} a {fin}", ln=True, align="C")
pdf2.ln(5)

agregar_fechas_pdf(pdf2, df_personal)

pdf2.image("grafica_personalizada.png", x=10, y=50, w=190)
pdf2.ln(110)

pdf2.set_font("Arial", size=12)
pdf2.cell(0, 10, f"Temperatura promedio: {resumen_personal['promedio']['temperatura']:.2f} °C", ln=True)
pdf2.cell(0, 10, f"Humedad promedio: {resumen_personal['promedio']['humedad']:.2f} %", ln=True)
pdf2.cell(0, 10, f"CO promedio: {resumen_personal['promedio']['co']:.2f}", ln=True)

pdf2.cell(0, 10, f"Temperatura máxima: {resumen_personal['maximo']['temperatura']:.2f} °C", ln=True)
pdf2.cell(0, 10, f"Humedad máxima: {resumen_personal['maximo']['humedad']:.2f} %", ln=True)
pdf2.cell(0, 10, f"CO máximo: {resumen_personal['maximo']['co']}", ln=True)

pdf2.cell(0, 10, f"Temperatura mínima: {resumen_personal['minimo']['temperatura']:.2f} °C", ln=True)
pdf2.cell(0, 10, f"Humedad mínima: {resumen_personal['minimo']['humedad']:.2f} %", ln=True)
pdf2.cell(0, 10, f"CO mínimo: {resumen_personal['minimo']['co']}", ln=True)

pdf2.ln(10)
pdf2.cell(0, 10, "Recomendaciones:", ln=True)
for rec in recomendaciones_personal:
    pdf2.multi_cell(0, 10, f"- {rec}")

pdf2.output("reporte_personalizado.pdf")

conexion.close()
