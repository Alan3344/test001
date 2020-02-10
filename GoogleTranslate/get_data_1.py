# File Name : get_data
# @date : 2020-02-07  18:13

from tkinter import *
from PIL import Image, ImageTk
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

def changeRgb(*rgb):
    RGB = []
    for r in rgb:
        RGB.append(r)
    return '#%02x%02x%02x' % (RGB[0],RGB[1],RGB[2])

def switch(language='Auto'):
    Language = {
        "Auto": "auto",
        "English": "en",
        "Chinese": "zh-CN",
        "German": "de",
        "Russian": "ru",
        "Japanese": "ja",
        "French": 'fr',
        "Korea": "ko",
    }
    if language in Language.keys():
        return Language[language]

class MainForm(object):
    def __init__(self):

        self.winWidth = 800
        self.winHeight = 600
        self.url = "http://www.baidu.com"
        self.winX = int((1920 - self.winWidth) / 2)
        self.winY = int((1080 - self.winHeight) / 2)
        self.background1 = changeRgb(132, 188, 80)
        self.background2 = changeRgb(178, 224, 223)

        self.dft_language1 = 'Chinese'
        self.dft_language2 = 'English'
        self.result = ''
        self.tip = ''
        self.translate_data = ''
        # self.history_data = ''

        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome()    # chrome_options=options
        self.driver.get(self.url)

    def new_url(self,words,SourceLanguage="auto",TranslateLanguage='en'):
        default_url = "https://translate.google.cn/#view=home&op=translate&sl="
        self.url = default_url + "{}&tl={}&text={}".format(SourceLanguage,TranslateLanguage,words)
        return self.url

    def operatingWeb(self, left_flag=False, right_flag=False):
        # switch language
        self.dft_language1 = 'Auto'
        self.dft_language2 = 'English'
        # handle = 1
        if left_flag is True:
            left_lang = input(
                'Input Current language category\n("Auto"/"English"/"Chinese"/"German"/"Russian"/"Japanese"/"French"/"Korea"): ')
            self.dft_language1 = left_lang
        if right_flag is True:
            right_lang = input(
                'Input Translate language category\n("Auto"/"English"/"Chinese"/"German"/"Russian"/"Japanese"/"French"/"Korea"): ')
            self.dft_language2 = right_lang
        while 1:
            words = input('Input you need translate words(:quit): ')
            if words == ":quit":
                print("The program is about to exit!!")
                self.driver.quit()
                sys.exit()

            l_format = switch(self.dft_language1)
            r_format = switch(self.dft_language2)

            # send requests
            request_new_url = self.new_url(words=words,SourceLanguage=l_format, TranslateLanguage=r_format)
            # try:
            #     handles = self.driver.window_handles
            #     self.driver.switch_to.window(handles[handle])
            # except:print("Current only one handle")
            self.driver.get(request_new_url)
            # js = "window.open('https://www.baidu.com')"
            # self.driver.execute_script(js)

            # print(handles)
            # print("历史的: self.history_data= %s" % self.history_data)
            try:
                while 1:
                    sleep(0.4)
                    self.translate_data = self.driver.find_element(By.CSS_SELECTOR,".tlid-translation.translation span").text
                    # if self.translate_data != self.history_data:
                    #     self.history_data = self.translate_data
                    break
                    # else:
                    #     continue

            except:pass
            self.tip = self.driver.find_element(By.CSS_SELECTOR,"div.gt-cc-l div.gt-cc-l-i").text
            print("The url: {}\n{}\n{}".format(request_new_url, self.translate_data, self.tip))

            # handle += 1



    def screen(self):
        win = Tk()
        win.geometry("{}x{}+{}+{}".format(self.winWidth, self.winHeight, self.winX, self.winY))
        area_size = (640, 10)
        button_size = (6, 1)
        # for i in range(5):
        #     Button(win, width=button_size[0], height=button_size[1], bg='blue', text="这是字", fg="gray", bd=0).place(x=60*i,y=0)
        area1 = Label(win, width=area_size[0], height=area_size[1], bg=self.background1)
        area1.place(x=0,y=20)
        # Label(win, width=area_size[0], height=1).pack()
        area2 = Label(win, width=area_size[0], height=area_size[1], bg=self.background2)
        area2.place(x=0,y=210)

        # win.mainloop()


def application():
    app = MainForm()
    # app.screen()  //主窗体
    app.operatingWeb()

if __name__ == '__main__':
    application()