from PySide.QtGui import *
from PySide.QtCore import *
import os
from module_vaults_list import TVaultsList


class TFormStart(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormStart, self).__init__()

		self.application = in_application

		self._init_db_()

		self._init_icons_()
		self._init_ui_()
		self._init_menu_()
		self._init_events_()

		self.load_vault_list()

	def _init_db_(self):
		self.vaults = TVaultsList("{0}/vaults.sqlie".format(self.application.PATH_COMMON))

	def _init_icons_(self):
		self.is_list_add    = QIcon("{0}/list-add.png".format(self.application.PATH_ICONS_SMALL))
		self.is_list_remove = QIcon("{0}/list-remove.png".format(self.application.PATH_ICONS_SMALL))
		self.is_list_rename = QIcon("{0}/list-edit.png".format(self.application.PATH_ICONS_SMALL))

	def _init_ui_(self):
		self.setWindowTitle("DVault - {0}".format(self.application.PATH_COMMON))

		self.setMinimumSize(640, 480)

		self.table_vaults = QTreeWidget()
		self.setCentralWidget(self.table_vaults)

		self.setContentsMargins(3, 3, 3, 3)

	def _init_events_(self):
		self.action_list_add.triggered.connect(self.event_list_add)
		self.action_list_remove.triggered.connect(self.event_list_remove)
		self.action_list_rename.triggered.connect(self.event_list_rename)

		self.table_vaults.currentItemChanged.connect(self.table_vault_onCurentItemChanged)

	def _init_menu_(self):
		self.menu_list = self.menuBar().addMenu("Список")

		self.action_list_add    = QAction(self.is_list_add,    "Добавить",      None)
		self.action_list_remove = QAction(self.is_list_remove, "Удалить",       None)
		self.action_list_rename = QAction(self.is_list_rename, "Переименовать", None)

		self.menu_list.addAction(self.action_list_add)
		self.menu_list.addAction(self.action_list_remove)
		self.menu_list.addSeparator()
		self.menu_list.addAction(self.action_list_rename)

	def load_vault_list(self):
		self.table_vaults.setHeaderLabels(["Название", "Путь"])

		self.table_vaults.resizeColumnToContents(0)
		self.table_vaults.resizeColumnToContents(1)

	def add_vault_to_list(self, in_name, in_filename):
		pass

	def event_list_add(self):
		_filename, _result = QFileDialog().getOpenFileName()

		if os.path.exists(_filename):
			_name, _result = QInputDialog().getText(self, "", "")

			if _result:
				self.add_vault_to_list(_name, _filename)

	def event_list_rename(self):
		pass

	def event_list_remove(self):
		pass

	def table_vault_onCurentItemChanged(self):
		_item_selected = self.table_vaults.currentItem() is not None

		self.action_list_rename.setEnabled(_item_selected)
		self.action_list_remove.setEnabled(_item_selected)