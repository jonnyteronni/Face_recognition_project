import face_recognition
import cv2
import numpy as np
from mss import mss
import sys
import os
import time
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)




# choose between webcam('w'), part of screen_part('sp'), fullscreen('fs') or video('v')

# -------DASHBOARD--------
type_of_input = 'sp'

# hog for cpu, cnn for GPU
MODEL_LOCATION = 'hog'

# large or small. Small is faster but less accurate
MODEL_ENCODING = 'large'

# How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
# Only integers
NUM_JITTERS_ENCODING = 1

# How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
TOLERANCE_RECOGNITION = 0.6

# Resize of 
resize_value = 1

# -------------

# Check what is the OS running

if os.name == 'Linux':
    print('Yeiii Linux is running here!')
else:
    print('Recommend using linux to run this script.')

sct=mss()    


if type_of_input == 'w':
    # with webcam
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Could not open webcam")
        sys.exit()
    
elif type_of_input == 'sp':
    # with screen_part
    monitor = {"top": 300, "left": 0, "width": 1000, "height": 800}
elif type_of_input == 'fs':
    # with fullscreen
    monitor = sct.monitors[2]
elif type_of_input =='v':
    # with video
    # webcam = cv2.VideoCapture('face_recognition/Zoom Meeting 2020-08-18 18-38-49.mp4')
    webcam = cv2.VideoCapture('Zoom Meeting 2020-08-19 09-00-21.mp4')



# video_capture = cv2.VideoCapture('Zoom Meeting 2020-08-20 14-38-19.mp4')
KNOWN_FACES_DIR = 'datasets'
known_faces = []
known_names= []

for name in os.listdir(KNOWN_FACES_DIR):

    # Next we load every file of faces of known person
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
    
        # Load an image
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
        print(f'Next encoding - {name} - {filename}')
        # Get 128-dimension face encoding
        # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        
        # for the faces not detected we need an exception
        try:
            encoding = face_recognition.face_encodings(image,num_jitters = 1)[0]
        except IndexError as error_message:
            print(error_message,': Face not found')
            
            # Remove file with no clear face
            os.remove(f'{KNOWN_FACES_DIR}/{name}/{filename}')
       
        
        # Append encodings and name
        known_faces.append(encoding)
        known_names.append(name)

# known_faces = np.genfromtxt('models/known_faces_model.csv',delimiter=',')
# known_names= np.genfromtxt('models/known_names_model.csv',delimiter=',')



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    # ret, frame = video_capture.read()
    
    initial_frame = time.time()
    
    if type_of_input == 'w' or type_of_input=='v':
        ret, frame = webcam.read()
        if not ret:
            print("Could not read frame")
            sys.exit()

    elif type_of_input=='sp' or type_of_input=='fs':
        webcam = np.array(sct.grab(monitor))
        # gray = cv2.cvtColor(webcam, cv2.COLOR_BGR2GRAY)
        # gray = cv2.resize(gray,(ash-1,ash))
        frame = np.delete(webcam, np.s_[-1], 2)

    # Frame from RGB to Gray
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)    



    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame,model = MODEL_LOCATION)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters = NUM_JITTERS_ENCODING, model = MODEL_ENCODING)
        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=TOLERANCE_RECOGNITION)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

            face_names.append(name)
            
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 1
        right *= 1
        bottom *= 1
        left *= 1

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    print(time.time() - initial_frame)

# Release handle to the webcam
webcam.release()
cv2.destroyAllWindows()