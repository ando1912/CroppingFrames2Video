import cv2
import os
import argparse
from yt_dlp import YoutubeDL
import urllib.parse
import datetime
import re

def pick_up_vid_list(url):
    pattern_watch = 'https://www.youtube.com/watch?'
    pattern_short = 'https://youtu.be/'

    # 通常URLのとき
    if re.match(pattern_watch,url):
        yturl_qs = urllib.parse.urlparse(url).query
        vid = urllib.parse.parse_qs(yturl_qs)['v'][0]

    # 短縮URLのとき
    elif re.match(pattern_short,url):
        # "https://youtu.be/"に続く11文字が動画ID
        vid = url[17:28]

    else:
        print('error:\n  URLは\"https://www.youtube.com/watch?\"か')
        print('  \"https://youtu.be/\"で始まるURLを指定してください。')
    return vid

class Video2IMG:
    def __init__(self):
        self.cap = ""
        self.youtube_url = ""
        self.video_path = ""
        self.dir_path = ""
        self.basename = ""
        self.ext = "jpg"
        self.fps = 30

    def download_youtube(self):
        if self.youtube_url == "":
            print("ERROR: NOT URL")
            return
        ydl_opts = {
            "format": "best",
            'outtmpl':'%(id)s.%(ext)s',
            "paths": {
                "home": "video"
            }
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtube_url])
        
        id = pick_up_vid_list(self.youtube_url)
        self.basename = id
        # print(f"filepath = ./{ydl_opts['paths']['home']}/{id}.mp4")
        
        # self.video_path =  os.path.join(f"./{ydl_opts['paths']['home']}", f"{id}.mp4")
        self.video_path = f"./{ydl_opts['paths']['home']}/{id}.mp4"
        
        self.read_video()
        # self.cap = cv2.VideoCapture(f"./{ydl_opts['paths']['home']}/{id}.mp4")

    def read_video(self):
        if self.video_path == "":
            print("ERROR: not video_path")
            return
        print(f"video_path = {self.video_path}")
        self.cap = cv2.VideoCapture(self.video_path)

    def save_all_frames(self):

        if not self.cap.isOpened():
            print("CAP is NONE")
            return

        os.makedirs(self.dir_path, exist_ok=True)
        os.makedirs(os.path.join(self.dir_path,self.basename), exist_ok=True)

        if self.basename is None:
            self.basename = os.path.splitext(os.path.basename(self.video_path))[0]
        # base_path = os.path.join(self.dir_path, self.basename)

        digit = len(str(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))))

        thresh = self.cap.get(cv2.CAP_PROP_FPS) / self.fps #フレーム何枚につき1枚処理するか

        n = 0
        frame_counter = 0

        total_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while True:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)
            ret, frame = self.cap.read()

            if not ret:
                break

            cv2.imwrite('{}/{}/{}_{}.{}'.format(self.dir_path, self.basename, self.basename, str(frame_counter).zfill(digit), self.ext), frame)
            print(f"\rframe_count:{str(frame_counter).zfill(digit)}/{total_frame}", end="")

            frame_counter += int(thresh)

if __name__=="__main__":

    now = datetime.datetime.now()
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--dir_path", help="The path of the directory to save", default="./result")
    parser.add_argument("--base_name", help="The basename of the file to save", default=now.strftime("%YY%mm%dd%H%M%S"))
    parser.add_argument("--youtube_url")
    parser.add_argument("--video_path")
    parser.add_argument("--fps", type=int, default=30)

    # オプション値の取得
    arg = parser.parse_args()

    savevideo = Video2IMG()

    savevideo.dir_path = arg.dir_path
    savevideo.basename = arg.base_name

    if arg.video_path is not None:
        savevideo.video_path = arg.video_path
        savevideo.read_video()
    if arg.youtube_url is not None:
        savevideo.youtube_url = arg.youtube_url
        savevideo.download_youtube()

    savevideo.fps = arg.fps

    savevideo.save_all_frames()