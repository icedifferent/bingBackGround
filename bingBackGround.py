#!/usr/bin/python3
# 用于获取bing的壁纸并设置为gnome桌面的壁纸
# 逻辑:
# 1.首先判断是否存在此壁纸
# 2.如果今天的壁纸还没获取,那么请求获取(每隔2个小时获取一次)
# 3.遇到网络问题直接跳过,等2小时后再获取
# 4.如成功获取,保存在本地,然后直接设置为新壁纸
import requests
import urllib
import json
import os
import time

class Bing():
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }

    def getBingPicture(self,url):
        try:
            HPImageArchive = requests.get(url,headers=self.headers).text
            # print(HPImageArchive)
            HPImageArchive_data=json.loads(HPImageArchive)
            if(len(HPImageArchive_data['images'])>=1):
                return HPImageArchive_data
            else:
                return False
        except:
            return False

class FileC():
    def saveImg(self,img_url,path,img_name):
        '''
        知道图片地址，下载图片到本地
        '''
        # 判断本地是否已经存在
        filename = path +"/"+ img_name
        if(os.path.isfile(filename)):
            return "failed"
        
        try:
            request = urllib.request.Request(img_url)
            response = urllib.request.urlopen(request)
            
            if (response.getcode() == 200):
                with open(filename, "wb") as f:
                    f.write(response.read()) # 将内容写入图片
                return filename
        except:
            return "failed"

    def saveText(self,text,path,name):
        # 判断本地是否已经存在
        filename = path +"/"+ name
        if(os.path.isfile(filename)):
            return "failed"
        with open(filename, "w") as f:
            f.write(json.dumps(text,ensure_ascii=False))


def timer(n):  
    ''''' 
    每n秒执行一次 
    '''  
    bing = Bing()
    fileC = FileC()
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
    while True:    
        try:
            HPImageArchive_data = bing.getBingPicture(url)
            if(HPImageArchive_data!=False):
                img_url = "https://cn.bing.com"+HPImageArchive_data['images'][0]['url']
                img_name = HPImageArchive_data['images'][0]['hsh']+".jpg"
                txt_name = HPImageArchive_data['images'][0]['hsh']+".txt"

                result = fileC.saveImg(img_url,"picture",img_name)
                fileC.saveText(HPImageArchive_data,"picture_json",txt_name)

                #print(filePath)
                if(result != "failed"):
                    filePath = "\"file:"+os.getcwd()+"/picture/" + img_name+"\""
                    os.system('gsettings set org.gnome.desktop.background picture-uri '+filePath)
                    # 获取成功
                    # 设置为新壁纸
        except:
            return "failed"
        time.sleep(n)
if __name__ == '__main__':
    timer(3600*2)