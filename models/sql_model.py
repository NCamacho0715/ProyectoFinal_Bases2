from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CuentaSQL(db.Model):
    __tablename__ = 'Cuentas'

    id_cuenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, nullable=False)
    tipo_cuenta = db.Column(db.String(50), nullable=False)
    saldo = db.Column(db.Numeric(15, 2), nullable=False)
    fecha_apertura = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id_cuenta": self.id_cuenta,
            "id_cliente": self.id_cliente,
            "tipo_cuenta": self.tipo_cuenta,
            "saldo": float(self.saldo),
            "fecha_apertura": self.fecha_apertura.isoformat(),
            "estado": self.estado
        }
