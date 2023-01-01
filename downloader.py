from __future__ import annotations
from enum import Enum
import abc
from dataclasses import dataclass


class DataType(Enum):
    MP4 = 'mp4'
    FLAC = 'flac'
    WAV = 'wav'
    MP3 = 'mp3'


class IDownloader(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'download') and callable(subclass.download)
            or NotImplemented
        )
    
    @abc.abstractmethod
    def download(self, data_type: DataType, url: str) -> Log_Message:
        pass


@IDownloader.register
class YouTubeDownloader(IDownloader):
    
    def download(self, data_type: DataType, url: str) -> Log_Message:

        success_msg = Log.success(f"Downloaded {data_type.value} from {url}.")
        
        if data_type == DataType.MP4:
            self._download_mp4(url)

            return success_msg
        elif data_type == DataType.FLAC:
            self._download_flac(url)

            return success_msg
        elif data_type == DataType.WAV:
            self._download_wav(url)

            return success_msg
        else:
            return Log.fail(f"Unable to download {data_type.value} from {url}.")


    def _get_out_file_title(self, out_file: str) -> str:
        return out_file.split('.')[0]


    def _get_normalized_file_name(self, file_name: str) -> str:
        old_name = file_name
        new_name = old_name

        if ascii(old_name) != old_name:
            import unicodedata

            new_name = ''.join(
                [unicodedata.normalize('NFD', i)[0] for i in list(old_name)]
            )
        
        return new_name

    
    def _normalize_file_name(self, file_name: str) -> str:
        old_name = file_name
        new_name = self._get_normalized_file_name(old_name)

        if old_name != new_name:        
            import os
            os.rename(old_name, new_name)
        
        return new_name

    
    def _get_current_year(self) -> str:
        from datetime import date

        return str(date.today().year)


    def _set_mp4_file_tags(self, file_name: str, url: str) -> None:
        from mutagen.mp4 import MP4
        from datetime import date

        file = MP4(file_name)

        mp4_keys = {
            "cmt": "\xa9cmt",
            "yr": "\xa9day",
            "title": "©nam"
        }    

        title = self._get_out_file_title(file_name)
        file[mp4_keys["title"]] = title

        file[mp4_keys["cmt"]] = url # https://mutagen.readthedocs.io/en/latest/api/mp4.html

        yr = self._get_current_year()
        file[mp4_keys["yr"]] = yr

        file.pprint()
        file.save()


    def _download_mp4(self, url: str, set_tags: bool = True, is_temp: bool = False) -> str:
        from pytube import YouTube
        import os
        from pyflac import FileEncoder
        from datetime import date

        yt = YouTube(url)
        
        highest_res_stream = yt.streams.get_highest_resolution()
        print(f"Highest resolution stream found: {highest_res_stream}")

        output_path = "." if not is_temp else r"temp"
        out_file = os.path.split(highest_res_stream.download(output_path=output_path))[-1]

        out_file = self._normalize_file_name(out_file)
        print(f"Normalized mp4 file name: {out_file}")

        if set_tags:
            self._set_mp4_file_tags(out_file, url)

        return out_file


    def _download_wav(self, url: str, is_temp: bool = False) -> str:
        out_file = f"temp\{self._download_mp4(url, set_tags=False, is_temp=True)}"

        import moviepy.editor as mp
        import os

        with mp.VideoFileClip(out_file) as file:
            wav_file = out_file.replace(u".mp4", u".wav")

            if not is_temp:
                wav_file = wav_file.replace("temp\\", "")
            
            file.audio.write_audiofile(wav_file)

        os.remove(f"{out_file}")

        return wav_file

    
    def _set_flac_file_tags(self, file_name: str, url: str) -> None:
        flac_file = file_name

        from mutagen.flac import FLAC
        
        file = FLAC(flac_file)
        
        title = self._get_out_file_title(file_name)
        file["title"] = title

        file["year"] = self._get_current_year()
        file["description"] = url
        
        file.pprint()
        file.save()


    def _download_flac(self, url: str, set_tags: bool = True) -> str:
        wav_file = self._download_wav(url, is_temp=True)

        flac_file = wav_file.replace(u".wav", u".flac").replace("temp\\", "")

        from pyflac import FileEncoder
        import os
    
        encoder = FileEncoder(input_file=wav_file, output_file=flac_file)
        encoder.process()

        os.remove(f"{wav_file}")

        if set_tags:
            self._set_flac_file_tags(flac_file, url)


if __name__ == "__main__":

    t = YouTubeDownloader()
    t.download(DataType.FLAC, 'abc')


class Log:
    _ok = "✅"
    _nok = "❌"

    @staticmethod
    def _get_function() -> str:
        import inspect
        try:
            return inspect.stack()[2].function
        except Exception as e:
            return f"Error while inspecting the stack: {e}"


    @staticmethod
    def _get_file_name() -> str:
        import inspect
        try:
            return inspect.stack()[2].filename
        except Exception as e:
            return f"Error while inspecting the stack: {e}"


    @staticmethod
    def _get_line_no() -> str:
        import inspect
        try:
            return inspect.stack()[2].lineno
        except Exception as e:
            return f"Error while inspecting the stack: {e}"
    

    @staticmethod
    def success(msg: str) -> Log_Message:
        return Log_Message(Log._ok, msg, Log._get_function(), Log._get_file_name(), Log._get_line_no())

    @staticmethod
    def fail(msg: str) -> Log_Message:
        return Log_Message(Log._nok, msg, Log._get_function(), Log._get_file_name(), Log._get_line_no())


@dataclass
class Log_Message:
    icon: str
    msg: str
    function: str
    file_name: str
    line_no: str


    def __str__(self):
        return f"{self.icon} {self.msg}"


    def __repr__(self):
        return f"""
{self.icon} {self.msg}
    See function `{self.function}` at `{self.file_name}`, line {self.line_no}
"""