from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

db = SQLAlchemy()
ma = Marshmallow()


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(String(80))
    day = Column(Integer)
    clock_time = Column(String(80))
    rainfall = Column(Float)

    def __repr__(self):
        return '<Year: %s | Month: %s | Day: %s | Clock time: %s | Rainfall: %s>' \
               % self.year, self.month, self.day, self.clock_time, self.rainfall


class MeasurementSchema(ma.Schema):
    class Meta:
        fields = ('id', 'year', 'month', 'day', 'clock_time', 'rainfall')


measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True)