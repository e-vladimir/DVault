from PySide.QtGui import *


class TFormStart(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormStart, self).__init__()

		self.application = in_application

		self._init_ui_()
		self._init_events_()

	def _init_ui_(self):
		self.setWindowTitle("DVault - {0}".format(self.application.PATH_COMMON))

		self.setMinimumSize(640, 480)

		self.table_vaults = QTreeWidget()
		self.setCentralWidget(self.table_vaults)

	def _init_events_(self):
		pass

	def load_vault_list(self):
		pass