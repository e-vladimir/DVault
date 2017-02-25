from module_sqlite import TSQLiteConnection
from simplecrypto import decrypt, encrypt, sha1


def _encrypt(in_message, in_password):
	return str(encrypt(in_message, in_password))


def _decrypt(in_message, in_password):
	return str(decrypt(in_message, in_password), 'utf-8')


class TVault:
	def __init__(self):
		self.sqlite   = None
		self.password = ""
		self.filename = ""

	def _init_db_(self, in_filename):
		self.sqlite   = TSQLiteConnection(in_filename)
		self.filename = in_filename

		_sql = "CREATE TABLE IF NOT EXISTS sys_info (field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

		_sql = "CREATE TABLE IF NOT EXISTS records (id INTEGER, field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

		_sql = "CREATE TABLE IF NOT EXISTS struct (id INTEGER, parent_id TEXT, name TEXT)"
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

	def add_struct(self, in_name, in_parent_id="-1"):
		last_id = self.sqlite.get_single("SELECT id FROM struct ORDER BY id DESC LIMIT 1")

		if last_id is None:
			last_id = -1

		_name = _encrypt(in_name, self.password)

		self.sqlite.exec_insert("INSERT INTO struct (id, name, parent_id) VALUES ('{0}', '{1}', '{2}')".format(int(last_id) + 1, _name, in_parent_id))

	def struct_get_list_by_id(self, in_parent_id):
		return self.sqlite.get_multiple("SELECT id FROM struct WHERE (parent_id = '{0}')".format(in_parent_id))

	def struct_get_name(self, in_id):
		_name = self.sqlite.get_single("SELECT name FROM struct WHERE (id='{0}')".format(in_id))

		if _name is not None:
			return _decrypt(_name, self.password)
		else:
			return None
