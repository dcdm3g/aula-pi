# models/event.py
from db import get_db

class Event:
    def __init__(self, id, titulo, descricao, data_evento, cota_valor, status='aguardando', criado_por=None, resultado=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data_evento = data_evento
        self.cota_valor = cota_valor
        self.status = status
        self.criado_por = criado_por
        self.resultado = resultado 

    @classmethod
    def create(cls, titulo, descricao, data_evento, cota_valor, criado_por):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO eventos (titulo, descricao, data_evento, cota_valor, criado_por)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descricao, data_evento, cota_valor, criado_por))
        db.commit()
        event_id = cursor.lastrowid
        cursor.close()
        return cls(event_id, titulo, descricao, data_evento, cota_valor, 'aguardando', criado_por)

    @classmethod
    def get_events_by_status(cls, status):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eventos WHERE status = %s", (status,))
        events_data = cursor.fetchall()
        cursor.close()
        return [cls(**event) for event in events_data]

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE eventos SET status = 'ocorrido'
            WHERE id = %s AND criado_por = %s AND status = 'aguardando'
        """, (self.id, self.criado_por))
        db.commit()
        cursor.close()

    @classmethod
    def get_event_by_id(cls, event_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eventos WHERE id = %s", (event_id,))
        event_data = cursor.fetchone()
        cursor.close()
        return cls(**event_data) if event_data else None

    def evaluate(self, status):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE eventos SET status = %s WHERE id = %s", (status, self.id))
        db.commit()
        cursor.close()

    def finish(self, resultado):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE eventos SET resultado = 'finalizado', resultado = %s WHERE id = %s", (resultado, self.id))
        db.commit()
        cursor.close()

    @classmethod
    def search_by_keyword(cls, keyword):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eventos WHERE titulo LIKE %s OR descricao LIKE %s", (f'%{keyword}%', f'%{keyword}%'))
        events_data = cursor.fetchall()
        cursor.close()
        return [cls(**event) for event in events_data]

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data_evento": self.data_evento,
            "cota_valor": self.cota_valor,
            "status": self.status,
            "criado_por": self.criado_por
        }