
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SELinux-Explorer")

        self.lblPath = QLabel("Path")
        self.lblSelectedPath = QLabel("Selected Path")
        self.edtCurrentSelectedPath = QLineEdit()

        self.lstSelectedPath = QListWidget()

        self.btnBrowseFile = QPushButton("Browse File")
        self.btnBrowseFolder = QPushButton("Browse Folder")
        self.btnAddToList = QPushButton("Add to")
        self.btnRemoveFromList = QPushButton("Remove from")
        self.btnAnalyzeAll = QPushButton("Analyze All")
        self.btnAnalyzeSelected = QPushButton("Analyze Selected")
        self.btnClearAnalyze = QPushButton("Clear Analyze")


        self.layoutPath = QHBoxLayout()
        self.layoutSelectedPath = QHBoxLayout()
        self.layoutSelectedPathButton = QVBoxLayout()
        self.layoutAnalyzer = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.container = QWidget()

        self.initUI()

    def initUI(self):
        self.setMinimumWidth(400)

        #layoutPath
        self.edtCurrentSelectedPath.setFixedWidth(500)
        self.edtCurrentSelectedPath.setReadOnly(True)

        self.layoutPath.addWidget(self.lblPath)
        self.layoutPath.addWidget(self.edtCurrentSelectedPath)
        self.layoutPath.addWidget(self.btnBrowseFile)
        self.layoutPath.addWidget(self.btnBrowseFolder)
        self.layoutPath.addStretch()

        self.btnBrowseFile.clicked.connect(self.browseFilePath)
        self.btnBrowseFolder.clicked.connect(self.browseFolderPath)


        #layoutSelectedPath
        self.layoutSelectedPathButton.addWidget(self.btnAddToList)
        self.layoutSelectedPathButton.addWidget(self.btnRemoveFromList)

        self.lblSelectedPath.setAlignment(Qt.AlignTop)
        self.lstSelectedPath.setFixedHeight(120)
        self.layoutSelectedPath.setAlignment(Qt.AlignTop)

        self.layoutSelectedPath.addLayout(self.layoutSelectedPathButton)
        self.layoutSelectedPath.addWidget(self.lstSelectedPath)

        self.btnAddToList.clicked.connect(self.addSelectedPathToList)
        self.btnRemoveFromList.clicked.connect(self.removeFromTheList)

        #layoutAnalyzer
        self.layoutAnalyzer.addWidget(self.btnAnalyzeAll)
        self.layoutAnalyzer.addWidget(self.btnAnalyzeSelected)
        self.layoutAnalyzer.addWidget(self.btnClearAnalyze)

        #mainLayout
        self.mainLayout.addLayout(self.layoutPath)
        self.mainLayout.addLayout(self.layoutSelectedPath)
        self.mainLayout.addLayout(self.layoutAnalyzer)

        self.container.setLayout(self.mainLayout)

        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

    def browseFilePath(self):
        dlg = QFileDialog()
        if dlg.exec_():
            self.edtCurrentSelectedPath.setText(dlg.selectedFiles()[0])

    def browseFolderPath(self):
        self.edtCurrentSelectedPath.setText(QFileDialog.getExistingDirectory(self, 'Hey! Select a Folder', options=QFileDialog.ShowDirsOnly))

    def addSelectedPathToList(self):
        item = QListWidgetItem(self.edtCurrentSelectedPath.text())
        print(self.edtCurrentSelectedPath.text())
        self.lstSelectedPath.addItem(item)

    def removeFromTheList(self):
        listItems=self.lstSelectedPath.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.lstSelectedPath.takeItem(self.lstSelectedPath.row(item))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()