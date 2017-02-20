from PySide.QtGui import *
from module_vault import TVault


class TFormMain(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormMain, self).__init__()

		self.application = in_application
		self.vault       = None

		self.setWindowTitle("DVault")

	def open_vault(self, in_filename):
		_password, _result = QInputDialog().getText(self, "Пароль доступа", "Введите пароль доступа")

		if _result:
			self.vault = TVault()
			_init_result = self.vault.init_vault(in_filename, _password)

			if _init_result:
				self.show()
				self.application.form_start.hide()
			elif _init_result is None:
				_pass, _result = QInputDialog.getText(self, "Установка пароля", "Для хранилища не задан пароль доступа.\nВведите повторно пароль, указанный при входе, \nчто бы использовать его для этого хранилища.")

				if _result:
					if _pass == _password:
						self.vault.set_password(_pass)
					else:
						QMessageBox.information(self, "Ошибка паролей", "Пароли не совпали, отмена инициализации хранилища.")

						self.application.form_start.show()
						self.close()
			else:
				QMessageBox.information(self, "Ошибка доступа", "Неправильный пароль, в доступе отказано")
