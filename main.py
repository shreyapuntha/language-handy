#be my eyes zinu/juno
import sys
import webbrowser
import cv2
import speech_recognition as sr
import playsound
import datetime
import pyjokes

from kivy.app import App
from kivy.uix.image import Image as ki
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import pytesseract as tess

tess.pytesseract.tesseract_cmd = r'C:\Users\Rajeev\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
from gtts import gTTS
import os


Builder.load_string('''
# ScreenManager:
#     CameraClick:
#     ImageWindow:
<CameraClick>:
    orientation: 'vertical'
    Button:
        size_hint_y: None
        height: '50dp'
        text: "Language Handy"
    Camera:
        id: camera
        resolution:(640, 480)
        play: True
    Button:
        size_hint_y: None
        height: '20dp'
        on_press: root.capture()
        #on_release: app.root.current=ImageWindow()

''')




def talk(words):
    if words != '':
        tts = gTTS(words, lang='en')
        filename = 'voice.mp3'
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)



def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say something')
        talk('what would you like me to do')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source)

    try:
        task = r.recognize_google(audio).lower()
        print(task)
    except sr.UnknownValueError:

        task = command()

    return task




def open_camera():

    class CameraClick(BoxLayout):
        def capture(self):
            camera = self.ids['camera']

            camera.export_to_png("opencv_frame_0.png")
            print("Captured")
            talk('           This is a handwritten example. write as good as you can')


    class TestCamera(App):
        def build(self):
            return CameraClick()

    TestCamera().run()


def make_something(task):
    words = ''
    url = ''

    if 'youtube' in task:
        words = 'Opening YouTube'
        url = 'youtube.com'

    elif 'facebook' in task:
        words = 'Opening Facebook'
        url = 'facebook.com'

    elif 'instagram' in task:
        words = 'Opening Instagram'
        url = 'instagram.com'

    elif 'joke' in task:
        words = pyjokes.get_joke()
        print(words)

    elif 'time' in task:
        words = str(datetime.datetime.now())

    elif 'stop' in task:
        talk('Alright, stopping program')
        sys.exit()

    elif 'let me read' in task:
        talk('opening camera to read')
        open_camera()

    # elif 'scan' in task:
    elif 'zeenu' in task:
        talk('hi. i am zeenu. what would you like me to do?')

    elif 'let me see' in task:

        talk('opening camera to see')
        thres = 0.45

        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        cap.set(10, 70)

        className = []
        classFile = 'coco.names'
        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')


        configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        while True:
            success, img = cap.read()
            classIds, confs, bbox = net.detect(img, confThreshold=thres)
            print(classIds, bbox)

            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


            cv2.imshow("Output", img)


            k = cv2.waitKey(1)
            if k % 256 == 27:

                print("Escape hit, closing...")
                break
        cap.release()

    print(task)

    talk(words)
    if url != '':
        webbrowser.open(url)

class ImageWindow(App):
    def build(self):
        talk('hi! i am zeenu')
        img = ki(source='zzz.png')
        return img


ImageWindow().run()
while 1:
    make_something(command())