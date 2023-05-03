from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize
from logic.AnalyzerLogic import *
from ui.FileUi import *
from ui.FilterUi import *
from ui.ResultUi import *
from ui.AnalyzerResultUi import *
from ui.ToolbarUi import *
from ui.StatusbarUi import *
from PythonUtilityClasses.FileWriter import *
from PythonUtilityClasses.FileReader import *
from AppSetting import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME + " " + APP_VERSION)
        self._init_variables()
        self._initMainLayout()
        self._config_signals()
        self.load_setting()

    def _init_variables(self):
        self.analyzer_logic = AnalyzerLogic()
        self.app_setting = AppSetting()
        self.setting_util = SettingClass()

    def load_setting(self):
        if os.path.isfile("app_setting.json"):
            json_str = FileReader().read_file("app_setting.json")
            self.app_setting = AppSetting.from_json(json_str)
            self.layout_path.last_opened_path = self.app_setting.last_opened_path
            self.toolbar.keep_result = self.app_setting.keep_the_result
            self.layout_filter.set_selected_filter_type(
                self.app_setting.selected_filter_type
            )
            print("AppSetting loaded!")
        else:
            self.save_setting()

    def save_setting(self):
        self.app_setting.last_opened_path = self.layout_path.last_opened_path
        self.app_setting.keep_the_result = self.toolbar.keep_result
        self.app_setting.selected_filter_type = (
            self.layout_filter.get_selected_filter_type()
        )

        FileWriter.write_file("app_setting.json", self.app_setting.to_json())
        print("AppSetting saved!")

    def _initMainLayout(self):
        self.layout_path = FileUi(self, self.app_setting)
        self.layout_filter = FilterUi(self, self.analyzer_logic)
        self.layout_result = ResultUi(self, self.analyzer_logic)
        self.layout_analyzer_result = AnalyzerResultUi(self, self.analyzer_logic)
        self.toolbar = ToolbarUi(self, self.analyzer_logic, self.app_setting)
        self.statusbar = StatusbarUi(self, self.analyzer_logic)
        self.main_layout_left = QVBoxLayout()
        self.main_layout_right = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.container = QWidget()

        self.main_layout_left.addLayout(self.layout_path)
        self.main_layout_left.addLayout(self.layout_result)
        self.main_layout.addLayout(self.main_layout_left)
        self.main_layout.addLayout(self.main_layout_right)

        self.main_layout_right.addLayout(self.layout_analyzer_result)
        self.main_layout_right.addLayout(self.layout_filter)

        self.container.setLayout(self.main_layout)
        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.setStatusBar(self.statusbar)

        self._set_window_position()

        app_icon = QIcon()
        app_icon.addFile(ICON_PATH + "icon_16.png", QSize(16, 16))
        app_icon.addFile(ICON_PATH + "icon_24.png", QSize(24, 24))
        app_icon.addFile(ICON_PATH + "icon_32.png", QSize(32, 32))
        app_icon.addFile(ICON_PATH + "icon_64.png", QSize(64, 64))
        app_icon.addFile(ICON_PATH + "icon_256.png", QSize(256, 256))
        self.setWindowIcon(app_icon)

    def _config_signals(self):
        self.toolbar.connect_to_get_selected_paths(self.layout_path.get_selected_paths)
        self.toolbar.connect_to_get_included_paths(self.layout_path.get_included_paths)
        self.toolbar.connect_to_get_excluded_paths(self.layout_path.get_excluded_paths)
        self.toolbar.connect_on_add_file_folder_included(
            self.layout_path.on_add_file_folder_included
        )
        self.layout_analyzer_result.connect_to_filter_ui(
            self.layout_filter.on_get_filter
        )
        self.analyzer_logic.set_statusbar_update_signal(self.statusbar.update_statusbar)

    def _set_window_position(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def dispose_objects(self):
        self.layout_result.on_dispose()
        self.toolbar.on_dispose()
        self.layout_analyzer_result.on_dispose()

    def closeEvent(self, event):
        result = QMessageBox().question(
            self,
            "Confirm Exit...",
            "Are you sure you want to exit ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        event.ignore()

        if result == QMessageBox.Yes:
            self.save_setting()
            self.dispose_objects()
            event.accept()
