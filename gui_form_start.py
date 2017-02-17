from PySide.QtGui import *
from PySide.QtCore import *
import os
from module_sqlite import TSQLiteConnection


class TFormStart(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormStart, self).__init__()

		self.application = in_application

		self._init_db_()

		self._init_icons_()
		self._init_ui_()
		self._init_menu_()
		self._init_events_()

		self.load_vaults_list()

		# TODO: Подумать как вызывать обработчик изменения таблицы, что бы установить доступность элементов меню
		self.table_vault_onCurentItemChanged()

	def _init_db_(self):
		self.sqlite = TSQLiteConnection("{0}/vaults.sqlite".format(self.application.PATH_COMMON))
		self.sqlite.exec_create("CREATE TABLE IF NOT EXISTS vaults (name TEXT, filename TEXT)")

	def _init_icons_(self):
		self.is_list_add = QIcon("{0}/list-add.png".format(self.application.PATH_ICONS_SMALL))
		self.is_list_remove = QIcon("{0}/list-remove.png".format(self.application.PATH_ICONS_SMALL))
		self.is_list_rename = QIcon("{0}/list-edit.png".format(self.application.PATH_ICONS_SMALL))

	def _init_ui_(self):
		self.setWindowTitle("DVault - {0}".format(self.application.PATH_COMMON))

		self.setMinimumSize(640, 480)

		self.table_vaults = QTreeWidget()
		self.table_vaults.setIndentation(0)
		self.setCentralWidget(self.table_vaults)

		self.setContentsMargins(3, 3, 3, 3)

	def _init_events_(self):
		self.action_list_add.triggered.connect(self.event_list_add)
		self.action_list_remove.triggered.connect(self.event_list_remove)
		self.action_list_rename.triggered.connect(self.event_list_rename)

		self.table_vaults.currentItemChanged.connect(self.table_vault_onCurentItemChanged)

	def _init_menu_(self):
		self.menu_list = self.menuBar().addMenu("Список")

		self.action_list_add = QAction(self.is_list_add, "Добавить", None)
		self.action_list_remove = QAction(self.is_list_remove, "Удалить", None)
		self.action_list_rename = QAction(self.is_list_rename, "Переименовать", None)

		self.menu_list.addAction(self.action_list_add)
		self.menu_list.addAction(self.action_list_remove)
		self.menu_list.addSeparator()
		self.menu_list.addAction(self.action_list_rename)

	def load_vaults_list(self):
		self.table_vaults.clear()

		self.table_vaults.setHeaderLabels(["Название", "Путь"])

		_sql = "SELECT name, filename FROM vaults ORDER BY name"

		vaults_names = self.sqlite.get_column(_sql, 0)
		vaults_filenames = self.sqlite.get_column(_sql, 1)

		for _index in range(len(vaults_names)):
			_name     = vaults_names[_index]
			_filename = vaults_filenames[_index]

			_item = QTreeWidgetItem()
			_item.setText(0, _name)
			_item.setText(1, _filename)

			if not os.path.exists(_filename):
				_item.setForeground(0, Qt.gray)
				_item.setForeground(1, Qt.gray)

			self.table_vaults.addTopLevelItem(_item)

		self.table_vaults.resizeColumnToContents(0)
		self.table_vaults.resizeColumnToContents(1)

		self.table_vaults.setColumnWidth(0, self.table_vaults.columnWidth(0) + 10)

	def add_vault_to_list(self, in_name, in_filename):
		_exist = False

		for _index in range(self.table_vaults.topLevelItemCount()):
			_name     = self.table_vaults.topLevelItem(_index).text(0)
			_filename = self.table_vaults.topLevelItem(_index).text(1)

			_exist = _name == in_name or _filename == in_filename

			if _exist:
				break

		if not _exist:
			_sql = "INSERT INTO vaults (name, filename) VALUES ('{0}', '{1}')".format(in_name, in_filename)
			self.sqlite.exec_insert(_sql)

			self.load_vaults_list()
		else:
			QMessageBox().information(self, "Отмена добавления", "Указанное имя\файл уже есть в списке")

	def event_list_add(self):
		_filename, _result = QFileDialog().getOpenFileName(self, filter="*.vault")

		if os.path.exists(_filename):
			_name, _result = QInputDialog().getText(self, "", "")

			if _result:
				self.add_vault_to_list(_name, _filename)

	def event_list_rename(self):
		_old_name         = self.table_vaults.currentItem().text(0)
		_new_name, _result = QInputDialog().getText(self, "Новое название", "Старое название: {0}".format(_old_name), text=_old_name)
		_exist            = False

		if _result:
			for _index in range(self.table_vaults.topLevelItemCount()):
				_name = self.table_vaults.topLevelItem(_index).text(0)

				_exist = _name == _new_name

				if _exist:
					break

			if not _exist:
				_sql = "UPDATE vaults SET name = '{0}' WHERE name='{1}'".format(_new_name, _old_name)

				self.sqlite.exec_update(_sql)
				self.load_vaults_list()
			else:
				QMessageBox().information(self, "Отмена добавления", "Указанное имя уже есть в списке")

	def event_list_remove(self):
		_name   = self.table_vaults.currentItem().text(0)
		_remove = QMessageBox().question(self, "Удаление", "Подтвердите удаление записи: {0}".format(_name), QMessageBox.No|QMessageBox.Yes) == QMessageBox.Yes

		if _remove:
			_sql = "DELETE FROM vaults WHERE name = '{0}'".format(_name)
			self.sqlite.exec_delete(_sql)

			self.load_vaults_list()

	def table_vault_onCurentItemChanged(self):
		_item_selected = self.table_vaults.currentItem() is not None

		self.action_list_rename.setEnabled(_item_selected)
		self.action_list_remove.setEnabled(_item_selected)

		self.table_vaults.setItemSelected(self.table_vaults.currentItem(), True)
