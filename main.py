from flask import Flask, request, jsonify
from models.user import User
from models.establishment import Establishment
from models.counter import Counter

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message='Hello world')

@app.route('/api/users/<int:user_id>', methods=['POST'])
@app.route('/api/users', methods=['POST'])
def user(user_id=None):
    body = request.get_json()
    user = User.save(
        id=user_id,
        name=body.get('name'),
        username=body.get('username'),
        password=body.get('password')
    )
    return jsonify(user.to_dict())

@app.route('/api/establishments/<int:establishment_id>', methods=['GET', 'POST'])
@app.route('/api/establishments', methods=['GET', 'POST'])
def establishments(establishment_id=None):
    if request.method == 'POST':
        body = request.get_json()
        establishment = Establishment.save(
            id=establishment_id,
            name=body.get('name')
        )
        return jsonify(establishment.to_dict())
    return jsonify({})

@app.route('/api/counter/<int:counter_id>', methods=['GET', 'POST', 'PUT'])
@app.route('/api/counter', methods=['POST'])
def counters(counter_id=None):
    if request.method == 'POST':
        body = request.get_json()
        counter = Counter.save(
            id=counter_id,
            establishment=body.get('establishment')
        )
        return jsonify(counter.to_dict())
    if request.method == 'PUT':
        if counter_id:
            body = request.get_json()
            counter = Counter.get_by_id(counter_id)
            if counter.auth_key == body.get('auth_key'):
                counter.step_up()
            return jsonify(counter.to_dict())
    counter = Counter.get_by_id(counter_id)
    return jsonify(counter.to_dict())
