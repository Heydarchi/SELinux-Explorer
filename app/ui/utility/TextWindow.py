from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QTextEdit
from PyQt5.QtWidgets import QDesktopWidget
import re


class TextWindow(QWidget):
    def __init__(self, title, data):
        super().__init__()
        self._init_variables()
        self._init_widgets()
        self._config_layout()
        self._set_data(title, data)

    def _init_variables(self):
        self._DEFAULT_WIDTH = 1024 * 2
        self._DEFAULT_HEIGHT = 860 * 2

    def _init_widgets(self):
        self.edt_data = QTextEdit()
        self.label = QLabel()
        self.layout = QVBoxLayout()

        self.edt_data.setMinimumWidth(self._DEFAULT_WIDTH / 2)
        self.edt_data.setMinimumHeight(self._DEFAULT_HEIGHT / 2)
        self.edt_data.setReadOnly(True)

    def _config_layout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edt_data)

        self.setLayout(self.layout)

        self.setMaximumWidth(self._DEFAULT_WIDTH)
        self.setMaximumHeight(self._DEFAULT_HEIGHT)

        # self.setGeometry(50,50,320,200)
        self.setWindowTitle("Diagram")
        self.set_window_position()

    def set_window_position(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _set_data(self, title, data):
        self.label.setText(title)
        if data != None:
            self.edt_data.setText(self._coloroze_item_names(data))

    def _coloroze_item_names(self, input_str):
        input_str = input_str.replace("\n", "<br/>")
        input_str = input_str.replace("\t", "&nbsp; &nbsp; &nbsp; &nbsp; ")
        pre_suffix = '<span style=" font-size:10pt; font-weight:600; color:#0000aa;" >'
        suffix = "</span>"
        pattern = r"(\w+):"
        replacement = r"%s\1:%s" % (pre_suffix, suffix)
        out_put = re.sub(pattern, replacement, input_str)
        # print(out_put)
        return out_put
