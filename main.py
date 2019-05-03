#SET PATH=%PATH%;C:\Users\Иванова\Desktop\НУЖНОЕ\1\We\source\p\fd\fd\myq
#python main.py
from PyQt5.QtWidgets import QApplication
from mainWindows import MainWindow
app = QApplication([])
livePleaseDontDelete=MainWindow()
livePleaseDontDelete.action_hexOpen()
app.exec_()