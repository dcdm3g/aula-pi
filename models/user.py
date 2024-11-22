# models/user.py
from db import get_db

class User:
    def __init__(self, id, nome, email, senha, data_nascimento, saldo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nascimento = data_nascimento
        self.saldo = saldo

    @classmethod
    def get_user_by_id(cls, user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        return cls(**user_data) if user_data else None

    @classmethod
    def get_user_by_email(cls, email):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        return cls(**user_data) if user_data else None

    @classmethod
    def create(cls, nome, email, senha, data_nascimento):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, data_nascimento)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, senha, data_nascimento))
        db.commit()
        cursor.close()
        return cls(cursor.lastrowid, nome, email, senha, data_nascimento)

    @classmethod
    def authenticate(cls, email, senha):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, saldo FROM usuarios WHERE email = %s AND senha = %s
        """, (email, senha))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return cls(user_data['id'], user_data['nome'], email, senha, user_data['saldo'])
        return None

    def add_funds(self, valor):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET saldo = saldo + %s WHERE id = %s", (valor, self.id))
        db.commit()
        cursor.close()

    def withdraw_funds(self, valor):
        if self.saldo >= valor:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE usuarios SET saldo = saldo - %s WHERE id = %s", (valor, self.id))
            db.commit()
            cursor.close()
            return True
        return False

    def bet_on_event(self, event, valor):
        if self.saldo >= valor:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE usuarios SET saldo = saldo - %s WHERE id = %s", (valor, self.id))
            cursor.execute("""
                INSERT INTO apostas (usuario_id, evento_id, valor)
                VALUES (%s, %s, %s)
            """, (self.id, event.id, valor))
            db.commit()
            cursor.close()
            return True
        return False