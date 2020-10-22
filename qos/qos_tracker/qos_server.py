from flask import Flask, request, Response
from qos_tracker import QoSTracker

app = Flask(__name__)
qos_tracker = QoSTracker()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/add_reservation', methods=['POST'])
def add_reservation():
    reservation_info = request.json

    if not reservation_info:
        return Response("Reservation info expected in json form", status=400, mimetype="application/json")

    qos_tracker.add_reservation(reservation_info)

    return Response(status=200, mimetype="application/json")

if __name__ == '__main__':
    qos_tracker.start()
    app.run()
