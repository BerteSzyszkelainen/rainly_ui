from flask import Flask, jsonify, request
import os

from api.models.db import Measurement, measurements_schema, db, ma

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'measurements.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
ma.init_app(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database created!")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped!")


@app.cli.command('db_seed')
def db_seed():
    measurement_1 = Measurement(year=2021,
                                month='December',
                                day=29,
                                clock_time="18:00:00",
                                rainfall=15.6)
    measurement_2 = Measurement(year=2021,
                                month='December',
                                day=30,
                                clock_time="19:00:00",
                                rainfall=5.0)
    measurement_3 = Measurement(year=2021,
                                month='December',
                                day=31,
                                clock_time="20:00:00",
                                rainfall=3.5)
    db.session.add(measurement_1)
    db.session.add(measurement_2)
    db.session.add(measurement_3)
    db.session.commit()
    print("Database seeded!")


@app.route('/add_measurement', methods=['POST'])
def add_measurement():
    year = int(request.form['year'])
    month = request.form['month']
    day = int(request.form['day'])
    clock_time = request.form['clock_time']
    rainfall = float(request.form['rainfall'])

    new_measurement = Measurement(year=year,
                                  month=month,
                                  day=day,
                                  clock_time=clock_time,
                                  rainfall=rainfall)

    db.session.add(new_measurement)
    db.session.commit()

    return jsonify(message='Measurement successfully added!'), 201


@app.route('/get_measurements', methods=['GET'])
def get_measurements():
    measurements_list = Measurement.query.all()
    result = measurements_schema.dump(measurements_list)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run()
