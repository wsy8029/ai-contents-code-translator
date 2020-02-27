from konlpy.tag import Komoran
import modi
import time

tagger = Komoran()

input_module_dic = {
            #sensor
            "버튼":"button", 

            "다이얼":"dial",

            "환경":"env", "environment":"env",

            "gyroscope":"gyro", "자이로":"gyro", "자이로스코프":"gyro",

            "infrared":"ir", "적외선":"ir",

            "마이크":"mic",

            "울트라소닉":"ultrasonic", "초음파":"ultrasonic"
            }

output_module_dic = {
            #actuator
            "디스플레이":"display", "화면":"display",

            "불":"led",
            
            "모터":"motor",

            "스피커":"speaker"
            }

input_method_dic = {
            #button
            "클릭":".get_clicked()",
            "두번 클릭":".get_double_clicked()", "더블 클릭":".get_double_clicked()"
            "누르":".get_pressed()",
            # "켜지":".get_toggled()",

            #motor
            "각도":".get_degree()",
            "회전속도":".get_turnspeed()",

            #env
            "온도":".get_temperature()",
            "습도":".get_humidity()",
            "밝기":".get_brightness()",
            "빨강":".get_red()",
            "초록":".get_green()",
            "파랑":".get_blue()",

            #gyro
            "롤":".get_roll()",
            "피치":".get_picth()",
            "요":".get_yaw()",
            "x축 각속도":".get_angular_vel_x()",
            "y축 각속도":".get_angular_vel_y()",
            "z축 각속도":".get_angular_vel_z()",
            "x축 각속도":".get_acceleration_x()",
            "y축 각속도":".get_acceleration_y()",
            "z축 각속도":".get_acceleration_z()",
            "진동":".get_vibration()",

            #ir, ultrasonic
            "거리":".get_distance()",

            #mic
            "음량":".get_volume()",
            "진동수":".get_frequency()"
            }

output_method_dic = {
            #display
            # "띄워":".set_text(,"
            "비워":".set_clear()",

            #led
            # "rgb":".set_rgb(",
            "켜":".set_on()",
            "꺼":".set_off()",
            "빨강":".set_red()",
            "초록":".set_green()",
            "파랑":".set_blue()",

            #motor
            # "첫번째 각도":".set_first_degree(",
            # "두번째 각도":".set_second_degree(",
            # "첫번째 속도":".set_first_speed(",
            # "두번째 속도":".set_second_speed(",
            # "첫번째 토크":".set_first_torque(",
            # "두번째 토크":".set_second_torque(",
            # "토크":".set_torque(",
            # "속도":".set_speed(",
            # "각도":".set_degree(",

            #speaker
            # "음정":".set_tune(",
            # "진동수":".set_frequency(",
            # "음량":".set_volume(",
            }

cond_dic = {
            #condition - 단일 조건
            "면":"if", "때":"if",
            #condition - 복합 조건(반대의 경우 함축적으로 포함된 경우)          
            "만":"else",
            "동안":"while", "고 있을 때":"while",
            "보다 클":">",
            "보다 크거나 같을":">=",
            "일":"==",
            "아닐":"!=",
            "보다 작을":"<",
            "보다 작거나 같을":"<="
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
    sentence = input("Enter: ")
    # sentence = '버튼 누르면 불 켜줘'
    # sentence = '버튼 누를때만 불켜줘'
    



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


