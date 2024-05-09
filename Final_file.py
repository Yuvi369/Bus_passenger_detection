import cv2
from datetime import datetime
import sqlite3

# Load the Haar Cascade Classifier for face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

dictionary_bus_route = {

    "bus_1": "Route_1",
    "bus_2": "Route_2",
    "bus_3": "Route_3",
    "bus_4": "Route_4",
    "bus_5": "Route_5",
    "bus_6": "Route_6",
    "bus_7": "Route_7",
    "bus_8": "Route_8",
    "bus_9": "Route_9",
    "bus_10": "Route_10"
}

def insertorupdate(date_detected, passenger_detected, available):
    conn = sqlite3.connect("sqlitepassenger.db")
    conn.execute("INSERT INTO passenger (date_detected, passenger_detected, available) VALUES (?, ?, ?)",
                 (date_detected, passenger_detected, available))
    conn.commit()
    conn.close()


while True:
    print("Enter Bus_id ---(bus_1/bus_2/bus_3/bus_4/bus_5/bus_6/bus_7/bus_8/bus_9/bus_10)")
    input_bus = input()
    a = input_bus[4:]
    a = int(a)
    List = []
    count_passenger =0
    b = 0

    if (a > 0) and ( a <= 10) :
        ret, frame = cam.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around the faces and count the number of faces
        passengers_present = len(faces)
        total_seats = 50  # Assuming there are 50 seats available

        current_date = datetime.now().date()
        count_passenger += passengers_present
        available_seats = total_seats - count_passenger
        # available_seats = available_seats - count_passenger
        if len(List) == 0:
            List.append(count_passenger)
        else:
            b = List[0] + count_passenger




        # Display the frame with rectangles drawn around faces
        cv2.putText(frame, f'Passengers Present: {count_passenger}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255), 2)
        cv2.putText(frame, f'Available Seats: {available_seats}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255), 2)
        cv2.putText(frame, f'Date: {current_date}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f'Bus_id: {input_bus}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Face Detection', frame)

        # Insert data into the database


    else:
        print("print Valid ID b/w 1-10")


    #Break the loop if 'q' is pressed

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
