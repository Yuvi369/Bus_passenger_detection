import cv2
from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, jsonify

# Load the Haar Cascade Classifier for face detection


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

dictionary_bus_route = {"bus_1" : "Route_1" ,"bus_2" : "Route_2","bus_3" : "Route_3","bus_4" : "Route_4","bus_5" : "Route_5","bus_6" : "Route_6",
              "bus_7" : "Route_7","bus_8" : "Route_8","bus_9" : "Route_9","bus_10" : "Route_10"}




def insertorupdate(date_detected, passenger_detected, available):
    conn = sqlite3.connect("sqlitepassenger.db")
    # Convert available seats to string
    #available_str = str(available)
    # Execute SQL insert statement to insert passenger details for the given date
    conn.execute("INSERT INTO passenger (date_detected,passenger_detected, available) VALUES (?, ?, ?)",
                 (date_detected,  passenger_detected, available))
    conn.commit()
    conn.close()


#@app.route('/')
#def index():
 #   return render_template('index.html')


while(True):

    print("Enter Bus_id ---(bus_1/bus_2/bus_3/bus_4/bus_5/bus_6/bus_7/bus_8/bus_9/bus_10")
    input_bus = input()

        # Read a frame from the camera
    for bus,route in dictionary_bus_route.items():
        if(input_bus == bus):
            ret, frame = cam.read()

        # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around the faces and count the number of faces
            passengers_present = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                passengers_present += 1

        # Calculate the number of available seats
                total_seats = 50  # Assuming there are 50 seats available
                available_seats = total_seats - passengers_present
                current_datetime = datetime.now()
                current_date = current_datetime.date()
                current_time = current_datetime.time()

        # Display the frame with rectangles drawn around faces

                cv2.putText(frame, f'Passengers Present: {passengers_present}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255), 2)
                cv2.putText(frame, f'Available Seats: {available_seats}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                    2)
                cv2.putText(frame, f'Date: {current_date}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                    2)
                cv2.putText(frame, f'Bus_id: {input_bus}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                            2)
                cv2.imshow('Face Detection', frame)
                insertorupdate(current_date, passengers_present, available_seats)
                print(current_date)
                print(passengers_present)
                print(available_seats)
                print(input_bus)

        # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break







# Release the camera and close all OpenCV windows



cam.release()
cv2.destroyAllWindows()
