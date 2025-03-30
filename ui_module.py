from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from recognition_module import single_classification
import datetime
import random


def get_current_season():
    month = datetime.datetime.now().month
    if 3 <= month <= 5:
        return 'spring'
    elif 6 <= month <= 8:
        return 'summer'
    elif 9 <= month <= 11:
        return 'autumn'
    else:
        return 'winter'


class Ui_MainWindow(object):
    def init(self):
        pass  # Removed redundant storage lists

    def ALL_PREDICT(self):
        try:
            # Allow multiple file selection and support multiple image formats
            files, _ = QFileDialog.getOpenFileNames(
                None, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            if not files:
                return

            for file in files:
                sub, info, res_place_holder = single_classification(file)
                item = QtWidgets.QListWidgetItem(info)
                item.setData(QtCore.Qt.UserRole, res_place_holder)

                if sub == "top":
                    self.TOP_LIST.addItem(item)
                elif sub == "bottom":
                    self.BOTTOM_LIST.addItem(item)
                elif sub == "foot":
                    self.SHOE_LIST.addItem(item)
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to process images: {str(e)}")

    # Generic list operations
    def handle_edit(self, list_widget, title):
        selected = list_widget.selectedItems()
        if not selected:
            QMessageBox.warning(None, "Warning", "Please select an item to edit.")
            return
        item = selected[0]
        text, ok = QtWidgets.QInputDialog.getText(
            None, "Edit", title,
            QtWidgets.QLineEdit.Normal, item.text()
        )
        if ok and text:
            item.setText(text)

    def handle_delete(self, list_widget):
        selected = list_widget.selectedItems()
        if not selected:
            QMessageBox.warning(None, "Warning", "Please select an item to delete.")
            return
        for item in selected:
            list_widget.takeItem(list_widget.row(item))

    # Top list operations
    def TOP_LIST_EDIT(self):
        self.handle_edit(self.TOP_LIST, "Edit Top Item:")

    def TOP_LIST_DEL(self):
        self.handle_delete(self.TOP_LIST)

    # Bottom list operations
    def BOTTOM_LIST_EDIT(self):
        self.handle_edit(self.BOTTOM_LIST, "Edit Bottom Item:")

    def BOTTOM_LIST_DEL(self):
        self.handle_delete(self.BOTTOM_LIST)

    # Shoe list operations
    def SHOE_LIST_EDIT(self):
        self.handle_edit(self.SHOE_LIST, "Edit Shoe Item:")

    def SHOE_LIST_DEL(self):
        self.handle_delete(self.SHOE_LIST)

    def Generate(self):
        # Check for empty categories
        if self.TOP_LIST.count() == 0 or self.BOTTOM_LIST.count() == 0 or self.SHOE_LIST.count() == 0:
            QMessageBox.warning(None, "Warning",
                                "Please add at least one item in each category before generating.")
            return

        # Get current season
        current_season = get_current_season()

        # Get all items with their data
        def get_category_items(list_widget):
            return [list_widget.item(i).data(QtCore.Qt.UserRole)
                    for i in range(list_widget.count())]

        tops = get_category_items(self.TOP_LIST)
        bottoms = get_category_items(self.BOTTOM_LIST)
        shoes = get_category_items(self.SHOE_LIST)

        # Filter by season
        seasonal_tops = [t for t in tops if t[3].lower() == current_season]
        top = random.choice(seasonal_tops if seasonal_tops else tops)

        # Find matching style
        matching_bottoms = [b for b in bottoms if b[4] == top[4]]
        bottom = random.choice(matching_bottoms if matching_bottoms else bottoms)

        matching_shoes = [s for s in shoes if s[4] == top[4]]
        shoe = random.choice(matching_shoes if matching_shoes else shoes)

        # Display results
        def set_image(label, path):
            pixmap = QtGui.QPixmap(path[-1]).scaled(281, 300)
            label.setPixmap(pixmap)

        set_image(self.listWidget_1, top)
        set_image(self.listWidget_2, bottom)
        set_image(self.listWidget_3, shoe)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 669)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # UI Elements setup
        self.TOP_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.TOP_LIST.setGeometry(QtCore.QRect(10, 30, 281, 181))
        self.TOP_LIST.setObjectName("TOP_LIST")

        self.AddTopButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddTopButton.setGeometry(QtCore.QRect(10, 210, 141, 41))
        self.AddTopButton.setObjectName("AddTopButton")

        self.DeleteTopButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteTopButton.setGeometry(QtCore.QRect(150, 210, 141, 41))
        self.DeleteTopButton.setObjectName("DeleteTopButton")

        self.BOTTOM_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.BOTTOM_LIST.setGeometry(QtCore.QRect(300, 30, 281, 181))
        self.BOTTOM_LIST.setObjectName("BOTTOM_LIST")

        self.AddBottomButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddBottomButton.setGeometry(QtCore.QRect(300, 210, 141, 41))
        self.AddBottomButton.setObjectName("AddBottomButton")

        self.DeleteBottomButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteBottomButton.setGeometry(QtCore.QRect(440, 210, 141, 41))
        self.DeleteBottomButton.setObjectName("DeleteBottomButton")

        self.SHOE_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.SHOE_LIST.setGeometry(QtCore.QRect(590, 30, 281, 181))
        self.SHOE_LIST.setObjectName("SHOE_LIST")

        self.AddShoeButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddShoeButton.setGeometry(QtCore.QRect(590, 210, 141, 41))
        self.AddShoeButton.setObjectName("AddShoeButton")

        self.DeleteShoeButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteShoeButton.setGeometry(QtCore.QRect(730, 210, 141, 41))
        self.DeleteShoeButton.setObjectName("DeleteShoeButton")

        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(440, 270, 431, 81))
        self.GenerateButton.setObjectName("GenerateButton")

        self.HistoryButton = QtWidgets.QPushButton(self.centralwidget)
        self.HistoryButton.setGeometry(QtCore.QRect(10, 270, 431, 81))
        self.HistoryButton.setObjectName("HistoryButton")

        self.TopLabel = QtWidgets.QLabel(self.centralwidget)
        self.TopLabel.setGeometry(QtCore.QRect(140, 10, 60, 16))
        self.TopLabel.setObjectName("TopLabel")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 10, 60, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(710, 10, 60, 16))
        self.label_2.setObjectName("label_2")

        self.listWidget_1 = QtWidgets.QLabel(self.centralwidget)
        self.listWidget_1.setGeometry(QtCore.QRect(10, 370, 281, 300))
        self.listWidget_1.setObjectName("listWidget_1")
        self.listWidget_1.setPixmap(QtGui.QPixmap("/Users/pingkefan/Desktop/top_question.png").scaled(281, 300))

        self.listWidget_2 = QtWidgets.QLabel(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(300, 370, 281, 300))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setPixmap(QtGui.QPixmap("/Users/pingkefan/Desktop/top_question.png").scaled(281, 300))

        self.listWidget_3 = QtWidgets.QLabel(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(590, 370, 281, 300))
        self.listWidget_3.setObjectName("listWidget_3")
        self.listWidget_3.setPixmap(QtGui.QPixmap("/Users/pingkefan/Desktop/top_question.png").scaled(281, 300))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 880, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect buttons to correct handlers
        self.AddTopButton.clicked.connect(self.TOP_LIST_EDIT)
        self.DeleteTopButton.clicked.connect(self.TOP_LIST_DEL)
        self.AddBottomButton.clicked.connect(self.BOTTOM_LIST_EDIT)
        self.DeleteBottomButton.clicked.connect(self.BOTTOM_LIST_DEL)
        self.AddShoeButton.clicked.connect(self.SHOE_LIST_EDIT)
        self.DeleteShoeButton.clicked.connect(self.SHOE_LIST_DEL)
        self.HistoryButton.clicked.connect(self.ALL_PREDICT)
        self.GenerateButton.clicked.connect(self.Generate)

    def retranslateUi(self, MainWindow):
        translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(translate("MainWindow", "Outfit Recommender"))
        self.AddTopButton.setText(translate("MainWindow", "EDIT"))
        self.DeleteTopButton.setText(translate("MainWindow", "DELETE"))
        self.AddBottomButton.setText(translate("MainWindow", "EDIT"))
        self.DeleteBottomButton.setText(translate("MainWindow", "DELETE"))
        self.AddShoeButton.setText(translate("MainWindow", "EDIT"))
        self.DeleteShoeButton.setText(translate("MainWindow", "DELETE"))
        self.GenerateButton.setText(translate("MainWindow", "Generate Today's Outfit Recommendation"))
        self.HistoryButton.setText(translate("MainWindow", "ADD PHOTOS"))
        self.TopLabel.setText(translate("MainWindow", "Top"))
        self.label.setText(translate("MainWindow", "Bottom"))
        self.label_2.setText(translate("MainWindow", "Shoes"))


def run_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

    # Custom stylesheet for improved UI
    style = """
    QMainWindow {
        background-color: #ff6347;
    }
    QListWidget {
        background-color: #0000ff;
        color: white;
        border: 1px solid #5a5a5a;
        border-radius: 5px;
    }
    QPushButton {
        background-color: #ffa500;
        color: white;
        border: 1px solid #404040;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #6a6a6a;
    }
    QLabel {
        color: white;
    }
    """
    app.setStyleSheet(style)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_ui()