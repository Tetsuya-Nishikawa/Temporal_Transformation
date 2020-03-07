import numpy as np
import skvideo.io
import cv2
import sys
import imutils

def ReadVideo(video_name):
    """
    ビデオを取得する
    引数：
        video_name->ビデオファイル名
    """
    return skvideo.io.vread(video_name)

def GetFrames(video_name):
    """
    フレーム数を取得する
    引数:
        video_name->ビデオファイル名
    """
    video = ReadVideo(video_name)
    return video.shape[0]

def IncreaseFrames(video_name, new_frames):
    """
    フレーム数を増やす
    引数：
        video_name->ビデオファイル名
        new_frames->新しいフレーム数
    """
    
    now_frames = GetFrames(video_name)
    if now_frames > new_frames:
        print("IncreaseFramesを使う場合、new_framesの方がnow_framesより大きくないといけません。")
        sys.exit()
    video = ReadVideo(video_name)
    index_list = [int(i) for i in np.linspace(1, now_frames, num=new_frames)]

    return np.array([video[i-1] for i in index_list])

def DecreaseFrames(video_name, new_frames):
    """
    フレーム数を減らす
    引数：
        video_name->ビデオファイル名
        new_frames->新しいフレーム数
    """
    
    now_frames = GetFrames(video_name)
    if now_frames < new_frames:
        print("DecreaseFramesを使う場合、now_framesの方がnew_framesより大きくないといけません。")
        sys.exit()
    video = ReadVideo(video_name)
    index_list = [int(i) for i in np.linspace(1, now_frames, num=new_frames)]

    return np.array([video[i-1] for i in index_list])


def SaveVideo(video, video_name):
    """
    ビデオの保存をする
    引数：
        video->ビデオ
        video_name->ビデオファイル名
    """
    format = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_name, format, 20.0, (video.shape[2],video.shape[1]))
    frames = video.shape[0]
    for i in range(frames):
        frame = video[i][:,:,::-1]
        out.write(frame)
    out.release()

#これはいつか使いそうなので、追加してみた。
def ResizeVideo(video):
    """
    ビデオをリサイズする
    引数:
        video->ビデオ
    """
    frames = video.shape[0]
    new_video = []
    for frame in video:
        new_frame = imutils.resize(frame, width=200)
        new_video.append(new_frame)

    return np.array(new_video)

if __name__ == '__main__':
    input_path = "./video/001_008_005.mp4"
    output_path = "./video/sampled_video.mp4"

    #sampled_video = IncreaseFrames(input_path, 100)
    sampled_video = ResizeVideo(ReadVideo(input_path))
    SaveVideo(sampled_video, output_path)
