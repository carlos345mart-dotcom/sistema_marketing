def generar_recomendacion(alcance, interacciones, conversiones, costo):

    if alcance == 0:
        return "No hay datos suficientes"

    tasa_conversion = (conversiones / alcance) * 100
    engagement = (interacciones / alcance) * 100

    if tasa_conversion > 5:
        return "Estrategia efectiva, mantener enfoque actual"
    
    elif engagement < 2:
        return "Bajo engagement, usar contenido más atractivo (videos o imágenes)"
    
    elif costo > 1000:
        return "Alto costo, optimizar inversión en campañas"
    
    else:
        return "Se recomienda ajustar horario y segmentación"