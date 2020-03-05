from code_translator import CodeTranslator
import sys

def main():

    translator = CodeTranslator()
    #translate new sentences until exit
    while True:
        translator.run()

if __name__ == '__main__':
    main()
