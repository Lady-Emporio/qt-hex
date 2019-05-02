from PyQt5.QtWidgets import (
QMainWindow,QMenuBar,QMenu,
QAction,QMdiArea)
from mdi import MdiArea
class MainWindow(QMainWindow):
	SUB_TO_TAB="Cуб на вкладки"
	TAB_TO_SUB="Вкладки на суб"
	def __init__(self):
		QMainWindow.__init__(self)
		centralWidget=MdiArea()
		self.setCentralWidget(centralWidget);
		
		self.changeViewMode=None
		self.createMenuBar()

		
		
		self.show()
		
		
	def createMenuBar(self):
		menuBar=QMenuBar(self)
		self.setMenuBar(menuBar)
		
		menuBar.addAction("Sub hex").triggered.connect(self.action_hexOpen)	
		self.createMenuViewsMode(menuBar)
		
	def createMenuViewsMode(self,menuBar):
		settings_view_menu=menuBar.addMenu("Настройки")
		self.changeViewMode=settings_view_menu.addAction("Установка текста в другой функции")
		self.changeViewMode.triggered.connect(self.action_changeViewMode)
		self.action_changeViewMode_setText()
		
		settings_view_menu.addAction("Sub Каскадом").triggered.connect(self.action_cascadeSubWindows)
		settings_view_menu.addAction("Sub Мозайкой").triggered.connect(self.action_tileSubWindows)
		settings_view_menu.addAction("Sub Закрыть все").triggered.connect(self.action_closeAllSubWindows)	
	def  action_changeViewMode(self):
		viewMode= QMdiArea.ViewMode.SubWindowView if self.centralWidget().viewMode()==QMdiArea.ViewMode.TabbedView else QMdiArea.ViewMode.TabbedView
		self.centralWidget().setViewMode(viewMode)
		
		self.action_changeViewMode_setText()
	def action_changeViewMode_setText(self):
		text_change_action=self.TAB_TO_SUB if self.centralWidget().viewMode()==QMdiArea.ViewMode.TabbedView else self.SUB_TO_TAB
		self.changeViewMode.setText(text_change_action)
	def action_tileSubWindows(self):
		self.centralWidget().tileSubWindows()
	def action_cascadeSubWindows(self):
		self.centralWidget().cascadeSubWindows()
	def action_closeAllSubWindows(self):
		self.centralWidget().closeAllSubWindows()
	def action_hexOpen(self):
		self.centralWidget().createNewSubHex()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	