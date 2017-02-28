from module_sqlite import TSQLiteConnection
import simplecrypto


def encrypt(in_message, in_password):
	return str(simplecrypto.encrypt(in_message, in_password))


def decrypt(in_message, in_password):
	return str(simplecrypto.decrypt(in_message, in_password), 'utf-8')


class TStructItem:
	def __init__(self, in_vault=None):
		self.vault = in_vault

		self.id   = None
		self.fields = dict()

		self.fields['name']      = ''
		# self.fields['icon']      = "folder"
		self.fields['parent_id'] = '-1'

	def save(self):
		_id_exist = not self.vault.sqlite.get_single("SELECT COUNT(ID) FROM struct WHERE id='{0}'".format(self.id)) == '0'

		if not _id_exist:
			self.vault.sqlite.transaction_start()

			for field in self.fields:
				_field = encrypt(field, self.vault.password)
				_value = encrypt(self.fields[field], self.vault.password)

				self.vault.sqlite.exec_insert("INSERT INTO struct (id, field, value) VALUES ('{0}', '{1}', '{2}')".format(self.id, _field, _value))

			self.vault.sqlite.transaction_commit()
		else:
			self.vault.sqlite.exec_delete("DELETE FROM struct WHERE id='{0}'".format(self.id))

			self.save()

	def delete(self):
		_id = self.id
		substructs = self.vault.struct_get_list_by_id(self.id)

		for id in substructs:
			self.load(id)
			self.delete()

		self.vault.sqlite.exec_delete("DELETE FROM struct WHERE id='{0}'".format(_id))

	def clear(self):
		self.id     = None
		self.fields = dict()

	def load(self, in_id=None):
		if in_id is not None:
			self.clear()
			self.id = in_id

			self.vault.sqlite.exec_select("SELECT field, value FROM struct WHERE id='{0}'".format(in_id))

			while self.vault.sqlite.query_select.next():
				_field = decrypt(self.vault.sqlite.query_select.value(0), self.vault.password)
				_value = decrypt(self.vault.sqlite.query_select.value(1), self.vault.password)

				self.set_field(_field, _value)

	def get_next_id(self):
		last_id = self.vault.sqlite.get_single("SELECT id FROM struct ORDER BY id DESC LIMIT 1")

		if last_id is None:
			last_id = -1
		else:
			last_id = int(last_id)

		return last_id + 1

	def get_field(self, in_field=None):
		if in_field is not None:
			if in_field in self.fields:
				return self.fields[in_field]
			else:
				return None
		else:
			return None

	def set_field(self, in_field, in_value):
		self.fields[in_field] = str(in_value)


class TRecordItem:
	def __init__(self, in_vault=None):
		self.vault = in_vault

		self.id   = None
		self.fields = dict()

		self.fields['name']      = ''
		self.fields['parent_id'] = '-1'

	def save(self):
		_id_exist = not self.vault.sqlite.get_single("SELECT COUNT(ID) FROM records WHERE id='{0}'".format(self.id)) == '0'

		if not _id_exist:
			self.id = self.get_next_id()

			self.vault.sqlite.transaction_start()

			for field in self.fields:
				_field = encrypt(field, self.vault.password)
				_value = encrypt(self.fields[field], self.vault.password)

				self.vault.sqlite.exec_insert("INSERT INTO records (id, field, value) VALUES ('{0}', '{1}', '{2}')".format(self.id, _field, _value))

			self.vault.sqlite.transaction_commit()
		else:
			self.vault.sqlite.exec_delete("DELETE FROM records WHERE id='{0}'".format(self.id))

			self.save()

	def delete(self):
		_id = self.id
		substructs = self.vault.struct_get_list_by_id(self.id)

		for id in substructs:
			self.load(id)
			self.delete()

		self.vault.sqlite.exec_delete("DELETE FROM records WHERE id='{0}'".format(_id))

	def clear(self):
		self.id     = None
		self.fields = dict()

	def load(self, in_id=None):
		if in_id is not None:
			self.clear()
			self.id = in_id

			self.vault.sqlite.exec_select("SELECT field, value FROM records WHERE id='{0}'".format(in_id))

			while self.vault.sqlite.query_select.next():
				_field = decrypt(self.vault.sqlite.query_select.value(0), self.vault.password)
				_value = decrypt(self.vault.sqlite.query_select.value(1), self.vault.password)

				self.set_field(_field, _value)

	def get_next_id(self):
		last_id = self.vault.sqlite.get_single("SELECT id FROM records ORDER BY id DESC LIMIT 1")

		if last_id is None:
			last_id = -1
		else:
			last_id = int(last_id)

		return last_id + 1

	def get_field(self, in_field=None):
		if in_field is not None:
			if in_field in self.fields:
				return self.fields[in_field]
			else:
				return None
		else:
			return None

	def set_field(self, in_field, in_value):
		self.fields[in_field] = str(in_value)


class TVault:
	def __init__(self):
		self.sqlite   = None
		self.password = ""
		self.filename = ""

		self.struct_item = TStructItem(self)
		self.record_item = TRecordItem(self)

	def _init_db_(self, in_filename):
		self.sqlite   = TSQLiteConnection(in_filename)
		self.filename = in_filename

		_sql = "CREATE TABLE IF NOT EXISTS sys_info (field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

		_sql = "CREATE TABLE IF NOT EXISTS struct (id INTEGER, field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

		_sql = "CREATE TABLE IF NOT EXISTS records (id INTEGER, field TEXT, value TEXT)"
		self.sqlite.exec_create(_sql)

	def init_vault(self, in_filename, in_password):
		self._init_db_(in_filename)

		_sql = "SELECT value FROM sys_info WHERE field='pass_hash'"
		_pass_hash_from_db = self.sqlite.get_single(_sql)
		_pass_hash         = simplecrypto.sha1(in_password)

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
		self.struct_item.clear()
		self.struct_item.id = self.struct_item.get_next_id()
		self.struct_item.set_field('name', in_name)
		self.struct_item.set_field('parent_id', in_parent_id)

		self.struct_item.save()

	def struct_get_list_by_id(self, in_parent_id):
		result = []

		self.sqlite.exec_select("SELECT id, field, value FROM struct ORDER BY id")

		while self.sqlite.query_select.next():
			_id    = self.sqlite.query_select.value(0)
			_field = decrypt(self.sqlite.query_select.value(1), self.password)
			_value = decrypt(self.sqlite.query_select.value(2), self.password)

			# print("{0}: {1} = {2}".format(_id, _field, _value))

			if _field == "parent_id" and _value == str(in_parent_id):
				result.append(_id)

		# print(in_parent_id, ":", result)

		return result

	def load_struct(self, in_id):
		self.struct_item.load(in_id)
