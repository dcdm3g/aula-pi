# services/event_service.py
from db import get_db

def add_new_event(titulo, descricao, data_evento, cota_valor, criado_por):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO eventos (titulo, descricao, data_evento, cota_valor, criado_por)
        VALUES (%s, %s, %s, %s, %s)
    """, (titulo, descricao, data_evento, cota_valor, criado_por))
    db.commit()
    cursor.close()
    return {"message": "Evento criado com sucesso, aguardando aprovação"}

def get_events(filtro_status=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM eventos"
    if filtro_status:
        query += " WHERE status = %s"
        cursor.execute(query, (filtro_status,))
    else:
        cursor.execute(query)
    events = cursor.fetchall()
    cursor.close()
    return events

def delete_event(event_id, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE eventos SET resultado = 'excluido' 
        WHERE id = %s AND criado_por = %s AND status = 'aguardando'
    """, (event_id, user_id))
    db.commit()
    cursor.close()
    return {"message": "Evento removido"}
