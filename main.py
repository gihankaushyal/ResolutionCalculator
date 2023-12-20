#!/usr/bin/env python3

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic

import numpy as np
import math as math

import sys

class MainWindow(qtw.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi("UI/mainWindow.ui", self)
        self.show()

        self.setWindowTitle("ResolutionCalculator")

        self.calculateButton.clicked.connect(self.calculateResolution)
        

    def waveLenthCaluclation(self, beamEnergy):
        return (6.626 * 10**-34 *  3 * 10**8)/(beamEnergy * 1000 * 1.602 * 10**-19) 
    
    def detectorSelection(self):
        detector = self.detectorSelector.currentText()

        if detector == 'Epix10K':
            width = 0.2816
            height = 0.3072
            return (width, height)
        elif detector == 'AGIPD':
            width = 0.2048
            height = 0.2064
            return (width, height)
        elif detector == 'Jungfrau':
            width = 0.1623
            height = 0.1548
            return (width, height)
        elif detector == 'Eiger4M':
            width = 0.1552
            height = 0.1625
            return (width, height)
        else:
            qtw.QMessageBox.critical(self, 'Caution', 'Please Select a detector')

    
    def calculateResolution(self):

        # reading the beam engergy from the gui
        beamEnergy = float(self.beamEnergy.text())

        # reading the detector distance from the gui
        detectorDistance = float(self.detectorDistance.text()) / 1000
        
        width, height = self.detectorSelection()

        edge = width/2
        diagonal = np.sqrt(width**2 + height**2)
        corner = diagonal/2

        print(self.waveLenthCaluclation(beamEnergy))
        print(edge)
        print(corner)
        resolutionAtEdge=round(self.waveLenthCaluclation(beamEnergy)/(2*math.sin(0.5*math.atan2(edge,detectorDistance)))* 10**10,2)
        resolutionAtCorner=round(self.waveLenthCaluclation(beamEnergy)/(2*math.sin(0.5*math.atan2(corner,detectorDistance))) * 10**10,2)

        # setting the caluclated values in the gui
        self.resolutionAtEdge.setText(str(resolutionAtEdge))
        self.resolutionAtCorner.setText(str(resolutionAtCorner))



    
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())