from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import json


class DictListModel(QAbstractTableModel):
    """A simple model to create a table from a homogeneous json list of objects.
    Example:
        Given the following json list:
        [{"name":"Charles","age":25,"gender":"male"},{"name":"Boby","age":50,"gender":"male"}]
        This will create a table with three columns (name,age,gender) and two lines, one per record
    """
    def __init__(self, name: str = "", parent=None) -> None:
        super().__init__(parent)
        self._items = []
        self._header = []
        self._name = name

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self._header[section]
        return

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        else:
            return len(self._items)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        else:
            return len(self._header)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> str:
        return self._items[index.row()][self._header[index.column()]]

    def setData(self, index: QModelIndex, value, role) -> bool:
        if role != Qt.EditRole:
            return False
        self._items[index.row()][self._header[index.column()]] = value
        return True

    def addRow(self):
        self.beginInsertRows(QModelIndex(), len(self._items) - 1, len(self._items) - 1)
        self._items.append({h: "" for h in self._header})
        self.endInsertRows()

    def removeRow(self, row: int, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row)
        del self._items[row]
        self.endRemoveRows()

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        self.beginResetModel()
        self._items.sort(
            lambda i: i[self._header[column]], reverse=order == Qt.DescendingOrder
        )
        self.endResetModel()

    def to_dict(self):
        return {self._name: self._items}

    def from_dict(self, d: dict):
        """Try to fill in the model with the given dictionnary

        Args:
            d (dict): A dictionnary with self's name to fill in the model
        """
        self.beginResetModel()
        self._items = d.get(self._name, [])
        if self._items:
            self._header = list(self._items[0].keys())
        self.endResetModel()


class DictListTableView(QWidget):
    def __init__(self, name="", parent=None):
        super().__init__(parent)

        self._model = DictListModel(name, self)
        self._view = QTableView(self)
        self._view.setModel(self._model)
        self._view.setSelectionMode(QAbstractItemView.SingleSelection)
        self._view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self._edit_buttons_layout = QVBoxLayout(self)

        self._add_button = QPushButton("Ajouter", self)
        self._add_button.clicked.connect(self._model.addRow)

        self._remove_button = QPushButton("Supprimer", self)
        self._remove_button.clicked.connect(self._model.removeRow)

        self._layout = QHBoxLayout(self)
        self._layout.addWidget(self._view)
        self._layout.addLayout(self._edit_buttons_layout)

    def save(self):
        return self._model.to_dict()

    def open(self, d: dict):
        self._model.from_dict(d)


class Window(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._menuBar = QMenuBar(self)

        self._tab_widget = QTabWidget(self)
        self.setup_menu_bar()

    def setup_menu_bar(self):
        file_menu = self._menuBar.addMenu("Fichier")

        self.open_action = QAction("Ouvrir")
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self._open)

        self.save_action = QAction("Enregistrer")
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self._save)

        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)

        self.setCentralWidget(self._tab_widget)

        self.setMenuBar(self._menuBar)

    def _open(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Ouvrir un json de CV")

        with open(fn) as f:
            data: dict = json.load(f)

            self._dict_pages = {
                name: DictListTableView(name, self)
                for name in data
                if isinstance(data[name], list)
            }
            print(self._dict_pages.keys())
            for name, list_data in self._dict_pages.items():
                self._dict_pages[name].open(data)

            for page_name, page in self._dict_pages.items():
                self._tab_widget.addTab(page_name, page)

    def _save(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le CV en json")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    exit(app.exec_())
