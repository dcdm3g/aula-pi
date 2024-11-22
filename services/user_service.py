# services/user_service.py
from db import get_db

def sign_up(nome, email, senha, data_nascimento):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha, data_nascimento)
        VALUES (%s, %s, %s, %s)
    """, (nome, email, senha, data_nascimento))
    db.commit()
    cursor.close()
    return {"message": "Usuário cadastrado com sucesso"}

def login(email, senha):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nome, saldo FROM usuarios WHERE email = %s AND senha = %s
    """, (email, senha))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return {"message": "Login bem-sucedido", "user": user}
    else:
        return {"message": "Email ou senha incorretos"}
