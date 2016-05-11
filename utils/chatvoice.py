'''
Pyvona TTS Engine API
'''


def chatvoice(string):
    v = pyvona.create_voice('GDNAI2AAUGNCQFO4TFSA', 'a+MtpzzlpqskQsYFPMaczgYMbzXurj/i5vduNEzL')
    # v.region('en-IN')
    # print v.list_voices()
    v.speak(string)
    # v.speak(a)
