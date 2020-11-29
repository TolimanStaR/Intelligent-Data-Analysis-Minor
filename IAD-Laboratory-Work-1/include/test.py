import pocketsphinx

import speech_recognition as sr


def f():
    for phrase in pocketsphinx.LiveSpeech():
        print(phrase)


def g():
    pass

