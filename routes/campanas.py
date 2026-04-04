from flask import Blueprint, request, redirect, render_template
from database.conexion import conectar
from models.recomendacion import generar_recomendacion

campanas_bp = Blueprint('campanas', __name__)

# GUARDAR CAMPAÑA + MÉTRICAS
@campanas_bp.route('/guardar', methods=['POST'])
def guardar():

    nombre = request.form['nombre']
    tipo = request.form['tipo']
    alcance = int(request.form['alcance'])
    interacciones = int(request.form['interacciones'])
    conversiones = int(request.form['conversiones'])
    costo = float(request.form['costo'])

    conexion = conectar()
    cursor = conexion.cursor()

    # Insertar campaña (usuario fijo por ahora)
    cursor.execute("INSERT INTO campañas (nombre, tipo, fecha, id_usuario) VALUES (%s,%s,NOW(),1)", (nombre, tipo))
    id_campaña = cursor.lastrowid

    # Insertar métricas
    cursor.execute("""
        INSERT INTO metricas (id_campaña, alcance, interacciones, conversiones, costo)
        VALUES (%s,%s,%s,%s,%s)
    """, (id_campaña, alcance, interacciones, conversiones, costo))

    conexion.commit()

    return redirect('/dashboard')


# DASHBOARD CON ANÁLISIS
@campanas_bp.route('/dashboard')
def ver_dashboard():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT c.id, c.nombre, m.alcance, m.interacciones, m.conversiones, m.costo
        FROM campañas c
        JOIN metricas m ON c.id = m.id_campaña
    """)

    datos = cursor.fetchall()

    resultados = []

    for d in datos:
        id_campaña = d[0]
        nombre = d[1]
        alcance = d[2]
        interacciones = d[3]
        conversiones = d[4]
        costo = d[5]

        tasa_conversion = (conversiones / alcance) * 100 if alcance > 0 else 0
        engagement = (interacciones / alcance) * 100 if alcance > 0 else 0

        recomendacion = generar_recomendacion(alcance, interacciones, conversiones, costo)

        resultados.append((
            nombre,
            alcance,
            interacciones,
            conversiones,
            costo,
            round(tasa_conversion, 2),
            round(engagement, 2),
            recomendacion
        ))

    return render_template('dashboard.html', datos=resultados)