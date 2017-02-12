import os
import sys
from PySide.QtGui import *


class TApp(QApplication):
	PATH_COMMON = ""
	PATH_ICONS = ""

	def __init__(self):
		super(TApp, self).__init__(sys.argv)

		self._init_path_()
		self._init_forms_()

	def _init_path_(self):
		self.PATH_COMMON        = "{0}/".format(os.path.abspath(os.curdir))

	def _init_forms_(self):
		pass

app = TApp()
sys.exit(app.exec_())