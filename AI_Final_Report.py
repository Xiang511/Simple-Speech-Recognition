import speech_recognition as sr    # recording, speech to text (STT)
from googletrans import Translator # translation
from gtts import gTTS              # text to speech (TTS)
from playsound import playsound    # play mp3 file
import tkinter as tk
import threading as th
import sys
import datetime as dt              #get what time is now


def get_job():
    
    fromidx = var1.get()
    toidx = var2.get()

    # recording
    r = sr.Recognizer()    #啟用麥克風
    r.energy_threshold = 1000    # try others for your microphone
    
    with sr.Microphone(device_index=1) as source:    # change for yours
        r.adjust_for_ambient_noise(source)    # device dependent
        audio = r.listen(source)    #recording

    # STT, speech to text
    sttTXT_org = r.recognize_google(audio, language = fromidx)    # STT

    #print('You say  : '+sttTXT_org)    #印出你說的的話
    print_say_text.set("You say : "+sttTXT_org)
    
    # translation
    translator = Translator()
    result = translator.translate(text=sttTXT_org, src=fromidx, dest=toidx)    #存取翻譯後的文字
    #print('Translated: '+result.text)    #印出翻譯後的文字
    tran_text.set("Translated: "+result.text)

    # TTS, text to speech
    tts = gTTS(result.text, lang=toidx)    #TTS

    # save the mp3 and play it
    
    date_string = dt.datetime.now().strftime('%d%m%Y%H%M%S')
    fileName = 'tts'+date_string+'.mp3'
    tts.save(fileName)    #playsound only from file, try other methods
    ps = playsound(fileName)
   

def start():

    #print('\nSay something...')
    lb_say = tk.Label(win,text="Say something...",font="微軟正黑體 15")
    lb_say.grid(row=3,column=0)

    #delete old labels
    global lb_print_say,lb_tran
    lb_print_say.destroy()
    lb_tran.destroy()

    #new define the two labels
    global print_say_text,tran_text
    print_say_text = tk.StringVar()
    print_say_text.set('You say : ')
    lb_print_say = tk.Label(win,textvariable=print_say_text,font="微軟正黑體 15")
    lb_print_say.grid(row=4,column=0)

    tran_text = tk.StringVar()
    tran_text.set('Translated: ')
    lb_tran = tk.Label(win,textvariable=tran_text,font="微軟正黑體 15")
    lb_tran.grid(row=5,column=0)
    
    getVoice = th.Thread(target = get_job)
    getVoice.start()

    
'''                                    main function                 '''
#create tkinter environment
win = tk.Tk()
win.title("Tai_Chi_Speech")
win.geometry("1000x1000")

def clr():
    win.destroy()
    sys.exit()
#interface
inputLang = ['', 'zh-TW', 'en', 'ja', 'ko', 'fr']   # English, Traditional Chinese, Japanese, Korean
outputLang = ['', 'zh-TW', 'en', 'ja', 'ko', 'fr']    # English, Traditional Chinese, Japanese, Korean
global var1,var2
var1 = tk.StringVar()
var1.set(inputLang[1])
var2 = tk.StringVar()
var2.set(outputLang[2])

lb1 = tk.Label(win,text="choose input language",font="微軟正黑體 15")
lb1.grid(row=0,column=0)

om1 = tk.OptionMenu(win,var1,*inputLang)
om1.grid(row=0,column=1)

lb2 = tk.Label(win,text="choose output language",font="微軟正黑體 15")
lb2.grid(row=1,column=0)

om2 = tk.OptionMenu(win,var2,*outputLang)
om2.grid(row=1,column=1)

#just define the two labels
lb_print_say = tk.Label(win)
lb_tran = tk.Label(win)

bt = tk.Button(win,text="go",bg="blue",font="微軟正黑體 15")
bt.grid(row=0,column=3,rowspan=2)
bt.config(command = start)

bt_clr = tk.Button(win,text="end",bg="yellow",font="微軟正黑體")
bt_clr.grid(row=0,column=4,rowspan=2)
bt_clr.config(command = clr)

win.mainloop()
