
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout,  QWidget, QMessageBox
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
        self.setWindowTitle("SELinux-Explorer " + APP_VERSION)
        self.initVariables()
        self.initMainLayout()
        self.configSignals()
        self.loadSetting()

    def initVariables(self):
        self.analyzerLogic = AnalyzerLogic()
        self.appSetting = AppSetting()
        self.settingUtil = SettingClass()

    def loadSetting(self):
        if os.path.isfile("app_setting.json"):
            json_str = FileReader().readFile("app_setting.json")
            self.appSetting = AppSetting.from_json(json_str) 
            self.layoutPath.lastOpenedPath = self.appSetting.lastOpenedPath
            self.toolbar.keepResult = self.appSetting.keepTheResult
            self.layoutFilter.setSelectedFilterType(self.appSetting.selectedFilterType)
            print("AppSetting loaded!")
        else:
            self.saveSetting()

    def saveSetting(self):
        self.appSetting.lastOpenedPath = self.layoutPath.lastOpenedPath
        self.appSetting.keepTheResult = self.toolbar.keepResult
        self.appSetting.selectedFilterType = self.layoutFilter.getSelectedFilterType()


        FileWriter().writeFile("app_setting.json", self.appSetting.to_json())
        print("AppSetting saved!")

    def initMainLayout(self):
        self.layoutPath = FileUi(self)
        self.layoutFilter = FilterUi(self, self.analyzerLogic)
        self.layoutResult = ResultUi(self, self.analyzerLogic)
        self.layoutAnalyzerResult = AnalyzerResultUi(self, self.analyzerLogic)
        self.toolbar = ToolbarUi(self, self.analyzerLogic, self.appSetting)
        self.statusbar = StatusbarUi(self, self.analyzerLogic)
        self.mainLayoutLeft = QVBoxLayout()
        self.mainLayoutRight = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.container = QWidget()


        self.mainLayoutLeft.addLayout(self.layoutPath)
        self.mainLayoutLeft.addLayout(self.layoutResult)
        self.mainLayout.addLayout(self.mainLayoutLeft)
        self.mainLayout.addLayout(self.mainLayoutRight)

        self.mainLayoutRight.addLayout(self.layoutAnalyzerResult)
        self.mainLayoutRight.addLayout(self.layoutFilter)

        self.container.setLayout(self.mainLayout)
        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.setStatusBar(self.statusbar)

        self.setWindowPosition()

        appIcon = QIcon()
        appIcon.addFile(ICON_PATH + 'icon_16.png', QSize(16,16))
        appIcon.addFile(ICON_PATH + 'icon_24.png', QSize(24,24))
        appIcon.addFile(ICON_PATH + 'icon_32.png', QSize(32,32))
        appIcon.addFile(ICON_PATH + 'icon_64.png', QSize(64,64))
        appIcon.addFile(ICON_PATH + 'icon_256.png', QSize(256,256))
        self.setWindowIcon(appIcon)


    def configSignals(self):
        self.toolbar.connectToGetSelectedPaths( self.layoutPath.getSelectedPaths)
        self.toolbar.connectToGetAllPaths( self.layoutPath.getAllPaths)
        self.toolbar.connectOnAddFileFolder( self.layoutPath.onAddFileFolder)
        self.layoutAnalyzerResult.connectToFilterUi( self.layoutFilter.onGetFilter)

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def disposeObjects(self):
        self.layoutResult.onDispose()

    def closeEvent(self,event):
            result = QMessageBox().question(self,
                        "Confirm Exit...",
                        "Are you sure you want to exit ?",
                        QMessageBox.Yes| QMessageBox.No)
            event.ignore()

            if result == QMessageBox.Yes:
                self.saveSetting()
                self.disposeObjects()
                event.accept()

