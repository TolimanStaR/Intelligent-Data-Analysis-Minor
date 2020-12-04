import pocketsphinx

import pyttsx3

import speech_recognition as sr


def voice():
    tts = pyttsx3.init()

    voices = tts.getProperty('voices')

    tts.setProperty('voice', 'ru')

    tts.say('привет')
    # tts.say('Hi')

    tts.runAndWait()


def psx():
    import os
    from pocketsphinx import LiveSpeech, get_model_path

    model_path = get_model_path()

    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'zero_ru.cd_cont_4000'),
        lm=os.path.join(model_path, 'ru.lm'),
        dic=os.path.join(model_path, 'ru.dic')
    )

    print("Ready")

    for phrase in speech:
        print(type(phrase))
        print(str(phrase))
