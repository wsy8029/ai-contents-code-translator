#module
input_module_dic = {
        #sensor
        "버튼":"button", 
        "다이얼":"dial",
        "환경":"env", "environment":"env",
        "gyroscope":"gyro", "자이로":"gyro", "자이로스코프":"gyro",
        "IR":"ir", "infrared":"ir", "적외선":"ir",
        "마이크":"mic",
        "울트라소닉":"ultrasonic", "초음파":"ultrasonic"
        }

output_module_dic = {
        #actuator
        "디스플레이":"display", "화면":"display",
        "불":"led", "led 불":"led", "led불":"led",
        "모터":"motor",
        "스피커":"speaker"
        }

#condition
cond_dic = {
        "면":"if", "때":"if",     
        "때만":"if else",
        "동안":"while else", "고 있을 때":"while else", "동안만":"while else", "고 있을 때만":"while else"
        }

operand_dic = {
        "보다 클":">", "보다 크":">",
        "보다 크거나 같":">=",
        "일":"==", "이":"==",
        "아닐":"!=",
        "보다 작":"<",
        "보다 작거나 같":"<="
        }

else_dic = {
        "display":"display.set_clear()",
        "led":"led.set_off()",
        "motor":"motor.set_speed(0,0)",
        "speaker":"speaker.volume(0)"
        }

#input modules
button_dic = {
        "버튼":"button.get_",

        "클릭":"clicked()",
        "두번 클릭":"double_clicked()", "더블 클릭":"double_clicked()",
        "누르":"pressed()", "눌리":"pressed()"
        }

dial_dic = {
        "다이얼":"dial.get_",

        "각도":"degree()",
        "속도":"turnspeed()"
        }

env_dic = {
        "환경":"env.get_", "environment":"env.get_",
        
        "온도":"temperature()",
        "습도":"humidity()",
        "밝기":"brightness()",
        "빨갛":"red()",
        "초록":"green()", "초록색":"green()",
        "파랗":"blue()"
        }

gyro_dic = {
        "gyroscope":"gyro.get_", "자이로":"gyro.get_", "자이로스코프":"gyro.get_",

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
        "IR":"ir.get_", "infrared":"ir.get_", "적외선":"ir.get_",

        "거리":"distance()"
        }

mic_dic = {
        "마이크":"mic.get_",
        
        "음량":"volume()",
        "진동수":"frequency()"
        }     

ultrasonic_dic = {
        "울트라소닉":"ultrasonic.get_", "초음파":"ultrasonic.get_",

        "거리":"distance()"
        }

#output modules
display_dic = {
        "디스플레이":"display.set_",

        # "띄우":"text(,"
        "비우":"clear()"
        }

led_dic = {
        "불":"led.set_", "led 불":"led.set_", "led불":"led.set_",

        # "rgb":"rgb(",
        "켜":"on()",
        "끄":"off()",
        "빨갛":"red()",
        "초록":"green()",
        "파랗":"blue()"
        }

motor_dic = {
        "모터":"motor.set_",

        "첫":"first_",
        "두":"second_",
        "토크":"torque(",
        "속도":"speed(",
        "각도":"degree("
        }

speaker_dic = {
        "스피커":"speaker.set_",

        "음정":"tune(",
        "진동수":"frequency(",
        "음량":"volume(", "볼륨":"volume("
        }