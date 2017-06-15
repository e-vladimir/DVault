from PySide.QtGui import *
from PySide.QtCore import *
from module_vault import SYSTEM_FIELDS


class TFormRecord(QMainWindow):
	def __init__(self, in_application=None):
		super(TFormRecord, self).__init__()

		self.application = in_application
		self.vault       = None

		self._init_icons_()
		self._init_ui_()
		self._init_events_()

	def _init_ui_(self):
		self.setWindowTitle("DVault")
		self.setMinimumSize(320, 480)

		self.btn_field_append = QPushButton()
		self.btn_field_append.setIcon(self.icon_list_add)
		self.btn_field_append.setFlat(True)
		self.btn_field_remove = QPushButton()
		self.btn_field_remove.setIcon(self.icon_list_remove)
		self.btn_field_remove.setFlat(True)
		self.btn_field_import = QPushButton()
		self.btn_field_import.setIcon(self.icon_table_append)
		self.btn_field_import.setFlat(True)
		self.btn_field_load   = QPushButton()
		self.btn_field_load.setIcon(self.icon_table_load)
		self.btn_field_load.setFlat(True)

		self.cb_import = QComboBox()

		self.btn_save   = QPushButton()
		self.btn_save.setIcon(self.icon_save)
		self.btn_save.setFlat(True)
		self.btn_cancel = QPushButton()
		self.btn_cancel.setIcon(self.icon_cancel)
		self.btn_cancel.setFlat(True)

		self.toolbar_main = QHBoxLayout()
		self.toolbar_main.addWidget(self.btn_field_append)
		self.toolbar_main.addWidget(self.btn_field_remove)
		self.toolbar_main.addWidget(self.cb_import)
		self.toolbar_main.addWidget(self.btn_field_import)
		self.toolbar_main.addWidget(self.btn_field_load)
		self.toolbar_main.setSpacing(0)
		self.toolbar_main.addStretch()
		self.toolbar_main.addWidget(self.btn_save)
		self.toolbar_main.addWidget(self.btn_cancel)

		self.edit_name      = QLineEdit()
		self.edit_name.setPlaceholderText("Название")
		self.edit_note      = QLineEdit()
		self.edit_note.setPlaceholderText("Примечание")
		self.widget_central = QWidget()
		self.layout_main    = QVBoxLayout(self.widget_central)
		self.layout_main.setContentsMargins(3, 3, 3, 3)

		self.table_fields = QTableWidget()
		self.table_fields.setColumnCount(2)
		self.table_fields.setHorizontalHeaderLabels(["Поле", "Значение"])

		self.layout_main.addLayout(self.toolbar_main)
		self.layout_main.addWidget(self.edit_name)
		self.layout_main.addWidget(self.edit_note)
		# self.layout_main.addStretch()
		self.layout_main.addWidget(self.table_fields)

		self.setCentralWidget(self.widget_central)

		self.resizeColumns()

	def _init_icons_(self):
		_folder = self.application.PATH_ICONS_SMALL

		self.icon_list_add     = QIcon(_folder + "/list-add.png")
		self.icon_list_remove  = QIcon(_folder + "/list-remove.png")

		self.icon_table_append = QIcon(_folder + "/table_insert.png")
		self.icon_table_load   = QIcon(_folder + "/table_rows_inser.png")

		self.icon_copy         = QIcon(_folder + "/copy.png")

		self.icon_save         = QIcon(_folder + "/diskette.png")
		self.icon_cancel       = QIcon(_folder + "/cross.png")

	def _init_events_(self):
		self.btn_field_append.clicked.connect(self.btn_field_append_onClick)
		self.btn_field_remove.clicked.connect(self.btn_field_remove_onClick)
		self.btn_field_import.clicked.connect(self.btn_field_import_onClick)
		self.btn_field_load.clicked.connect(self.btn_field_load_onClick)
		self.btn_cancel.clicked.connect(self.btn_cancel_onClick)
		self.btn_save.clicked.connect(self.btn_save_onClick)

		self.table_fields.itemChanged.connect(self.resizeColumns)

	def set_vault(self, in_vault=None):
		self.vault = in_vault

	def load_record(self):
		_struct_name = self.vault.struct_item.get_field('name')
		_record_name = self.vault.record_item.get_field('name')

		self.table_fields.setRowCount(0)

		fields = list(self.vault.record_item.fields)
		fields.sort()

		for field in fields:
			if field not in SYSTEM_FIELDS:
				value = self.vault.record_item.fields[field]
				item_field = QTableWidgetItem()
				item_field.setText(field)
				item_value = QTableWidgetItem()
				item_value.setText(value)

				index = self.table_fields.rowCount()

				self.table_fields.setRowCount(self.table_fields.rowCount() + 1)

				self.table_fields.setItem(index, 0, item_field)
				self.table_fields.setItem(index, 1, item_value)

		self.resizeColumns()

		self.setWindowTitle("{0} [{1}]".format(_record_name, _struct_name))
		self.edit_name.setText(self.vault.record_item.get_field('name'))
		self.edit_note.setText(self.vault.record_item.get_field('note'))

		self.show()

	def resizeColumns(self):
		self.table_fields.setSortingEnabled(True)
		# self.table_fields.sortItems(0, Qt.AscendingOrder)
		# self.table_fields.sortByColumn(0, Qt.AscendingOrder)
		self.table_fields.resizeColumnsToContents()
		self.table_fields.resizeRowsToContents()

	def btn_field_append_onClick(self):
		self.table_fields.setRowCount(self.table_fields.rowCount() + 1)

		self.resizeColumns()

	def btn_field_remove_onClick(self):
		self.table_fields.removeRow(self.table_fields.currentRow())

		self.resizeColumns()

	def btn_field_import_onClick(self):
		pass

	def btn_field_load_onClick(self):
		pass

	def btn_save_onClick(self):
		icon = self.vault.record_item.fields["icon"]
		self.vault.record_item.clear()
		self.vault.record_item.set_field("icon", icon)
		self.vault.record_item.set_field('name', self.edit_name.text())
		self.vault.record_item.set_field('note', self.edit_note.text())
		self.vault.record_item.set_field('parent_id', self.vault.struct_item.id)

		for _index in range(self.table_fields.rowCount()):
			item_field = self.table_fields.item(_index, 0)
			item_value = self.table_fields.item(_index, 1)

			field = item_field.text()

			if item_value is None:
				value = ""
			else:
				value = item_value.text()

			self.vault.record_item.set_field(field, value)

		self.vault.record_item.save()

		self.close()
		self.application.form_main.load_records()

	def btn_cancel_onClick(self):
		self.close()
