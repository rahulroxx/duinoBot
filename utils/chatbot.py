'''
Simple web Chatbot
'''
import chatvoice
import requests
import xml.etree.ElementTree as ET

def chatbot(string):
    payload = {'input':string,'botid':'9fa364f2fe345a10','custid':'d4e1b510ee06e5f8'}
    r = requests.get("http://fiddle.pandorabots.com/pandora/talk-xml", params=payload)
    for child in ET.fromstring(r.text):
        if child.tag == "that":
            chatvoice(child.text)