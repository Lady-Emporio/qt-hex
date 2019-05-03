

from PyQt5.QtWidgets import QTableWidgetItem ,QAbstractItemDelegate ,QItemDelegate,QWidget,QHBoxLayout,QLineEdit 
class HexItem(QTableWidgetItem):
	def __init__(self,bytes,hex,dec):
		QTableWidgetItem.__init__(self)	
		self.bytes=bytes
		self.hex=hex
		
		self.setText(bytes)
		
# class Delegate(QAbstractItemDelegate):
class Delegate(QItemDelegate):
	def __init__(self):
		QAbstractItemDelegate.__init__(self)
		
	# def  paint(self, qPainter, qStyleOptionViewItem,qModelIndex):
		# pass
	def createEditor(self,QWidget_parent, QStyleOptionViewItem_option, qModelIndex ):
		print([QWidget_parent,QStyleOptionViewItem_option,qModelIndex])
		return EditBytesVersion_2(QWidget_parent)
		
		
class EditBytes(QWidget):
	def __init__(self,parent):
		QWidget.__init__(self)
		self.setParent(parent)
		horizontal=QHBoxLayout()
		self.setLayout(horizontal)
		horizontal.addWidget(QLineEdit())
		
class EditBytesVersion_2(QLineEdit):
	def __init__(self,parent):
		QLineEdit.__init__(self,parent)
