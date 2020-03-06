from code_translator import CodeTranslator
import sys
import modi

def main():
    bundle = modi.MODI()
    translator = CodeTranslator()
    #translate new sentences until exit
    while True:
        translator.run(bundle)

if __name__ == '__main__':
    main()
