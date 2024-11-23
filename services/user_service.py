from db import get_db

def sign_up(name, email, password, date_of_birth):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO users (name, email, password, date_of_birth)
        VALUES (%s, %s, %s, %s)
    """, (name, email, password, date_of_birth))
    db.commit()
    cursor.close()
    return {"message": "Usuário cadastrado com sucesso"}

def login(email, password):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, name, balance FROM users WHERE email = %s AND password = %s
    """, (email, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return {"message": "Login bem-sucedido", "user": user}
    else:
        return {"message": "Email ou password incorretos"}
