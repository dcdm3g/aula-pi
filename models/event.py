from db import get_db

class Event:
  def __init__(self, id, title, description, date, quota_value, status='aguardando', created_by=None, result=None):
    self.id = id
    self.title = title
    self.description = description
    self.date = date
    self.quota_value = quota_value
    self.status = status
    self.created_by = created_by
    self.result = result 

  @classmethod
  def create(cls, title, description, date, quota_value, created_by):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
      INSERT INTO events (title, description, date, quota_value, created_by)
      VALUES (%s, %s, %s, %s, %s)
    """, (title, description, date, quota_value, created_by))
    db.commit()
    event_id = cursor.lastrowid
    cursor.close()
    return cls(event_id, title, description, date, quota_value, 'aguardando', created_by)

  @classmethod
  def get_events_by_status(cls, status):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE status = %s", (status,))
    events_data = cursor.fetchall()
    cursor.close()
    return [cls(**event) for event in events_data]

  def delete(self):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
      UPDATE events SET status = 'ocorrido'
      WHERE id = %s AND created_by = %s AND status = 'aguardando'
    """, (self.id, self.created_by))
    db.commit()
    cursor.close()

  @classmethod
  def get_event_by_id(cls, event_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event_data = cursor.fetchone()
    cursor.close()
    return cls(**event_data) if event_data else None

  def evaluate(self, status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE events SET status = %s WHERE id = %s", (status, self.id))
    db.commit()
    cursor.close()

  def finish(self, result):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE events SET result = 'finalizado', result = %s WHERE id = %s", (result, self.id))
    db.commit()
    cursor.close()

  @classmethod
  def search_by_keyword(cls, keyword):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE title LIKE %s OR description LIKE %s", (f'%{keyword}%', f'%{keyword}%'))
    events_data = cursor.fetchall()
    cursor.close()
    return [cls(**event) for event in events_data]

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "date": self.date,
      "quota_value": self.quota_value,
      "status": self.status,
      "created_by": self.created_by
    }