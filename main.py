import pickle
from datetime import datetime

import cv2
import os
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-b163c-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "facerecognition-b163c.appspot.com"
})
bucket = storage.bucket()
# camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

try:
    while True:

        success, img = cap.read()
        # thu nho hinh anh de tien cho qua trinh xu li
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25, None)
        # chuyen hinh anh sang he mau RGB
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # nhan dien khuon mat trong camera
        faceCurFrame = face_recognition.face_locations(imgS)
        # ma hoa khuon mat trong camera
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        # chieu cao, chieu rong khung
        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            # zip lai de su dung vong lap for cho ca 2 cung mot luc
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                # so sanh du lieu ma hoa camera voi du lieu ma hoa hinh anh:giong hay khong
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace) #true/false
                print(matches)
                # khoang cach: cang thap thi cang phu hop
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print("faceDis",faceDis)
                # gia tri thap nhat
                matchIndex = np.argmin(faceDis)
                print("Match Index", matchIndex)

                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                # scale ve  kich thuoc ban dau
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                # tao khung xung quanh khuon mat
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)


                if faceDis[matchIndex] < 0.44:

                    id = studentIds[matchIndex]
                    print("id", id)
                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

                    if counter != 0:

                        if counter == 1:
                            # Get the Data
                            studentInfo = db.reference(f'Students/{id}').get()
                            # Get the Image from the storage
                            blob = bucket.get_blob(f'Images/{id}.png')

                            array = np.frombuffer(blob.download_as_string(), np.uint8)
                            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                            # Update data of attendance
                            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                               "%Y-%m-%d %H:%M:%S")
                            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                            print(secondsElapsed)
                            if secondsElapsed > 20:
                                ref = db.reference(f'Students/{id}')
                                studentInfo['total_attendance'] += 1
                                ref.child('total_attendance').set(studentInfo['total_attendance'])
                                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            else:
                                modeType = 3
                                counter = 0
                                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        if modeType != 3:
                            print("if modeType != 3")
                            if 10 < counter < 20:
                                modeType = 2
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                            if counter <= 10:
                                cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                                cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                                cv2.putText(imgBackground, str(id), (1006, 493),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                                cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                                cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                                cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                                # căn giữa tên
                                (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                                offset = (414 - w) // 2
                                cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                                # hiển thị hình ảnh sinh viên
                                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                            counter += 1

                            if counter >= 20:
                                counter = 0
                                modeType = 0
                                studentInfo = []
                                imgStudent = []
                                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                else:
                    text_coordinates = (808, 44)
                    text_content = "NOT FOUND STUDENT"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    font_thickness = 2
                    font_color = (255, 255, 255)
                    text_image = np.zeros((633, 414, 3), dtype=np.uint8)
                    cv2.putText(text_image, text_content, (40, 320), font, font_scale, font_color, font_thickness)
                    imgBackground[44:44 + 633, 808:808 + 414] = text_image
        else:
            modeType = 0
            counter = 0
        # cv2.imshow("Webcam", img)
        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)
except Exception as e:
    # Code to handle other exceptions
    print(f"An error occurred: {e}")
