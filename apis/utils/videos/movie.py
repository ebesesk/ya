import os
import ffmpeg
import integv
from PIL import Image
import cv2
import subprocess
from datetime import datetime
from pathlib import Path
from fastapi import Header
from core.config import settings

ROOT_DIR: str = settings.ROOT_DIR   # "/home/yadong/"
TEMP_DIR: str = settings.TEMP_DIR   # "/home/temp/"
WASTE_DIR: str = settings.WASTE_DIR # "_waste/"
GIF: str = settings.GIF             # "gif/"
WEBP: str = settings.WEBP           # "webp/"
FRAME_MIN = settings.FRAME_MIN
FRAME_MAX = settings.FRAME_MAX
GIF_SIZE = settings.GIF_SIZE
CHUNK_SIZE = settings.CHUNK_SIZE


def get_vmeta_ffmpeg(src):
    vmeta = ffmpeg.probe(src)
    # pprint(vmeta)
    bitrate = vmeta['format']['bit_rate']
    duration = vmeta['format']['duration']
    filesize = vmeta['format']['size']
    try:
        width = vmeta['streams'][0]['coded_width']
        height = vmeta['streams'][0]['coded_height']
    except:
        width = vmeta['streams'][1]['coded_width']
        height = vmeta['streams'][1]['coded_height']
    try:
        date = vmeta['format']['tags']['creation_time']
        date = date[:date.rfind('.')].replace('T', ' ')
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except:
        return ({
            # '파일명': src, 
            'width': int(width),
            'height': int(height),
            'showtime': int(round(float(duration),0)),
            'bitrate': int(bitrate),
            'size': int(filesize),
            })
    
    return ({
            # '파일명': file_name, 
            'width': int(width),
            'height': int(height),
            'showtime': int(round(float(duration),0)),
            'bitrate': int(bitrate),
            'size': int(filesize),
            'cdate': date,
            })


def check_err_integv(src, suffix):
    try:
        return integv.verify(src, suffix)
    except OverflowError as e:
        # print('OverflowError: ', src)
        return 'OverflowError'
    except NotImplementedError as e:
        # print(e)
        # print('NotImplementedError: ', src)
        return 'NotImplementedError'
    except FileNotFoundError as e:
        # print(e)
        # print( 'FileNotFoundError: ' ,src)
        return 'FileNotFoundError'        


def make_gif(src, dest, cut_times):
    vidcap =cv2.VideoCapture(src)
    imgs = []
    for i, cut_time in enumerate(cut_times):
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        if fps == 1:
            return 'Image file'
        vidcap.set(cv2.CAP_PROP_POS_MSEC, cut_time*1000)
        success, image = vidcap.read()
        if success == False:
            return False
        if success:
            if image.shape[1] > GIF_SIZE:
                image = cv2.resize(image, (GIF_SIZE, int(GIF_SIZE*image.shape[0]/image.shape[1])))
            filename = TEMP_DIR + str(i).zfill(2) + '.png'
            cv2.imwrite(filename, image)
            imgs.append(filename)
    vidcap.release()
    imgs = [Image.open(f) for f in imgs]
    frame_one = imgs[0]
    frame_one.save(dest, format='GIF', append_images=imgs,
                   save_all=True, duration=500, loop=0)
    return dest


def make_webp(src, dest, cut_time):
    vidcap = cv2.VideoCapture(src)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, cut_time*1000)
    success, image = vidcap.read()
    if success == False:
        return False
    if success:
        if image.shape[1] > GIF_SIZE:
            image = cv2.resize(image, (GIF_SIZE, int(GIF_SIZE*image.shape[0]/image.shape[1])))
        cv2.imwrite(dest, image)
        vidcap.release()


def make_rotate_webp(src, dest, cut_time):
    vidcap = cv2.VideoCapture(src)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, cut_time*1000)
    success, image = vidcap.read()
    # print('success', success)
    print(src)
    if success == False:
        return False
    if success:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        if image.shape[1] > GIF_SIZE:
            image = cv2.resize(image, (GIF_SIZE, int(GIF_SIZE*image.shape[0]/image.shape[1])))
        cv2.imwrite(dest, image)
        vidcap.release()


def make_rotate_gif(src, dest, cut_times):
    vidcap =cv2.VideoCapture(src)
    imgs = []
    for i, cut_time in enumerate(cut_times):
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        if fps == 1:
            return 'Image file'
        vidcap.set(cv2.CAP_PROP_POS_MSEC, cut_time*1000)
        success, image = vidcap.read()
        if success == False:
            return False
        if success:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            if image.shape[1] > GIF_SIZE:
                image = cv2.resize(image, (GIF_SIZE, int(GIF_SIZE*image.shape[0]/image.shape[1])))
            filename = TEMP_DIR + str(i).zfill(2) + '.png'
            cv2.imwrite(filename, image)
            imgs.append(filename)
    vidcap.release()
    imgs = [Image.open(f) for f in imgs]
    frame_one = imgs[0]
    frame_one.save(dest, format='GIF', append_images=imgs,
                   save_all=True, duration=500, loop=0)
    return dest


def cnv_tsTomp4(dbid):
    _ts = ROOT_DIR + dbid
    _mp4 = ROOT_DIR + dbid[:dbid.rfind('.')] + '.mp4'
    command = f'ffmpeg -i {_ts} -acodec copy -vcodec copy {_mp4}'
    # print(_ts,'      ===========')
    # print(_mp4,'     ===========')
    # print(command)
    subprocess.run(['ffmpeg', '-y', '-i',  _ts, '-acodec', 'copy', '-vcodec', 'copy', _mp4])
    os.remove(_ts)
    return f'{_ts} -> {_mp4} completed'


