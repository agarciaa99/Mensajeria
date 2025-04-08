from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.models.login import LoginRequest
from app.db.connection import get_connection
import random

router = APIRouter()

@router.post("/registro")
def registrar_usuario(user: Usuario):
    # Generar nombre de usaurio
    usuario_generado = (
        user.nombre[:3] + 
        user.apellido_paterno[:3] +
        user.apellido_materno[:3]
    ).capitalize()

    # Generar contraseña
    numeros = random.randint(100, 999)
    contrasena_generada = f"{user.nombre}{numeros}"


    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si el usuario ya existe
        # cursor.execute("SELECT * FROM Usuarios WHERE usuario = %s", (usuario_generado,))
        # if cursor.fetchone():
        #     raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        
        # Guardar datos
        cursor.execute("""
                       INSERT INTO Usuarios (nombre, apellido_paterno, apellido_materno, usuario, contrasena)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (user.nombre, user.apellido_paterno, user.apellido_materno, usuario_generado, contrasena_generada))
        conn.commit()

        return {
            "message": "Usuario registrado exitosamente",
            "usuario": usuario_generado,
            "contrasena": contrasena_generada
        }
    
    finally:
        cursor.close()
        conn.close()

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