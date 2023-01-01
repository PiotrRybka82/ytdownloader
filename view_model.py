from __future__ import annotations
from PyQt5 import QtWidgets
from view import Ui_MainWindow
from downloader import IDownloader, DataType
import sys


class ViewModel:

    def __init__(self, downloader: IDownloader) -> None:

        self.downloader = downloader

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self.add_logic()
        
        MainWindow.show()
        
        sys.exit(app.exec_())


    def add_logic(self) -> None:
        
        self.ui.btn_download.clicked.connect(self.download_handler)


    def get_selected_data_type(self) -> DataType:
        if self.ui.rad_flac.isChecked(): 
            return DataType.FLAC

        if self.ui.rad_mp4.isChecked():
            return DataType.MP4

        if self.ui.rad_wav.isChecked():
            return DataType.WAV


    def get_urls(self) -> list[str]:
        
        urls = self.ui.inp_url.toPlainText()
        
        if not urls:
            return []
        
        import re
        urls = re.split(",|\n", urls)
        urls = filter(lambda item: item, urls)
        urls = list(urls)

        return urls


    def update_input(self) -> None:
        pass


    def update_output(self, msg: str) -> None:
        content = self.ui.out_result_log.toPlainText().split('\n')
        content.append(msg)
        self.ui.out_result_log.setPlainText('\n'.join(content))


    def download_handler(self) -> None:
        urls = self.get_urls()
        data_type = self.get_selected_data_type()

        for url in urls:
            try:
                log_msg = self.downloader.download(data_type, url).__str__()

                self.update_output(log_msg)
            except Exception as e:
                self.update_input("❌Error")


#     # def __init_ui(self):
#     #     self.lbl_url = QtWidgets.QLabel(self)
#     #     self.lbl_url.setText("URL:")
#     #     self.lbl_url.move(50, 50)

#     #     self.btn_download = QtWidgets.QPushButton(self)
#     #     self.btn_download.setText("⤵️Download")
#     #     self.btn_download.move(50, 80)
#     #     self.btn_download.clicked.connect(self.download)


#     # def update(self):
#     #     self.lbl_url.adjustSize()


#     # def download(self):
#     #     print("It's alive!")
#     #     # self.lbl_url.setText("ups!")
#     #     self.update()


# # def window():
#     # app = QApplication(sys.argv)
#     # win = Window()

#     # win.show()
#     # sys.exit(app.exec_())

if __name__ == "__main__":
    from downloader import YouTubeDownloader
    ViewModel(YouTubeDownloader())