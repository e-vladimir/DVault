from PySide.QtGui import *
from module_vault import TVault


class TFormMain(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormMain, self).__init__()

		self.application = in_application
		self.vault       = None

		self._init_icons_()
		self._init_ui()

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

		self.toolbar_main = QHBoxLayout()
		self.toolbar_main.setSpacing(0)
		self.toolbar_main.addWidget(self.btn_main_add)
		self.toolbar_main.addWidget(self.btn_main_addsub)
		self.toolbar_main.addWidget(self.btn_main_edit)
		self.toolbar_main.addWidget(self.btn_main_remove)
		self.toolbar_main.addStretch()

		self.layout_main = QVBoxLayout(self.panel_main)
		self.layout_main.setContentsMargins(3, 3, 3, 3)
		self.layout_main.setSpacing(3)
		self.layout_main.addLayout(self.toolbar_main)
		self.layout_main.addWidget(self.tree_main)

		# Записи
		self.tree_records = QTreeWidget()
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

		self.edit_record_filter = QLineEdit()

		self.toolbar_record = QHBoxLayout()
		self.toolbar_record.setSpacing(0)
		self.toolbar_record.addWidget(self.btn_record_add)
		self.toolbar_record.addWidget(self.btn_record_edit)
		self.toolbar_record.addWidget(self.btn_record_remove)
		self.toolbar_record.addStretch()
		self.toolbar_record.addWidget(self.edit_record_filter)

		self.panel_records = QWidget()

		self.layout_record = QVBoxLayout(self.panel_records)
		self.layout_record.setContentsMargins(3, 3, 3, 3)
		self.layout_record.setSpacing(3)
		self.layout_record.addLayout(self.toolbar_record)
		self.layout_record.addWidget(self.tree_records)

		# Поля
		self.tree_fields = QTreeWidget()
		self.tree_fields.setHeaderHidden(True)

		self.panel_fields = QWidget()

		self.btn_fields_copy = QPushButton()
		self.btn_fields_copy.setIcon(self.icon_copy)
		self.btn_fields_copy.setFlat(True)

		self.btn_fields_web = QPushButton()
		self.btn_fields_web.setIcon(self.icon_web)
		self.btn_fields_web.setFlat(True)

		self.btn_fields_show = QPushButton()
		self.btn_fields_show.setIcon(self.icon_key)
		self.btn_fields_show.setFlat(True)

		self.toolbar_fields = QHBoxLayout()
		self.toolbar_fields.setSpacing(0)
		self.toolbar_fields.addWidget(self.btn_fields_show)
		self.toolbar_fields.addWidget(self.btn_fields_copy)
		self.toolbar_fields.addWidget(self.btn_fields_web)
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

	def _open_vault_(self):
		self.show()
		self.application.form_start.hide()

		self.setWindowTitle("DVault    {0}".format(self.vault.filename))

	def open_vault(self, in_filename):
		_password, _result = QInputDialog().getText(self, "Пароль доступа", "Введите пароль доступа")

		if _result:
			self.vault = TVault()
			_init_result = self.vault.init_vault(in_filename, _password)

			if _init_result:
				self.vault.password = _password
				self._open_vault_()
			elif _init_result is None:
				_pass2, _result = QInputDialog.getText(self, "Установка пароля", "Для хранилища не задан пароль доступа.\nВведите повторно пароль, указанный при входе, \nчто бы использовать его для этого хранилища.")

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
