from PyQt5.QtWidgets import QAction, QToolBar, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from logic.AnalyzerLogic import *
from PyQt5.QtCore import Qt
from ui.UiUtility import *
from ui.AboutUi import *
from PythonUtilityClasses.SystemUtility import *
from PythonUtilityClasses.FileWriter import *
from PythonUtilityClasses.FileReader import *
from AppSetting import *


class ToolbarUi(QToolBar):
    def __init__(self, main_window, analyzer_logic, app_setting):
        super().__init__()
        self.main_window = main_window
        self.analyzer_logic = analyzer_logic
        self.app_setting = app_setting
        self._init_variables()
        self._init_widgets()
        self._config_signals()
        self._config_layout()

    def _init_variables(self):
        self.keep_result = False
        self.about = None
        self.lst_results = []

    def _init_widgets(self):
        self.act_add_path = QAction(
            QIcon(ICON_PATH + "add-folder.png"),
            "Add a Path to the list",
            self.main_window,
        )
        self.act_remove_output = QAction(
            QIcon(ICON_PATH + "remove.png"), "Remove Outputs", self.main_window
        )
        self.act_clear_analyze = QAction(
            QIcon(ICON_PATH + "reset.png"), "Clear Analyze", self.main_window
        )
        self.act_wipe_all = QAction(
            QIcon(ICON_PATH + "broom.png"),
            "Wipe all(output, analyze, etc.)",
            self.main_window,
        )
        self.act_make_reference = QAction(
            QIcon(ICON_PATH + "reference.png"),
            "Make reference from the analyzed data",
            self.main_window,
        )
        self.act_analyze_all = QAction(
            QIcon(ICON_PATH + "magic-wand.png"),
            "Analyze all the files/paths",
            self.main_window,
        )
        self.act_keep_result = QAction(
            QIcon(ICON_PATH + "hosting.png"),
            "Don't erase the current result before Analyzing",
            self.main_window,
        )
        self.act_about = QAction(
            QIcon(ICON_PATH + "information.png"), "About", self.main_window
        )

        self.act_keep_result.setCheckable(True)

    def _config_signals(self):
        self.addAction(self.act_analyze_all)
        self.addSeparator()
        self.addAction(self.act_make_reference)
        self.addSeparator()
        self.addAction(self.act_remove_output)
        self.addAction(self.act_clear_analyze)
        self.addAction(self.act_wipe_all)
        self.addSeparator()
        self.addAction(self.act_keep_result)
        self.addSeparator()
        self.addAction(self.act_about)

    def _config_layout(self):
        self.act_analyze_all.triggered.connect(self.on_analyze_all)
        self.act_clear_analyze.triggered.connect(self.on_clear_analyze)
        self.act_remove_output.triggered.connect(self.on_clear_output_folder)
        self.act_wipe_all.triggered.connect(self.on_wipe_all)
        self.act_keep_result.triggered.connect(self.on_clicked_keep_result)
        self.act_make_reference.triggered.connect(self.on_make_reference)
        self.act_about.triggered.connect(self.on_about)

        self.setOrientation(Qt.Vertical)

    def connect_on_add_file_folder_included(self, on_add_file_folder_included):
        self.add_file_folder = on_add_file_folder_included

    def connect_to_get_selected_paths(self, get_selected_path):
        self.get_selected_paths = get_selected_path

    def connect_to_get_included_paths(self, get_included_paths):
        self.get_included_paths = get_included_paths

    def connect_to_get_excluded_paths(self, get_excluded_paths):
        self.get_excluded_paths = get_excluded_paths

    def add_path_to_list(self, path):
        self.app_setting.last_opened_path = path
        self.add_file_folder(path)

    def on_analyze_selected_paths(self):
        paths = self.get_selected_paths()
        self.analyzer_logic.analyze_all(paths)
        UiUtility.show_message("Analyzer", "The selected files are analyzed!")

    def on_analyze_all(self):
        included_paths = self.get_included_paths()
        excluded_paths = self.get_excluded_paths()
        self.analyzer_logic.analyze_all(included_paths, excluded_paths)
        UiUtility.show_message("Analyzer", "All the files are analyzed!")

    def on_clear_analyze(self):
        self.analyzer_logic.clear()
        print("Cleared analyzer!")

    def on_clear_output_folder(self):
        self.analyzer_logic.clear_output()
        print("Cleared output!")

    def on_wipe_all(self):
        self.on_clear_output_folder()
        self.on_clear_analyze()
        self.analyzer_logic.on_analyze_finished(None)
        print("Wiped all!")

    def on_result_added(self, file_path):
        item = QListWidgetItem(file_path)
        self.lst_results.addItem(item)

    def on_analyze_finished(self):
        self.lst_results.clear()
        for file in self.analyzer_logic.list_of_diagrams:
            self.lst_results.addItem(QListWidgetItem(file))

    def on_selected_result(self):
        list_items = self.lst_results.selectedItems()
        if len(list_items) > 0:
            self.diagram = DiagramWindow(list_items[0].text())
            self.diagram.show()

    def on_clicked_keep_result(self):
        self.keep_result = self.sender().isChecked()
        self.analyzer_logic.set_keep_result(self.sender().isChecked())

    def on_make_reference(self):
        ref_name, confirm = QInputDialog.getText(
            self, "Text Input Dialog", "Enter your name:"
        )
        if confirm:
            SettingClass.save_list_as_json(
                ref_name, self.analyzer_logic.list_of_policy_files
            )
            print("AppSetting saved!")

    def on_about(self):
        self.about = AboutWindow()
        self.about.show()

    def on_dispose(self):
        if self.about is not None:
            self.about.close()
