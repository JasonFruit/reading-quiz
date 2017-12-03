# -*- coding: utf-8 -*-

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals

import os, sys, random
from glob import glob

from PySide.QtCore import *
from PySide.QtGui import *

from pygame.mixer import *

init()

qapp = QApplication([])

class WordButton(QPushButton):
    def __init__(self, word, sound, handler):
        QPushButton.__init__(self, word)
        self.setMinimumSize(600, 100)
        self._word = word
        self.word = word
        self.handler = handler
        self.clicked.connect(self.on_click)
        self.sound = sound

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, new_word):
        self._word = new_word
        self.setStyleSheet("""QPushButton { font-family: Century Schoolbook, serif; font-size: 18pt; } """)
        self.setText(new_word)
        
    def on_click(self):
        self.handler(self.word)
        
class ReadingGame(QWidget):
    def __init__(self, word_dir):
        QWidget.__init__(self)

        self.word_dir = word_dir

        self.choose_words()

        self._yays = 0
        self._boos = 0
        
        self.do_layout()

    def do_layout(self):
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.score_hbox = QHBoxLayout()
        self.layout.addLayout(self.score_hbox)

        self.yay = QLabel("0")
        self.boo = QLabel("0")
        self.yay.setStyleSheet("QLabel { font-size: 36pt; font-weight: bold; color: green; }")
        self.boo.setStyleSheet("QLabel { font-size: 36pt; font-weight: bold; color: red; }")

        self.score_hbox.addWidget(self.yay)
        self.score_hbox.addStretch()
        self.score_hbox.addWidget(self.boo)

        self.layout.addStretch()
        
        self.play_button = QPushButton("Play >")
        self.play_button.setStyleSheet("QPushButton {font-size: 48pt;}")
        
        self.play_button.setMinimumSize(600, 150)

        self.play_button.clicked.connect(lambda: self.play_word(self.word, False))

        self.layout.addWidget(self.play_button)

        self.layout.addStretch()
        
        self.word_buttons = []

        for word in self.choices:
            self.word_buttons.append(
                WordButton(word,
                           self.words[word],
                           self.play_word))

        for btn in self.word_buttons:
            self.layout.addWidget(btn)

    def choose_words(self):
        self.words = {}

        for fn in glob(os.path.join(self.word_dir, "*")):
            self.words[self.fn_to_word(fn)] = fn

        self.choices = random.sample(self.words, 4)
        self.word = self.choices[random.randint(0,3)]

    def redo_labels(self):
        for i in range(len(self.word_buttons)):
            self.word_buttons[i].word = self.choices[i]

    @property
    def yays(self):
        return self._yays

    @yays.setter
    def yays(self, new_val):
        self._yays = new_val
        self.yay.setText(str(self._yays))

    @property
    def boos(self):
        return self._boos

    @boos.setter
    def boos(self, new_val):
        self._boos = new_val
        self.boo.setText(str(self._boos))
        
    def fn_to_word(self, fn):
        base = os.path.basename(fn)
        return base[:base.index(".")]

    def play_word(self, word, do_score=True):
        if word == self.word and do_score:
            sound = Sound(os.path.join("tada.ogg"))
            sound.play()
            self.yays += 1
            self.choose_words()
            self.redo_labels()
        else:
            sound = Sound(os.path.join(self.word_dir, word + ".ogg"))
            sound.play()
            if do_score:
                self.boos += 1
            

dir = sys.argv[1]

win = ReadingGame(dir)
win.show()

qapp.exec_()
