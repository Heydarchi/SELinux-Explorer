from PyQt5.QtWidgets import QGroupBox, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize
from logic.AnalyzerLogic import *
from AppSetting import *
from PythonUtilityClasses.FileReader import *
from PythonUtilityClasses.FileWriter import *


class FileUi(QVBoxLayout):
    def __init__(self, main_window, app_setting):
        super().__init__()
        self.main_window = main_window
        self.app_setting = app_setting
        self._init_variables()
        self._init_widgets()
        self._config_signals()
        self._config_layout()
        self.EXCLUDED_ITEM_COLOR = QColor(0xFCEEEE)
        self.INCLUDED_ITEM_COLOR = QColor(0xE9FFE9)

    def _init_variables(self):
        self.last_opened_path = ""
        self.LIST_MINIMUM_HEIGHT = 120
        self.LIST_MINIMUM_WIDTH = 680

    def _init_widgets(self):
        self.grp_result = QGroupBox("Files and Paths")
        self.layout_main = QVBoxLayout()

        self.layout_included_path = QHBoxLayout()
        self.layout_excluded_path = QHBoxLayout()
        self.layout_included_path_button = QVBoxLayout()
        self.layout_excluded_path_button = QVBoxLayout()

        self.lst_included_path = QListWidget()
        self.lst_excluded_path = QListWidget()

        self.btn_add_included_file = QPushButton(icon=QIcon(ICON_PATH + "add-file.png"))
        self.btn_add_included_file.setToolTip("Add a File to the included list")
        self.btn_add_included_file.setMinimumSize(24, 24)
        self.btn_add_included_file.setIconSize(QSize(24, 24))

        self.btn_add_excluded_file = QPushButton(icon=QIcon(ICON_PATH + "add-file.png"))
        self.btn_add_excluded_file.setToolTip("Add a File to the excluded list")
        self.btn_add_excluded_file.setMinimumSize(24, 24)
        self.btn_add_excluded_file.setIconSize(QSize(24, 24))

        self.btn_add_included_path = QPushButton(
            icon=QIcon(ICON_PATH + "add-folder.png")
        )
        self.btn_add_included_path.setToolTip("Add a Path to the included list")
        self.btn_add_included_path.setMinimumSize(24, 24)
        self.btn_add_included_path.setIconSize(QSize(24, 24))

        self.btn_add_excluded_path = QPushButton(
            icon=QIcon(ICON_PATH + "add-folder.png")
        )
        self.btn_add_excluded_path.setToolTip("Add a Path to the excluded list")
        self.btn_add_excluded_path.setMinimumSize(24, 24)
        self.btn_add_excluded_path.setIconSize(QSize(24, 24))

        self.btn_remove_from_included = QPushButton(
            icon=QIcon(ICON_PATH + "delete.png")
        )
        self.btn_remove_from_included.setToolTip(
            "Remove selected item from the included list"
        )
        self.btn_remove_from_included.setMinimumSize(24, 24)
        self.btn_remove_from_included.setIconSize(QSize(24, 24))

        self.btn_remove_from_excluded = QPushButton(
            icon=QIcon(ICON_PATH + "delete.png")
        )
        self.btn_remove_from_excluded.setToolTip(
            "Remove selected item from the excluded list"
        )
        self.btn_remove_from_excluded.setMinimumSize(24, 24)
        self.btn_remove_from_excluded.setIconSize(QSize(24, 24))

        self.btn_save_included_file = QPushButton(icon=QIcon(ICON_PATH + "save.png"))
        self.btn_save_included_file.setToolTip("Save the the included list to a file")
        self.btn_save_included_file.setMinimumSize(24, 24)
        self.btn_save_included_file.setIconSize(QSize(24, 24))

        self.btn_load_included_file = QPushButton(
            icon=QIcon(ICON_PATH + "open-file.png")
        )
        self.btn_load_included_file.setToolTip("Save the the included list from a file")
        self.btn_load_included_file.setMinimumSize(24, 24)
        self.btn_load_included_file.setIconSize(QSize(24, 24))

        self.btn_save_excluded_file = QPushButton(icon=QIcon(ICON_PATH + "save.png"))
        self.btn_save_excluded_file.setToolTip("Save the the excluded list to a file")
        self.btn_save_excluded_file.setMinimumSize(24, 24)
        self.btn_save_excluded_file.setIconSize(QSize(24, 24))

        self.btn_load_excluded_file = QPushButton(
            icon=QIcon(ICON_PATH + "open-file.png")
        )
        self.btn_load_excluded_file.setToolTip("Save the the excluded list from a file")
        self.btn_load_excluded_file.setMinimumSize(24, 24)
        self.btn_load_excluded_file.setIconSize(QSize(24, 24))

    def _config_signals(self):
        self.btn_add_included_file.clicked.connect(self.on_add_file_included)
        self.btn_add_excluded_file.clicked.connect(self.on_add_file_excluded)
        self.btn_add_included_path.clicked.connect(self.on_add_included_path)
        self.btn_add_excluded_path.clicked.connect(self.on_add_excluded_path)
        self.btn_remove_from_included.clicked.connect(self.remove_from_included_list)
        self.btn_remove_from_excluded.clicked.connect(self.remove_from_excluded_list)
        self.btn_save_included_file.clicked.connect(self.save_included_file)
        self.btn_save_excluded_file.clicked.connect(self.save_excluded_file)
        self.btn_load_included_file.clicked.connect(self.load_included_file)
        self.btn_load_excluded_file.clicked.connect(self.load_excluded_file)

    def _config_layout(self):
        # layout_included_path
        self.layout_included_path_button.addWidget(self.btn_add_included_file)
        self.layout_included_path_button.addWidget(self.btn_add_included_path)
        self.layout_included_path_button.addWidget(self.btn_remove_from_included)
        self.layout_included_path_button.addWidget(self.btn_save_included_file)
        self.layout_included_path_button.addWidget(self.btn_load_included_file)
        self.layout_included_path_button.setAlignment(Qt.AlignTop)

        self.layout_excluded_path_button.addWidget(self.btn_add_excluded_file)
        self.layout_excluded_path_button.addWidget(self.btn_add_excluded_path)
        self.layout_excluded_path_button.addWidget(self.btn_remove_from_excluded)
        self.layout_excluded_path_button.addWidget(self.btn_save_excluded_file)
        self.layout_excluded_path_button.addWidget(self.btn_load_excluded_file)
        self.layout_excluded_path_button.setAlignment(Qt.AlignTop)

        self.lst_included_path.setMinimumHeight(self.LIST_MINIMUM_HEIGHT)
        self.lst_included_path.setMinimumWidth(self.LIST_MINIMUM_WIDTH)
        self.layout_included_path.setAlignment(Qt.AlignTop)

        self.lst_excluded_path.setMinimumHeight(self.LIST_MINIMUM_HEIGHT)
        self.lst_excluded_path.setMinimumWidth(self.LIST_MINIMUM_WIDTH)
        self.layout_excluded_path.setAlignment(Qt.AlignTop)

        self.layout_included_path.addWidget(self.lst_included_path)
        self.layout_included_path.addLayout(self.layout_included_path_button)

        self.layout_excluded_path.addWidget(self.lst_excluded_path)
        self.layout_excluded_path.addLayout(self.layout_excluded_path_button)

        self.layout_main.addLayout(self.layout_included_path)
        self.layout_main.addLayout(self.layout_excluded_path)

        self.grp_result.setLayout(self.layout_main)

        self.addWidget(self.grp_result)
        # self.addLayout(self.layout_included_path)

    def on_add_included_path(self):
        path = QFileDialog(
            directory=self.app_setting.last_opened_path
        ).getExistingDirectory(
            self.main_window,
            "Hey! Select a Folder",
            options=QFileDialog.ShowDirsOnly,
        )
        if path:
            self.on_add_file_folder_included(path)

    def on_add_excluded_path(self):
        path = QFileDialog(
            directory=self.app_setting.last_opened_path
        ).getExistingDirectory(
            self.main_window,
            "Hey! Select a Folder",
            options=QFileDialog.ShowDirsOnly,
        )
        if path:
            self.on_add_file_folder_excluded(path)

    def on_add_file_included(self):
        dlg = QFileDialog(directory=self.app_setting.last_opened_path)
        if dlg.exec_():
            self.on_add_file_folder_included(dlg.selectedFiles()[0])

    def on_add_file_excluded(self):
        dlg = QFileDialog(directory=self.app_setting.last_opened_path)
        if dlg.exec_():
            self.on_add_file_folder_excluded(dlg.selectedFiles()[0])

    def remove_from_included_list(self):
        list_items = self.lst_included_path.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.lst_included_path.takeItem(self.lst_included_path.row(item))

    def remove_from_excluded_list(self):
        list_items = self.lst_excluded_path.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.lst_excluded_path.takeItem(self.lst_excluded_path.row(item))

    def get_selected_paths(self):
        paths = []
        items = self.lst_included_path.selectedItems()
        for item in items:
            paths.append(item.text())
        return paths

    def get_included_paths(self):
        paths = []
        for i in range(self.lst_included_path.count()):
            paths.append(self.lst_included_path.item(i).text())
        return paths

    def get_excluded_paths(self):
        paths = []
        for i in range(self.lst_excluded_path.count()):
            paths.append(self.lst_excluded_path.item(i).text())
        return paths

    def on_add_file_folder_included(self, path):
        print(path)
        item = QListWidgetItem(path)
        item.setBackground(self.INCLUDED_ITEM_COLOR)
        self.lst_included_path.addItem(item)

    def on_add_file_folder_excluded(self, path):
        print(path)
        item = QListWidgetItem(path)
        item.setBackground(self.EXCLUDED_ITEM_COLOR)
        self.lst_excluded_path.addItem(item)

    def save_included_file(self):
        lst_file = list()
        lst_file.append("SELINUX_EXPLORE_PATHS: INCLUDED")
        lst_file.extend(self.get_included_paths())
        file_path = QFileDialog(
            directory=self.app_setting.last_opened_path
        ).getSaveFileName(self.main_window, "Save an included path to a file")
        if file_path[0]:
            FileWriter.write_list_to_file(file_path[0], lst_file)

    def save_excluded_file(self):
        lst_file = list()
        lst_file.append("SELINUX_EXPLORE_PATHS: EXCLUDED")
        lst_file.extend(self.get_excluded_paths())
        file_path = QFileDialog(
            directory=self.app_setting.last_opened_path
        ).getSaveFileName(self.main_window, "Save an excluded path to a file")
        if file_path[0]:
            FileWriter.write_list_to_file(file_path[0], lst_file)

    def load_included_file(self):
        file_path = QFileDialog(
            directory=self.app_setting.last_opened_path
        ).getOpenFileName(self.main_window, "Open an included file path")
        if file_path[0]:
            lst_file = FileReader.read_file_lines(file_path[0])
            if "SELINUX_EXPLORE_PATHS:" not in lst_file[0]:
                QMessageBox.warning(
                    self.main_window,
                    "Warning",
                    "This is not a valid file",
                    QMessageBox.Ok,
                )
                return

            if "INCLUDED" not in lst_file[0]:
                result = QMessageBox().question(
                    self.main_window,
                    "Warning",
                    "This file is not included file. Do you want to continue?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if result == QMessageBox.No:
                    return

            for i in range(1, len(lst_file)):
                self.on_add_file_folder_included(lst_file[i])

    def load_excluded_file(self):
        file_path = QFileDialog(
            directory=self.app_setting.last_opened_path
        ).getOpenFileName(self.main_window, "Open an excluded file path")
        if file_path[0]:
            lst_file = FileReader.read_file_lines(file_path[0])
            if "SELINUX_EXPLORE_PATHS:" not in lst_file[0]:
                QMessageBox.warning(
                    self.main_window,
                    "Warning",
                    "This is not a valid file",
                    QMessageBox.Ok,
                )
                return

            if "EXCLUDED" not in lst_file[0]:
                result = QMessageBox().question(
                    self.main_window,
                    "Warning",
                    "This file is not excluded file. Do you want to continue?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if result == QMessageBox.No:
                    return

            for i in range(1, len(lst_file)):
                self.on_add_file_folder_excluded(lst_file[i])
