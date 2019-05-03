
from PyQt5.QtWidgets import QMainWindow,QFileDialog,QMessageBox,QTableWidget,QTableWidgetItem,QHeaderView 
from os.path import getmtime
from math import ceil
from hexTable import HexItem,Delegate
class HexEdit(QMainWindow):
	EMPTY_TITLE="File not choose."
	def __init__(self,path=None):
		QMainWindow.__init__(self)	
		self.pathToFile=path
		self.bytes_file_text=b""
		self.versionFile=""
		self.createMenuBar()
		self._setWindowTitle()
		
		table=QTableWidget(0,8,self)
		self.setCentralWidget(table)
		table.setItemDelegate(Delegate())
		for i in range(0,9):
			# self.centralWidget().horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents);
			self.centralWidget().horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch);
		
	def _setWindowTitle(self):
		if self.pathToFile==None:
			self.setWindowTitle(self.EMPTY_TITLE)
		else:
			self.setWindowTitle(self.pathToFile)
	
	
	def createMenuBar(self):
		menuBar=self.menuBar()
		file_menu=menuBar.addMenu("File")
		file_menu.addAction("Choose file").triggered.connect(self.action_choose_file)	
		menuBar.addAction("Read").triggered.connect(self.action_readFile)	
	
	
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
			
		table=self.centralWidget()
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
			# item.setText(stringBytes)
			table.setItem(row, column,item);
			
			column+=1
			if column>=8:
				row+=1
				column=0
			
		