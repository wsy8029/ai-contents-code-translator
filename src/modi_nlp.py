from konlpy.tag import Komoran
import modi
import time

tagger = Komoran()

module_dic = {
            #sensor
            "버튼":"button", 
            #actuator
            "모터":"motor","바퀴":"motor",
            "led":"led","불":"led",
            #sensing
            "누르":".get_clicked()",
            #acting
            "켜":".set_red(255)",

            #initialize module
            "led":".set_off()"
            
            }

cond_dic = {
            #condition - 단일 조건
            "면":"if", "때":"if",
            #condition - 복합 조건(반대의 경우 함축적으로 포함된 경우)          
            "만":"else"
            }

def get_morph(sen, mor):
    pos = tagger.pos(sen)
    morph = []
    for i in range(len(pos)):
        if pos[i][1] in mor:
            morph.append(pos[i][0])
    
    return morph


def find_dic(noun):
    module = module_dic[noun]

    return module

def add_indent(string,num): # 들여쓰기
    tmp = ''
    for i in range(num):
        tmp += '\t'
    tmp = tmp + string + '\n'

    return tmp

def main():
    bundle = modi.MODI()

    code = []   # 코드가 담길 배열
    sentence = '버튼 누르면 불 켜줘'
    #sentence = '버튼 누를때만 불켜줘'
    



    print('기본 형태소 분석', tagger.pos(sentence))
    
    # 0. if 해당 형태소를 기준으로 chunk1 과 chunk2를 나눔
    # 0-1.if 해당 형태소 추출
    index = ''
    pos = tagger.pos(sentence)
    for elem in pos:
        try:
            x = cond_dic[elem[0]]
            if x == 'if':           # if 하나만 넣어도 되는 경우
                index = elem[0]
            elif x == 'else':       # else까지 암묵적으로 넣어줘야하는 경우
                index = elem[0]
        except:
            pass
    print("인덱스 : ", index)
    # 0-2.조건문 if 해당 형태소를 기준으로 chunk 1,2 분할
    sen = sentence.split(index)
    chunk1 = sen[0]
    chunk2 = sen[1]
    print(chunk1)
    print(chunk2)
    
    # 1. 각 chunk에 대하여 명사(모듈)만 추출하여 선언 (ex: motor = bundle.motors[0])
    nouns = tagger.nouns(sentence) # 명사 형태소 추출
    print(nouns)
    for noun in nouns:
        if noun in module_dic:
            module = find_dic(noun)
            tmp = module + ' = bundle.' + module + 's[0]'
            code.append(tmp + '\n')
    
    # 2. 각 chunk에 대해 명사와 동사(모듈과 동작)만 추출하여 pair를 만듦 (ex: led.on() )
    tag_noun = ['NNP', 'NNG']
    tag_verb = ['VV']

    #chunk1
    n1 = find_dic(get_morph(chunk1,tag_noun)[0])
    v1 = find_dic(get_morph(chunk1,tag_verb)[0])

    #chunk2
    n2 = find_dic(get_morph(chunk2,tag_noun)[0])
    v2 = find_dic(get_morph(chunk2,tag_verb)[0])

    # case에 따라 append 되도록 해야하며, 들여쓰기를 유의해야 함.
    # 위에서 else로 들어갈 경우, else문도 새로 만들어서 추가하도록 할 것.

    ind = cond_dic[index]
    code.append('while True:\n')
    if ind == 'if' or ind == 'else':
        code.append(add_indent('if '+n1+v1+':',1))
        code.append(add_indent(n2+v2,2))
        if ind == 'else':
            code.append(add_indent('else:',1))
            code.append(add_indent(n2+module_dic[n2],2))
    else:
        code.append(add_indent(n2+v2,0))
    code.append(add_indent('time.sleep(0.01)',1))
    
    code = ''.join(code)
    print(code)
    exec(code)
    

if __name__ == '__main__':
    main()


