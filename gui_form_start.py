from PySide.QtGui import *


class TFormStart(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormStart, self).__init__()

		self.application = in_application

		self.setWindowTitle("Secure storage")
