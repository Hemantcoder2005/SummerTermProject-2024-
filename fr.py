from cv2 import resize, cvtColor, COLOR_BGR2RGB
import pickle
from face_recognition import face_locations, face_encodings, compare_faces, face_distance
import numpy as np

def isRecognized(imgMatrix, encodeListKnown) -> bool:
    # Preprocess Image
    imgMatrix = cvtColor(resize(imgMatrix, None, fx=0.25, fy=0.25), COLOR_BGR2RGB)
    
    faceCurrentFrame = face_locations(imgMatrix)
    encodeCurrentFrame = face_encodings(imgMatrix, faceCurrentFrame)

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        for known_encoding in encodeListKnown:
            distance = np.linalg.norm(known_encoding - encodeFace)
            if distance < 0.6:  # Adjust the threshold as needed
                return True
    
    return False

