button_dic = {
            "클릭":".get_clicked()",
            "두번 클릭":".get_double_clicked()", "더블 클릭":".get_double_clicked()",
            "누르":".get_pressed()"
            }

dial_dic = {
            "각도":".get_degree()",
            "속도":".get_turnspeed()"
            }

env_dic = {
            "온도":".get_temperature()",
            "습도":".get_humidity()",
            "밝기":".get_brightness()",
            "빨갛":".get_red()",
            "초록":".get_green()",
            "파랗":".get_blue()"
            }

gyro_dic = {
            "롤":".get_roll()",
            "피치":".get_picth()",
            "요":".get_yaw()",
            "x축 각속도":".get_angular_vel_x()",
            "y축 각속도":".get_angular_vel_y()",
            "z축 각속도":".get_angular_vel_z()",
            "x축 가속도":".get_acceleration_x()",
            "y축 가속도":".get_acceleration_y()",
            "z축 가속도":".get_acceleration_z()",
            "진동":".get_vibration()"
            }

ir_dic = {
            "거리":".get_distance()"
        }

ultrasonic_dic = {
            "거리":".get_distance()"
        }

mic_dic = {
            "음량":".get_volume()",
            "진동수":".get_frequency()"
        }        

display_dic = {
            # "띄우":".set_text(,"
            "비우":".set_clear()"
        }

led_dic = {
            # "rgb":".set_rgb(",
            "켜":".set_on()",
            "끄":".set_off()",
            "빨갛":".set_red()",
            "초록":".set_green()",
            "파랗":".set_blue()"
        }

motor_dic = {
            # "첫번째 각도":".set_first_degree(",
            # "두번째 각도":".set_second_degree(",
            # "첫번째 속도":".set_first_speed(",
            # "두번째 속도":".set_second_speed(",
            # "첫번째 토크":".set_first_torque(",
            # "두번째 토크":".set_second_torque(",
            # "토크":".set_torque(",
            # "속도":".set_speed(",
            # "각도":".set_degree("
        }

speaker_dic = {
            # "음정":".set_tune(",
            # "진동수":".set_frequency(",
            # "음량":".set_volume(",
        }

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

cond_dic = {
            "면":"if", "때":"if",     
            "만":"else",
            "동안":"while", "고 있을 때":"while",
            "보다 클":">",
            "보다 크거나 같을":">=",
            "일":"==",
            "아닐":"!=",
            "보다 작을":"<",
            "보다 작거나 같을":"<="
            }

else_dic = {
            #display
            "display":"display.set_clear()",
            "led":"led.set_off()"
            # "motor":
            # "speaker":
            }