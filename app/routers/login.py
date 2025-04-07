from fastapi import APIRouter, HTTPException
from app.models.login import LoginRequest
from app.db.connection import get_connection

router = APIRouter()

@router.post("/login")
def login_usuario(user: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                       SELECT id_usuario, nombre, apellido_paterno, apellido_materno, usuario
                       FROM usuarios
                       WHERE usuario = %s AND contrasena = %s
                       """, (user.usuario, user.contrasena))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        return {
            "message": "Inicio de sesión exitoso",
            "usuario": result
        }
    
    finally:
        cursor.close()
        conn.close()
