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

		self.tree_main = QTreeWidget()
		self.tree_main.setHeaderHidden(True)

		self.panel_main  = QWidget()

		self.btn_main_add = QPushButton()
		self.btn_main_add.setIcon(self.icon_list_add)
		self.btn_main_add.setFlat(True)

		self.btn_main_edit = QPushButton()
		self.btn_main_edit.setIcon(self.icon_list_edit)
		self.btn_main_edit.setFlat(True)

		self.btn_main_remove = QPushButton()
		self.btn_main_remove.setIcon(self.icon_list_remove)
		self.btn_main_remove.setFlat(True)

		self.toolbar_main = QHBoxLayout()
		self.toolbar_main.setSpacing(3)
		self.toolbar_main.addWidget(self.btn_main_add)
		self.toolbar_main.addWidget(self.btn_main_edit)
		self.toolbar_main.addWidget(self.btn_main_remove)
		self.toolbar_main.addStretch()

		self.layout_main = QVBoxLayout(self.panel_main)
		self.layout_main.setContentsMargins(3, 3, 3, 3)
		self.layout_main.setSpacing(3)
		self.layout_main.addLayout(self.toolbar_main)
		self.layout_main.addWidget(self.tree_main)

		self.tree_records = QTreeWidget()
		self.tree_records.setHeaderHidden(True)

		self.splitter_central = QSplitter()
		# self.splitter_central.setContentsMargins(3, 3, 3, 3)
		self.splitter_central.addWidget(self.panel_main)
		self.splitter_central.addWidget(self.tree_records)
		self.splitter_central.setStretchFactor(0, 1)
		self.splitter_central.setStretchFactor(1, 2)

		self.setCentralWidget(self.splitter_central)

	def _init_icons_(self):
		_folder = self.application.PATH_ICONS_SMALL

		self.icon_list        = QIcon(_folder + "/list.png")
		self.icon_list_add    = QIcon(_folder + "/list-add.png")
		self.icon_list_edit   = QIcon(_folder + "/list-edit.png")
		self.icon_list_remove = QIcon(_folder + "/list-remove.png")

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
