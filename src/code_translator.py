from konlpy.tag import Komoran
import modi_dic
import text_process
import re
import time
import sys
import keyboard
import traceback

class CodeTranslator(object):

    def __init__(self):
        self.tagger = Komoran(userdic='user_dic.txt')
        self.cond_divider = re.compile('(고 있을\s?때\s?만|때\s?만|동안\s?만|고 있을\s?때|때\s?마다|때|동안|면)')
        self.int_divider = re.compile('(-?\d+,\s?-?\d+,\s?-?\d+|-?\d+,\s?-?\d+|-?\d+)')
        self.op_divider = re.compile('(고|거나)')

    #initialize for new sentence
    def initial(self):
        self.block = []

        self.input_module = []
        self.output_module = []

        self.input_dic = []
        self.output_dic = []

        self.code = ""

    #record speech
    def record(self, r, mic):
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print('ready')
            time.sleep(1)
            print('speak')
            audio = r.listen(source)
            print('end')
        sentence = r.recognize_google(audio,language='ko-KR')
        print(f"You said: {sentence}")
        return sentence

    #create entire code
    def create_code(self, sentence):
        #split chunks into value, operand, and others
        chunks = self.cond_divider.split(sentence)
        #set input and output modules and their dictionaries
        input_chunk, output_chunk = self.set_modules(chunks)
        #basic: with no condition
        if len(chunks)==1:
            basic_code = self.convert_chunk('output', output_chunk).replace('\n\t\t', '\n\t')
            self.code += f"\t{basic_code}\n\ttime.sleep(0.1)"

        #advanced: with condition
        else:
            #if clause
            if modi_dic.cond_dic[chunks[1]] == "if":
                self.code += f"\tif {self.convert_chunk('input', input_chunk)}:\n\t\t{self.convert_chunk('output', output_chunk)}\n\t\ttime.sleep(0.1)"
            #if-else clause
            elif modi_dic.cond_dic[chunks[1]] == "if else":
                self.code += f"\tif {self.convert_chunk('input', input_chunk)}:\n\t\t{self.convert_chunk('output', output_chunk)}\n\t\ttime.sleep(0.1)\n"
                self.code += f"\telse:{self.convert_else()}\n\t\ttime.sleep(0.1)"
            #while-else clause
            else:
                self.code += f"\twhile {self.convert_chunk('input', input_chunk)}:\n\t\t{self.convert_chunk('output', output_chunk)}\n\t\ttime.sleep(0.1)\n"
                self.code += f"\telse:{self.convert_else()}\n\t\ttime.sleep(0.1)"

    #split phrase into value, operand, and others
    '''
    input: 초음파 거리가 30이
    returns:    phrase - ['초음파', '거리', '가']
                value - 30
                operand - '이'
    '''
    def split_phrase(self, phrase):
        operand = None
        value = None
        #extract integer(parameter) of module method
        if self.int_divider.search(phrase) != None:
            parts = self.int_divider.split(phrase)
            phrase = self.tagger.morphs(parts[0])
            value = parts[1]
            operand = self.tagger.morphs(parts[-1])
        else:
            phrase = self.tagger.morphs(phrase)
        return phrase, value, operand

    #convert chunks to code
    '''
    input:  ' 불 켜고 모터 속도 30으로 해줘'
    returns:    'led.set_on() and motor.set_speed(30)'
    '''
    def convert_chunk(self, type, chunk):
        code = ""
        try:
            code += getattr(self, f"convert_phrase")(type, chunk[0], 0)
            if type == "input":
                code += f" {modi_dic.operand_dic[chunk[1]]} "
                code += getattr(self, f"convert_phrase")(type, chunk[2], 1)
            elif type == "output":
                code += "\n\t\t"+ getattr(self, f"convert_phrase")(type, chunk[2], 1)
        except:
            pass
        return code

    #convert phrases to code
    '''
    input: ' 불 켜고'
    returns: 'led.set_on()'
    '''
    def convert_phrase(self, type, phrase, index):
        module = getattr(self, f"{type}_module")[index]
        dic = getattr(self, f"{type}_dic")[index]
        if type == "output":
            phrase_code = f"{module}.set_"
        elif type == "input":
            phrase_code = f"{module}.get_"
        phrase, value, operand = self.split_phrase(phrase)
        #module name and method
        for morph in phrase:
            try:
                phrase_code += dic[morph]
            except:
                pass
        if value != None:
            phrase_code += getattr(self, f"set_{type}_param")(value, operand)
        return phrase_code

    #set input parameters to code
    '''
    input:  value - 30
            operand - '보다 크'
    returns: ' > 30'
    '''
    def set_input_param(self, value, operand):
        param_code = ""
        #operand
        oper_word = None
        for morph in operand:
            oper_word = modi_dic.operand_dic.get(morph)
            if oper_word !=None:
                param_code += f" {oper_word} {value}"
                break
        #'이':'==' case
        if oper_word == None:
            param_code += f" == {value}"
        return param_code

    #set output parameters to code
    '''
    input:  value - 30
    returns: '30)'
    '''
    def set_output_param(self, value, _):
        return f"{value})"

    #set input and output modules and their dictionaries
    '''
    input: '버튼 누르거나 초음파 거리가 30이면 불 켜고 모터 속도 30으로 해줘'
    returns: 'button = bundle.buttons[0]\nultrasonic = bundle.ultrasonics[0]\nled = bundle.leds[0]\nmotor = bundle.motors[0]'
    '''
    def set_modules(self, chunks):
        if len(chunks) == 1:
            input_chunk = None
            output_chunk = self.op_divider.split(chunks[0])

        else:
            input_chunk = self.op_divider.split(chunks[0])
            output_chunk = self.op_divider.split(chunks[-1])

        try:
            self.find_module("input", input_chunk[0])
            self.find_module("input", input_chunk[2])
        except:
            pass

        try:
            self.find_module("output", output_chunk[0])
            self.find_module("output", output_chunk[2])
        except:
            pass

        self.code += "while 1:\n"
        return input_chunk, output_chunk

    #edit typo and find module in dic
    '''
    input: '버턴 누르면 불 켜줘'
    returns: 'button = bundle.buttons[0]\nled = bundle.leds[0]'
    '''
    def find_module(self, type, chunk):
        chunk = chunk.strip()
        chunk = chunk.split(" ")
        for raw in chunk:
            module = getattr(modi_dic, f'{type}_module_dic').get(raw)
            #edit typo
            if module == None:
                word, dist = text_process.edit(type, raw)
                if dist > 1.0:
                    continue
                else:
                    module = getattr(modi_dic, f'{type}_module_dic')[word]
                    break
            else:
                break
        getattr(self, f'{type}_module').append(module)
        getattr(self, f'{type}_dic').append(getattr(modi_dic, f'{module}_dic'))
        self.code += f"{module} = bundle.{module}s[0]\n"

    #create code for else statement
    def convert_else(self):
        else_code = ""
        try:
            for module in self.output_module:
                else_code += f"\n\t\t{modi_dic.else_dic[module]}"
        except:
            pass
        return else_code

    def run(self, bundle, r, mic):
        #initial
        sentence = ""
        type = input("Select Type\nEnter (s) for Speak, (w) for Write: ")
        # sr.energy_threshold = 4000
        while 1:
            try:
                self.initial()
                #write sentence
                if type == 'w' or type == 'W':    
                    sentence = input("Enter sentence: ")
                #speak sentence
                else:
                    sentence = self.record(r, mic)
                sentence = ' '.join(sentence.split())
                #terminate
                if sentence == 'q':
                    break
                self.code = ""
                print(self.tagger.morphs(sentence))
                self.create_code(sentence)
                print(self.code)
                #break to get new sentence
                self.code += "\n\tif keyboard.is_pressed(' '):\n\t\tbreak"
                exec(self.code)
            except:
                traceback.print_exc()
                print("Try again")
        bundle.exit()
        sys.exit()