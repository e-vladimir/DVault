from PySide.QtGui import *


class TFormItem(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormItem, self).__init__()

		self.application = in_application

		self.setWindowTitle("Secure storage")
