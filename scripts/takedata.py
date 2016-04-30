import speech_recognition as sr
import pyvona
from threading import Thread
import urllib2
import cookielib
from getpass import getpass
import os
import sys
import cv2
import Queue
import requests


def uploadImage():
    url = "http://imgup.net/upload"
    data = {'utf8': '&#x2713;', '_method': 'put'}
    f = open('new.jpg', "rb")  # open in binary mode
    files = {'image[image][]': f}
    r = requests.post(url, files=files, data=data)
    f.close()
    return (r.json()['direct_link'])

def speak():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        string =  r.recognize_google(audio)
        print "you said "+string
        return string
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def chatvoice(string):

    v = pyvona.create_voice('token','key')
    #v.region('en-IN')
    #print v.list_voices()
    v.speak(string)
    #v.speak(a)

def takeData():
    chatvoice('What is your name')
    takeString = speak()
    sendString = takeString
    f = open("data.txt",'w+')
    f.write("name:"+takeString)
    chatvoice('what your message')
    takeString = speak()
    sendString += " ;message:"+takeString
    f.write("\n"+"message:"+takeString)
    savepic()
    image_url = uploadImage()
    sendString += " ;image_url:"+image_url
    chatvoice('Thank you ! I will deliever this message to rahul')
    sendSms(sendString)
    f.close()


def sendSms(sendStr):
    username = "mobile_number"
    passwd = "passwd"
    message = sendStr
    number = "target_number"
    message = "+".join(message.split(' '))

    # Logging into the SMS Site
    url = 'http://site24.way2sms.com/Login1.action?'
    data = 'username=' + username + '&password=' + passwd + '&Submit=Sign+in'

    # For Cookies:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Adding Header detail:
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]


    try:
        usock = opener.open(url, data)
    except IOError:
        print ("\n[-] CAN NOT CONNECT TO SERVER...CHECK USERNAME AND PASSWORD AND INTERNET CONNECTION ALSO")
        raw_input("\n[-] PRESS ENTER TO EXIT")
        sys.exit(1)


    jession_id = str(cj).split('~')[1].split(' ')[0]
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    send_sms_data = 'ssaction=ss&Token=' + jession_id + \
        '&mobile=' + number + '&message=' + message + '&msgLen=136'

    opener.addheaders = [
        ('Referer', 'http://site25.way2sms.com/sendSMS?Token=' + jession_id)]


    try:
        sms_sent_page = opener.open(send_sms_url, send_sms_data)
    except IOError:
        print ("\n[-] ERROR WHILE SENDING THE SMS...PLEASE UPDATE THE CONTACT LIST")
        sys.exit(1)
    print ("\n\n\t[+] SMS SENT")

def savepic():
    faceCascade = cv2.CascadeClassifier(sys.argv[1])

    video_capture = cv2.VideoCapture(1)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(40, 40),
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            flags = 0
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imwrite("new.png", frame)
        import time
        time.sleep(5)
        break


    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Thread(target = takeData()).start()
    #Thread(target = takeData).start()
