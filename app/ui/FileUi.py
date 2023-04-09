from PyQt5.QtWidgets import QGroupBox, QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from logic.AnalyzerLogic import *
from AppSetting import *


class FileUi(QVBoxLayout):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_variables()
        self._init_widgets()
        self._config_signals()
        self._config_layout()

    def _init_variables(self):
        self.last_opened_path = ""
        self.LIST_MINIMUM_HEIGHT = 120
        self.LIST_MINIMUM_WIDTH = 680

    def _init_widgets(self):
        self.grp_result = QGroupBox("Files and Paths")

        self.layout_selected_path = QVBoxLayout()
        self.layout_selected_path_button = QVBoxLayout()

        self.lst_selected_path = QListWidget()
        self.btn_remove_from_list = QPushButton(icon=QIcon(ICON_PATH + "delete.png"))
        self.btn_remove_from_list.setToolTip("Remove selected item from the list")
        self.btn_remove_from_list.setMinimumSize(24, 24)
        self.btn_remove_from_list.setIconSize(QSize(24, 24))

    def _config_signals(self):
        self.btn_remove_from_list.clicked.connect(self.remove_from_the_list)

    def _config_layout(self):
        # layout_selected_path
        self.layout_selected_path_button.addWidget(self.btn_remove_from_list)
        self.layout_selected_path_button.setAlignment(Qt.AlignTop)

        self.lst_selected_path.setMinimumHeight(self.LIST_MINIMUM_HEIGHT)
        self.lst_selected_path.setMinimumWidth(self.LIST_MINIMUM_WIDTH)
        self.layout_selected_path.setAlignment(Qt.AlignTop)

        self.layout_selected_path.addWidget(self.lst_selected_path)
        self.layout_selected_path.addLayout(self.layout_selected_path_button)

        self.grp_result.setLayout(self.layout_selected_path)

        self.addWidget(self.grp_result)
        # self.addLayout(self.layout_selected_path)

    def remove_from_the_list(self):
        list_items = self.lst_selected_path.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.lst_selected_path.takeItem(self.lst_selected_path.row(item))

    def get_selected_paths(self):
        paths = []
        items = self.lst_selected_path.selectedItems()
        for item in items:
            paths.append(item.text())
        return paths

    def get_all_paths(self):
        paths = []
        for i in range(self.lst_selected_path.count()):
            paths.append(self.lst_selected_path.item(i).text())
        return paths

    def on_add_file_folder(self, path):
        print(path)
        item = QListWidgetItem(path)
        self.lst_selected_path.addItem(item)
