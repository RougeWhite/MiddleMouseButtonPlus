# -*- coding: utf-8 -*-
# 一个简单的search实例
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
        print("解析数据")
        brelist.pop()
        print(prelist)
        print(brelist)
        for j in range(len(brelist)):
            result = result + data[brelist[j]+1:prelist[j+1]]
        return result
    else:
        return data

if __name__ == '__main__':
    data='''<a target=_blank href="/item/%E5%AE%8B%E6%89%BF%E5%AE%AA/230832" data-lemmaid="230832">宋承宪</a>、<a target=_blank href="/item/%E9%AB%98%E9%9B%85%E6%8B%89/1498918" data-lemmaid="1498918">高雅拉</a>、<a target=_blank href="/item/%E9%87%91%E6%A1%90%E4%BF%8A/2602968" data-lemmaid="2602968">金桐俊</a>、<a target=_blank href="/item/%E6%9D%8E%E8%89%BE%E5%84%BF/1865977" data-lemmaid="1865977">李艾儿</a>
'''
    data1 = "aaa"
    dataParse(data)
