from __future__ import unicode_literals
import asyncio
from asyncio import subprocess

# pip install pyqt5
# pip install pyqt5-tools
# pyuic5 -x .\gui.ui -o view.py

# designer.exe localization
# C:\repos\yt_download\venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe

def change_encoding(input: str) -> str:
    return ''.join(
        [chr(i) for i in list(
            input.encode('utf-8')
        )]
    )


def normalize_file_name(file: str) -> str:
    
    old_name = file
    new_name = old_name

    if ascii(old_name) != old_name:
        import unicodedata

        new_name = ''.join(
            [unicodedata.normalize('NFD', i)[0] for i in list(old_name)]
        )
    
        import os
        os.rename(old_name, new_name)
    
    return new_name


def download(url: str, convert_to_flac: bool = True) -> None:
    from pytube import YouTube
    import moviepy.editor as mp
    import os, stat
    # from pydub import AudioSegment
    from pyflac import FileEncoder
    from datetime import date

    yt = YouTube(url)
    
    res = yt.streams.get_highest_resolution()

    print(res)

    out_file = os.path.split(res.download(output_path="."))[-1]

    title = out_file.split('.')[0]

    out_file = normalize_file_name(out_file)

    print(out_file)

    from mutagen.mp4 import MP4
    file = MP4(out_file)
    mp4_keys = {
        "cmt": "\xa9cmt",
        "yr": "\xa9day",
        "title": "©nam"
    }    
    file[mp4_keys["title"]] = title
    file[mp4_keys["cmt"]] = url # https://mutagen.readthedocs.io/en/latest/api/mp4.html
    yr = str(date.today().year)
    file[mp4_keys["yr"]] = yr
    file.pprint()
    file.save()

    # {'©nam': ['Hands A Dublin Bookbinder'], '©day': ['2022'], '©cmt': ['https://www.youtube.com/watch?v=RBd67qQy96k'], '©wrt': ['composer1/composer2'], 'tmpo': [0], '©gen': ['genre'], '©ART': ['contributin artist1/artist2']}
    # {'©day': ['2022'], 'titl': ['Hands A Dublin Bookbinder.mp4'], '©cmt': ['https://www.youtube.com/watch?v=RBd67qQy96k'], '©nam': ['title']}

    if convert_to_flac:
        with mp.VideoFileClip(out_file) as file:
            wav_file = out_file.replace(u".mp4", u".wav")
            # wav_file = out_file.replace(u".mp4", u".mp3")
            
            file.audio.write_audiofile(wav_file)

        os.remove(out_file)

        flac_file = wav_file.replace(u".wav", u".flac")
       
        encoder = FileEncoder(input_file=wav_file, output_file=flac_file)
        encoder.process()

        os.remove(wav_file)

        

        from mutagen.flac import FLAC
        file = FLAC(flac_file)
        file["title"] = title
        file["year"] = yr
        file["description"] = url
        file.pprint()
        file.save()

        # {'year': ['2022'], 'mood': ['mood'], 'conductor': ['conductor'], 'genre': ['genre'], 'tracknumber': ['10'], 'organization': ['publisher'], 'encoder': ['encoded by'], 'artist': ['contributing artists1', 'artist2'], 'publisher': ['https://www.youtube.com/watch?v=dUrkYc4Z9yk'], 'albumartist': ['album artist'], 'composer': ['composer1', 'composer2'], 'title': ['Front Mission 4 OST - Track 19 - Deserters.flac'], 'album': ['album'], 'discnumber': ['part of set'], 'description': ['This is comment here.']}

        # import music_tag
        # file = music_tag.load_file(flac_file)
        # file['title'] = flac_file
        # file['year'] = yr
        # file['composer'] = url
        # file.save()
        # see documentation: https://pypi.org/project/music-tag/

    # from pydub import AudioSegment
    # AudioSegment.ffmpeg = r"C:\repos\yt_download\venv\Lib\site-packages\ffmpeg"    
    # AudioSegment.converter = r"C:\repos\yt_download\venv\Lib\site-packages\ffmpeg"    

    # file = AudioSegment.from_file(wav_file, format="wav")    
    # file.export("res.mp3", format="mp3")
    # os.remove(wav_file)
    

if __name__ == "__main__":
    data = [
        ("https://www.youtube.com/watch?v=dUrkYc4Z9yk", True ),
        ("https://www.youtube.com/watch?v=RBd67qQy96k", False),
        ("https://www.youtube.com/watch?v=ZjKyQ7cUlO8", False),
        ("https://www.youtube.com/watch?v=BTYzAtj6auM", True ),
        ("https://www.youtube.com/watch?v=yJ_H28GoaCs", True ),
        ("https://www.youtube.com/watch?v=u-q1GIxqv6g", True ),
        ("https://www.youtube.com/watch?v=u-q1GIxqv6g", False),
        ("https://www.youtube.com/watch?v=BycXfQS-Ipg", True ),

        ("https://www.youtube.com/watch?v=A1EmGAAmy34&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs", True ),
        ("https://www.youtube.com/watch?v=f7xPpmlx0Ls&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=2", True),
        ("https://www.youtube.com/watch?v=PVH2txpwQiQ", True),
        ("https://www.youtube.com/watch?v=wnlt8p0ZQ5c&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=4", True),
        ("https://www.youtube.com/watch?v=KgwcXTdPTV0&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=5", True),
        ("https://www.youtube.com/watch?v=1ZKyCKU1PCQ&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=6", True),
        ("https://www.youtube.com/watch?v=SlKefLTiwgk&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=7", True),
        ("https://www.youtube.com/watch?v=ZIvwNbN1xCc&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=8", True),
        ("https://www.youtube.com/watch?v=L6quam3cEaE&list=PLzpHvgk6ivsF5V26YebvWad_VSZ8JpPGs&index=9", True),
        ("https://www.youtube.com/watch?v=GnWIvSyvStg", False),
        ("https://www.youtube.com/watch?v=MJenceQ9IEw", True),
        ("https://www.youtube.com/watch?v=VXwuWgI6IS8", True),
        ("https://www.youtube.com/watch?v=2zBYVO42Mkw&t=1253s", True),
        ("https://www.youtube.com/watch?v=9ejpkedAxLU", False),
        ("https://www.youtube.com/watch?v=2zBYVO42Mkw&t=1253s", True),
        ("https://www.youtube.com/watch?v=8dnbKWS-1Zc", True),
        ("https://www.youtube.com/watch?v=jxFD4__XQ7k", True),
        ("https://www.youtube.com/watch?v=jxFD4__XQ7k", False),
        ("https://www.youtube.com/watch?v=Dj6kcpys_Tg", True),
        ("https://www.youtube.com/watch?v=Dj6kcpys_Tg", False),
        ("https://www.youtube.com/watch?v=bwoasXzLdVY", True),
        ("https://www.youtube.com/watch?v=Lbs7cUuk9z4", True),
        ("https://www.youtube.com/watch?v=VN9RqDImNgM", True),
        ("https://www.youtube.com/watch?v=bV-hSgL1R74", True),
        ("https://www.youtube.com/watch?v=bV-hSgL1R74", False),
        ("https://www.youtube.com/watch?v=1KzJFJZYGM8", True),
        ("https://www.youtube.com/watch?v=1yLUIjAsuY0", True),
        ("https://www.youtube.com/watch?v=sNrJFKPiZi0", True),
    ]

    # path = r"https://www.youtube.com/watch?v=dUrkYc4Z9yk"
    # # path = r"https://www.youtube.com/watch?v=RBd67qQy96k"
    # path = r"https://www.youtube.com/watch?v=BTYzAtj6auM"
    # path = r"https://www.youtube.com/watch?v=yJ_H28GoaCs"
    # path = r"https://www.youtube.com/watch?v=u-q1GIxqv6g"
    # path = r"https://www.youtube.com/watch?v=ZjKyQ7cUlO8"
    # download(*data[-1])

    from downloader import YouTubeDownloader, DataType

    yt = YouTubeDownloader()
    msg = yt.download(DataType.MP4, data[-1][0])
    msg = yt.download(DataType.WAV, data[-1][0])
    msg = yt.download(DataType.FLAC, data[-1][0])
    print(f"{msg}")