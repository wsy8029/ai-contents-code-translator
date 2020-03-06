#module
input_module_dic = {
        #sensor
        "버튼":"button", "Button":"button", "button":"button",
        "다이얼":"dial", "Dial":"dial", "dial":"dial",
        "환경":"env", "environment":"env", "Environment":"env", "Env":"env", "env":"env",
        "Gyroscope":"gyro", "gyroscope":"gyro", "Gyro":"gyro", "gyro":"gyro", "자이로":"gyro", "자이로스코프":"gyro",
        "IR":"ir", "infrared":"ir", "적외선":"ir", "ir":"ir",
        "마이크":"mic", "Mic":"mic", "mic":"mic",
        "울트라소닉":"ultrasonic", "초음파":"ultrasonic", "Ultrasonic":"ultrasonic", "ultrasonic":"ultrasonic"
        }

output_module_dic = {
        #actuator
        "디스플레이":"display", "Display":"display", "display":"display",
        "불":"led", "led 불":"led", "led불":"led", "LED":"led", "led":"led",
        "모터":"motor", "Motor":"motor", "motor":"motor",
        "스피커":"speaker", "Speaker":"speaker", "speaker":"speaker"
        }

#condition
cond_dic = {
        "면":"if", "때":"if",     
        "때 만":"if else", "때만":"if else", "때 마다":"if else", "때마다":"if else",
        "동안":"while else", "동안 만":"while else", "동안만":"while else",
        "고 있을 때":"while else", "고 있을때":"while else",
        "고 있을 때 만":"while else", "고 있을 때만":"while else", "고 있을때만":"while else", "고 있을때 만":"while else"
        }

operand_dic = {
        "보다 클":">", "보다 크":">", "크":">",
        "보다 크거나 같":">=", "이상":">=",
        "아닐":"!=", "아니":"!=",
        "보다 작":"<", "작":"<",
        "보다 작거나 같":"<=", "이하":"<="
        }

else_dic = {
        "display":"display.set_clear()",
        "led":"led.set_off()",
        "motor":"motor.set_speed(0,0)",
        "speaker":"speaker.set_volume(0)"
        }

#input modules
button_dic = {
        "클릭":"clicked()",
        "두번 클릭":"double_clicked()", "더블 클릭":"double_clicked()",
        "누르":"pressed()", "눌리":"pressed()"
        }

dial_dic = {
        "각도":"degree()",
        "속도":"turnspeed()"
        }

env_dic = {
        "온도":"temperature()",
        "습도":"humidity()",
        "밝기":"brightness()",
        "빨갛":"red()", "빨간":"red()", "빨강색":"red()",
        "초록":"green()", "초록색":"green()",
        "파랗":"blue()", "파란":"blue()", "파랑색":"blue()"
        }

gyro_dic = {
        "롤":"roll()",
        "피치":"picth()",
        "요":"yaw()",
        "x축 각속도":"angular_vel_x()",
        "y축 각속도":"angular_vel_y()",
        "z축 각속도":"angular_vel_z()",
        "x축 가속도":"acceleration_x()",
        "y축 가속도":"acceleration_y()",
        "z축 가속도":"acceleration_z()",
        "진동":"vibration()"
        }

ir_dic = {
        "거리":"distance()"
        }

mic_dic = {
        "음량":"volume()",
        "진동수":"frequency()"
        }     

ultrasonic_dic = {
        "거리":"distance()"
        }

#output modules
display_dic = {
        # "띄우":"text(", "띄워":"text(", "보이":"text(", "보여":"text(",
        "비우":"clear()"
        }

led_dic = {
        "rgb":"rgb(",
        "켜":"on()",
        "끄":"off()", "꺼":"off()",
        "빨갛":"red()",
        "초록":"green()",
        "파랗":"blue()"
        }

motor_dic = {
        "첫":"first_",
        "두":"second_",
        "토크":"torque(",
        "속도":"speed(",
        "각도":"degree("
        }

speaker_dic = {
        "음정":"tune(",
        "진동수":"frequency(",
        "음량":"volume(", "볼륨":"volume("
        }