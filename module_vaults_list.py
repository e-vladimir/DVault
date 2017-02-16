from module_sqlite import TSQLiteConnection


class TVaultsList:
	def __init__(self, in_fileName):
		self.filename = in_fileName

		self._init_db_()

	def _init_db_(self):
		self.connection = TSQLiteConnection(self.filename)

		_sql = "CREATE TABLE IF NOT EXISTS vaults (name TEXT, filename TEXT)"
		self.connection.exec_create(_sql)
