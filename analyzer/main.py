
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFileDialog, QCheckBox, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from AnalyzerLogic import *
import sys




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SELinux-Explorer")
        self.initVariables()

        self.createPathLayout()
        self.createAnalyzeLayout()
        self.initMainLayout()

    def initVariables(self):
        self.keepResult = False
        self.analyzerLogic = AnalyzerLogic()

    def createPathLayout(self):
        self.layoutPath = QHBoxLayout()
        self.layoutSelectedPath = QHBoxLayout()
        self.layoutSelectedPathButton = QVBoxLayout()

        self.lblPath = QLabel("Path")
        self.lblSelectedPath = QLabel("Selected Path")
        self.edtCurrentSelectedPath = QLineEdit()

        self.lstSelectedPath = QListWidget()

        self.btnBrowseFile = QPushButton("Browse File")
        self.btnBrowseFolder = QPushButton("Browse Folder")
        self.btnAddToList = QPushButton("Add to")
        self.btnRemoveFromList = QPushButton("Remove from")

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

    def createAnalyzeLayout(self):
        self.layoutAnalyzer = QVBoxLayout()
        self.layoutAnalyzerConfig = QHBoxLayout()
        self.layoutAnalyzerAnalyze = QHBoxLayout()

        self.btnAnalyzeAll = QPushButton("Analyze All")
        self.btnAnalyzeSelected = QPushButton("Analyze Selected")
        self.btnClearAnalyze = QPushButton("Clear Analyze")

        self.chkKeepAnalyze = QCheckBox("Keep the analyze result")
        self.chkKeepAnalyze.setEnabled(False)

        #layoutAnalyzer
        self.layoutAnalyzerAnalyze.addWidget(self.btnAnalyzeAll)
        self.layoutAnalyzerAnalyze.addWidget(self.btnAnalyzeSelected)
        self.layoutAnalyzerAnalyze.addWidget(self.btnClearAnalyze)

        #layoutAnalyzerConfig
        self.layoutAnalyzerConfig.addWidget(self.chkKeepAnalyze)

        self.btnAnalyzeAll.clicked.connect(self.onAnalyzeAll)
        self.btnAnalyzeSelected.clicked.connect(self.onAnalyzeSelectedPaths)
        self.btnClearAnalyze.clicked.connect(self.onClearAnalyze)

        self.chkKeepAnalyze.toggled.connect(self.onClickedKeepResult)       

        self.layoutAnalyzer.addLayout(self.layoutAnalyzerAnalyze)
        self.layoutAnalyzer.addLayout(self.layoutAnalyzerConfig)

    def initMainLayout(self):
        self.mainLayout = QVBoxLayout()
        self.container = QWidget()

        #mainLayout
        self.mainLayout.addLayout(self.layoutPath)
        self.mainLayout.addLayout(self.layoutSelectedPath)
        self.mainLayout.addLayout(self.layoutAnalyzer)

        self.container.setLayout(self.mainLayout)
        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

        self.setWindowPosition()

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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

    def onAnalyzeSelectedPaths(self):
        paths = list()
        items = self.lstSelectedPath.selectedItems()
        for item in items:
            paths.append(item.text())
        self.analyzerLogic.analyzeAll(paths)

    def onAnalyzeAll(self):
        paths = list()
        for i in range(self.lstSelectedPath.count()):
            paths.append(self.lstSelectedPath.item(i).text())
        self.analyzerLogic.analyzeAll(paths)

    def onClearAnalyze(self):
        self.analyzerLogic.clear()     

    def onClickedKeepResult(self):
        self.analyzerLogic.setKeepResult( self.sender().isChecked())

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()