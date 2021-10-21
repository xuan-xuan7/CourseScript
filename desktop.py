from PyQt5.QtWidgets import QApplication, QWidget


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        # self.initUI()  # 界面绘制交给InitUi方法

    # def initUI(self):
    #     self.desktop = QApplication.desktop()
    #
    #     # 获取显示器分辨率大小
    #     self.screenRect = self.desktop.screenGeometry()
    #     self.height = self.screenRect.height()
    #     self.width = self.screenRect.width()
    #
    #     print(self.height)
    #     print(self.width)
    #
    #     # 显示窗口
    #     # self.show()


app = QApplication([])
ex = Example()


