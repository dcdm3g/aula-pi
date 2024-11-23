from db import get_db

def add_new_event(title, description, date, quota_value, created_by):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO events (title, description, date, quota_value, created_by)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, description, date, quota_value, created_by))
    db.commit()
    cursor.close()
    return {"message": "Evento criado com sucesso, aguardando aprovação"}

def get_events(status_filter=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM events"
    if status_filter:
        query += " WHERE status = %s"
        cursor.execute(query, (status_filter,))
    else:
        cursor.execute(query)
    events = cursor.fetchall()
    cursor.close()
    return events

def delete_event(event_id, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE events SET result = 'excluido' 
        WHERE id = %s AND created_by = %s AND status = 'aguardando'
    """, (event_id, user_id))
    db.commit()
    cursor.close()
    return {"message": "Evento removido"}
