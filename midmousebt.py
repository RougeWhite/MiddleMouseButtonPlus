# -*- coding:utf-8 -*-
#                 ____                                       _____  __         
#                /\  _`\                                    /\___ \/\ \        
#                \ \ \L\_\  __  __     __      ___          \/__/\ \ \ \___    
#                 \ \ \L_L /\ \/\ \  /'__`\  /' _ `\           _\ \ \ \  _ `\  
#                  \ \ \/, \ \ \_\ \/\ \L\.\_/\ \/\ \         /\ \_\ \ \ \ \ \ 
#                   \ \____/\ \____/\ \__/.\_\ \_\ \_\        \ \____/\ \_\ \_\
#                    \/___/  \/___/  \/__/\/_/\/_/\/_/  _______\/___/  \/_/\/_/
#                                                      /\______\               
#                                                      \/______/  
'''
@FileName  :midmousebt.py

@Time      :2022/7/24 8:44

@Author    :Guan_jh

@Email     :guan_jh@qq.com

@Describe  :
'''


def on_click(x,y,button,pressed):
    global drag_flag,mouse_press,_mouse_release
    drag_flag = not drag_flag
    if drag_flag:
        if mouse_press != _mouse_release:
            control = keyboard.Controller()
            time.sleep(0.1)
            with control.pressed(keyboard.Key.ctrl):
                control.press('c')
                control.release('c')



if __name__ == '__main__':
    print_hi('Python')
