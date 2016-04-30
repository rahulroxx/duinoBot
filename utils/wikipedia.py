'''
Scrapping wikipedia data
'''
import chatvoice
import wikipedia

def wikileaks(string):
    string=wikipedia.summary(string,sentences=1)
    chatvoice(string)