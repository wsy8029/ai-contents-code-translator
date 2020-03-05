from konlpy.tag import Komoran
import modi_dic
import modi
import re
import time
import traceback
import sys
import keyboard

class CodeTranslator(object):

    def __init__(self):
        self.tagger = Komoran(userdic='user_dic.txt')
        self.cond_divider = re.compile('(고 있을 때만|때만|동안만|고 있을 때|때|동안|만|면)')
        self.int_divider = re.compile('(\d+(\, \d+)?)')

        self.input_module = None
        self.output_module = None
        self.input_dic = None
        self.output_dic = None

        self.code = ""

    #split chunks into value, operand, and others
    def split_chunk(self, chunk):
        operand = None
        value = None
        #extract integer(parameter) of module method
        if self.int_divider.search(chunk) != None:
            split_chunk = self.int_divider.split(chunk)
            chunk = self.tagger.pos(split_chunk[0])
            value = split_chunk[1]
            operand = self.tagger.pos(split_chunk[-1])
        else:
            chunk = self.tagger.pos(chunk)
        return chunk, value, operand

    #convert input chunks to code
    def convert_input(self, chunk):
        input_code = ""
        chunk, value, operand = self.split_chunk(chunk)
        #module name and method
        for morph in chunk:
                if self.input_dic.get(morph[0])!=None:
                    input_code += self.input_dic[morph[0]]
        #methods with return value
        if value != None:
            #operand
            for morph in operand:
                oper_word = modi_dic.operand_dic.get(morph[0])
                if oper_word !=None:
                    input_code += f" {oper_word} {value}"
            #'이':'==' case
            if oper_word == None:
                input_code += f" == {value}"
        return input_code

    #convert output chunks to code
    def convert_output(self, chunk):
        output_code = ""
        chunk, value, _ = self.split_chunk(chunk)
        #module name and method
        for morph in chunk:
            if self.output_dic.get(morph[0])!=None:
                output_code += self.output_dic[morph[0]]
        #methods with parameter
        if value != None:
            output_code += f"{value})"
        return output_code
                
    #set input and output modules and their dictionaries
    def set_modules(self, chunks):
        if len(chunks) != 1:
            self.input_module = modi_dic.input_module_dic[self.tagger.nouns(chunks[0])[0]]
            self.input_dic = getattr(modi_dic, f"{self.input_module}_dic")
            self.code += f"{self.input_module} = bundle.{self.input_module}s[0]\n"

        self.output_module = modi_dic.output_module_dic[self.tagger.nouns(chunks[-1])[0]]
        self.output_dic = getattr(modi_dic, f"{self.output_module}_dic")
        self.code += f"{self.output_module} = bundle.{self.output_module}s[0]\nwhile True:\n"

    #create entire code
    def create_code(self, sentence):
        #split chunks into value, operand, and others
        chunks = self.cond_divider.split(sentence)
        #set input and output modules and their dictionaries
        self.set_modules(chunks)
        #basic: with no condition
        if len(chunks)==1:
            self.code += f"\t{self.convert_output(chunks[0])}\n\ttime.sleep(0.1)"

        #advanced: with condition
        else:
            #if clause
            if modi_dic.cond_dic[chunks[1]] == "if":
                self.code += f"\tif {self.convert_input(chunks[0])}:\n\t\t{self.convert_output(chunks[-1])}"
            #if-else clause
            elif modi_dic.cond_dic[chunks[1]] == "if else":
                self.code += f"\tif {self.convert_input(chunks[0])}:\n\t\t{self.convert_output(chunks[-1])}\n\t\ttime.sleep(0.1)\n"
                self.code += f"\telse:\n\t\t{modi_dic.else_dic[self.output_module]}\n\t\ttime.sleep(0.1)"
            #while-else clause
            else:
                self.code += f"\twhile {self.convert_input(chunks[0])}:\n\t\t{self.convert_output(chunks[-1])}\n\t\ttime.sleep(0.1)\n"
                self.code += f"\telse:\n\t\t{modi_dic.else_dic[self.output_module]}\n\t\ttime.sleep(0.1)"

    def run(self):
        #initial
        bundle = modi.MODI()
        sentence = ""
    
        while True:
            #input sentence
            sentence = input("Enter: ")
            sentence = ' '.join(sentence.split())
            #terminate
            if sentence == 'q':
                break
            self.code = ""
            print(self.tagger.pos(sentence))
            try:
                self.create_code(sentence)
                print(self.code)
                #break to get new sentence
                self.code += "\n\tif keyboard.is_pressed(' '):\n\t\tbreak"
                exec(self.code)
            except:
                print("Try again")
        bundle.exit()
        sys.exit()