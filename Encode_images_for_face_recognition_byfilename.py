

import os
import numpy as np
import face_recognition
import cv2


def encode_images():
    
    KNOWN_FACES_DIR = 'static/images'###################################
    known_faces = []
    known_names= []
    
    for name in os.listdir(KNOWN_FACES_DIR):
    
        
        # Load an image
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}')
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
        print(f'Next encoding - {name}')
        # Get 128-dimension face encoding
        # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        
        # for the faces not detected we need an exception
        try:
            encoding = face_recognition.face_encodings(image,num_jitters = 1)[0]
            # Append encodings and name
            known_faces.append(encoding)
            name = name.split('.')[0]
            known_names.append(name)
            
        except IndexError as error_message:
            print(error_message,': Face not found')
            
            # Remove file with no clear face
            os.remove(f'{KNOWN_FACES_DIR}/{name}')
       
        
            
    #############################################################################
    np.savetxt('../models/known_faces_model.csv',known_faces,delimiter=',',fmt='%f')
    
    np.savetxt('../models/known_names_model.csv',known_names,delimiter=',',fmt='%s')