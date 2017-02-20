from module_sqlite import TSQLiteConnection
from simplecrypto import decrypt, encrypt, sha1


def encrypto(in_message, in_password):
	return str(encrypt(in_message, in_password))


def decrypto(in_message, in_password):
	return str(decrypt(in_message, in_password), 'utf-8')


class TVault:
	def __init__(self):
		self.sqlite   = None
		self.password = ""

	def _init_db_(self, in_filename):
		self.sqlite = TSQLiteConnection(in_filename)

		_sql = "CREATE TABLE IF NOT EXISTS sys_info (field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

		_sql = "CREATE TABLE IF NOT EXISTS data_items (id INTEGER, field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

	def init_vault(self, in_filename, in_password):
		self._init_db_(in_filename)

		_sql = "SELECT value FROM sys_info WHERE field='pass_hash'"
		_pass_hash_from_db = self.sqlite.get_single(_sql)
		_pass_hash         = sha1(in_password)

		if _pass_hash_from_db is None:
			return None
		else:
			if _pass_hash == _pass_hash_from_db:
				return True
			else:
				return False

	def set_password(self, in_password):
		self.password = in_password

		self.sqlite.transaction_start()

		self.sqlite.exec_delete("DELETE FROM sys_info WHERE field='pass_hash'")
		self.sqlite.exec_insert("INSERT INTO sys_info (field, value) VALUES ('pass_hash', '{0}')".format(sha1(in_password)))

		self.sqlite.transaction_commit()
