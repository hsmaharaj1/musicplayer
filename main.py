# This is the main file for the Music Player
# HYTE Codes, Inc.

from PyQt5 import uic, QtCore, QtWidgets, QtMultimedia, QtGui
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

        #Current Working Directory
        self.cwd = os.getcwd()
        self.cwd = self.cwd.replace("\\", "/")
        # print(self.cwd)

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
    
    def hhmmss(self, ms):
        s = round(ms/1000)
        m,s = divmod(s,60)
        h,m = divmod(m,60)
        return("%02d:%02d:%02d" %(h,m,s) if h else "00:%02d:%02d" %(m,s))

    def position_changed(self, position):
        self.horizontalSlider.blockSignals(True)
        self.horizontalSlider.setValue(position)
        self.horizontalSlider.blockSignals(False)

        if position>0:
            self.cur_dur.setText(self.hhmmss(position))
        
    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)

        if duration>0:
            self.max_dur.setText(self.hhmmss(duration))

    def play(self):
        try:
            self.new = QtCore.QUrl.fromLocalFile(r"%s." % self.mplay[0])
            self.content = QtMultimedia.QMediaContent(self.new)
            self.player.setMedia(self.content)

            # self.btn2.setText("Pause")
            self.btn2.setIcon(QtGui.QIcon(self.cwd + "/Resources/pause.png"))
            # print(self.cwd + "/Resources/pause.png")
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
                # self.btn2.setText("Resume")
                self.btn2.setIcon(QtGui.QIcon(self.cwd + "/Resources/play.png"))
                self.chk = 1
            else:
                self.player.play()
                # self.btn2.setText("Pause")
                self.btn2.setIcon(QtGui.QIcon(self.cwd + "/Resources/pause.png"))
                self.label.setText("Now Playing...")
                self.chk = 0
        except AttributeError:
            self.label_2.setText("No Songs")    

    def open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open file")
        self.chk = 0
        self.label.setText("")
        # self.btn2.setText("Pause")
        self.btn2.setIcon(QtGui.QIcon(self.cwd + "/Resources/pause.png"))
        self.mplay = []
        for i in fname:
            if ".mp3" in i:
                self.mplay.append(i)
        try:
            self.label_2.setText(os.path.basename(self.mplay[0]))
        except IndexError:
            self.label.setText("Please Open a Song!")
        # print(self.mplay)
        
os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'

App = QtWidgets.QApplication(sys.argv)
window = main_player()
window.show()
App.exec_()
