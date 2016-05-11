'''
Face Detection
'''

import cv2

cascPath = "../scripts/haarcascade_frontalface_alt2.xml"


def Camera():
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(40, 40),
            # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            flags=0
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', gray)
        keypress = cv2.waitKey(1)
        if keypress & 0xFF == ord('q'):
            break
        if keypress & 0xFF == ord('b'):
            cv2.imwrite('example.jpg', gray)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
