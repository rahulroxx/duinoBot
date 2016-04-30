import cv2
import numpy

a = 0

def buildDataset():

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

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
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            flags = 0
        )
        keypress = cv2.waitKey(1)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)

        global a

        if keypress & 0xFF == ord('f'):
            if len(faces):
                x = faces[0][0]
                y = faces[0][1]
                w = faces[0][2]
                h = faces[0][3]
                roi = frame[y:y+h, x:x+w]
                cv2.imwrite(str(a)+'.png',roi)
                #print faces
                print (x)
                print (y)
                print (w)
                print (h)
                a = a+1
        if keypress & 0xFF == ord('q'):
            break
      # Display the resulting frame
        cv2.imshow('Video', gray)



    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    buildDataset()