import os
import sys
from PySide.QtGui import *
from gui_form_start  import TFormStart
from gui_form_main   import TFormMain
from gui_form_record import TFormRecord


class TApp(QApplication):
	PATH_COMMON = ""
	PATH_ICONS = ""

	VERSION = "0.17.05.17"

	def __init__(self):
		super(TApp, self).__init__(sys.argv)

		self._init_path_()
		self._init_forms_()

	def _init_path_(self):
		self.PATH_COMMON      = "{0}".format(os.path.abspath(os.curdir))
		self.PATH_ICONS       = "{0}/icons".format(self.PATH_COMMON)
		self.PATH_ICONS_SMALL = "{0}/small".format(self.PATH_ICONS)

	def _init_forms_(self):
		self.form_start  = TFormStart(self)
		self.form_main   = TFormMain(self)
		self.form_record = TFormRecord(self)

app = TApp()
app.form_start.show()
sys.exit(app.exec_())
