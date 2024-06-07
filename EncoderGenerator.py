from  face_recognition import face_encodings
import pickle
import os
from datetime import datetime
from cv2 import cvtColor,COLOR_BGR2RGB
import cv2

import fr
class Encode:
    def __init__(self) -> None:
       
        self.date = datetime.now().date()
        self.encodings = []
        self.DBchanged = False
        self.backup()
    def findEncodings(self, imgMatrix):
        '''Find the encoding of imgMatrix'''
        imgMatrix = cv2.cvtColor(imgMatrix, cv2.COLOR_BGR2RGB)
        face_encoding = face_encodings(imgMatrix)
        
        # Check if any face is detected in the image
        if len(face_encoding) > 0:
            self.encodings.append(face_encoding[0])
            self.DBchanged = True
            self.backup()
            print("Face encoding added successfully.")
            return True
        else:
            print("No face detected in the image.")
            return False


    def SyncDataBase(self):
        '''This will Sync the database'''
        findDatabase = [f for f in os.listdir(os.getcwd()) if f.endswith('.p')]
        
        # if database is empty we have to setup from new
        if findDatabase == []:
            return

        # if db exist then we have to check is it of same day
        currDate = datetime.now().date()
        db_date = datetime.strptime(findDatabase[0][:10],"%Y-%m-%d").date()

        if db_date != currDate:
            #Removing File and Setting Date to current and encodings to empty
            self.date = currDate
            self.encodings = []
            os.remove(f"{db_date}.p")
            return
        
        # Now we will check the database and encodings are sync to each other or not (if bot get discharged the it will set to default settings)
        loadedEncodings = self.readDatabase()
        if loadedEncodings != self.encodings and (not self.DBchanged):
            self.encodings = loadedEncodings

    def backup(self):
        '''This will take the backup of encoding and saved it in binary file.'''
        self.SyncDataBase()
        file = open(f'{self.date}.p','wb')
        pickle.dump(self.encodings,file)
        file.close()
        self.DBchanged = False

    def readDatabase(self):
        '''This will return list of all encodings saved in database.'''
        file = open(f'{self.date}.p','rb')
        return pickle.load(file)

# encode = Encode()
# a = cv2.imread("2.jpg")
# x = encode.readDatabase()
# print(len(encode.encodings))
# # print(fr.isRecognized(a,x))
