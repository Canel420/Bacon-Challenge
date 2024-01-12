from config import app, db
from sqlalchemy import exc
from models.metrics import Metrics
def init_db():
    db.create_all()

    default_rows = [
        Metrics(word='bacon', frequency=40),
        Metrics(word='pork', frequency=20),
        Metrics(word='beef', frequency=30),
        Metrics(word='filet', frequency=10),
        Metrics(word='ribs', frequency=5),
    ]

    for row in default_rows:
        existing_row = Metrics.query.filter_by(word=row.word).first()
        if existing_row is None:
            try:
                db.session.add(row)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
