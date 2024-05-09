import cv2
from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, jsonify

# Load the Haar Cascade Classifier for face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

app = Flask(__name__)

def insertorupdate(date_detected, passenger_detected, available):
    conn = sqlite3.connect("sqlitepassenger.db")
    # Execute SQL insert statement to insert passenger details for the given date
    conn.execute("INSERT INTO passenger (date_detected, passenger_detected, available) VALUES (?, ?, ?)",
                 (date_detected, passenger_detected, available))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_detection', methods=['POST'])
def update():
    # Read a frame from the camera
    ret, frame = cam.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Count the number of passengers present
    passengers_present = len(faces)

    # Calculate the number of available seats
    total_seats = 50  # Assuming there are 50 seats available
    available_seats = total_seats - passengers_present

    # Get the current date
    current_date = datetime.now().date()

    # Update the passenger details in the database for the current date
    insertorupdate(current_date, passengers_present, available_seats)

    # Return the results
    return jsonify({'passengers_present': passengers_present, 'available_seats': available_seats})

# Release the camera and close all OpenCV windows
@app.route('/shutdown', methods=['POST'])
def shutdown():
    cam.release()
    cv2.destroyAllWindows()
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    app.run(debug=True)
