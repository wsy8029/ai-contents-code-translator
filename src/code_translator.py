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

    # Initialize for new sentence
    def initialize(self):
        self.input_module = []
        self.output_module = []

        self.input_dic = []
        self.output_dic = []

        self.code = ""

    # Record speech
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

    # Create entire code
    def create_code(self, sentence):
        # Split chunks into value, operand, and others
        chunks = self.cond_divider.split(sentence) # ['버튼 누르고 초음파 거리가 30', '일 때', '불 켜고 모터 속도 30으로 해줘']
        # Set input and output modules and their dictionaries
        input_chunk, output_chunk = self.set_modules(chunks)
        # Basic: with no condition
        if len(chunks)==1:
            basic_code = self.convert_chunk('output', output_chunk).replace('\n\t\t', '\n\t')
            self.code += f"\t{basic_code}\n\ttime.sleep(0.1)"

        # Advanced: with condition
        else:
            # If clause
            if modi_dic.cond_dic[chunks[1]] == "if":
                self.code += f"\tif {self.convert_chunk('input', input_chunk)}:\n\t\t{self.convert_chunk('output', output_chunk)}\n\t\ttime.sleep(0.1)"
            # If-else clause
            elif modi_dic.cond_dic[chunks[1]] == "if else":
                self.code += f"\tif {self.convert_chunk('input', input_chunk)}:\n\t\t{self.convert_chunk('output', output_chunk)}\n\t\ttime.sleep(0.1)\n"
                self.code += f"\telse:{self.convert_else()}\n\t\ttime.sleep(0.1)"
            # While-else clause
            else:
                self.code += f"\twhile {self.convert_chunk('input', input_chunk)}:\n\t\t{self.convert_chunk('output', output_chunk)}\n\t\ttime.sleep(0.1)\n"
                self.code += f"\telse:{self.convert_else()}\n\t\ttime.sleep(0.1)"

    '''
    Split phrase into value, operand, and others
    input: 초음파 거리가 30보다 작을
    returns:    phrase - ['초음파', '거리', '가']
                value - 30
                operand - '보다 작을'
    '''
    def split_phrase(self, phrase):
        operand = None
        value = None
        # Extract integer(parameter) of module method
        if self.int_divider.search(phrase) is not None:
            parts = self.int_divider.split(phrase) # ['초음파 거리가 ', '30', '이']
            phrase = self.tagger.morphs(parts[0]) # ['초음파', '거리', '가']
            value = parts[1] # '30'
            operand = self.tagger.morphs(parts[-1]) # '보다 작을'
        # No return value
        else:
            phrase = self.tagger.morphs(phrase)  # ['버튼', '누르', '면']
        return phrase, value, operand # ['초음파', '거리', '가'], '30', '보다 작을'

    '''
    Convert chunks to code
    input:  "output", [' 불 켜', '고', '모터 속도 30으로 해줘']
    returns:    'led.set_on() and motor.set_speed(30)'
    '''
    def convert_chunk(self, type_, chunk): # "input", ['버튼 누르', '고', '초음파 거리가 30보다 작을'] / "output", [' 불 켜', '고', '모터 속도 30으로 해줘']
        code = ""
        try:
            code += getattr(self, f"convert_phrase")(type_, chunk[0], 0) # 'input', '버튼 누르', 0 -> "button.get_pressed()" / 'output', ' 불 켜', 0 -> "led.set_on()"
            # convert input code
            if type_ == "input":
                code += f" {modi_dic.operand_dic[chunk[1]]} " # '고' -> ' and '
                code += getattr(self, f"convert_phrase")(type_, chunk[2], 1) # 'input', '초음파 거리가 30보다 작을', 1 -> "ultrasonic.get_distance() < 30"
            # convert output code
            elif type_ == "output":
                code += "\n\t\t"+ getattr(self, f"convert_phrase")(type_, chunk[2], 1) # 'output', '모터 속도 30으로 해줘', 1 -> "motor.set_speed('30')"
        except:
            pass
        return code

    '''
    Convert phrases to code
    input: "input", '초음파 거리가 30보다 작을', 1
    returns: 'ultrasonic.get_distance() < 30'
    '''
    def convert_phrase(self, type_, phrase, index):
        module = getattr(self, f"{type_}_module")[index]
        dic = getattr(self, f"{type_}_dic")[index]
        # Output module
        if type_ == "output":
            phrase_code = f"{module}.set_"
        # Input module
        elif type_ == "input":
            phrase_code = f"{module}.get_" # 'ultrasonic.get_'
        # Extract value and operand
        phrase, value, operand = self.split_phrase(phrase) # '초음파 거리가 30보다 작을 -> '초음파 거리가', '30', '보다 작을'
        # method
        for morph in phrase:
            try:
                phrase_code += dic[morph] # 'distance()'
            except KeyError:
                pass
        # Return value exists
        if value is not None:
            phrase_code += getattr(self, f"set_{type_}_param")(value, operand) # '30', '보다 작을' -> '< 30'
        return phrase_code # 'ultrasonic.get_distance() < 30'

    '''
    Set input parameters to code
    input:  value - 30
            operand - '보다 작을'
    returns: ' < 30'
    '''
    def set_input_param(self, value, operand):
        param_code = ""
        #operand
        oper_word = None
        for morph in operand:
            oper_word = modi_dic.operand_dic.get(morph) # <
            if oper_word is not None:
                param_code += f" {oper_word} {value}" # ' < 30'
                break
        #'이':'==' case
        if oper_word is None:
            param_code += f" == {value}" # ' == 30'
        return param_code # ' < 30'

    '''
    Set output parameters to code
    input:  value - 30
    returns: '30)'
    '''
    def set_output_param(self, value, operand):
        return f"{value})" # '30)'

    '''
    Set input and output modules and their dictionaries
    input: '버튼 누르거나 초음파 거리가 30보다 작을 때 불 켜고 모터 속도 30으로 해줘'
    returns: 'button = bundle.buttons[0]\nultrasonic = bundle.ultrasonics[0]\nled = bundle.leds[0]\nmotor = bundle.motors[0]'
    '''
    def set_modules(self, chunks):
        # Basic
        if len(chunks) == 1:
            input_chunk = None
            output_chunk = self.op_divider.split(chunks[0]) #'불 켜줘'
        # Advanced
        else:
            # ['버튼 누르거나 초음파 거리가 30보다 작을', '때', '불 켜고 모터 속도 30으로 해줘']
            input_chunk = self.op_divider.split(chunks[0]) #['버튼 누르', '거나', '초음파 거리가 30보다 작을']
            output_chunk = self.op_divider.split(chunks[-1]) #['불 켜', '고', '모터 속도 30으로 해줘']
        # Find input modules
        try:
            self.find_module("input", input_chunk[0]) # '버튼 누르' -> 'button'
            self.find_module("input", input_chunk[2]) # '초음파 거리가 30보다 작을' -> 'ultrasonic'
        except:
            pass
        # Find output modules
        try:
            self.find_module("output", output_chunk[0]) # '불 켜' -> 'led'
            self.find_module("output", output_chunk[2]) # '모터 속도 30으로 해줘' -> 'motor'
        except:
            pass

        self.code += "while 1:\n"
        return input_chunk, output_chunk #['버튼 누르', '거나', '초음파 거리가 30보다 작을'], ['불 켜', '고', '모터 속도 30으로 해줘']

    '''
    Edit typo and find module in dic
    input: '버턴 누르면 불 켜줘'
    returns: 'button = bundle.buttons[0]\nled = bundle.leds[0]'
    '''
    def find_module(self, type_, chunk):
        chunk = chunk.strip()
        chunk = chunk.split()
        # Get matched module name from dic
        for raw in chunk:
            module = getattr(modi_dic, f'{type_}_module_dic').get(raw)
            # Edit typo
            if module is None: # '버턴'
                word, dist = text_process.edit_distance(type_, raw) # '버튼', '0.3'
                # Not a module name typo
                if dist > 1.0:
                    continue 
                # Is a module name typo
                else:
                    module = getattr(modi_dic, f'{type_}_module_dic')[word] # '버튼' -> 'button'
                    break
            else:
                break
        # Set module and dic
        getattr(self, f'{type_}_module').append(module)
        getattr(self, f'{type_}_dic').append(getattr(modi_dic, f'{module}_dic'))
        # Initialize modules in execution code
        self.code += f"{module} = bundle.{module}s[0]\n" # 'button = bundle.buttons[0]\n'
    '''
    Create code for else statement
    input: 'led.set_on()'
    returns: 'led.set_off()'
    '''
    def convert_else(self):
        else_code = ""
        try:
            for module in self.output_module:
                else_code += f"\n\t\t{modi_dic.else_dic[module]}" # '\n\t\tled.set_off()'
        except:
            pass
        return else_code # '\n\t\tled.set_off()'

    def run(self, bundle, r, mic):
        # Initial
        sentence = ""
        type_ = input("Select type\nEnter (s) for Speak, (w) for Write: ")
        while 1:
            try:
                self.initialize()
                # Write sentence
                if type_ == 'w' or type_ == 'W':    
                    sentence = input("Enter sentence: ")
                # Speak sentence
                else:
                    sentence = self.record(r, mic)
                sentence = ' '.join(sentence.split())
                # Terminate
                if sentence == 'q':
                    break
                print(self.tagger.morphs(sentence))
                self.create_code(sentence)
                print(self.code)
                # Break to get new sentence
                self.code += "\n\tif keyboard.is_pressed(' '):\n\t\tbreak"
                exec(self.code)
            except:
                traceback.print_exc()
                print("Try again")
        bundle.exit()
        sys.exit()