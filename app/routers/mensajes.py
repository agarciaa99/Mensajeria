from fastapi import APIRouter, HTTPException
from app.models.mensajes import MensajeBase
from app.db.connection import get_connection

router = APIRouter()

@router.post("/enviar")
def enviar_mensaje(mensaje: MensajeBase):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                       INSERT INTO mensajes (id_emisor, id_receptor, contenido)
                       VALUES (%s, %s, %s)
                       """, (mensaje.id_emisor, mensaje.id_receptor, mensaje.contenido))
        
        conn.commit()
        return {"message": "Mensaje enviado exitosamente"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

@router.get("/recibidos/{id_usuario}")
def obtener_mensajes_recibidos(id_usuario: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                       SELECT m.id_mensaje, m.contenido, m.id_emisor, u.nombre AS emisor
                       FROM mensajes m
                       JOIN usuarios u ON m.id_emisor = u.id_usuario
                       WHERE m.id_receptor = %s
                       """, (id_usuario,))
       
        mensajes = cursor.fetchall()
        return mensajes
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

@router.get("/conversacion/{usuario1_id}/{usuario2_id}")
def obtener_conversacion(usuario1_id: int, usuario2_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT m.id_mensaje, m.contenido, u.nombre AS emisor
            FROM mensajes m
            JOIN usuarios u ON m.id_emisor = u.id_usuario
            WHERE (m.id_emisor = %s AND m.id_receptor = %s)
               OR (m.id_emisor = %s AND m.id_receptor = %s)
            ORDER BY m.id_mensaje ASC
        """, (usuario1_id, usuario2_id, usuario2_id, usuario1_id))

        mensajes = cursor.fetchall()
        return mensajes

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
