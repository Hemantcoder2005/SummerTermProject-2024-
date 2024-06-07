import fr
import EncoderGenerator
import cv2
from ultralytics import YOLO
import cvzone
from sort.sort import *
import pygame

pygame.init()
pygame.mixer.init()

encoderClass = EncoderGenerator.Encode()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 720)

# Loading Model
model = YOLO("yolov8n.pt", verbose=False)


tracker = Sort(max_age = 20,min_hits = 3,iou_threshold = 0.3 )
unique_ids = []

sound = pygame.mixer.Sound("hello.mp3") 
def greet():
    print("Hello!")
    
while True:
    success, img = cap.read()
    results = model(img, stream=True, verbose=False)
    detections = np.empty((0,5))
    person_count = 0  # Initialize the person counter

    for r in results:
        Boxes = r.boxes
        for box in Boxes:
            confidence = round(int(box.conf[0] * 100)) / 100
            isconfident = (confidence) >= 0.8
            isPerson = int(box.cls[0]) == 0

            if isPerson and isconfident:
                person_count += 1  # Increment the person counter
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                currentArray = np.array([x1,y1,x2,y2,confidence])
                detections = np.vstack((detections,currentArray))

                cvzone.cornerRect(img, (x1, y1, w, h))
    resultsTracker = tracker.update(detections)
    for res in resultsTracker:
        x1, y1, x2, y2, Id = map(int, res)
       
        if Id not in unique_ids:
            encodeListKnown = encoderClass.readDatabase()
            extracted_Img = img[y1:y2, x1:x2]
            unique_ids.append(Id)
            extracted_Img = img[y1:y2, x1:x2]
            
            # Ensure the extracted image is not empty before processing
            if extracted_Img.size > 0:
                cv2.imshow(str(Id),extracted_Img)
                cv2.waitKey(1)
                if not fr.isRecognized(extracted_Img, encodeListKnown):
                    if (encoderClass.findEncodings(extracted_Img)):
                        greet()
                        sound.play()
            else:
                print("Found!")

    # Display the person count on the frame
    cv2.putText(img, f'Persons: {person_count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
