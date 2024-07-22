from flask import Flask, request, jsonify
from models import db, Location, Machine

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([location.name for location in locations])

@app.route('/location', methods=['POST'])
def add_location():
    data = request.get_json()
    new_location = Location(name=data['name'])
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': 'Location added successfully'}), 201

@app.route('/machines', methods=['GET'])
def get_machines():
    machines = Machine.query.all()
    return jsonify([{'name': machine.name, 'status': machine.status, 'location': machine.location.name} for machine in machines])

@app.route('/machine', methods=['POST'])
def add_machine():
    data = request.get_json()
    location = Location.query.filter_by(name=data['location']).first()
    if location is None:
        return jsonify({'message': 'Location not found'}), 404

    new_machine = Machine(name=data['name'], status=data['status'], location_id=location.id)
    db.session.add(new_machine)
    db.session.commit()
    return jsonify({'message': 'Machine added successfully'}), 201

@app.route('/machine/<int:machine_id>', methods=['PUT'])
def update_machine(machine_id):
    data = request.get_json()
    machine = Machine.query.get(machine_id)
    if machine is None:
        return jsonify({'message': 'Machine not found'}), 404

    if 'status' in data:
        machine.status = data['status']
    if 'location' in data:
        location = Location.query.filter_by(name=data['location']).first()
        if location is None:
            return jsonify({'message': 'Location not found'}), 404
        machine.location_id = location.id

    db.session.commit()
    return jsonify({'message': 'Machine updated successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
