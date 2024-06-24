# pip3 install pyqt5 googletrans==4.0.0-rc1 gtts

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit
from PyQt5.QtGui import QFont
from languages import *
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
import os
from PyQt5.QtMultimedia import QSound
class GoogleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setting()
        self.initUI()
        self.button_click()
    # Setting
    def setting(self):
        self.resize(500, 300)
        self.setWindowTitle("Translator")


    # UI
    def initUI(self):
        self.title = QLabel("Translator")
        self.title.setFont(QFont("Cochin", 25))
        self.language1 = QComboBox()
        self.language2 = QComboBox()
        self.translate_but = QPushButton("Translate")
        self.speak_but = QPushButton("Speak")
        self.reset = QPushButton("Reset")
        self.inputbox = QTextEdit()
        self.outputbox = QTextEdit()
        self.reverse = QPushButton("🔄")
        self.reverse.setFont(QFont("Party LET", 15))
        self.language1.addItems(values)
        self.language2.addItems(values)
        self.language1.setCurrentIndex(21)
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        row1 = QHBoxLayout()
        
        col1.addWidget(self.title)
        col1.addWidget(self.language1)
        col1.addWidget(self.language2)
        col1.addWidget(self.translate_but)
        col1.addWidget(self.speak_but)
        col1.addWidget(self.reset)
        col2.addWidget(self.inputbox)
        col2.addWidget(self.reverse)
        col2.addWidget(self.outputbox)

        row1.addLayout(col1, 40)
        row1.addLayout(col2, 75)
        self.setLayout(row1)
        
        self.setStyleSheet("""
        
        QWidget{background-color: #aaa9ee}
        QLabel{font-family: copperplate;
        font-weight: 500}

        QPushButton{background-color: gray;
        font-size: 20px;
        font-family: Copperplate}

        QPushButton:hover{background-color: blue}
    


        """)

    
    def button_click(self):
        self.translate_but.clicked.connect(self.text_on_screen)
        self.reverse.clicked.connect(self.switch)
        self.reset.clicked.connect(self.restart)
        self.speak_but.clicked.connect(self.text_to_speech)
    #Translator
    def translate_text(self, text, dest_lang, src_lang):
        speaker = Translator()
        translation = speaker.translate(text, dest = dest_lang, src = src_lang)
        return translation.text



    #Translate Spoken Text
    def text_on_screen(self):
        try:
            print("test 1")
            value_from_box1 = self.language1.currentText()
            value_from_box2 = self.language2.currentText()
            key_from_box1 = [key for key, value in LANGUAGES.items() if value == value_from_box1]
            key_from_box2 = [key for key, value in LANGUAGES.items() if value == value_from_box2]

            self.script = self.translate_text(self.inputbox.toPlainText(), key_from_box2[0], key_from_box1[0])

            self.outputbox.setText(self.script)
        except Exception as e:
            print(f"Error: {e}")
    

    def restart(self):
        self.inputbox.clear()
        self.outputbox.clear()

    def switch(self):
        self.text_on_screen()
        l1, l2 = self.language1.currentText(), self.language2.currentText()
        t1, t2 = self.inputbox.toPlainText(), self.outputbox.toPlainText()
        self.outputbox.setText(t1)
        self.inputbox.setText(t2)
        self.language1.setCurrentText(l2)
        self.language2.setCurrentText(l1)

    def text_to_speech(self):
        text = self.outputbox.toPlainText()
        try:
            tts = gTTS(text=text, lang="en")
            tts.save("output.mp3")
            # os.system("start output.mp3")
            sound = AudioSegment.from_mp3("output.mp3")
            sound.export("output.wav",format="wav")

            QSound.play("output.wav")

            os.remove("oupput.mp3")
            os.remove("oupput.wav")


        except Exception as e:
            print("Error:", e)

if __name__ in "__main__":
    app = QApplication([])
    window = GoogleApp()
    window.show()
    app.exec_()
