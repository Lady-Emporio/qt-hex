


from PyQt5.QtWidgets import QMdiArea,QMdiSubWindow
from PyQt5.QtCore   import Qt
from hexEdit import HexEdit
class MdiArea(QMdiArea):
	def __init__(self):
		QMdiArea.__init__(self)
		
	def createNewSubHex(self):
		newHex = QMdiSubWindow();
		newHex.setWidget(HexEdit());
		newHex.setAttribute(Qt.WA_DeleteOnClose);
		self.addSubWindow(newHex);
		newHex.show()