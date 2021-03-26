# This is the main file for the Music Player
# HYTE Codes, Inc.

from PyQt5 import uic, QtCore, QtWidgets, QtMultimedia
import sys
import os

class main_player(QtWidgets.QMainWindow):
    def __init__(self):
        super(main_player, self).__init__()
        uic.loadUi("basic2.ui", self)

        self.btn1.clicked.connect(self.play)
        self.btn2.clicked.connect(self.pause)
        self.btn3.clicked.connect(self.open)

        self.player = QtMultimedia.QMediaPlayer()
        self.label_2.setText("No Songs Selected")

        # Slider Making
        # self.horizontalSlider.setRange(0,0)
        self.horizontalSlider.sliderMoved.connect(self.set_position)

        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

        #Volume Slider
        self.volume_ctrl.sliderMoved.connect(self.volume)

    def volume(self):
        vol = self.volume_ctrl.value()
        self.player.setVolume(vol)

    def set_position(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)

    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)

    def play(self):
        try:
            self.new = QtCore.QUrl.fromLocalFile(r"%s." % self.mplay[0])
            self.content = QtMultimedia.QMediaContent(self.new)
            self.player.setMedia(self.content)

            self.btn2.setText("Pause")
            self.chk = 0

            self.label.setText("Now Playing...")
            self.player.play()
        except AttributeError:
            self.label.setText("No Song is Selected")
        except IndexError:
            self.label.setText("Please Open a Song File")

    def pause(self):
        try:
            if not self.chk:
                self.player.pause()
                self.label.setText("Paused!")
                self.btn2.setText("Resume")
                self.chk = 1
            else:
                self.player.play()
                self.btn2.setText("Pause")
                self.label.setText("Now Playing...")
                self.chk = 0
        except AttributeError:
            self.label_2.setText("No Songs")    

    def open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open file")
        self.chk = 0
        self.label.setText("")
        self.btn2.setText("Pause")
        self.mplay = []
        for i in fname:
            if ".mp3" in i:
                self.mplay.append(i)
        try:
            self.label_2.setText(os.path.basename(self.mplay[0]))
        except IndexError:
            self.label.setText("Please Open a Song!")
        # print(self.mplay)
        

App = QtWidgets.QApplication(sys.argv)
window = main_player()
window.show()
App.exec_()
