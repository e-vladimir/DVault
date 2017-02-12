from PySide.QtGui import *


class TFormBackup(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormBackup, self).__init__()

		self.application = in_application

		self.setWindowTitle("Secure storage")
