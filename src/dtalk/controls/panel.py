#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2014 Deepin, Inc.
#               2011 ~ 2014 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# DON'T DELETE BELOW CODE!
# Calls XInitThreads() as part of the QApplication construction in order to make Xlib calls thread-safe. 
# This attribute must be set before QApplication is constructed.
# Otherwise, you will got error:
#     "python: ../../src/xcb_conn.c:180: write_vec: Assertion `!c->out.queue_len' failed."
# 
# Qt5 application hitting the race condition when resize and move controlling for a frameless window.
# Race condition happened while Qt was using xcb to read event and request window position movements from two threads. 
# Same time rendering thread was drawing scene with opengl. 
# Opengl driver (mesa) is using Xlib for buffer management. Result is assert failure in libxcb in different threads. 
# 

from __future__ import unicode_literals

import os
from PyQt5 import QtCore
if os.name == 'posix':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True) 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt5 import QtWidgets, QtGui
from dtalk.utils.xdg import get_qml
from dtalk.controls.managers import commonManager, controlManager, sessionManager
from dtalk.views.base import BaseView
from dtalk.controls.trayicon import TrayIcon
from dtalk.keybinder import keyBinder
from dtalk.controls import signals as cSignals
# from dtalk.views.chatWindow import ChatWindow


class Panel(BaseView):
    
    hideOtherWindow = QtCore.pyqtSignal()
    mousePressed = QtCore.pyqtSignal(QtCore.QPointF)
    focusLosed =QtCore.pyqtSignal()
    
    def __init__(self):
        super(Panel, self).__init__()
        self.setMinimumSize(QtCore.QSize(336, 550))        
        self.resize(336, 700)
        QtWidgets.qApp.focusWindowChanged.connect(self.onFocusWindowChanged)
        self.setIcon(QtGui.QIcon(":/images/common/logo.png"))
        self.setTitle("Deepin Talk")
        QtWidgets.qApp.setApplicationName("Deepin Talk")
        
        cSignals.raise_window.connect(self.requestRaiseWindow)
        
        self.initTray()        
        self.setContextProperty("commonManager", commonManager)
        self.setContextProperty("controlManager", controlManager)
        self.setContextProperty("serverManager", sessionManager)
        self.setContextProperty("trayIcon", self.trayIcon)
        self.setSource(QtCore.QUrl.fromLocalFile(get_qml('Main.qml')))
        # self.chat = ChatWindow(None, None)
        # self.chat.show()

        self.initKeybinder()
        
    def onFocusWindowChanged(self, focusWindow):    
        if focusWindow.__class__.__name__ != "QQuickWindow":
            self.hideOtherWindow.emit()
        if focusWindow is None:    
            self.focusLosed.emit()
            
    def initTray(self):        
        self.trayIcon = TrayIcon(self)
        self.trayIcon.show()

    def initKeybinder(self):    
        keyBinder.bind("Ctrl+Alt+P", self.requestRaiseWindow)
        keyBinder.start()
        
    @QtCore.pyqtSlot()    
    def closeWindow(self):

        keyBinder.stop()
        sessionManager.disconnect()        

        self.hide()
        self.close()
        
        for w in QtWidgets.qApp.allWindows():
            w.hide()
            w.close()
        self.trayIcon.hide()
        
        QtWidgets.qApp.quit()                

        
    def mousePressEvent(self, event):    
        self.mousePressed.emit(QtCore.QPointF(event.x(), event.y()))
        return super(Panel, self).mousePressEvent(event)
        
    def requestRaiseWindow(self, *args, **kwargs):
        if self.windowState() == QtCore.Qt.WindowMinimized:
            self.show()
            self.requestActivate()
        else:    
            self.doMinimized()
    
