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



import pyperclip
import time
import random
import hashlib
import copy
import urllib.parse
import requests
from pynput.mouse import Listener
from pynput import keyboard
# from bs4 import BeautifulSoup
import re
import os
import sys
import json
import tkinter as tk
from DragWindow import DragWindow
import math
import webbrowser
import wx  #  pip install wxPython
import wx.adv
import ast
from PIL import Image, ImageTk
from threading import Thread

drag_flag = True
mouse_press =(0,0)
mouse_release =(0,0)
# 全局结束
global stop_threads
# 卡片控制
global opencardbool


# 百度翻译方法
def baidu_translate(content):
    if len(content) > 4891:
        return '输入请不要超过4891个字符！'
    salt = str(random.randint(0, 50))
    # 申请网站 http://api.fanyi.baidu.com/api/trans
    appid = '20200606000487712' # 这里写你自己申请的
    secretKey = 'anwvFpJWVLRN2B4QjPzo'# 这里写你自己申请的
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()
    head = {'q': f'{content}',
            'from': 'en',
            'to': 'zh',
            'appid': f'{appid }',
            'salt': f'{salt}',
            'sign': f'{sign}'}
    j = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', head)
    res = j.json()['trans_result'][0]['dst']
    res = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub(' ', res)
    return res


# 退出
def demoexit():
    sys.exit()

# 包含中文
def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

# 图片重定位
def resize(path):
    image = Image.open(path)
    raw_width, raw_height = image.size[0], image.size[1]
    min_height = 20
    min_width = int(raw_width * min_height / raw_height)
    return image.resize((min_width, min_height))
# 前页




# 新建文件
def text_create(path, msg):
    f = open(path, 'w',encoding='utf-8')
    f.write(msg)
    f.close()

# # 动态写入用户配置
# def WriteUserSet(SetJson,error_List):
#     Now_Path = os.getcwd()
#     user_setting_filename = SetJson["userconfig"]
#     User_setting_filename_dir =Now_Path + "\\" + user_setting_filename
#     # 获取设置
#     UserSet = json.loads(str(GetUserSet(SetJson)).split('\'')[1])
#     try:
#         UserSet.remove(error_List[0])
#     except:
#         print("页面已经移除了")
#     text_create(User_setting_filename_dir, str(UserSet))
#     Result_List = UserSet4Data(UserSet, Data_List)
#     return UserSet,Result_List

# 系统设置
def Setting(retval,default_setting_filename):

    default_setting_filename_dir = retval + "\\" + default_setting_filename
    if os.path.exists(default_setting_filename_dir):
        # 读取配置文件
        SetJson = loadSet(default_setting_filename_dir)
        User_Setting_filename = SetJson["userconfig"]
        User_setting_filename_dir = retval + "\\" + User_Setting_filename
        #  创建配置文件
        if os.path.exists(User_setting_filename_dir) ^ 1:
            print("正在创建配置文件,请稍后")
            # xuanzhong = InIdata(SetJson)
            text_create(User_setting_filename_dir, "这里填入配置文件")
            print("用户配置文件创建完成")
            return SetJson
        else:
            print("用户配置文件存在")
            return SetJson
    else:
        print("code:400 初始化失败:配置文件丢失")
        sys.exit()

# 获取用户设置
def GetUserSet(SetJson):
    Now_Path = os.getcwd()
    UserSetFileName = SetJson["userconfig"]
    Dir_Name = Now_Path+"\\"+UserSetFileName
    f = open(Dir_Name)
    data = f.readlines()
    return data

# 加载系统设置
def loadSet(default_setting_filename_dir):
    with open(default_setting_filename_dir, 'r') as f:
        SetJson = json.load(f)
    return SetJson

# # 初始化数据
# def InIdata(SetJson):
#     Result_List = GetData(SetJson)
#     xuanzhong = str(list(range(len(Result_List))))
#     return xuanzhong


# 开启系统推盘
class FolderBookmarkTaskBarIcon(wx.adv.TaskBarIcon):
    ICON = 'icon.ico'
    TITLE = '超级中键'

    MENU_ID1, MENU_ID2 = wx.NewIdRef(count=2)

    def __init__(self):
        super().__init__()

        # 设置图标和提示
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)

        # 绑定菜单项事件
        self.Bind(wx.EVT_MENU, self.onExit, id=self.MENU_ID1)

    def CreatePopupMenu(self):
        '''生成菜单'''

        menu = wx.Menu()
        # 添加两个菜单项
        # menu.Append(self.MENU_ID1, '弹个框')
        menu.Append(self.MENU_ID1, '退出')
        return menu


    def onExit(self, event):
        try:
            wx.Exit()
        # time.sleep(1)
            sys.exit()
        except:
            sys.exit()




class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__()
        FolderBookmarkTaskBarIcon()


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True

recent_txt = ''

notblock =[0,0,0,0]

def calnotblock(SetJson,x,y):
    witdh = SetJson['widget_width']
    height = SetJson['widget_height']
    notblock[0] = x
    notblock[1] = y
    notblock[2] = x+witdh
    notblock[3] = y+height
    return notblock

def notblockToF(x,y,notblock):
    # print(x,y,notblock)
    if x>notblock[0] and x<notblock[2] and y > notblock[1] and y<notblock[3]:
        # print("在区域内")
        return True
    else:
        # print("在区域外")
        return False


widget_display = False
root_list = []

def on_click(x,y,button,pressed):
    global drag_flag,mouse_press,mouse_release,recent_txt,widget_display,notblock,mouse_x,mouse_y

    recent_txt = pyperclip.paste()

    mouse_x = x
    mouse_y = y
    if button.name == 'middle' and pressed:
        if widget_display == False:
            root = DragWindow()
            root_list.append(root)
            widget_display = True
            Gui(root, SetJson,x,y,recent_txt)
            # 计算区域
            notblock = calnotblock(SetJson, x, y)
            root.mainloop()
        # 计算触摸区域



    drag_flag = not drag_flag
    # 鼠标点击
    if pressed and button.name == 'left':
        mouse_press =(x,y)
        # 验证是否有页面出现
        if widget_display and button.name == 'left':
            root = root_list.pop()
            # 验证是否在页面中点击 True 是 False 否
            blockToF = notblockToF(x, y, notblock)
            if not blockToF:
                try:
                    while cardroot_list:
                        cardroot = cardroot_list.pop()
                        cardroot.quit()
                    root.quit()
                except:
                    print("列表不存在")
                    root.quit()
                widget_display = False
            else:
                root_list.append(root)
#     if not pressed and button.name == 'left':
#         mouse_release=(x,y)
#     if drag_flag:
#         if mouse_press != mouse_release:
#             control = keyboard.Controller()
#             time.sleep(0.01)
#             with control.pressed(keyboard.Key.ctrl):
#                 control.press('c')
#                 control.release('c')
#             time.sleep(0.01)
#             recent_txt = pyperclip.paste()
# #            处理文本
#         else:
#             pass

def midmouseplus():
    time.sleep(0.4)
    with Listener(on_click=on_click) as listener:
        listener.join()

# 打开系统托盘
def OpenSystemPLANT():
    app = MyApp()
    app.MainLoop()

# 单词内容长度判断
def len4text(text,length):

    if len(text) > int(length):
        text = text[0:length] + "..."
    return text

def baidubaike(bk_key,lenth):
    result = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }
    # "王者荣耀"
    datastr = "http://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="+bk_key+"&bk_length="+str(lenth)
    j = requests.get(datastr,headers=headers, timeout=5, allow_redirects = True)
    if j.json() != json.loads("{}"):
        desc = j.json()['desc']
        abstract = j.json()['abstract']
        card = j.json()['card']
        totalUrl = j.json()['url']
        result.append(str(desc))
        result.append(str(abstract))
        result.append(str(card))
        result.append(str(totalUrl))
    else:
        result = ['查询失败','查询失败','查询失败','']
    return result

# 字符换行
def len4data(context,length):
    tmplist = list(context)
    for i in range(len(tmplist)):
        if i % int(length) == 0 and i!=0:
            tmplist.insert(i, '\n')
    context = ''.join(tmplist)
    return context


# Gui
def Gui(root,SetJson,x,y,recent_txt):
    # 创建Tk对象，Tk代表窗口
    # root = tk.Tk()
    # 设置窗口标题
    # 创建Label对象，第一个参数指定该Label放入root
    # 　导入DragWindow类
    widget_width = int(SetJson["widget_width"])
    widget_height = int(SetJson["widget_height"])
    widget_postion_width = int(x)
    widget_postion_height = int(y)

    root.set_window_size(widget_width, widget_height)
    root.set_display_postion(widget_postion_width, widget_postion_height)
    # 对关键词搜索
    jsoncontext = baidubaike(recent_txt, 600)
    des = jsoncontext[0]
    abstract = jsoncontext[1]
    card = jsoncontext[2]
    try:
        cardtext_list = ast.literal_eval(card)
    except:
        print("值无效")
        cardtext_list = []
    url = jsoncontext[3]
    # 定义图片
    global card_img
    card_img = ImageTk.PhotoImage(resize(os.getcwd() + './images/card.png'))
    # 创建画布
    canvas = tk.Canvas(root, width=widget_width, height=widget_height, bg="white")
    canvas.place(x=1, y=0)
    canvas.create_line(20, 0, 20, 325)
    # 创建按钮
    pre_bt = tk.Button(root
                       # , text="<<"
                      , command=lambda: OpenCard(cardtext_list)
                      , bg="white"
                      , activebackground="white"
                      , activeforeground="white"
                      , fg="white"
                      , relief="flat"
                      )
    pre_bt.config(image=card_img)
    pre_bt.place(x=175,y = 0)


    # 判断输入词汇是否是中文
    if not (recent_txt.encode( 'UTF-8' ).isalpha()):
        # 中文
        # 单词内容长度判断
        if is_chinese(recent_txt):
            if len(recent_txt)>7:
                recent_txt = recent_txt[0:7]+"..."
        else:
            if len(recent_txt)>14:
                recent_txt = recent_txt[0:14]+"..."

        text_bai1 = tk.Label(root, text='百',  # 设置文本内容
                             justify='left',  # 设置文本对齐方式：左对齐
                             anchor='nw',  # 设置文本在label的方位：西北方位
                             font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                             fg="black",
                             bg="white")
        text_bai1.place(x=1, y=42)
        text_du = tk.Label(root, text='度',  # 设置文本内容
                           justify='left',  # 设置文本对齐方式：左对齐
                           anchor='nw',  # 设置文本在label的方位：西北方位
                           font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                           fg="black",
                           bg="white")
        text_du.place(x=1, y=104)
        text_bai2 = tk.Label(root, text='百',  # 设置文本内容
                             justify='left',  # 设置文本对齐方式：左对齐
                             anchor='nw',  # 设置文本在label的方位：西北方位
                             font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                             fg="black",
                             bg="white")
        text_bai2.place(x=1, y=166)
        text_ke = tk.Label(root, text='科',  # 设置文本内容
                           justify='left',  # 设置文本对齐方式：左对齐
                           anchor='nw',  # 设置文本在label的方位：西北方位
                           font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                           fg="black",
                           bg="white")
        text_ke.place(x=1, y=228)
        # 原内容
        origin_text =tk.Label(root, text=recent_txt,  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 15,'bold'),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        origin_text.place(x=25, y=5)

        des_text =tk.Label(root, text="描述",  # 设置文本内容
                 justify='center',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 8),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        des_text.place(x=23, y=35)

        des_text =tk.Label(root, text=des,  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 8),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white"
                           ,wraplength=165)
        des_text.place(x=23, y=54)
        des_text.bind('<Button>', lambda event: openUrl(event, url))

        abstract_text =tk.Label(root, text="介绍",  # 设置文本内容
                 justify='center',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 8),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        abstract_text.place(x=23, y=75)
        abstract = "    "+abstract
        abstract_text =tk.Label(root, text=abstract,  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 9),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white"
                ,wraplength=165
                                )
        abstract_text.place(x=23, y=95)
        abstract_text.bind('<Button>', lambda event: openUrl(event, url))

    else:
        # 英文
        text_fan = tk.Label(root, text='翻',  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        text_fan.place(x=1, y=20)
        text_yi = tk.Label(root, text='译',  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        text_yi.place(x=1, y=50)
        # 单词中文判断

        # 单词内容长度判断
        recent_txt = len4text(recent_txt,14)
        origin = tk.Label(root, text=recent_txt  # 设置文本内容
                 ,justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 15,"bold"),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        origin.place(x=25, y=5)

        baidufanyi = tk.Label(root, text="以下翻译来源---百度翻译"  # 设置文本内容
                 ,justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 8),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        baidufanyi.place(x=40, y=33)



        # 翻译后的原文
        tran_context = baidu_translate(recent_txt)
        tran_context = len4text(tran_context,10)
        baidufanyi_context = tk.Label(root, text= tran_context # 设置文本内容
                 ,justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 15,"bold"),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        baidufanyi_context.place(x=23, y=50)


        canvas.create_line(0, 90, 200, 90)

        text_bai1 = tk.Label(root, text='百',  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        text_bai1.place(x=1, y=133)
        text_du = tk.Label(root, text='度',  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")

        text_du.place(x=1, y=163)
        text_bai2 = tk.Label(root, text='百',  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        text_bai2.place(x=1, y=193)
        text_ke = tk.Label(root, text='科',  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        text_ke.place(x=1, y=223)


        des_text =tk.Label(root, text=des,  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 13),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        des_text.place(x=23, y=95)
        des_text.bind('<Button>', lambda event: openUrl(event, url))
        abstract = "    "+abstract
        abstract_text =tk.Label(root, text=abstract,  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 9),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white"
                ,wraplength=165
                                )
        abstract_text.place(x=23, y=125)
        abstract_text.bind('<Button>', lambda event: openUrl(event, url))





# 打开连接
def openUrl(event,j):
    webbrowser.open(j, new=0, autoraise=True)

# 数据解析
def dataParse(data):
    result = ''
    if data.find(">")!= -1 or data.find("<")!= -1:
        pre = "<"
        prelist = []
        bre = ">"
        brelist = []
        for index ,i in enumerate(data):
            if i == pre:
                prelist.append(index)
            if i ==bre:
                brelist.append(index)
        if prelist[0]!=0:
            result = data[0:prelist[0]]
        brelist.pop()
        for j in range(len(brelist)):
            result = result + data[brelist[j]+1:prelist[j+1]]
        return result
    else:
        return data



def CardGui(SetJson,x,y,num,cardtext_list):
    # 开启卡片列表
    global cardroot_list
    temp_list = []
    j = 0
    for i in range(int(num)):
        if i%6==0:
            cardx = x+5 + j*(int(SetJson["card_width"])+5)
            j = j+1
        cardy = (i-((j-1)*6))*(int(SetJson["card_height"])+5)+y
        root = DragWindow()
        root.set_window_size(int(SetJson["card_width"]), int(SetJson["card_height"]))
        root.set_display_postion(cardx, cardy)
        # eval(str(cardtext_list[i]))['name']
        title_text =tk.Label(root, text=eval(str(cardtext_list[i]))['name'],  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 10),  # 设置字体：微软雅黑，字号：18
                 fg="black",
                 bg="white")
        title_text.place(x=0, y=-1)

        getcard_des = str(eval(str(cardtext_list[i]))['format'])

        getcard_des_tmp_list = getcard_des.split("\'")
        new_des = getcard_des_tmp_list[1]
        thedes = dataParse(new_des)
        card_des=tk.Label(root, text=thedes,  # 设置文本内容
                 justify='left',  # 设置文本对齐方式：左对齐
                 anchor='nw',  # 设置文本在label的方位：西北方位
                 font=('微软雅黑', 7),  # 设置字体：微软雅黑，字号：18
                 fg="black",
         wraplength = 98,
                 bg="white")
        card_des.place(x=0, y=18)

        temp_list.append(root)

    cardroot_list = [i for i in temp_list]
    # print(cardroot_list)
    while temp_list:
        root = temp_list.pop()
        root.mainloop()
# 卡片控制
def OpenCard(cardtext_list):
    global opencardbool
    opencardbool = not opencardbool
    if not opencardbool:
        # print("打开卡片")
        num = len(cardtext_list)
        firstcardx = notblock[2]
        firstcardy = notblock[1]
        cardthread = Thread(target=CardGui(SetJson, firstcardx, firstcardy, num,cardtext_list))
        # 打开系统托盘
        cardthread.daemon = True
        cardthread.start()

    else:
        # print("关闭卡片")
        while cardroot_list:
            cardroot = cardroot_list.pop()
            cardroot.quit()


if __name__ == '__main__':
    opencardbool = True
    #  系统初始化
    Now_Path = os.getcwd()
    default_setting_filename = "config.json"
    default_setting_filename_dir = Now_Path + "\\" + default_setting_filename
    task_list =[]

    #  Setting
    # 获取系统设置
    SetJson = Setting(Now_Path, default_setting_filename)
    # 获取用户设置
    # UserSet = json.loads(str(GetUserSet(SetJson)).split('\'')[1])
    # print(UserSet)

    t1 = Thread(target=midmouseplus)
    task_list.append(t1)
    # 打开系统托盘
    t1.daemon = True
    t1.start()
    OpenSystemPLANT()


    # # 测试用力
    # recent_txt = "关家豪"
    # baidubaike(recent_txt,600)
    # root = DragWindow()
    # x = 1500
    # y = 540
    #
    # Gui(root, SetJson, x, y, recent_txt)
    #
    # root.mainloop()


