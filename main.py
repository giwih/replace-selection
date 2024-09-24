import sys
import webbrowser
import re
import winreg as wrg

import ctypes
from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class MainWindow(QMainWindow):
	def __init__(self):
		#init
		super(MainWindow, self).__init__()
		uic.loadUi('design.ui', self)
		self.setFixedSize(513, 234)#600, 280
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		QCoreApplication.setLibraryPaths(["qt.conf"])

		#init winreg
		self.location = wrg.HKEY_CURRENT_USER 
		self.key = wrg.OpenKey(self.location, r'Control Panel\\Colors', access=wrg.KEY_SET_VALUE)#wrg.KEY_ALL_ACCESS

		#github button
		self.github.clicked.connect(lambda: webbrowser.open('https://github.com/giwih', new=2))

		#exit button
		self.exit.clicked.connect(lambda: sys.exit())

		#refresh button
		self.refresh.clicked.connect(self.refresh_frame_func)

		#apply buttons
		self.dfl_btn.clicked.connect(self.setToDefault)
		self.apply_btn.clicked.connect(self.setToCustom)

		#move
		self.move_frame.mousePressEvent = self.mousePressEvent1
		self.move_frame.mouseMoveEvent = self.mouseMoveEvent1

		self.color_picker_button_1.clicked.connect(self.colorPick)
		self.color_picker_button_2.clicked.connect(self.colorPick2)


    #moving if the cursor is taken over move_frame
	def mousePressEvent1(self, event):
		self.start = self.mapToGlobal(event.pos())
		self.pressing = True

	def mouseMoveEvent1(self, event):
		if self.pressing:
			self.end = self.mapToGlobal(event.pos())
			self.movement = self.end-self.start
			self.move(self.mapToGlobal(self.movement))
			self.start = self.end


	def setToDefault(self):
		#sets default values
		default = "0 102 204"
		default_border = "0 120 215"
		self.key = wrg.OpenKey(self.location, r'Control Panel\\Colors', access=wrg.KEY_SET_VALUE)
		wrg.SetValueEx(self.key, "Hilight", 0, wrg.REG_SZ, default_border)
		wrg.SetValueEx(self.key, "HotTrackingColor", 0, wrg.REG_SZ, default)
		if self.key: 
			wrg.CloseKey(self.key)
		self.question_msg()


	def setToCustom(self):
		#sets custom values
		basic_color = self.bsic_c.text()
		border_color = self.border_c.text()

		rgb_pattern = re.compile(r'^\d+,\s\d+,\s\d+$') #check for RGB format

		if not rgb_pattern.match(basic_color) or not rgb_pattern.match(border_color):
			message_box = QMessageBox()
			message_box.setIcon(QMessageBox.Icon.Warning)
			message_box.setText("One or both edit lines do not contain RGB format. (maybe you forgot the commas?)")
			message_box.setWindowTitle("Error")
			message_box.exec()
		else:
			self.key = wrg.OpenKey(self.location, r'Control Panel\\Colors', access=wrg.KEY_SET_VALUE)
			wrg.SetValueEx(self.key, "Hilight", 0, wrg.REG_SZ, border_color.replace(",", ""))
			wrg.SetValueEx(self.key, "HotTrackingColor", 0, wrg.REG_SZ, basic_color.replace(",", ""))
			if self.key: 
				wrg.CloseKey(self.key)
			self.question_msg() #call a message box about applying the settings

	def colorPick(self):
		color = QColorDialog.getColor()
		if color.isValid():
			rgb_string = f"{color.red()}, {color.green()}, {color.blue()}"
			self.bsic_c.setText(rgb_string)

	def colorPick2(self):
		color = QColorDialog.getColor()
		if color.isValid():
			rgb_string = f"{color.red()}, {color.green()}, {color.blue()}"
			self.border_c.setText(rgb_string)

	def question_msg(self):
		#messagebox
		msg = QMessageBox(text="Parameters successfully changed! To apply the changes you need to re-login to the Windows session. Leave the session? (All programs will close)")
		msg.setIcon(QMessageBox.Icon.Question)
		msg.setStandardButtons(QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
		msg.buttonClicked.connect(self.output)
		msg.exec()


	def output(self, button):
		#Logging out of Windows session
		if button.text() == 'OK':
			ctypes.windll.user32.ExitWindowsEx(0, 1)
		elif button.text() == 'Cancel':
			pass
		

	def refresh_frame_func(self):
		basic_color = self.bsic_c.text()
		border_color = self.border_c.text()
		rgb_pattern = re.compile(r'^\d+,\s\d+,\s\d+$')
		if not rgb_pattern.match(basic_color) or not rgb_pattern.match(border_color):
			message_box = QMessageBox()
			message_box.setIcon(QMessageBox.Icon.Warning)
			message_box.setText("One or both edit lines do not contain RGB format. (maybe you forgot the commas?)")
			message_box.setWindowTitle("Error")
			message_box.exec()
		else:
			self.refresh_frame.setStyleSheet(f"background-color: rgba({basic_color}, 0.2); border: 1px solid rgb({border_color});")

def application():
	app = QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('icon.ico'))
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	application()