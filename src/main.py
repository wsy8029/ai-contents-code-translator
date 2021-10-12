from code_translator import CodeTranslator
import sys
import speech_recognition as sr
import modi

def main():
    bundle = modi.MODI() # PyMODI 번들 선언
    r = sr.Recognizer() # 음성 인식을 위해 SR 패키지의 recognizer 선언
    mic = sr.Microphone() # 음성 인식을 위해 SR 패키지의 mic 선언
    translator = CodeTranslator()
    #translate new sentences until exit
    while 1:
        translator.run(bundle, r, mic)

if __name__ == '__main__':
    main()