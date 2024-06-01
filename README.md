# CroppingFrames2Video
 動画データから指定したfps間隔でフレーム画像を切り出して保存する

## 環境構築
```
pip install -r requirements.txt
```

## 使用

###ディレクトリ内の動画データからフレームを切り出す
```
python video2img.py --dir_path ./result --video_path movie.mp4 --base_name sumple
```

### Youtubeの動画からフレームを切り出す
```
python video2img.py --youtube_url https://www.youtube.com/watch?v=xxxxxxxxxxx
```

### 指定オプション
|Option name|Discliption|Default|
|:--|:--|:--|
|--dir_path|保存するディレクトリを指定|./result|
|--base_name|画像ファイルの基本名|YYmmddHMS|
|--youtube_url|Youtube動画のURL||
|--video_path|動画データのパス||
|--fps|1秒あたりに切り出すフレーム数|30|
