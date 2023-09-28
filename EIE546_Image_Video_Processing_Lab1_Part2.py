#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2023-2024 The Hong Kong Polytechnic University All Rights Reserved 
#
# @Supervisor : Dr. WANG Yi
# @Contributor: Mr. YAO Lei
# Department of Electronic and Information Engineering

import os
import cv2
import yaml
import time
import numpy as np


def read_video_config(file='video.yaml'):
    """Read the configuration file of the image.
    
    Args:
        file: the path of the configuration file.
    Returns:
        raw_file: the path of the raw image file.
        width: the width of the image.
        height: the height of the image.
        frame_rate: the frame rate of the video.
        n_frames: the number of frames of the video.
    """
    with open(file, 'r') as f:
        cfg = yaml.safe_load(f)

    file_size = os.path.getsize(cfg['InputFile'])
    n_frames = file_size // (cfg['Width'] * cfg['Height'] * 3 // 2)

    print("== Configuration File =================================\n")
    print(" Input File   : ", cfg['InputFile'])
    print(" Width        : ", cfg['Width'])
    print(" Height       : ", cfg['Height'])
    print(" Frame Rate   : ", cfg['FrameRate'])
    print(" Frame Number : ", n_frames)
    print("=======================================================\n")
    
    return cfg['InputFile'], cfg['Width'], cfg['Height'], cfg['FrameRate'], n_frames

def yuv2bgr(yuv):
    """Convert the image from YUV format to BGR format.

    Args:
        yuv: the image in YUV format.

    Returns:
        bgr: the image in BGR format.
    """
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
    return bgr

def play_video(raw_file, n_frames, width, height, sleep_time = 0):
    """Play the video.

    Args:
        raw_file: the path of the raw video file.
        n_frames: the number of frames of the video.
        width: the width of the video.
        height: the height of the video.
        sleep_time: the time interval between two frames.

    Returns:
        None
    """
    f = open(raw_file, 'rb')

    for i in range(n_frames):
        source_time = time.time()
        yuv = np.frombuffer(f.read(width * height * 3 // 2), dtype=np.uint8)
        print('t_source: ', time.time() - source_time)

        process_time = time.time()
        yuv = yuv.reshape((int(height * 3 / 2), width))
        bgr = yuv2bgr(yuv)
        print('t_process: ', time.time() - process_time)

        display_time = time.time()
        # cv2.imwrite('results/bgr_{}.png'.format(i), bgr)
        cv2.imshow("video", bgr)
        cv2.waitKey(1) # ms
        print('t_display: ', time.time() - display_time)

        time_elapse = time.time() - source_time
        print('time_elapse: ', time_elapse)

        time.sleep(sleep_time) # s
    
    cv2.destroyAllWindows()
    print("\n Finished playback.\n")
    
def seek_video(raw_file, n_frames, width, height):
    """Seek the video.

    Args:
        raw_file: the path of the raw video file.
        n_frames: the number of frames of the video.
        width: the width of the video.
        height: the height of the video.

    Returns:
        None
    """
    seek_frame = input("\n Please enter the [Frame Number] : ")
    seek_frame = int(seek_frame)
    
    f = open(raw_file, 'rb')
    bgr_list= []
    for _ in range(n_frames):
        yuv = np.frombuffer(f.read(width * height * 3 // 2), dtype=np.uint8)
        yuv = yuv.reshape((int(height * 3 / 2), width))
        bgr_list.append(yuv2bgr(yuv))

    if seek_frame >= n_frames:
        print("\n Seek frame should be smaller than maximum frame number.\n")
        return
    # cv2.imwrite('results/bgr_{}.png'.format(seek_frame), bgr_list[seek_frame])
    cv2.imshow('frame_{}'.format(seek_frame), bgr_list[seek_frame])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def play_from_seek_video(raw_file, n_frames, width, height, sleep_time = 0):
    """Play the video from the seek frame.

    Args:
        raw_file: the path of the raw video file.
        n_frames: the number of frames of the video.
        width: the width of the video.
        height: the height of the video.
        sleep_time: the time interval between two frames.

    Returns:
        None
    """
    seek_frame = input("\n Please enter the [Frame Number] : ")
    seek_frame = int(seek_frame)

    f = open(raw_file, 'rb')

    bgr_list = []
    for _ in range(n_frames):
        yuv = np.frombuffer(f.read(width * height * 3 // 2), dtype=np.uint8)

        yuv = yuv.reshape((int(height * 3 / 2), width))
        bgr_list.append(yuv2bgr(yuv))
    
    for i in range(seek_frame, n_frames):
        # cv2.imwrite('results/bgr_{}.png'.format(i), bgr_list[i])
        cv2.imshow('from frame_{}'.format(seek_frame), bgr_list[i])
        cv2.waitKey(1)
        time.sleep(sleep_time)
    
    cv2.destroyAllWindows()
    print("\n Finished play from {}.\n".format(seek_frame))

def play_pause_video(raw_file, n_frames, width, height, sleep_time = 0):
    """Play the video from the seek frame.

    Args:
        raw_file: the path of the raw video file.
        n_frames: the number of frames of the video.
        width: the width of the video.
        height: the height of the video.
        sleep_time: the time interval between two frames.

    Returns:
        None
    """

    f = open(raw_file, 'rb')

    bgr_list = []
    for _ in range(n_frames):
        yuv = np.frombuffer(f.read(width * height * 3 // 2), dtype=np.uint8)

        yuv = yuv.reshape((int(height * 3 / 2), width))
        bgr_list.append(yuv2bgr(yuv))
    
    
    for i in range(n_frames):
        # cv2.imwrite('results/bgr_{}.png'.format(i), bgr_list[i])
        cv2.imshow("Play and Pause", bgr_list[i])
        k = cv2.waitKey(30)
        if k == ord(' '): 
            cv2.waitKey(0)
            print("current timestamp: ", i)

        if k == 27:
            break
        time.sleep(sleep_time)

    print("\n Finished play.\n")


def menu(raw_file, n_frames, width, height, sleep_time = 0):
    """Menu of the video player.

    Args:
        raw_file: the path of the raw video file.
        n_frames: the number of frames of the video.
        width: the width of the video.
        height: the height of the video.
        sleep_time: the time interval between two frames.

    Returns:
        None
    """
    while True:
        print("Menu: [p] play, [s] seek, [q] quit \n")
        command = input("Please enter the [player command]  : ")
        
        if command == 'p':
            print("Displaying the video.")
            play_video(raw_file, n_frames, width, height, sleep_time = 0.01)
        elif command == 's':
            play_from_seek_video(raw_file, n_frames, width, height, sleep_time = 0.01)
            # seek_video(raw_file, n_frames, width, height)
        elif command == 'q':
            print("QUIT!")
            break
        else:
            print("\nINCORRECT player command.\n\n")
    

if __name__ == '__main__':

    raw_file, width, height, fp, n_frames = read_video_config(file='video.yaml')

    # play_video(raw_file, n_frames, width, height, sleep_time = 0.05) # e.g. 0.1, 0.01
    # menu(raw_file, n_frames, width, height)
    # seek_video(raw_file, n_frames, width, height)
    # play_from_seek_video(raw_file, n_frames, width, height)
    # play_pause_video(raw_file, n_frames, width, height)
    
