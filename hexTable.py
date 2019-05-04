

from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget ,QAbstractItemDelegate ,QItemDelegate,QWidget,QHBoxLayout,QLineEdit 
from PyQt5.QtGui import QIntValidator,QRegExpValidator,QPalette,QColor,QBrush
from PyQt5.QtCore   import QRegExp,Qt

class HexTable(QTableWidget):
	def __init__(self,row,col,parent):
		QTableWidget.__init__(self,row,col,parent)
		self.colorChange=[]
		self.itemClicked.connect(self.action_cellActivated)
		self.itemDoubleClicked.connect(self.action_itemClicked)
		
	def action_cellActivated(self,item):
		for itemOldBackground in self.colorChange:
			itemOldBackground.setBackground(QBrush(QColor(255,255,255)))
		self.colorChange=self.findItems(item.text(), Qt.MatchContains)
		
		brush=QBrush(QColor(255,0,0))
		for itemForCOlor in self.colorChange:
			itemForCOlor.setBackground(brush)
	def action_itemClicked(self,item):
		_HexCentalWidget=self.parent()
		_HexCentalWidget.setBiteEdit(item)
	def clearContents(self):
		super().clearContents()
		self.colorChange=[]
class HexItem(QTableWidgetItem):
	def __init__(self,bytes,hex,dec):
		QTableWidgetItem.__init__(self)	
		self.bytes=bytes
		self.hex=hex
		self.update()
	def update(self):
		self.setText(self.bytes)

class Delegate(QItemDelegate):
	def __init__(self):
		QAbstractItemDelegate.__init__(self)
	def createEditor(self,QWidget_parent, QStyleOptionViewItem_option, qModelIndex ):
		return None