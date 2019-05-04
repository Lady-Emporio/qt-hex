
from PyQt5.QtWidgets import (QMainWindow,QFileDialog,QMessageBox,QTableWidget,
QTableWidgetItem,QHeaderView ,QStackedLayout ,QWidget,QLabel,
QHBoxLayout,QPushButton,QGraphicsDropShadowEffect,QVBoxLayout,QSizePolicy)
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore   import Qt
from os.path import getmtime
from math import ceil
from hexTable import HexItem,HexTable,Delegate

class BiteEdit(QWidget):
	def __init__(self,parent,item=None ):
		QWidget.__init__(self,parent)	
		self.setFixedSize(200,100)
		self.buttonList=[]
		Pal=self.palette()
		# Pal.setColor(QPalette.Background, Qt.red);
		self.setAutoFillBackground(True)
		self.setPalette(Pal);
		
		self.item=item
		
		
		mainLayout=QVBoxLayout(self)
		self.setLayout(mainLayout)
		
		buttonLayout=QHBoxLayout()
		closeLayout=QHBoxLayout()
		title=QLabel("Item: "+str(self.item.row()+1)+" " +str(self.item.column()+1))
		mainLayout.addWidget(title)
		mainLayout.addLayout(buttonLayout)
		mainLayout.addLayout(closeLayout)
		
		saveButton=QPushButton("save")
		saveButton.setMaximumWidth(50)
		closeButton=QPushButton("X")
		closeButton.setMaximumWidth(50)
		closeLayout.addWidget(saveButton)
		closeLayout.addWidget(closeButton)
		
		closeLayout.setAlignment(closeButton,Qt.AlignRight)
		
		for i in range(0,8):
			text=item.bytes[i]
			button=QPushButton(text)
			buttonLayout.addWidget(button)		
			self.buttonList.append(button)
			button.clicked.connect(self.action_button_bite_change)
			button.setWhatsThis(button.text())
		effect=QGraphicsDropShadowEffect ()
		effect.setColor(QColor(255, 0, 0));
		
		effect.setXOffset(0);
		effect.setYOffset(0);
		effect.setBlurRadius(20);
		effect.setColor(QColor(0, 0, 0));
		
		self.setGraphicsEffect(effect)
		
		closeButton.clicked.connect(self.action_close)
		saveButton.clicked.connect(self.action_save)
		
		self.setAttribute(Qt.WA_DeleteOnClose);
		
	
	def action_close(self):
		self.close()
		self.parent().parent().activateTable()
	def action_save(self):
		text=""
		for i in range(0,8):
			text+=self.buttonList[i].text()
		self.item.bytes=text
		self.item.update()
		
		self.close()
		self.parent().parent().setBiteEdit(self.item)
		
	def action_button_bite_change(self):
		button=self.sender()
		textNow=button.text()
		textNext="0" if textNow=="1" else "1"
		button.setText(textNext)
		
		effect=QGraphicsDropShadowEffect ()
		effect.setColor(QColor(0, 0, 0,0))
		if button.text()!=button.whatsThis():
			effect.setColor(QColor(255, 0, 0));
			effect.setXOffset(0);
			effect.setYOffset(0);
			effect.setBlurRadius(10);
			effect.setColor(QColor(255, 0, 0));
		button.setGraphicsEffect(effect)
		
class HexCentalWidget(QWidget):
	def __init__(self,parent):
		QWidget.__init__(self,parent)	
		self.mainLayout=QStackedLayout()
		self.mainLayout.setStackingMode(QStackedLayout.StackingMode.StackAll)
		self.setLayout(self.mainLayout)
		
		self.table=HexTable(0,8,self);
		
		self.mainLayout.addWidget(self.table)
		# self.setBiteEdit()
	def setBiteEdit(self,item):
		wid=QWidget()
		subLayput=QHBoxLayout(wid)
		wid.setLayout(subLayput)
		self.biteEdit=BiteEdit(wid,item)
		subLayput.addWidget(self.biteEdit)
		
		self.mainLayout.insertWidget(0 , wid)
		self.mainLayout.setCurrentWidget(wid)
	def activateTable(self):
		self.mainLayout.setCurrentWidget(self.table)
		
class HexEdit(QMainWindow):
	EMPTY_TITLE="File not choose."
	def __init__(self,path=None):
		QMainWindow.__init__(self)	
		self.pathToFile=path
		self.bytes_file_text=b""
		self.versionFile=""
		self.createMenuBar()
		self._setWindowTitle()
		
		
		cenralWidget=HexCentalWidget(self)
		self.setCentralWidget(cenralWidget)
		self.getTable().setItemDelegate(Delegate())
		for i in range(0,9):
			# self.getTable().horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents);
			self.getTable().horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch);
		
	def getTable(self):
		return self.centralWidget().table
	def _setWindowTitle(self):
		if self.pathToFile==None:
			self.setWindowTitle(self.EMPTY_TITLE)
		else:
			self.setWindowTitle(self.pathToFile)
	
	
	def createMenuBar(self):
		menuBar=self.menuBar()
		file_menu=menuBar.addMenu("File")
		file_menu.addAction("Choose file").triggered.connect(self.action_choose_file)	
		file_menu.addAction("Save").triggered.connect(self.action_save_file)	
		menuBar.addAction("Read").triggered.connect(self.action_readFile)	
	def action_save_file(self):
		if self.pathToFile==None:
			QMessageBox.critical(self,"File not choose","The file not choose.")
			return;
		try:
			with open(self.pathToFile,"wb") as file:
				table=self.getTable()
				array=[]
				for row in range(0,table.rowCount()):
					for col in range(0,table.columnCount()):
						item=table.item(row,col)
						if item==None:
							continue
						v=item.text()
						decValueBytes=int(v[0])*128+int(v[1])*64+int(v[2])*32+int(v[3])*16+int(v[4])*8+int(v[5])*4+int(v[6])*2+int(v[7])
						array.append(decValueBytes)
						# print([item,row,col,v,decValueBytes])
						# file.write(bin(decValueBytes))
						
				file.write(bytes(array))
				# bytes=bytearray(text)
				# print([type(text),dir(text),text])
		except Exception as e:
			QMessageBox.critical(self,"Exception.",str(e))
			
	def action_choose_file(self):
		filePathWithTypes = QFileDialog.getOpenFileName(self,"Choose file", "./");
		filePath=filePathWithTypes[0]
		if filePath!="":
			self.pathToFile=filePath
			
		else:
			self.pathToFile=None
		self._setWindowTitle()
		
	def action_readFile(self):
		if self.pathToFile==None:
			QMessageBox.critical(self,"File not choose","The file not choose.")
			return;
		try:
			with open(self.pathToFile,"rb") as file:
				self.bytes_file_text=file.read()
				self.versionFile=getmtime(self.pathToFile)
				self.setTextInTable()
		except Exception as e:
			QMessageBox.critical(self,"Exception.",str(e))
			
	def setTextInTable(self):
		if self.pathToFile==None:
			QMessageBox.critical(self,"File not choose","The file not choose.")
			return;
			
		table=self.getTable()
		# table=self.centralWidget()
		table.clearContents()
		
		if self.bytes_file_text==b"":
			QMessageBox.warning(self,"Empty file.","В файле ничего нет. Он пустой")
			return
			
		table.setRowCount( ceil(len(self.bytes_file_text)/8) )
		row=0
		column=0
		for dex_value in self.bytes_file_text:
			stringBytes=bin(dex_value)[2:].zfill(8)
			stringHex=hex(dex_value)[2:].zfill(2)
			item = HexItem(stringBytes,stringHex,dex_value);
			table.setItem(row, column,item);
			
			column+=1
			if column>=8:
				row+=1
				column=0
			
		