from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexión al servidor MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["banco_db"]
mongo_cuentas = mongo_db["cuentas"]

def serialize_cuenta(cuenta):
    return {
        "id": str(cuenta["_id"]),
        "id_cuenta": cuenta.get("id_cuenta"),
        "id_cliente": cuenta.get("id_cliente"),
        "tipo_cuenta": cuenta.get("tipo_cuenta"),
        "saldo": cuenta.get("saldo"),
        "fecha_apertura": cuenta.get("fecha_apertura"),
        "estado": cuenta.get("estado"),
    }
