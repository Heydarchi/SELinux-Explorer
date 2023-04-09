
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QLabel
from PyQt5.QtWidgets import  QTableWidget, QComboBox, QGroupBox
from PyQt5.QtGui import QIcon
from logic.AnalyzerLogic import *
from logic.FilterResult import *
from ui.UiUtility import *
from PythonUtilityClasses.SystemUtility import *
from AppSetting import *


class FilterUi(QHBoxLayout):
    def __init__(self, main_window, analyzer_logic):
        super().__init__()
        self.mainWindow = main_window
        self.analyzer_logic = analyzer_logic
        self._init_variables()
        self._init_layout()
        self._init_widgets()
        self._config_signals()
        self._config_layout()

    def _init_variables(self):
        self.lst_rules = []
        self.BTN_WIDTH = 28
        self.BTN_HEIGHT = 48
        self.selected_filter_type = None
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_COLUMNS_NUMBER = 3
        self.COL_TITLE_WIDTH = 320
        self.COL_TYPE_WIDTH = 140
        self.COL_EXACT_WORD_WIDTH = 100
        self.MARGIN = 20
        self.TABLE_MIN_WIDTH = self.COL_TITLE_WIDTH + \
            self.COL_TYPE_WIDTH + self.MARGIN + self.COL_EXACT_WORD_WIDTH
        self.COL_TITLE_INDEX = 0
        self.COL_TYPE_INDEX = 1
        self.COL_EXACT_WORD_INDEX = 2

    def _init_widgets(self):
        self.tbl_rule = QTableWidget()
        self.lbl_pattern = QLabel("Pattern")
        self.lbl_filter_type = QLabel("Rule type")
        self.edt_pattern = QLineEdit()

        self.btn_filter = UiUtility.create_button("Generate output", QIcon(
            ICON_PATH + "filter.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btn_add_filter_rule = UiUtility.create_button(
            "Add a new filter", QIcon(
                ICON_PATH + "add.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btn_clear_filter_rules = UiUtility.create_button(
            "Clear all the filters", QIcon(
                ICON_PATH + "broom.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btn_remove_selected = UiUtility.create_button(
            "Remove the selected filter", QIcon(
                ICON_PATH + "minus.png"), self.BTN_WIDTH, self.BTN_HEIGHT)

        self.chbx_exact_word = QCheckBox("Exact Word")

        self.cmb_rule_type = QComboBox()
        self.group_box = QGroupBox("Filter Rules")

        for filter_type in FilterType:
            self.cmb_rule_type.addItem(filter_type.name)

        self.tbl_rule.setColumnCount(self.TABLE_COLUMNS_NUMBER)
        self.tbl_rule.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.tbl_rule.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

        self.tbl_rule.setColumnWidth(self.COL_TITLE_INDEX, self.COL_TITLE_WIDTH)
        self.tbl_rule.setColumnWidth(self.COL_TYPE_INDEX, self.COL_TYPE_WIDTH)
        self.tbl_rule.setColumnWidth(
            self.COL_EXACT_WORD_INDEX,
            self.COL_EXACT_WORD_WIDTH)
        self.tbl_rule.setSelectionMode(QTableWidget.SingleSelection)
        self.tbl_rule.setSelectionBehavior(QTableWidget.SelectRows)

    def _init_layout(self):
        self.layout_left = QVBoxLayout()
        self.layout_filter_entry = QHBoxLayout()
        self.layout_filter_buttons = QVBoxLayout()
        self.layout_user_input = QHBoxLayout()
        self.grp_layout = QHBoxLayout()

    def _config_signals(self):
        self.btn_filter.clicked.connect(self.on_filter)
        self.btn_add_filter_rule.clicked.connect(self.on_add_filter_rule)
        self.btn_clear_filter_rules.clicked.connect(self.on_clear_filter_rules)
        self.btn_remove_selected.clicked.connect(self.on_remove_selected)
        self.cmb_rule_type.currentIndexChanged.connect(self.on_index_changed)

    def _config_layout(self):
        # layoutAnalyzer
        self.grp_layout.addWidget(self.lbl_filter_type)
        self.grp_layout.addWidget(self.cmb_rule_type)

        # layoutAnalyzerConfig
        self.layout_filter_entry.addWidget(self.lbl_pattern)
        self.layout_filter_entry.addWidget(self.edt_pattern)
        self.layout_filter_entry.addWidget(self.chbx_exact_word)

        self.layout_filter_buttons.addWidget(self.btn_add_filter_rule)
        self.layout_filter_buttons.addWidget(self.btn_remove_selected)
        self.layout_filter_buttons.addWidget(self.btn_clear_filter_rules)
        self.layout_filter_buttons.addWidget(self.btn_filter)

        self.layout_user_input.addWidget(self.tbl_rule)
        self.layout_user_input.addLayout(self.layout_filter_buttons)

        self.layout_left.addLayout(self.grp_layout)
        self.layout_left.addLayout(self.layout_filter_entry)
        self.layout_left.addLayout(self.layout_filter_buttons)
        self.layout_left.addLayout(self.layout_user_input)

        self.group_box.setMinimumWidth(
            self.TABLE_MIN_WIDTH + 3 * self.BTN_WIDTH)
        self.group_box.setLayout(self.layout_left)
        self.addWidget(self.group_box)

    def on_filter(self):
        if not self.lst_rules:
            return
        file_name, filtered_policy_file = FilterResult().filter(
            self.lst_rules, self.analyzer_logic.ref_policy_file)
        print(file_name)
        self.analyzer_logic.on_analyze_finished(filtered_policy_file)

    def on_clear_filter_rules(self):
        self.lst_rules.clear()
        self.tbl_rule.clear()
        self.tbl_rule.setRowCount(0)

    def on_add_filter_rule(self):
        rule = FilterRule()
        rule.exact_word = self.chbx_exact_word.isChecked()
        rule.keyword = self.edt_pattern.text().strip()
        if rule.keyword == "":
            return
        print("self.selected_filter_type: ", self.selected_filter_type)
        rule.filter_type = FilterRule.get_filter_type_from_str(
            self.cmb_rule_type.currentText())

        self.on_get_filter(rule)

    def on_get_filter(self, rule):
        self.lst_rules.append(rule)
        index = self.tbl_rule.rowCount()
        self.tbl_rule.setRowCount(index + 1)
        self.tbl_rule.setItem(
            index,
            self.COL_TITLE_INDEX,
            QTableWidgetItem(
                rule.keyword.strip()))
        self.tbl_rule.setItem(
            index, self.COL_TYPE_INDEX, QTableWidgetItem(
                rule.filter_type.name.strip()))
        self.tbl_rule.setItem(index,
                              self.COL_EXACT_WORD_INDEX,
                              QTableWidgetItem(str(rule.exact_word)))

    def on_remove_selected(self):
        row = self.tbl_rule.currentRow()
        if row == -1:
            return
        index = self.tbl_rule.selectedIndexes()[0].row()
        # print("index: ", index)
        # print("selectedIndex: ", self.tbl_rule.selectedIndexes())
        self.tbl_rule.removeRow(row)
        # print("self.lst_rules: ", self.lst_rules)
        del self.lst_rules[index]
        # print("self.lst_rules: ", self.lst_rules)

    def on_index_changed(self, i):
        self.selected_filter_type = FilterRule.get_filter_type_from_str(
            self.cmb_rule_type.currentText())
        # print("self.selected_filter_type: ", self.selected_filter_type)

    def get_selected_filter_type(self):
        return self.selected_filter_type

    def set_selected_filter_type(self, filter_type):
        if not isinstance(filter_type, type(FilterType)):
            filter_type = FilterType.DOMAIN
        self.selected_filter_type = FilterType(filter_type)
