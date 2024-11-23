from flask import Flask, request, jsonify
from services.user_service import sign_up, login
from services.event_service import add_new_event, get_events, delete_event
from db import close_db
from models.user import User
from models.event import Event

app = Flask(__name__)
app.teardown_appcontext(close_db)

@app.route('/sign-up', methods=['POST'])
def sign_up_route():
  data = request.json
  result = sign_up(data['name'], data['email'], data['password'], data['date_of_birth'])
  return jsonify(result)

@app.route('/login', methods=['POST'])
def login_route():
  data = request.json
  result = login(data['email'], data['password'])
  return jsonify(result)

@app.route('/events', methods=['POST'])
def add_event_route():
  data = request.json
  result = add_new_event(data['title'], data['description'], data['date'], data['quota_value'], data['created_by'])
  return jsonify(result)

@app.route('/events', methods=['GET'])
def get_events_route():
  filtro_status = request.args.get('status')
  result = get_events(filtro_status)
  return jsonify(result)

@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event_route(event_id):
  user_id = request.json['user_id']
  result = delete_event(event_id, user_id)
  return jsonify(result)

# Rota para /evaluateNewEvent
@app.route('/events/<event_id>/evaluate', methods=['PATCH'])
def evaluate_new_event(event_id):
  status = request.json.get('status')
  event = Event.get_event_by_id(event_id)

  if event:
    event.evaluate(status)
    return jsonify({"message": "Evento avaliado com sucesso"}), 200
  else:
    return jsonify({"error": "Evento não encontrado"}), 404

# Rota para /addFunds
@app.route('/funds', methods=['POST'])
def add_funds():
  user_id = request.json.get('user_id')
  amount = request.json.get('amount')
    
  user = User.get_user_by_id(user_id)

  if user:
    user.add_funds(amount)
    return jsonify({"message": "Fundos adicionados com sucesso"}), 200
  else:
    return jsonify({"error": "Usuário não encontrado"}), 404

# Rota para /withdrawFunds
@app.route('/funds/withdraw', methods=['POST'])
def withdraw_funds():
  user_id = request.json.get('user_id')
  amount = request.json.get('amount')
    
  user = User.get_user_by_id(user_id)
  if user and user.withdraw_funds(amount):
    return jsonify({"message": "Saque realizado com sucesso"}), 200
  else:
    return jsonify({"error": "Usuário não encontrado ou balance insuficiente"}), 400

# Rota para /betOnEvent
@app.route('/events/<event_id>/bet', methods=['POST'])
def bet_on_event(event_id):
  email = request.json.get('email')
  valor = request.json.get('valor')
    
  user = User.get_user_by_email(email)
  event = Event.get_event_by_id(event_id)

  if user and event:
    if user.bet_on_event(event, valor):
      return jsonify({"message": "Aposta realizada com sucesso"}), 200
    else:
      return jsonify({"error": "balance insuficiente ou erro na aposta"}), 400
    
  return jsonify({"error": "Usuário ou evento não encontrado"}), 404

# Rota para /finishEvent
@app.route('/events/<event_id>/finish', methods=['PATCH'])
def finish_event(event_id):
  result = request.json.get('result')
  event = Event.get_event_by_id(event_id)

  if event:
    event.finish(result)
    return jsonify({"message": "Evento finalizado com sucesso"}), 200
  else:
    return jsonify({"error": "Evento não encontrado"}), 404

# Rota para /searchEvent
@app.route('/events/search', methods=['GET'])
def search_event():
  keyword = request.args.get('keyword')

  events = Event.search_by_keyword(keyword)
  return jsonify([event.to_dict() for event in events]), 200


if __name__ == '__main__':
  app.run(debug=True)
