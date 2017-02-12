from PySide.QtGui import *


class TFormMain(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormMain, self).__init__()

		self.application = in_application

		self.setWindowTitle("Secure storage")
