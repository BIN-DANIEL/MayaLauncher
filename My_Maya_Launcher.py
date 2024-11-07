import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication,QLabel,QPushButton,QDialog,QHBoxLayout,QWidget,QMainWindow,QVBoxLayout,QStyle, QComboBox
from typing import Callable
from PySide6 import QtCore
from PySide6.QtGui import *
from PySide6.QtWidgets import QFileIconProvider, QToolButton,QSizePolicy
# Daniel Maya Launcher
class MayaLauncher(QWidget):
    maya_path = {'Maya_2023': "E:/Maya2023/bin/maya.exe",
                        'Maya_2018': "E:/Maya2018/bin/maya.exe"}
    SHELF_PATH = "C:/Users/ASUS/Desktop/CSLearning/StanDouDevShelf"
    PLUGIN_PATH = "C:/Users/ASUS/Desktop/CSLearning/PluginDevPath"

    BUTTON_SIZE = QtCore.QSize(48, 48)
    env_args = ['Dev','Default']
    def __init__(self):
        super().__init__()
        self.setWindowTitle("启动器")
        self.setMinimumSize(400, 150)
        self.createWidgets()
        self.createLayout()
        self.bindSlot()
    
    def createWidgets(self):
        self.env_select = QComboBox()
        self.env_select.addItems(MayaLauncher.env_args)
        self.maya_2023_btn = ButtonWidget('Maya_2023', MayaLauncher.maya_path['Maya_2023'])
        self.maya_2018_btn = ButtonWidget('Maya_2018', MayaLauncher.maya_path['Maya_2018'])
        
    

    def createLayout(self):
        
        main_layout = QVBoxLayout(self)
        # create layout for Environment Selection
        env_layout = QHBoxLayout()
        env_layout.addStretch()
        env_layout.addWidget(self.env_select)
        # create layout for Maya Button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.maya_2023_btn)
        button_layout.addWidget(self.maya_2018_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(env_layout)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
    def bindSlot(self):
        self.maya_2018_btn.clicked.connect(self.openFile)
        self.maya_2023_btn.clicked.connect(self.openFile)

    def openFile(self, app_path):
        maya_env = os.environ.copy()
        if self.env_select.currentText() == 'Dev':
            maya_env['MAYA_SHELF_PATH'] = self.SHELF_PATH
            maya_env['MAYA_PLUG_IN_PATH'] = self.PLUGIN_PATH
        subprocess.Popen([app_path], env=maya_env)
        return
    def call(func):
        def x(self):
            print("正在调用 {0}.{1}".format(type(self).__name__,func.__name__))
            result = func(self)
            print("结束调用 {0}.{1}".format(type(self).__name__,func.__name__))
            return result
        return x

class ButtonWidget(QWidget):
    clicked = QtCore.Signal(str)
    def __init__(self, name, app_path):
        super().__init__()
        self.app_path = app_path
        self.button = self.createButton()
        # builtin clicked 绑定 onclick, 二次触发自定义传参方法
        self.button.clicked.connect(self.onclick)

        #Button Layout init
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.button)
        buttonlayout.addStretch()
    
        
        #Main Layout init

        name = QLabel(name)
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(buttonlayout)
        mainLayout.addWidget(name)
        mainLayout.addStretch()

        # set size policy to be fixed
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(policy)
       
    def createButton(self):
        file_info = QtCore.QFileInfo(self.app_path)
        icon_provider = QFileIconProvider()
        button = QToolButton()
        button.setIconSize(MayaLauncher.BUTTON_SIZE)     
        icon = icon_provider.icon(file_info)
        button.setIcon(icon)
        print(button.sizePolicy().horizontalPolicy().name)
        print(button.sizePolicy().verticalPolicy().name)
        return button
    
    def onclick(self):
        
        self.clicked.emit(self.app_path)

    def colorBackGround(self):
        pal = QPalette()
        pal.setColor(QPalette.ColorRole.Window, QColor(255, 0,0,127))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

if __name__ == '__main__':
    app = QApplication()
    window = MayaLauncher()
    window.show()
    app.exec()


