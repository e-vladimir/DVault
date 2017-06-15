from PySide.QtGui import *
from PySide.QtCore import *
from module_vault import TVault
from module_vault import SYSTEM_FIELDS
from glob import glob
from os.path import basename


class TFormMain(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormMain, self).__init__()

		self.application = in_application
		self.vault       = None

		self.select_struct = None
		self.select_record = None
		self.select_field  = None

		self._init_icons_()
		self._init_ui()
		self._init_events_()

		self.gui_enabled_disabled()

	def _icons_to_cb_(self, in_path, in_combobox):
		in_combobox.clear()

		icons_path = glob(in_path)

		for icon_path in icons_path:
			_icon = QIcon(icon_path)
			_index = in_combobox.count()

			in_combobox.addItem("")
			in_combobox.setItemIcon(_index, _icon)
			in_combobox.setItemData(_index, basename(icon_path))

	def _init_ui(self):
		self.setMinimumSize(640, 480)

		# Структура
		self.tree_main = QTreeWidget()
		self.tree_main.setHeaderHidden(True)

		self.panel_main  = QWidget()

		self.btn_main_add = QPushButton()
		self.btn_main_add.setIcon(self.icon_list_add)
		self.btn_main_add.setFlat(True)

		self.btn_main_addsub = QPushButton()
		self.btn_main_addsub.setIcon(self.icon_list_addsub)
		self.btn_main_addsub.setFlat(True)

		self.btn_main_edit = QPushButton()
		self.btn_main_edit.setIcon(self.icon_list_edit)
		self.btn_main_edit.setFlat(True)

		self.btn_main_remove = QPushButton()
		self.btn_main_remove.setIcon(self.icon_list_remove)
		self.btn_main_remove.setFlat(True)

		self.cb_main_icons = QComboBox()
		self.cb_main_icons.setMaximumWidth(50)
		self._icons_to_cb_(self.application.PATH_ICONS + "/*.png", self.cb_main_icons)

		self.toolbar_main = QHBoxLayout()
		self.toolbar_main.setSpacing(0)
		self.toolbar_main.addWidget(self.btn_main_add)
		self.toolbar_main.addWidget(self.btn_main_addsub)
		self.toolbar_main.addWidget(self.btn_main_edit)
		self.toolbar_main.addWidget(self.btn_main_remove)
		self.toolbar_main.addStretch()
		self.toolbar_main.addWidget(self.cb_main_icons)

		self.layout_main = QVBoxLayout(self.panel_main)
		self.layout_main.setContentsMargins(3, 3, 3, 3)
		self.layout_main.setSpacing(3)
		self.layout_main.addLayout(self.toolbar_main)
		self.layout_main.addWidget(self.tree_main)

		# Записи
		self.tree_records = QTreeWidget()
		self.tree_records.setIndentation(0)
		self.tree_records.setHeaderHidden(True)

		self.btn_record_add = QPushButton()
		self.btn_record_add.setIcon(self.icon_list_add)
		self.btn_record_add.setFlat(True)

		self.btn_record_edit = QPushButton()
		self.btn_record_edit.setIcon(self.icon_list_edit)
		self.btn_record_edit.setFlat(True)

		self.btn_record_remove = QPushButton()
		self.btn_record_remove.setIcon(self.icon_list_remove)
		self.btn_record_remove.setFlat(True)

		self.cb_record_icons = QComboBox()
		self.cb_record_icons.setMaximumWidth(50)
		self._icons_to_cb_(self.application.PATH_ICONS + "/*.png", self.cb_record_icons)

		self.toolbar_record = QHBoxLayout()
		self.toolbar_record.setSpacing(0)
		self.toolbar_record.addWidget(self.btn_record_add)
		self.toolbar_record.addWidget(self.btn_record_edit)
		self.toolbar_record.addWidget(self.btn_record_remove)
		self.toolbar_record.addStretch()
		self.toolbar_record.addWidget(self.cb_record_icons)

		self.panel_records = QWidget()

		self.layout_record = QVBoxLayout(self.panel_records)
		self.layout_record.setContentsMargins(3, 3, 3, 3)
		self.layout_record.setSpacing(3)
		self.layout_record.addLayout(self.toolbar_record)
		self.layout_record.addWidget(self.tree_records)

		# Поля
		self.tree_fields = QTreeWidget()
		self.tree_fields.setIndentation(0)
		self.tree_fields.setHeaderHidden(True)

		self.panel_fields = QWidget()

		self.btn_fields_copy = QPushButton()
		self.btn_fields_copy.setIcon(self.icon_copy)
		self.btn_fields_copy.setFlat(True)

		self.btn_fields_web = QPushButton()
		self.btn_fields_web.setIcon(self.icon_web)
		self.btn_fields_web.setFlat(True)

		self.btn_fields_key = QPushButton()
		self.btn_fields_key.setIcon(self.icon_key)
		self.btn_fields_key.setFlat(True)

		self.toolbar_fields = QHBoxLayout()
		self.toolbar_fields.setSpacing(0)
		self.toolbar_fields.addWidget(self.btn_fields_copy)
		self.toolbar_fields.addWidget(self.btn_fields_web)
		self.toolbar_fields.addWidget(self.btn_fields_key)
		self.toolbar_fields.addStretch()

		self.layout_fields = QVBoxLayout(self.panel_fields)
		self.layout_fields.setContentsMargins(3, 3, 3, 3)
		self.layout_fields.setSpacing(3)
		self.layout_fields.addLayout(self.toolbar_fields)
		self.layout_fields.addWidget(self.tree_fields)

		# Компоновка
		self.splitter_central = QSplitter()
		self.splitter_central.addWidget(self.panel_main)
		self.splitter_central.addWidget(self.panel_records)
		self.splitter_central.addWidget(self.panel_fields)
		self.splitter_central.setStretchFactor(0, 1)
		self.splitter_central.setStretchFactor(1, 2)
		self.splitter_central.setStretchFactor(2, 2)

		self.setCentralWidget(self.splitter_central)

	def _init_icons_(self):
		_folder = self.application.PATH_ICONS_SMALL

		self.icon_list        = QIcon(_folder + "/list.png")
		self.icon_list_add    = QIcon(_folder + "/list-add.png")
		self.icon_list_addsub = QIcon(_folder + "/list-addsub.png")
		self.icon_list_edit   = QIcon(_folder + "/list-edit.png")
		self.icon_list_remove = QIcon(_folder + "/list-remove.png")

		self.icon_copy        = QIcon(_folder + "/copy.png")
		self.icon_web         = QIcon(_folder + "/internet.png")
		self.icon_key         = QIcon(_folder + "/key.png")
		self.icon_user        = QIcon(_folder + "/user_gray.png")
		self.icon_note        = QIcon(_folder + "/note.png")
		self.icon_internet    = QIcon(_folder + "/internet.png")
		self.icon_phone       = QIcon(_folder + "/phone.png")
		self.icon_email       = QIcon(_folder + "/email.png")

	def _init_events_(self):
		self.tree_main.currentItemChanged.connect(self.tree_main_onClick)
		self.tree_main.doubleClicked.connect(self.btn_main_edit_onClick)

		self.tree_records.currentItemChanged.connect(self.tree_record_onClick)
		self.tree_records.doubleClicked.connect(self.btn_record_edit_onClick)
		self.tree_fields.currentItemChanged.connect(self.tree_fields_onClick)

		self.btn_main_add.clicked.connect(self.btn_main_add_onClick)
		self.btn_main_addsub.clicked.connect(self.btn_main_addsub_onClick)
		self.btn_main_edit.clicked.connect(self.btn_main_edit_onClick)
		self.btn_main_remove.clicked.connect(self.btn_main_remove_onClick)

		self.btn_record_add.clicked.connect(self.btn_record_add_onClick)
		self.btn_record_edit.clicked.connect(self.btn_record_edit_onClick)
		self.btn_fields_key.clicked.connect(self.btn_fields_show_onClick)

		self.cb_main_icons.currentIndexChanged.connect(self.cb_main_icons_onChange)
		self.cb_record_icons.currentIndexChanged.connect(self.cb_record_icons_onChange)

	def _open_vault_(self):
		self.show()
		self.application.form_start.hide()

		self.setWindowTitle("DVault - {0} - {1}".format(self.application.VERSION, self.vault.filename))

		self.load_struct()
		self.application.form_record.set_vault(self.vault)

	def open_vault(self, in_filename):
		_password, _result = QInputDialog().getText(self, "Пароль доступа", "Введите пароль доступа", echo=QLineEdit.Password)

		if _result:
			self.vault = TVault()
			_init_result = self.vault.init_vault(in_filename, _password)

			if _init_result:
				self.vault.password = _password
				self._open_vault_()
			elif _init_result is None:
				_pass2, _result = QInputDialog.getText(self, "Установка пароля", "Для хранилища не задан пароль доступа.\nВведите повторно пароль, указанный при входе, \nчто бы использовать его для этого хранилища.", echo=QLineEdit.Password)

				if _result:
					if _pass2 == _password:
						self.vault.set_password(_pass2)

						self._open_vault_()
					else:
						QMessageBox.information(self, "Ошибка паролей", "Пароли не совпали, отмена инициализации хранилища.")

						self.application.form_start.show()
						self.close()
			else:
				QMessageBox.information(self, "Ошибка доступа", "Неправильный пароль, в доступе отказано")

	def load_struct(self, in_parent_item=None):
		if in_parent_item is None:
			self.tree_main.clear()
			struct_ids = self.vault.struct_get_list_by_id("-1")
		else:
			struct_ids = self.vault.struct_get_list_by_id(in_parent_item.data(0, Qt.UserRole))

		if struct_ids is not None:
			for struct_id in struct_ids:
				self.vault.load_struct(struct_id)

				_name = self.vault.struct_item.get_field("name")

				if _name is not None:
					_icon_filename = self.vault.struct_item.get_field('icon')

					_item = QTreeWidgetItem()
					_item.setText(0, _name)
					_item.setData(0, Qt.UserRole, struct_id)

					if _icon_filename is not None:
						_icon = QIcon("{0}/{1}".format(self.application.PATH_ICONS, _icon_filename))
						_item.setIcon(0, _icon)

					if in_parent_item is None:
						self.tree_main.addTopLevelItem(_item)
					else:
						in_parent_item.addChild(_item)

					self.load_struct(_item)

		self.tree_main.expandAll()
		self.tree_main.sortByColumn(0, Qt.AscendingOrder)

		self.read_selected_struct()

	def load_records(self):
		self.tree_records.clear()

		if self.select_struct is not None:
			record_ids = self.vault.record_get_list_by_id(self.select_struct.data(0, Qt.UserRole))

			if record_ids is not None:
				for record_id in record_ids:
					self.vault.record_item.load(record_id)

					_name = self.vault.record_item.get_field("name")

					if _name is not None:
						_icon_filename = self.vault.record_item.get_field('icon')

						_item = QTreeWidgetItem()
						_item.setText(0, _name)
						_item.setData(0, Qt.UserRole, record_id)

						if _icon_filename is not None:
							_icon = QIcon("{0}/{1}".format(self.application.PATH_ICONS, _icon_filename))
							_item.setIcon(0, _icon)

						self.tree_records.addTopLevelItem(_item)

			self.tree_records.expandAll()
			self.tree_records.sortByColumn(0, Qt.AscendingOrder)

	def gui_enabled_disabled(self):
		self.btn_main_addsub.setDisabled(self.select_struct is None)
		self.btn_main_edit.setDisabled(self.select_struct is None)
		self.btn_main_remove.setDisabled(self.select_struct is None)
		self.cb_main_icons.setDisabled(self.select_struct is None)

		self.btn_record_add.setDisabled(self.select_struct is None)
		self.btn_record_edit.setDisabled(self.select_struct is None)
		self.btn_record_remove.setDisabled(self.select_struct is None)

		self.btn_fields_copy.setDisabled(self.select_struct is None or self.select_field is None)
		self.btn_fields_web.setDisabled(self.select_struct is None or self.select_field is None)

	def read_selected_struct(self):
		self.select_struct = self.tree_main.currentItem()

		if self.select_struct is not None:
			self.vault.struct_item.load(self.select_struct.data(0, Qt.UserRole))

			icon = self.vault.struct_item.get_field('icon')

			for index in range(self.cb_main_icons.count()):
				if self.cb_main_icons.itemData(index) == icon:
					self.cb_main_icons.setCurrentIndex(index)

					break
			else:
				self.cb_main_icons.setCurrentIndex(-1)
		else:
			self.cb_main_icons.setCurrentIndex(-1)

		self.load_records()
		self.read_selected_record()

		self.gui_enabled_disabled()

	def read_selected_record(self):
		self.select_record = self.tree_records.currentItem()

		if self.select_record is not None:
			self.vault.record_item.load(self.select_record.data(0, Qt.UserRole))

			icon = self.vault.record_item.get_field('icon')

			for index in range(self.cb_record_icons.count()):
				if self.cb_record_icons.itemData(index) == icon:
					self.cb_record_icons.setCurrentIndex(index)

					break
			else:
				self.cb_record_icons.setCurrentIndex(-1)
		else:
			self.vault.record_item.clear(True)
			self.cb_record_icons.setCurrentIndex(-1)

		self.show_fields()

		self.gui_enabled_disabled()

	def show_fields(self):
		self.tree_fields.clear()
		self.tree_fields.setHeaderLabels(["Field", "Value"])

		fields = list(self.vault.record_item.fields)
		fields.sort()

		for field in fields:
			if field not in SYSTEM_FIELDS:
				value = self.vault.record_item.fields[field]

				item_field = QTreeWidgetItem()
				item_field.setText(0, field)
				item_field.setText(1, "***")
				item_field.setData(1, Qt.UserRole, value)

				if field in ["Пароль", "Код"]:
					item_field.setIcon(0, self.icon_key)
				elif field in ["Имя", "Логин", "Пользователь"]:
					item_field.setIcon(0, self.icon_user)
				elif field in ["Почта", "Email", "E-Mail", "email", "e-mail"]:
					item_field.setIcon(0, self.icon_email)
				elif field in ["Сайт", "Ссылка"]:
					item_field.setIcon(0, self.icon_internet)
				elif field in ["Телефон"]:
					item_field.setIcon(0, self.icon_phone)
				elif field in ["Примечания", "Заметка", "Примечание"]:
					item_field.setIcon(0, self.icon_note)

				self.tree_fields.addTopLevelItem(item_field)

		self.tree_fields.resizeColumnToContents(0)
		self.tree_fields.setAlternatingRowColors(True)

		self.gui_enabled_disabled()

	def tree_main_onClick(self):
		self.read_selected_struct()

	def tree_record_onClick(self):
		self.read_selected_record()

	def tree_fields_onClick(self):
		self.gui_enabled_disabled()

	def btn_main_add_onClick(self):
		if self.select_struct is not None:
			parent_item = self.select_struct.parent()
		else:
			parent_item = None

		if parent_item is None:
			parent_id = "-1"
			parent_name = "Верхний уровень"
		else:
			parent_id   = parent_item.data(0, Qt.UserRole)
			parent_name = parent_item.text(0)

		name, result = QInputDialog().getText(self, "Новая категория", "Введите имя новой категории\nСтруктура: {0}".format(parent_name))

		if result:
			self.vault.add_struct(name, parent_id)
			self.load_struct()

	def btn_main_addsub_onClick(self):
		parent_id = self.select_struct.data(0, Qt.UserRole)
		parent_name = self.select_struct.text(0)

		name, result = QInputDialog().getText(self, "Новая категория", "Введите имя новой категории\nСтруктура: {0}".format(parent_name))

		if result:
			self.vault.add_struct(name, parent_id)
			self.load_struct()

	def btn_main_remove_onClick(self):
		delete = QMessageBox().information(self, "Удаление категории", "Подтвердите удаление категории: {0}".format(self.vault.struct_item.get_field('name')), QMessageBox.No | QMessageBox.Yes) == QMessageBox.Yes

		if delete:
			self.vault.struct_item.delete()

			self.load_struct()

	def btn_main_edit_onClick(self):
		old_name = self.vault.struct_item.get_field('name')
		new_name, result = QInputDialog().getText(self, "Редактирование: {0}".format(old_name), "Укажите новое название категории {0}".format(old_name), text=old_name)

		if result:
			self.vault.struct_item.set_field('name', new_name)
			self.vault.struct_item.save()

			self.select_struct.setText(0, new_name)

	def cb_main_icons_onChange(self):
		if self.select_struct is not None:
			_index = self.cb_main_icons.currentIndex()
			_new_icon = str(self.cb_main_icons.itemData(_index))

			_old_icon = str(self.vault.struct_item.get_field('icon'))

			if not (_old_icon == _new_icon):
				self.vault.struct_item.set_field("icon", _new_icon)
				self.vault.struct_item.save()

				self.select_struct.setIcon(0, self.cb_main_icons.itemIcon(self.cb_main_icons.currentIndex()))

	def cb_record_icons_onChange(self):
		if self.select_record is not None:
			_index = self.cb_record_icons.currentIndex()
			_new_icon = str(self.cb_record_icons.itemData(_index))

			_old_icon = str(self.vault.record_item.get_field('icon'))

			if not (_old_icon == _new_icon):
				self.vault.record_item.set_field("icon", _new_icon)
				self.vault.record_item.save()

				self.select_record.setIcon(0, self.cb_record_icons.itemIcon(self.cb_record_icons.currentIndex()))

	def btn_record_add_onClick(self):
		self.vault.record_item.clear(True)
		self.vault.record_item.set_field('name', "Новая запись")
		self.vault.record_item.set_field('icon', "")
		self.application.form_record.load_record()

	def btn_record_edit_onClick(self):
		self.vault.record_item.load(self.select_record.data(0, Qt.UserRole))
		self.application.form_record.load_record()

	def btn_fields_show_onClick(self):
		for index in range(self.tree_fields.topLevelItemCount()):
			item = self.tree_fields.topLevelItem(index)

			psw = item.data(1, Qt.UserRole)

			item.setText(1, psw)
