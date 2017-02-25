# -*- coding: utf-8 -*-
# Библиотека работы с SQL БД. Приоритетно - SQLite
# V2-20170225

from PySide import QtSql


class TSQLiteConnection(object):
	fileName        = ""
	connectionName  = ""

	error           = ""

	query_create    = None
	query_select    = None
	query_insert    = None
	query_delete    = None
	query_temp      = None

	def __init__(self, in_fileName, in_connectionName="default"):
		self.fileName = in_fileName
		self.connectionName = in_connectionName

		self.SQL_connection = QtSql.QSqlDatabase.addDatabase("QSQLITE", self.connectionName)
		self.SQL_connection.setDatabaseName(self.fileName)

		if self.SQL_connection.open():
			self.query_create   = QtSql.QSqlQuery(self.SQL_connection)
			self.query_select   = QtSql.QSqlQuery(self.SQL_connection)
			self.query_insert   = QtSql.QSqlQuery(self.SQL_connection)
			self.query_delete   = QtSql.QSqlQuery(self.SQL_connection)
			self.query_temp     = QtSql.QSqlQuery(self.SQL_connection)
		else:
			self.error = self.SQL_connection.lastError()

	def exec_sql(self, in_sql_text, in_query=query_temp):
		if in_query.exec_(in_sql_text):
			return True
		else:
			self.error = in_query.lastError()

			print("Error: {0} \nSQL:{1}".format(self.error, in_sql_text))

			return False

	def exec_create(self, in_sql_text):
		return self.exec_sql(in_sql_text, self.query_create)

	def exec_insert(self, in_sql_text):
		return self.exec_sql(in_sql_text, self.query_insert)

	def exec_update(self, in_sql_text):
		return self.exec_sql(in_sql_text, self.query_insert)

	def exec_delete(self, in_sql_text):
		return self.exec_sql(in_sql_text, self.query_delete)

	def exec_select(self, in_sql_text):
		return self.exec_sql(in_sql_text, self.query_select)

	def exec_select_temp(self, in_sql_text):
		return self.exec_sql(in_sql_text, self.query_temp)

	def transaction_start(self):
		self.SQL_connection.transaction()

	def transaction_commit(self):
		self.SQL_connection.commit()

	def transaction_rollback(self):
		self.SQL_connection.rollback()

	def get_column(self, in_sql_text, in_column=0):
		if self.exec_select_temp(in_sql_text):
			result = []

			while self.query_temp.next():
				result.append(str(self.query_temp.value(in_column)))

			return result
		else:
			return []

	def get_single(self, in_sql_text):
		try:
			if self.exec_select_temp(in_sql_text):
				if self.query_temp.next():
					return str(self.query_temp.value(0))
				else:
					return None
			else:
				return None
		except:
			return None

	def get_multiple(self, in_sql_text, count=None):
		try:
			if self.exec_select_temp(in_sql_text):
				result = []

				_now_count = 0

				while self.query_temp.next():
					result.append(str(self.query_temp.value(0)))

					if count is not None:
						_now_count += 1

						if _now_count == count:
							break

				return result
			else:
				return None
		except:
			return None

	def read_value(self, in_table, in_search_condition, in_field_value="value"):
		SQL_text = "SELECT {0} " \
				   "FROM {1} " \
				   "WHERE ({2})".format(in_field_value, in_table, in_search_condition, in_field_value)
		return self.get_single(SQL_text)

	def get_id_struct(self, in_table_name="", in_id_parent="", in_include_parent=True):
		if in_include_parent:
			result = [in_id_parent]
		else:
			result = []

		sql_text = "SELECT id " \
				   "FROM {0} " \
				   "WHERE id_parent='{1}'".format(in_table_name, in_id_parent)

		id_list = self.get_list(sql_text)

		for id_item in id_list:
			result += self.get_id_struct(in_table_name, id_item)

		return result