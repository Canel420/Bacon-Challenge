from config import db, ma

class Metrics(db.Model):
    __tablename__ = 'metrics'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

class MetricsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metrics
        load_instance = True
        sqla_session = db.session