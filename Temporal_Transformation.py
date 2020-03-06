import numpy as np
import skvideo.io
import glob
import cv2
import sys

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

def UpSample(video_name, new_frames):
    """
    フレーム数を増やす
    引数：
        video_name->ビデオファイル名
        new_frames->新しいフレーム数
    """
    
    now_frames = GetFrames(video_name)
    if now_frames > new_frames:
        print("UpSampleを使う場合、now_framesの方がnew_framesより大きくないといけません。")
        sys.exit()
    video = ReadVideo(video_name)
    index_list = [int(i) for i in np.linspace(1, now_frames, num=new_frames)]

    return np.array([video[i-1] for i in index_list])

def DownSample(video_name, new_frames):
    """
    フレーム数を減らす
    引数：
        video_name->ビデオファイル名
        new_frames->新しいフレーム数
    """
    
    now_frames = GetFrames(video_name)
    if now_frames < new_frames:
        print("DownSampleを使う場合、new_framesの方がnow_framesより大きくないといけません。")
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
    print(video.shape)
    out = cv2.VideoWriter(video_name, format, 20.0, (video.shape[2],video.shape[1]))
    frames = video.shape[0]
    print("framesは、", frames)
    for i in range(frames):
        frame = video[i][:,:,::-1]
        print(frame.shape)
        out.write(frame)
    out.release()

video_list = glob.glob("/Users/mori/Desktop/all_cut/*.mp4")
print(ReadVideo(video_list[0]).shape)
video = UpSample(video_list[0], 100)
print(video.shape)
SaveVideo(video, "upsampled_video.mp4")
SaveVideo(ReadVideo(video_list[0]), "video.mp4")
