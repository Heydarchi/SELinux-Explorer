
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QListWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QGroupBox, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from logic.AnalyzerLogic import *
from ui.UiUtility import *
from PythonUtilityClasses.SystemUtility import *
from AppSetting import *


class DiagramWindow(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self._init_variables()
        self._init_widgets()
        self._config_layout()

    def _init_variables(self):
        self.DEFAULT_WIDTH = 1200 * 2
        self.DEFAULT_HEIGHT = 1024 * 2

    def _init_widgets(self):
        self.im = QPixmap(self.file_path)
        self.label = QLabel()
        self.grid = QGridLayout()

    def _config_layout(self):
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)

        self.setMaximumWidth(self.DEFAULT_WIDTH)
        self.setMaximumHeight(self.DEFAULT_HEIGHT)
        self.label.setPixmap(self.im)

        # self.setGeometry(50,50,320,200)
        self.setWindowTitle("Diagram")
        self.set_window_position()

    def set_window_position(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.label.setPixmap(
            self.im.scaled(
                self.label.width(),
                self.label.height(),
                Qt.KeepAspectRatio))


class ResultUi(QVBoxLayout):
    def __init__(self, main_window, analyzer_logic):
        super().__init__()
        self.main_window = main_window
        self.analyzer_logic = analyzer_logic
        self._init_variables()
        self._init_widgets()
        self._config_signals()
        self._config_layout()

    def _init_variables(self):
        self.diagram = None
        self.lst_diagrams = []

    def _init_widgets(self):
        self.lst_results = QListWidget()
        self.layout_button = QHBoxLayout()
        self.grp_layout = QVBoxLayout()
        self.grp_result = QGroupBox("Results")

        self.lst_results.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.btn_delete_selected = UiUtility.create_button(
            "Delete the selected file", QIcon(
                ICON_PATH + "delete.png"), 24, 24)
        self.btn_open_multiple = UiUtility.create_button(
            "Open selected files(Multiple", QIcon(
                ICON_PATH + "multiple.png"), 24, 24)
        self.btn_open_single = UiUtility.create_button(
            "Open the selected file(Single)", QIcon(
                ICON_PATH + "single.png"), 24, 24)

    def _config_signals(self):
        self.btn_delete_selected.clicked.connect(self._on_delete_selected_file)
        self.btn_open_single.clicked.connect(self.on_open_single_file)
        self.btn_open_multiple.clicked.connect(self.on_open_multiple_files)
        self.analyzer_logic.set_ui_update_signal(self.on_analyze_finished)

    def _config_layout(self):
        self.layout_button.addWidget(self.btn_delete_selected)
        self.layout_button.addWidget(self.btn_open_multiple)
        self.layout_button.addWidget(self.btn_open_single)

        self.grp_layout.addWidget(self.lst_results)
        self.grp_layout.addLayout(self.layout_button)
        self.grp_result.setLayout(self.grp_layout)

        self.addWidget(self.grp_result)

    def _on_delete_selected_file(self):
        items = self.lst_results.selectedItems()
        if not items:
            return
        for item in items:
            file_path = item.text()
            self.lst_results.takeItem(self.lst_results.row(item))
            self.analyzer_logic.remove_file(file_path)

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

    def on_open_single_file(self):
        self.on_selected_result()

    def on_open_multiple_files(self):
        list_items = self.lst_results.selectedItems()
        if len(list_items) > 0:
            for item in list_items:
                diagram = DiagramWindow(item.text())
                diagram.show()
                self.lst_diagrams.append(diagram)

    def on_dispose(self):
        if self.diagram is not None:
            self.diagram.close()

        if len(self.lst_diagrams) > 0:
            for diagram in self.lst_diagrams:
                diagram.close()
