import os
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QFileDialog, QVBoxLayout
from PyQt6.QtCore import Qt
import time

app = QApplication([])

class Window(QMainWindow):
      selectedFolders = []
      foldersList = ""
      widgetPlaced = False
      def __init__(self): 
            super().__init__()
            #set up basic window and layout
            self.setWindowTitle("Home Backup")
            self.setMinimumSize(300, 200)
            self.centerWidget = QWidget()
            self.layout = QVBoxLayout()
            #create widgets
            self.backupButton = QPushButton("Backup Files") #backup button widget
            self.addFolderButton = QPushButton("Add Folder") #add folder widget
            self.destFolderButton = QPushButton("Set Destination Folder")
            self.folderListWidget = QLabel("No folders yet")
            #add widgets to layout
            self.layout.addWidget(self.addFolderButton)
            self.layout.addWidget(self.destFolderButton)
            self.layout.addWidget(self.backupButton)
            self.layout.addWidget(self.folderListWidget, alignment=Qt.AlignmentFlag.AlignLeft)
            #add the layout to the window
            self.centerWidget.setLayout(self.layout)
            self.setCentralWidget(self.centerWidget)
            self.layout.setSpacing(0)            
            #connect button to event handler
            self.addFolderButton.clicked.connect(self.folderDialogClickHandler)
            self.destFolderButton.clicked.connect(self.destDialogClickHandler)
            self.backupButton.clicked.connect(self.backupButtonClickHandler)

            self.layout.setSpacing(1)
      def folderDialogClickHandler(self):
            folderDialog = QFileDialog()
            folderDialog.setFileMode(QFileDialog.FileMode.Directory)
            successful = folderDialog.exec()

            
            if successful:
                  folder = str(folderDialog.selectedFiles())
                  if len(self.foldersList) > 0:
                        self.foldersList = str(self.foldersList + ", " + folder[2:-2])
                  else:
                        self.foldersList = str(folder[2:-2])
                  
                  #print(folder[1:-1])
                  
                  self.selectedFolders.append(folder[1:-1])
                  self.layout.removeWidget(self.folderListWidget)
                  self.folderListWidget = QLabel(self.foldersList)
                  self.layout.addWidget(self.folderListWidget)

                  #print(self.selectedFolders)
      def destDialogClickHandler(self):
            self.destFolder = ""
            destDialog = QFileDialog()
            destDialog.setFileMode(QFileDialog.FileMode.Directory)
            destSuccessful = destDialog.exec()
            
            if destSuccessful:
                  self.destFolder = str(destDialog.selectedFiles())[1:-1]
                  self.destFolderButton.setText(self.destFolder)
                  #print(self.destFolder)
      def backupButtonClickHandler(self):
            self.backupButton.setText("Backing Up Files")
            foldersLen = len(self.selectedFolders)
            count = 0
            if self.selectedFolders == []:
                  self.backupButton.setText("No folders were selected.")
            elif self.destFolder == "":
                  self.backupButton.setText("Destination wasn't selected.")
            else: 
                  while count < foldersLen:
                        print(self.selectedFolders[count])
                        print(f"cp -r {self.selectedFolders[count]} {self.destFolder}")
                        os.system(f"cp -r {self.selectedFolders[count]} {self.destFolder}")
                        count = count + 1
                  self.backupButton.setText("Done.")
            time.sleep(1)
            self.backupButton.setText("Backup Files")     
window = Window()
window.show()
app.exec()