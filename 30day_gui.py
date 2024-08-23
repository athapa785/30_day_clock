from pydm import Display
import subprocess
import pandas as pd
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtTest
import sys
import os
import time
import subprocess


class ThirtyDay(Display):
    
    def __init__(self, parent=None, args=None):
        super(ThirtyDay, self).__init__(parent=parent, args=args)

        self.label_widgets = [
            self.ui.ebd_fee,
            None,
            self.ui.bth,
            self.ui.bthw,
            self.ui.narc,
            self.ui.sarc,
            self.ui.nit,
            self.ui.sit,
            self.ui.bsy,
            self.ui.thirty,
            self.ui.twenty_six_nine,
            self.ui.twenty_four_five,
            self.ui.twenty_one_three,
            self.ui.lcls_inj,
            self.ui.twenty,
            self.ui.ninteen,
            self.ui.eighteen,
            self.ui.seventeen,
            self.ui.sixteen,
            self.ui.fifteen,
            self.ui.fourteen,
            self.ui.thirteen,
            self.ui.twelve,
            self.ui.eleven,
            self.ui.ten,
            self.ui.s10_inj,
            self.ui.eight_ten_a,
            self.ui.one_seven,
            self.ui.inj_west
        ]


        self.df = pd.read_csv('/home/physics/aaditya/workspace/pydm/30_day_clock/search_data.csv')
        self.ui.update.clicked.connect(self.timerEvent)
        self.load()
        self.refresh = QTimer(self)
        self.refresh.setInterval(5000)
        
        self.timer = self.startTimer(5000)

    
    def ui_filename(self):
        return '/home/physics/aaditya/workspace/pydm/30_day_clock/30day.ui'
        
    def timerEvent(self, event):
        self.ui.update.setText("...")
        self.ui.msg_box.setText("Running backend... Gathering data")
        subprocess.run(["python", "/home/physics/aaditya/workspace/pydm/30_day_clock/backend_30.py"])
        QtTest.QTest.qWait(4000)
        self.ui.update.setText('Update')
        self.df = pd.read_csv('/home/physics/aaditya/workspace/pydm/30_day_clock/search_data.csv')
        self.load()
        self.ui.msg_box.setText("Done.")
        QtTest.QTest.qWait(4000)
        self.ui.msg_box.setText("")    

    def load(self):
        for i,label_widget in enumerate(self.label_widgets):
            if i == 1: continue
            name, state = self.df.iloc[i,0], self.df.iloc[i,1]
            if name == 'BTH West': name = 'BTH W'
            if name == 'S20 INJ': name = 'LCLS INJ'
            label_widget.setText(f'{name} {state}')
            label_widget.setStyleSheet(f"background-color:{self.df.iloc[i,2]}; border-radius:10px;")
        return
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThirtyDay()
    window.show()
    sys.exit(app.exec_())
