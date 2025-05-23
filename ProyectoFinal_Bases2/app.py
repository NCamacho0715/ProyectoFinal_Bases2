from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from models.mongo_model import mongo_cuentas, serialize_cuenta
from models.sql_model import db, CuentaSQL
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)

# Obtener todas las cuentas
@app.route('/mongo/obtenerCuentas', methods=['GET'])
def get_mongo_cuentas():
    cuentas = mongo_cuentas.find()
    return jsonify([serialize_cuenta(cuenta) for cuenta in cuentas])

# Crear una cuenta
@app.route('/mongo/crearCuenta', methods=['POST'])
def create_mongo_cuenta():
    data = request.json
    result = mongo_cuentas.insert_one(data)
    return jsonify({"message": "Cuenta creada", "id": str(result.inserted_id)}), 201

# Actualizar una cuenta
@app.route('/mongo/actualizarCuenta/<string:id>', methods=['PUT'])
def update_mongo_cuenta(id):
    data = request.json
    result = mongo_cuentas.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Cuenta no encontrada"}), 404
    return jsonify({"message": "Cuenta actualizada"})

# Eliminar una cuenta
@app.route('/mongo/eliminarCuenta/<string:id>', methods=['DELETE'])
def delete_mongo_cuenta(id):
    result = mongo_cuentas.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Cuenta no encontrada"}), 404
    return jsonify({"message": "Cuenta eliminada"})

# Obtener todas las cuentas SQL
@app.route('/sql/obtenerCuentas', methods=['GET'])
def get_sql_cuentas():
    cuentas = CuentaSQL.query.all()
    return jsonify([
        {
            "id_cuenta": c.id_cuenta,
            "id_cliente": c.id_cliente,
            "tipo_cuenta": c.tipo_cuenta,
            "saldo": float(c.saldo),
            "fecha_apertura": c.fecha_apertura.isoformat(),
            "estado": c.estado
        } for c in cuentas
    ])

# Crear una cuenta SQL
@app.route('/sql/crearCuenta', methods=['POST'])
def create_sql_cuenta():
    data = request.json
    nueva_cuenta = CuentaSQL(
        id_cliente=data['id_cliente'],
        tipo_cuenta=data['tipo_cuenta'],
        saldo=data['saldo'],
        fecha_apertura=datetime.strptime(data['fecha_apertura'], "%Y-%m-%d"),
        estado=data['estado']
    )
    db.session.add(nueva_cuenta)
    db.session.commit()
    return jsonify({"message": "Cuenta SQL creada", "id": nueva_cuenta.id_cuenta}), 201

# Actualizar cuenta SQL
@app.route('/sql/actualizarCuenta/<int:id>', methods=['PUT'])
def update_sql_cuenta(id):
    cuenta = CuentaSQL.query.get(id)
    if not cuenta:
        return jsonify({"error": "Cuenta no encontrada"}), 404

    data = request.json
    cuenta.tipo_cuenta = data.get('tipo_cuenta', cuenta.tipo_cuenta)
    cuenta.saldo = data.get('saldo', cuenta.saldo)
    cuenta.fecha_apertura = datetime.strptime(data.get('fecha_apertura', cuenta.fecha_apertura.isoformat()), "%Y-%m-%d")
    cuenta.estado = data.get('estado', cuenta.estado)

    db.session.commit()
    return jsonify({"message": "Cuenta actualizada"})

# Eliminar cuenta SQL
@app.route('/sql/eliminarCuenta/<int:id>', methods=['DELETE'])
def delete_sql_cuenta(id):
    cuenta = CuentaSQL.query.get(id)
    if not cuenta:
        return jsonify({"error": "Cuenta no encontrada"}), 404

    db.session.delete(cuenta)
    db.session.commit()
    return jsonify({"message": "Cuenta eliminada"})

if __name__ == '__main__':
    app.run(debug=True)