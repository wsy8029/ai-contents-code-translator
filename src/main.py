from code_translator import CodeTranslator
import sys
import speech_recognition as sr
import modi

def main():
    bundle = modi.MODI()
    r = sr.Recognizer()
    mic = sr.Microphone()
    translator = CodeTranslator()
    #translate new sentences until exit
    while 1:
        translator.run(bundle, r, mic)

if __name__ == '__main__':
    main()