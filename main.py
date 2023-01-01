from view_model import ViewModel
from downloader import YouTubeDownloader


if __name__ == "__main__":
    
    vm = ViewModel(
        downloader=YouTubeDownloader()
    )

