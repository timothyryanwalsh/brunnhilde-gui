#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
import subprocess
import sys

import design

class BrunnhildeApp(QMainWindow, design.Ui_Brunnhilde):

    def __init__(self, parent=None):
        super(BrunnhildeApp, self).__init__(parent)
        self.setupUi(self)

        # build browse functionality buttons
        self.dirSourceBtn.clicked.connect(self.browse_dirsource)
        self.diskImageSourceBtn.clicked.connect(self.browse_diskimage)
        self.dirDestinationBtn.clicked.connect(self.browse_dirdest)
        self.diskImageDestinationBtn.clicked.connect(self.browse_diskimagedest)

        # build start functionalities
        self.dirStartScanBtn.clicked.connect(self.start_scan_dir)
        self.diskImageStartScan.clicked.connect(self.start_scan_diskimage)

    @pyqtSlot()
    def readStdOutputDir(self):
        self.dirOutput.append(QString(self.proc.readAllStandardOutput()))

    @pyqtSlot()
    def readStdErrorDir(self):
        self.dirOutput.append(QString(self.proc.readAllStandardError()))

    @pyqtSlot()
    def readStdOutputDiskImage(self):
        self.diskImageOutput.append(QString(self.proc.readAllStandardOutput()))

    @pyqtSlot()
    def readStdErrorDiskImage(self):
        self.diskImageOutput.append(QString(self.proc.readAllStandardError()))

    def browse_dirsource(self):
        self.dirSource.clear() # clear directory source text
        directory = QFileDialog.getExistingDirectory(self, "Select folder")

        if directory: # if user didn't pick directory don't continue
            self.dirSource.setText(directory)

    def browse_diskimage(self):
        self.diskImageSource.clear() # clear existing disk image source text
        diskimage = QFileDialog.getOpenFileName(self, "Select disk image")

        if file: # if user didn't pick file don't continue
            self.diskImageSource.setText(diskimage)

    def browse_dirdest(self):
        self.dirDestination.clear() # clear existing report destination text
        directory = Q
        FileDialog.getExistingDirectory(self, "Select folder")

        if directory: # if user didn't pick directory don't continue
            self.dirDestination.setText(directory)

    def browse_diskimagedest(self):
        self.diskImageDestination.clear() # clear existing report destination text
        directory = Q
        FileDialog.getExistingDirectory(self, "Select folder")

        if directory: # if user didn't pick directory don't continue
            self.diskImageDestination.setText(directory)

    def start_scan_dir(self):
        # clear output window
        self.dirOutput.clear()

        # create list for process
        self.process_list = list()
        
        # give indication process has started
        self.dirOutput.append('Process started.')

        # universal option handling
        if not self.virusScan.isChecked():
            self.process_list.append('-n')
        if self.largeFiles.isChecked():
            self.process_list.append('-l')
        if self.bulkExtractor.isChecked():
            self.process_list.append('-b')
        if self.scanArchives.isChecked():
            self.process_list.append('-z')
        if self.throttleSiegfried.isChecked():
            self.process_list.append('-t')
        if self.sfWarnings.isChecked():
            self.process_list.append('-w')
        if self.sha1.isChecked():
            self.process_list.append('--hash')
            self.process_list.append('sha1')
        if self.sha256.isChecked():
            self.process_list.append('--hash')
            self.process_list.append('sha256')
        if self.sha512.isChecked():
            self.process_list.append('--hash')
            self.process_list.append('sha512')

        self.process_list.append(self.dirSource.text())
        self.process_list.append(self.dirDestination.text())
        self.process_list.append(self.dirIdentifier.text())


        # run brunnhilde.py as QProcess and redirect stdout and stderr to GUI
        self.proc = QProcess()
        self.proc.start("brunnhilde.py", self.process_list)
        self.proc.setProcessChannelMode(QProcess.MergedChannels);
        QObject.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self, SLOT("readStdOutputDir()"));
        QObject.connect(self.proc, SIGNAL("readyReadStandardError()"), self, SLOT("readStdErrorDir()"));

    def start_scan_diskimage(self):
            
        # clear output window
        self.diskImageOutput.clear()

        # create list for process
        self.process_list = list()

        # add disk image flag  
        self.process_list.append('-d')
        
        # universal option handling
        if not self.virusScan.isChecked():
            self.process_list.append('-n')
        if self.largeFiles.isChecked():
            self.process_list.append('-l')
        if self.bulkExtractor.isChecked():
            self.process_list.append('-b')
        if self.scanArchives.isChecked():
            self.process_list.append('-z')
        if self.throttleSiegfried.isChecked():
            self.process_list.append('-t')
        if self.sfWarnings.isChecked():
            self.process_list.append('-w')
        if self.sha1.isChecked():
            self.process_list.append('--hash')
            self.process_list.append('sha1')
        if self.sha256.isChecked():
            self.process_list.append('--hash')
            self.process_list.append('sha256')
        if self.sha512.isChecked():
            self.process_list.append('--hash')
            self.process_list.append('sha512')

        # disk image option handling
        if self.removeFiles.isChecked():
            self.process_list.append('-r')
        if self.hfsDisk.isChecked():
            self.process_list.append('--hfs')
        if self.resForks.isChecked():
            self.process_list.append('--resforks')

         # run brunnhilde.py as QProcess and redirect stdout and stderr to GUI
        self.proc = QProcess()
        self.proc.start("brunnhilde.py", QStringList() << self.process_list << 
            self.diskImageSource.text() << self.diskImageDestination.text() << self.diskImageIdentifier.text())
        self.proc.setProcessChannelMode(QProcess.MergedChannels);
        QObject.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self, SLOT("readStdOutputDiskImage()"));
        QObject.connect(self.proc, SIGNAL("readyReadStandardError()"), self, SLOT("readStdErrorDiskImage()"));

def main():
    app = QApplication(sys.argv)
    form = BrunnhildeApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
