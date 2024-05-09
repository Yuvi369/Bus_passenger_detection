from flask import Flask, render_template, request
import cv2
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Load the Haar Cascade Classifier for face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def insertorupdate(date_detected, passenger_detected, available):
    conn = sqlite3.connect("sqlitepassenger.db")
    conn.execute("INSERT INTO passenger (date_detected, passenger_detected, available) VALUES (?, ?, ?)",
                 (date_detected, passenger_detected, available))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    input_bus = request.form['bus_id']
    a = int(input_bus[4:])
    List = []
    count_passenger = 0

    if 0 < a <= 10:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        passengers_present = len(faces)
        total_seats = 50  # Assuming there are 50 seats available
        current_date = datetime.now().date()
        count_passenger += passengers_present
        available_seats = total_seats - count_passenger
        if len(List) == 0:
            List.append(count_passenger)

        # Insert data into the database
        insertorupdate(current_date, passengers_present, available_seats)

        return render_template('index.html', bus_id=input_bus, passengers_present=passengers_present, available_seats=available_seats, current_date=current_date)
    else:
        return "Invalid Bus ID"

if __name__ == '__main__':
    app.run(debug=True)
