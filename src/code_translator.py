from konlpy.tag import Komoran
import modi_dic
import modi
import re
import time
import traceback
import sys

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

    def convert_input(self, chunk):
        input_code = ""
        value = None
        if self.int_divider.search(chunk) != None:
            split_chunk = self.int_divider.split(chunk)
            chunk = self.tagger.pos(split_chunk[0])
            value = split_chunk[1]
            operand = self.tagger.pos(split_chunk[-1])
        else:
            chunk = self.tagger.pos(chunk)

        if value != None:
            for morph in chunk:
                if self.input_dic.get(morph[0])!=None:
                    input_code += self.input_dic[morph[0]]
            for morph in operand:
                if modi_dic.operand_dic.get(morph[0])!=None:
                    input_code += modi_dic.operand_dic[morph[0]]
                    input_code += value
        else:
            for morph in chunk:
                if self.input_dic.get(morph[0])!=None:
                    input_code += self.input_dic[morph[0]]
        return input_code

    def convert_output(self, chunk):
        output_code = ""
        value = None
        if self.int_divider.search(chunk) != None:
            split_chunk = self.int_divider.split(chunk)
            chunk = self.tagger.pos(split_chunk[0])
            value = split_chunk[1]
        else:
            chunk = self.tagger.pos(chunk)

        if value != None:
            for morph in chunk:
                if self.output_dic.get(morph[0])!=None:
                    output_code += self.output_dic[morph[0]]
            output_code += value + ")"
        else:
            for morph in chunk:
                if self.output_dic.get(morph[0])!=None:
                    output_code += self.output_dic[morph[0]]
        return output_code
                
    def set_modules(self, chunks):
        if len(chunks) != 1:
            self.input_module = modi_dic.input_module_dic[self.tagger.nouns(chunks[0])[0]]
            self.input_dic = getattr(modi_dic, f"{self.input_module}_dic")
            self.code += f"{self.input_module} = bundle.{self.input_module}s[0]\n"

        self.output_module = modi_dic.output_module_dic[self.tagger.nouns(chunks[-1])[0]]
        self.output_dic = getattr(modi_dic, f"{self.output_module}_dic")
        self.code += f"{self.output_module} = bundle.{self.output_module}s[0]\nwhile True:\n"

    def run(self):
        # bundle = modi.MODI()
        sentence = input("Enter: ")
        print(self.tagger.pos(sentence))
        try:
            chunks = self.cond_divider.split(sentence)
            self.set_modules(chunks)
            #basic
            if len(chunks)==1:
                self.code += f"\t{self.convert_output(chunks[0])}\n\ttime.sleep(1)"
            #advanced
            else:
                if modi_dic.cond_dic[chunks[1]] == "if":
                    self.code += f"\tif {self.convert_input(chunks[0])}:\n\t\t{self.convert_output(chunks[-1])}"
                elif modi_dic.cond_dic[chunks[1]] == "if else":
                    self.code += f"\tif {self.convert_input(chunks[0])}:\n\t\t{self.convert_output(chunks[-1])}\n\t\ttime.sleep(1)\n"
                    self.code += f"\telse:\n\t\t{modi_dic.else_dic[self.output_module]}\n\t\ttime.sleep(1)"
                else:
                    self.code += f"\twhile {self.convert_input(chunks[0])}:\n\t\t{self.convert_output(chunks[-1])}\n\t\ttime.sleep(1)\n"
                    self.code += f"\telse:\n\t\t{modi_dic.else_dic[self.output_module]}\n\t\ttime.sleep(1)"
            print(self.code)
            # exec(self.code)

        except:
            traceback.print_exc()
            print("Try again")
        finally:
            sys.exit()