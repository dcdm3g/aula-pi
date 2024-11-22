# app.py
from flask import Flask, request, jsonify
from services.user_service import sign_up, login
from services.event_service import add_new_event, get_events, delete_event
from db import close_db
from models.user import User
from models.event import Event

app = Flask(__name__)
app.teardown_appcontext(close_db)

@app.route('/signUp', methods=['POST'])
def sign_up_route():
    data = request.json
    result = sign_up(data['nome'], data['email'], data['senha'], data['data_nascimento'])
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login_route():
    data = request.json
    result = login(data['email'], data['senha'])
    return jsonify(result)

@app.route('/addNewEvent', methods=['POST'])
def add_event_route():
    data = request.json
    result = add_new_event(data['titulo'], data['descricao'], data['data_evento'], data['cota_valor'], data['criado_por'])
    return jsonify(result)

@app.route('/getEvents', methods=['GET'])
def get_events_route():
    filtro_status = request.args.get('status')
    result = get_events(filtro_status)
    return jsonify(result)

@app.route('/deleteEvent', methods=['DELETE'])
def delete_event_route():
    data = request.json
    result = delete_event(data['event_id'], data['user_id'])
    return jsonify(result)

# Rota para /evaluateNewEvent
@app.route('/evaluateNewEvent', methods=['PATCH'])
def evaluate_new_event():
    event_id = request.json.get('event_id')
    status = request.json.get('status')
    
    event = Event.get_event_by_id(event_id)
    if event:
        event.evaluate(status)
        return jsonify({"message": "Evento avaliado com sucesso"}), 200
    else:
        return jsonify({"error": "Evento não encontrado"}), 404

# Rota para /addFunds
@app.route('/addFunds', methods=['POST'])
def add_funds():
    user_id = request.json.get('user_id')
    valor = request.json.get('valor')
    
    user = User.get_user_by_id(user_id)
    if user:
        user.add_funds(valor)
        return jsonify({"message": "Fundos adicionados com sucesso"}), 200
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

# Rota para /withdrawFunds
@app.route('/withdrawFunds', methods=['POST'])
def withdraw_funds():
    user_id = request.json.get('user_id')
    valor = request.json.get('valor')
    
    user = User.get_user_by_id(user_id)
    if user and user.withdraw_funds(valor):
        return jsonify({"message": "Saque realizado com sucesso"}), 200
    else:
        return jsonify({"error": "Usuário não encontrado ou saldo insuficiente"}), 400

# Rota para /betOnEvent
@app.route('/betOnEvent', methods=['POST'])
def bet_on_event():
    email = request.json.get('email')
    event_id = request.json.get('event_id')
    valor = request.json.get('valor')
    
    user = User.get_user_by_email(email)
    event = Event.get_event_by_id(event_id)
    if user and event:
        if user.bet_on_event(event, valor):
            return jsonify({"message": "Aposta realizada com sucesso"}), 200
        else:
            return jsonify({"error": "Saldo insuficiente ou erro na aposta"}), 400
    return jsonify({"error": "Usuário ou evento não encontrado"}), 404

# Rota para /finishEvent
@app.route('/finishEvent', methods=['PATCH'])
def finish_event():
    event_id = request.json.get('event_id')
    resultado = request.json.get('resultado')
    
    event = Event.get_event_by_id(event_id)
    if event:
        event.finish(resultado)
        return jsonify({"message": "Evento finalizado com sucesso"}), 200
    else:
        return jsonify({"error": "Evento não encontrado"}), 404

# Rota para /searchEvent
@app.route('/searchEvent', methods=['GET'])
def search_event():
    keyword = request.args.get('keyword')
    
    events = Event.search_by_keyword(keyword)
    return jsonify([event.to_dict() for event in events]), 200


if __name__ == '__main__':
    app.run(debug=True)
