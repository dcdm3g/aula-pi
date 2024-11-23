from db import get_db

class User:
  def __init__(self, id, name, email, password, date_of_birth, balance):
    self.id = id
    self.name = name
    self.email = email
    self.password = password
    self.date_of_birth = date_of_birth
    self.balance = balance

  @classmethod
  def get_user_by_id(cls, user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    return cls(**user_data) if user_data else None

  @classmethod
  def get_user_by_email(cls, email):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()
    return cls(**user_data) if user_data else None

  @classmethod
  def create(cls, name, email, password, date_of_birth):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
      INSERT INTO users (name, email, password, date_of_birth)
      VALUES (%s, %s, %s, %s)
    """, (name, email, password, date_of_birth))
    db.commit()
    cursor.close()
    return cls(cursor.lastrowid, name, email, password, date_of_birth)

  @classmethod
  def authenticate(cls, email, password):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
      SELECT id, name, balance FROM users WHERE email = %s AND password = %s
    """, (email, password))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
      return cls(user_data['id'], user_data['name'], email, password, user_data['balance'])
    return None

  def add_funds(self, valor):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (valor, self.id))
    db.commit()
    cursor.close()

  def withdraw_funds(self, valor):
    if self.balance >= valor:
      db = get_db()
      cursor = db.cursor()
      cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (valor, self.id))
      db.commit()
      cursor.close()
      return True

    return False

  def bet_on_event(self, event, valor):
    if self.balance >= valor:
      db = get_db()
      cursor = db.cursor()
      cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (valor, self.id))
      cursor.execute("""
        INSERT INTO apostas (usuario_id, evento_id, valor)
        VALUES (%s, %s, %s)
      """, (self.id, event.id, valor))
      db.commit()
      cursor.close()
      return True
    return False