from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QGroupBox, QLabel, QCheckBox, QLineEdit
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *
from logic.FilterResult import *
from ui.UiUtility import *
from ui.utility.TextWindow import TextWindow
from AppSetting import *
from model.PolicyEntities import *


class AnalyzerResultUi(QVBoxLayout):
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
        self.result_policy_file = PolicyFile()
        self.last_rules_result = []
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_COLUMNS_NUMBER = 2
        self.COL_TITLE_WIDTH = 420
        self.COL_TYPE_WIDTH = 140
        self.MARGIN = 20
        self.TABLE_MIN_WIDTH = self.COL_TITLE_WIDTH + self.COL_TYPE_WIDTH + self.MARGIN
        self.COL_TITLE_INDEX = 0
        self.COL_TYPE_INDEX = 1
        self.BTN_WIDTH = 28
        self.BTN_HEIGHT = 48
        self._info_window = None

    def _init_widgets(self):
        self.lbl_search = QLabel("Search")
        self.edt_search = QLineEdit()
        self.chk_case_sensitive = QCheckBox("Case sensitive")
        self.btn_reset_search = UiUtility.create_button(
            "Reset search",
            ICON_PATH + "reset_green.png",
            self.BTN_WIDTH,
            self.BTN_HEIGHT,
        )

        self.btn_item_info = UiUtility.create_button(
            "Info of the selected item",
            ICON_PATH + "information.png",
            self.BTN_WIDTH,
            self.BTN_HEIGHT,
        )
        self.tbl_result = QTableWidget()
        self.layout_filter = QHBoxLayout()
        self.group_box = QGroupBox("Analyzer result")
        self.grp_layout = QVBoxLayout()
        self.layout_search = QHBoxLayout()
        self.layout_right = QVBoxLayout()
        self.layout_table = QHBoxLayout()

        self.chk_case_sensitive.setChecked(False)

        self.btn_add_selected = UiUtility.create_button(
            "Add to the filters",
            ICON_PATH + "down-arrow.png",
            self.BTN_WIDTH,
            self.BTN_HEIGHT,
        )

        self.cmb_filter = QComboBox()
        self.cmb_filter.addItem("ALL")
        for filter_type in FilterType:
            self.cmb_filter.addItem(filter_type.name)

        self.lbl_filter_type = QLabel("Filter type")

        self.tbl_result.setColumnCount(self.TABLE_COLUMNS_NUMBER)
        self.tbl_result.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.tbl_result.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

        self.tbl_result.setColumnWidth(self.COL_TITLE_INDEX, self.COL_TITLE_WIDTH)
        self.tbl_result.setColumnWidth(self.COL_TYPE_INDEX, self.COL_TYPE_WIDTH)
        self.tbl_result.setSelectionMode(QTableWidget.SingleSelection)
        self.tbl_result.setSelectionBehavior(QTableWidget.SelectRows)

    def _config_signals(self):
        self.btn_add_selected.clicked.connect(self.on_add_selected_filter)
        self.analyzer_logic.set_ui_update_analyzer_data_signal(self.on_analyze_finished)
        self.cmb_filter.currentIndexChanged.connect(self.on_filter_changed)
        self.edt_search.textChanged.connect(self._on_seach_text_changed)
        self.btn_reset_search.clicked.connect(self.on_reset_search)
        self.chk_case_sensitive.clicked.connect(self._on_case_sensitive_changed)
        self.btn_item_info.clicked.connect(self.on_item_info)

    def _config_layout(self):
        self.layout_search.addWidget(self.lbl_search)
        self.layout_search.addWidget(self.edt_search)
        self.layout_search.addWidget(self.chk_case_sensitive)
        self.layout_search.addWidget(self.btn_reset_search)

        self.layout_filter.addWidget(self.lbl_filter_type)
        self.layout_filter.addWidget(self.cmb_filter)

        self.layout_right.addWidget(self.btn_item_info)
        self.layout_right.addSpacerItem(
            QSpacerItem(
                self.BTN_WIDTH,
                self.BTN_WIDTH,
                QSizePolicy.Minimum,
                QSizePolicy.Expanding,
            )
        )
        self.layout_right.addWidget(self.btn_add_selected)

        self.layout_table.addWidget(self.tbl_result)
        self.layout_table.addLayout(self.layout_right)

        self.grp_layout.addLayout(self.layout_search)
        self.grp_layout.addLayout(self.layout_filter)
        self.grp_layout.addLayout(self.layout_table)

        self.group_box.setLayout(self.grp_layout)

        self.addWidget(self.group_box)

    def _on_case_sensitive_changed(self):
        self._on_seach_text_changed()

    def on_add_selected_filter(self):
        row = self.tbl_result.currentRow()
        if row < 0:
            return

        rule = FilterRule()
        rule.exact_word = UiUtility.ask_question(
            self.main_window, "Exact word", "Do you want to add the exact word?"
        )
        rule.keyword = self.tbl_result.item(row, self.COL_TITLE_INDEX).text().strip()
        rule.filter_type = FilterRule.get_filter_type_from_str(
            self.tbl_result.item(row, self.COL_TYPE_INDEX).text().strip()
        )
        self.send_to_filter_ui(rule)

    def on_analyze_finished(self, ref_policy_file):
        print("onAnalyzeFinished")
        if ref_policy_file is None:
            ref_policy_file = PolicyFile()
        self.result_policy_file = ref_policy_file
        self.on_filter_changed()

    def _on_seach_text_changed(self):
        lst_rules = []
        if self.edt_search.text().strip() != "":
            lst_rules = self.search_result(
                self.last_rules_result,
                self.edt_search.text().strip(),
                self.chk_case_sensitive.isChecked(),
            )
        else:
            lst_rules = self.last_rules_result
        self.update_table(lst_rules)

    def on_reset_search(self):
        self.edt_search.setText("")

    def _collect_domain_rule(self, policy_file):
        domain_rules = []
        if policy_file is None:
            return domain_rules

        for type_def in policy_file.type_def:
            if type_def.name.strip() != "":
                domain_rules.append(FilterRule(FilterType.DOMAIN, type_def.name, False))

        for se_apps in policy_file.se_apps:
            if se_apps.domain.strip() != "":
                domain_rules.append(
                    FilterRule(FilterType.DOMAIN, se_apps.domain, False)
                )

        for context in policy_file.contexts:
            if context.domain_name.strip() != "":
                domain_rules.append(
                    FilterRule(FilterType.DOMAIN, context.domain_name, False)
                )

        for attribute in policy_file.attribute:
            if attribute.name.strip() != "":
                domain_rules.append(
                    FilterRule(FilterType.DOMAIN, attribute.name, False)
                )

        domain_rules = list(set(domain_rules))
        return domain_rules

    def _collect_file_path_rule(self, policy_file):
        file_path_rules = []
        if policy_file is None:
            return file_path_rules

        for se_apps in policy_file.se_apps:
            if se_apps.name.strip() != "":
                file_path_rules.append(
                    FilterRule(FilterType.FILE_PATH, se_apps.name, False)
                )

        for context in policy_file.contexts:
            if context.path_name.strip() != "":
                file_path_rules.append(
                    FilterRule(FilterType.FILE_PATH, context.path_name, False)
                )

        file_path_rules = list(set(file_path_rules))
        return file_path_rules

    def _collect_permission_rule(self, policy_file):
        permission_rules = []
        if policy_file is None:
            return permission_rules

        for rule in policy_file.rules:
            if len(rule.permissions) > 0:
                for permission in rule.permissions:
                    permission_rules.append(
                        FilterRule(FilterType.PERMISSION, permission, False)
                    )

        for macro in policy_file.macros:
            if len(macro.rules) > 0:
                for rule in macro.rules:
                    for permission in rule.permissions:
                        permission_rules.append(
                            FilterRule(FilterType.PERMISSION, permission, False)
                        )

        permission_rules = list(set(permission_rules))
        return permission_rules

    def _collect_class_type(self, policy_file):
        class_type_rules = []
        if policy_file is None:
            return class_type_rules

        for type_def in policy_file.type_def:
            for _type in type_def.types:
                if _type.strip() != "":
                    class_type_rules.append(
                        FilterRule(FilterType.CLASS_TYPE, _type, False)
                    )

        for context in policy_file.contexts:
            for _type in context.type_def.types:
                if _type.strip() != "":
                    class_type_rules.append(
                        FilterRule(FilterType.CLASS_TYPE, _type, False)
                    )

        for rule in policy_file.rules:
            if rule.class_type.strip() != "":
                class_type_rules.append(
                    FilterRule(FilterType.CLASS_TYPE, rule.class_type, False)
                )

        class_type_rules = list(set(class_type_rules))
        return class_type_rules

    def on_dispose(self):
        if self.diagram is not None:
            self.diagram.close()

    def connect_to_filter_ui(self, on_add_filter_event):
        self.send_to_filter_ui = on_add_filter_event

    def on_filter_changed(self):
        """Filter the result table based on the selected filter type,
        If it's ALL, show all the results"""
        # print("onFilterChanged")
        lst_rules = []
        if self.cmb_filter.currentText() == "ALL":
            lst_rules.extend(self._collect_domain_rule(self.result_policy_file))
            lst_rules.extend(self._collect_file_path_rule(self.result_policy_file))
            lst_rules.extend(self._collect_permission_rule(self.result_policy_file))
            lst_rules.extend(self._collect_class_type(self.result_policy_file))
        elif self.cmb_filter.currentText() == FilterType.DOMAIN.name:
            lst_rules.extend(self._collect_domain_rule(self.result_policy_file))
        elif self.cmb_filter.currentText() == FilterType.FILE_PATH.name:
            lst_rules.extend(self._collect_file_path_rule(self.result_policy_file))
        elif self.cmb_filter.currentText() == FilterType.PERMISSION.name:
            lst_rules.extend(self._collect_permission_rule(self.result_policy_file))
        elif self.cmb_filter.currentText() == FilterType.CLASS_TYPE.name:
            lst_rules.extend(self._collect_class_type(self.result_policy_file))

        self.last_rules_result = lst_rules
        # print("Total rules: " + str(len(lst_rules)))
        if self.edt_search.text().strip() != "":
            lst_rules = self.search_result(
                lst_rules,
                self.edt_search.text().strip(),
                self.chk_case_sensitive.isChecked(),
            )

        self.update_table(lst_rules)

    def update_table(self, lst_rules):
        # print("updateTable")
        # print("Total rules: " + str(lst_rules))
        lst_rules = list(set(lst_rules))
        self.clear_table()
        self.tbl_result.setRowCount(len(lst_rules))
        for i in range(len(lst_rules)):
            self.tbl_result.setItem(
                i, self.COL_TITLE_INDEX, QTableWidgetItem(lst_rules[i].keyword.strip())
            )
            self.tbl_result.setItem(
                i,
                self.COL_TYPE_INDEX,
                QTableWidgetItem(lst_rules[i].filter_type.name.strip()),
            )

    def search_result(self, lst_rules, keyword, case_sensitive):
        lst_search_result = []
        for item in lst_rules:
            if self.is_similar(keyword, item.keyword, case_sensitive):
                lst_search_result.append(item)

        return lst_search_result

    def clear_table(self):
        self.tbl_result.clear()
        self.tbl_result.setRowCount(0)

    def is_similar(self, keyword, target, case_sensitive):
        if not case_sensitive:
            return keyword.lower() in target.lower()
        else:
            return keyword in target

    def on_item_info(self):
        # print("onItemInfo")
        row = self.tbl_result.currentRow()
        if row < 0:
            return

        filter_type = FilterRule(
            FilterRule.get_filter_type_from_str(
                self.tbl_result.item(row, self.COL_TYPE_INDEX).text()
            ),
            self.tbl_result.item(row, self.COL_TITLE_INDEX).text(),
            True,
        )

        item_info = self.analyzer_logic.get_info_of_item(filter_type)

        if item_info != None:
            self._info_window = TextWindow(
                self.tbl_result.item(row, self.COL_TITLE_INDEX).text(),
                "".join([item.to_string() for item in item_info]),
            )
            self._info_window.show()
        else:
            UiUtility.show_message("Info", "Nothing to show!")

    def on_dispose(self):
        if self._info_window is not None:
            self._info_window.close()
