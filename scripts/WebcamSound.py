import urllib2
import cookielib
import imaplib
import email
import multiprocessing
import cv2
import re
import sys
import shlex, subprocess 
import speech_recognition as sr
import pyvona
import xml.etree.ElementTree as ET
import time
import requests
from facerec import *
from pykeyboard import PyKeyboard
from takedata import savepic
selfiepatterns = ['selfie','picture','group photo']
chatpatterns = ['chat','talk','bored','time pass','hi','hello']
recognitionpatterns = ['recongnize','remember']
byepatterns = ['bye bye']

def SendSms(sendStr, num):
    username = "mobile_num"
    passwd = "password"
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
def Smssend():
    chatvoice("Tell me Phone number ")
    takeString = speak()
    number = takeString
    chatvoice('what your message')
    takeString = speak()
    sendString = " ;message:"+takeString
    SendSms(sendString, number)
    chatvoice("I have deliever this message.")

def update_emails():
    while True:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        (retcode, capabilities) = mail.login('username','pass')
        mail.list()
        mail.select('inbox')

        n=0
        (retcode, messages) = mail.search(None, '(UNSEEN)')
        if retcode == 'OK':

           for num in messages[0].split() :
              print 'Processing '
              n=n+1
              typ, data = mail.fetch(num,'(RFC822)')
              for response_part in data:
                 if isinstance(response_part, tuple):
                     original = email.message_from_string(response_part[1])
                     print original['From']
                     chatvoice("recieved mail from" +original['From'])
                     for part in original.walk():
                        # each part is a either non-multipart, or another multipart message
                        # that contains further parts... Message is organized like a tree
                        # if part.get_content_type() == 'text/plain':
                        #     print part.get_payload() # prints the raw text
                        typ, data = mail.store(num,'+FLAGS','\\Seen')


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



        
def intelbot(string):
    payload = {'input':string,'botid':'9fa364f2fe345a10','custid':'d4e1b510ee06e5f8'}
    r = requests.get("http://fiddle.pandorabots.com/pandora/talk-xml", params=payload)
    for child in ET.fromstring(r.text):
        if child.tag == "that":
         #urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', child.text)
         print child.text
         chatvoice(child.text)


def Camera():
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

    video_capture = cv2.VideoCapture(0)
    import time
    time.sleep(10)
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

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imwrite("new.jpg", frame)
        import time
        time.sleep(5)
        break


    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()



def Sound():
    while True:
            takeString = speak()
            takeString = str(takeString)
            if takeString is None:
                continue
            for pattern in selfiepatterns:
                if re.search(pattern,  takeString):
                    chatvoice("Yes ! why not ")
                    Camera()
            for pattern in chatpatterns:
                if re.search(pattern,  takeString):
                    chat()

def chat():
    i = 10
    while True:
        takeString = speak()
        for pattern in byepatterns:
            if re.search(pattern, takeString):
                chatvoice("Bye see you later !")
                return
        intelbot(takeString)



if __name__ == '__main__':
    #Thread(target = Camera).start()
    import time
    #multiprocessing.Process(target=start).start()
    #multiprocessing.Process(target=Sound).start()
    Sound()

    #Camera()
    #time.sleep(5)
    #multiprocessing.Process(target=update_emails()).start()
    #calldriver("example.jpg")
    #Smssend()

