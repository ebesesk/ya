from pprint import pprint
from sqlalchemy.orm import Session
from sqlalchemy import or_
import os
import ffmpeg
import integv
from PIL import Image
import cv2
from pathlib import Path
import subprocess
from pprint import pprint
from datetime import datetime
# import shutil 

from fastapi import  Depends
# from sqlalchemy.orm import Session
import os, shutil
import sqlalchemy
from db.session import get_db
from db.repository import videos as videos_crud
# from core.config import settings


from db.repository.videos import del_video_dbid, get_all_dbid, create_new_video
from core.config import settings
from db.models.videos import Video
from schemas.videos import CreateVideo

ROOT_DIR: str = settings.ROOT_DIR   # "/home/yadong/"
TEMP_DIR: str = settings.TEMP_DIR   # "/home/temp/"
WASTE_DIR: str = settings.WASTE_DIR # "_waste/"
GIF: str = settings.GIF             # "gif/"
WEBP: str = settings.WEBP           # "webp/"
FRAME_MIN = settings.FRAME_MIN
FRAME_MAX = settings.FRAME_MAX
GIF_SIZE = settings.GIF_SIZE



def print_dict(d):
    l = 0
    for k in d.keys():
        if len(k) > l:
            l = len(k)
    print('-'.center(l*2,'-'))
    for k in d.keys():
        print(k.ljust(l, ' '), ': ', d[k])
    print('-'.center(l*2, '-'))

def get_dbid(suf):  # suf = 하위디렉토리 없으면 '', 있으면 '/gif/'
    ids = []
    for x in os.listdir(ROOT_DIR):
        if os.path.isdir(os.path.join(ROOT_DIR, x)):
            waste = WASTE_DIR.replace('/','')
            if (x != waste):
                try:
                    for y in os.listdir(os.path.join(ROOT_DIR + x + suf)):
                        if ('.' in y) & (y != '@eaDir') & (y != 'Thumbs.db'):
                            ids.append(x + '/' + suf[1:] + y)
                except FileNotFoundError as e:
                    os.mkdir(ROOT_DIR + x + suf)
                    pass
    return ids


def split_file_name(file_name):
    stem = file_name[file_name.rfind('/')+1:file_name.rfind('.')]
    suffix = file_name[file_name.rfind('.')+1:]
    name = stem + '.' + suffix
    _dir = file_name.replace(name, '')
    return {'dir': _dir, 'name':name, 'stem': stem, 'suffix': suffix}


def count_gif_frame(showtime):
    if  FRAME_MIN > (showtime / 120):
        return FRAME_MIN
    elif  FRAME_MAX < (showtime / 120):
        return FRAME_MAX
    else:
        return int(showtime / 120)




def get_vmeta_ffmpeg(src):
    print(src)
    try:
        vmeta = ffmpeg.probe(src)
    except ffmpeg._run.Error:
        dest = ROOT_DIR + WASTE_DIR + src[src.rfind('/')+1:]
        # shutil.move(src, dest)
        return "not video file"
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




def count_dir_size():
    def get_dir_size(_dir):
        total = 0
        for d in _dir:
            total += os.path.getsize(ROOT_DIR+d)
        return total
    
    videos = get_dbid('')
    gif = get_dbid('/'+ GIF)
    webp = get_dbid('/'+ WEBP)
    videos_size = get_dir_size(videos)
    gif_size = get_dir_size(gif)
    webp_size = get_dir_size(webp)
    videos_size = f'{videos_size:,}'
    gif_size = f'{gif_size:,}'
    webp_size = f'{webp_size:,}'
    
    return {
        'videos': videos_size,
        'gif': gif_size,
        'webp': webp_size,  
    }




def cnv_gifpath(dbid):
    p = Path(dbid)
    return ROOT_DIR / p.parent / GIF / (p.stem + '.gif')



def cnv_webppath(dbid):
    p = Path(dbid)
    return ROOT_DIR / p.parent / WEBP / (p.stem + '.webp')





def del_gif(dbid):
    p = Path(dbid)
    src = ROOT_DIR / p.parent / GIF / (p.stem + '.gif')
    dest = ROOT_DIR + WASTE_DIR + p.stem + '.gif'
    # print('gif_src  :' ,src)
    # print('gif_dest: ', dest)
    if src.is_file():
        shutil.move(src, dest)
        return src
    else:
        return f'파일 없음  {src}'

    
def del_webp(dbid):
    p = Path(dbid)
    src = ROOT_DIR / p.parent / WEBP / (p.stem + '.webp')
    dest = ROOT_DIR + WASTE_DIR + p.stem + '.webp'
    # print('webp_src: ', src)
    # print("webp_dest: ", dest)
    if src.is_file():
        shutil.move(src, dest)
        return src
    else:
        return f'파일 없음  {src}'

def del_viedo(dbid):
    p = Path(dbid)
    src = Path(ROOT_DIR + dbid)
    dest = ROOT_DIR + WASTE_DIR + p.name
    # print('src  :' ,src)
    # print('dest: ', dest)
    # print(src.is_file())
    if src.is_file():
        shutil.move(src, dest)
        return src
    else:
        return f'파일 없음  {src}'


def cut_filename_len(db: Session = Depends(get_db)):
    # db.rollback()
    # videos = videos_crud.get_all_videos(db)
    dbid = [i.dbid for i in videos_crud.get_all_videos(db)]
    # print(dbid)
    videos = [settings.ROOT_DIR + i.dbid for i in videos_crud.get_all_videos(db)]
    gifs = []
    webps = []
    # print(dbid)
    j = 0
    for i in dbid:
        # print(i)
        title = i[i.find('/')+1:i.rfind('.')]
        # print(_prepix, '     ', title, '     ', _suffix, '     ', i)
        if len(title) > 100:
            j = j + 1
            print(j, '======================')
            _suffix = i[i.rfind('.'):]
            _prepix = i[:i.find('/')+1]
            # print(title, '\n', i, '\n', _suffix)
            # dbid = i
            # video = settings.ROOT_DIR + i
            dbid = i
            _dbid = _prepix + title[:100] + _suffix
            video = settings.ROOT_DIR + _prepix + title + _suffix
            _video = settings.ROOT_DIR + _prepix + title[:100] + _suffix
            video_dir = settings.ROOT_DIR + _prepix
            gif = settings.ROOT_DIR + _prepix + settings.GIF + title + '.gif'
            _gif = settings.ROOT_DIR + _prepix + settings.GIF + title[:100] + '.gif'
            gif_dir = settings.ROOT_DIR + _prepix + settings.GIF
            webp = settings.ROOT_DIR + _prepix + settings.WEBP + title + '.webp'
            _webp = settings.ROOT_DIR + _prepix + settings.WEBP + title[:100] + '.webp'
            webp_dir =settings.ROOT_DIR + _prepix + settings.WEBP
            if ((title+_suffix) in os.listdir(video_dir)) and ((title+'.gif')in os.listdir(gif_dir)) and ((title+'.webp')in os.listdir(webp_dir)):
                try:
                    print(' dbid' + dbid, '\n_dbid', _dbid, '\nvideo', video, '\n_video', _video, '\ngif', gif, '\n_gif', _gif, '\nwebp', webp, '\n_webp', _webp, '\n\n')
                    print(j)
                    n = videos_crud.update_dbid(dbid_0=dbid, dbid_1=_dbid, db=db)
                    print(n.dbid)
                    shutil.move(video, _video)
                    shutil.move(gif, _gif)
                    shutil.move(webp, _webp)
                except sqlalchemy.exc.PendingRollbackError:
                    db.rollback()
                    raise
                except sqlalchemy.exc.IntegrityError:
                    dbid = i
                    _dbid = _prepix + title[:97] + '1' + _suffix
                    video = settings.ROOT_DIR + _prepix + title + _suffix
                    _video = settings.ROOT_DIR + _prepix + title[:97] + '1' + _suffix
                    video_dir = settings.ROOT_DIR + _prepix
                    gif = settings.ROOT_DIR + _prepix + settings.GIF + title + '.gif'
                    _gif = settings.ROOT_DIR + _prepix + settings.GIF + title[:97] + '1' + '.gif'
                    gif_dir = settings.ROOT_DIR + _prepix + settings.GIF
                    webp = settings.ROOT_DIR + _prepix + settings.WEBP + title + '.webp'
                    _webp = settings.ROOT_DIR + _prepix + settings.WEBP + title[:97] + '1' + '.webp'
                    webp_dir =settings.ROOT_DIR + _prepix + settings.WEBP
                    n = videos_crud.update_dbid(dbid_0=dbid, dbid_1=_dbid, db=db)
                    print(n.dbid)
                    shutil.move(video, _video)
                    shutil.move(gif, _gif)
                    shutil.move(webp, _webp)
                    break
    print('end')    





def refix_video(db:Session = Depends(get_db)):
    
    cut_filename_len(db)
    
    videos = get_dbid('')
    _videos = [i[:i.rfind('.')] for i in videos]
    gif_videos = get_dbid('/' + GIF)
    _gif_videos = [i[:i.rfind('.')].replace(GIF, '') for i in gif_videos]
    webp_videos = get_dbid('/' + WEBP)
    _webp_videos = [i[:i.rfind('.')].replace(WEBP, '') for i in webp_videos]
    # db_videos = [i[0] for i in db.query(Video.dbid).all()]
    db_videos = [i[0] for i in get_all_dbid(db)]

    del_gifs = [i.replace('/', '/'+GIF) + '.gif' for i in list(set(_gif_videos)-set(_videos)) if 'Thumbs' not in i]
    del_webps = [i.replace('/', '/'+WEBP) + '.webp' for i in list(set(_webp_videos)-set(_videos)) if 'Thumbs' not in i]
    del_dbs = list(set(db_videos) - set(videos))

    if len(del_dbs) > 0:
        for i in del_dbs:
            del_video_dbid(dbid=i, db=db)
    wastes = []
    for i in del_gifs:
        wastes.append(del_gif(i))
    for i in del_webps:
        wastes.append(del_webp(i))

    add_gif = [i for i in list(set(_videos)-set(_gif_videos)) if 'Thumbs' not in i]
    add_webp = [i for i in list(set(_videos)-set(_webp_videos)) if 'Thumbs' not in i]
    add_gif = [videos[_videos.index(i)] for i in add_gif]
    add_webp = [videos[_videos.index(i)] for i in add_webp]
    add_db = list(set(videos) - set(db_videos))
    
    print(len(set(_gif_videos)))
    print(len(set(_videos)))
    print(set(_videos)-set(_gif_videos))
    for dbid in add_db:
        if Path(dbid).suffix == '.ts':
            print(dbid)
            cnv_tsTomp4(dbid)
            refix_video(db)
    
    add_gifs = []
    add_webps = []
    add_dbs = []

    corrupted = []
    OverflowErrors = []
    NotImplementedErrors = []
    FileNotFoundErrors = []
    webp_faile = []
    gif_faile = []

    for i in list(set(add_gif + add_webp + add_db)):
        src = ROOT_DIR +i
        print(src)
        suffix = split_file_name(src)['suffix']
        chk_video = check_err_integv(src, suffix)
        if chk_video == False:
            corrupted.append(src)
            shutil.move(src, ROOT_DIR + WASTE_DIR + split_file_name(src)['name'])
            print(src, 'chk_video chk_video chk_video chk_video chk_video')
            continue
        if chk_video == 'integv OverflowError':
            OverflowErrors.append(src)
            shutil.move(src, ROOT_DIR + WASTE_DIR + split_file_name(src)['name'])
            print(src, 'integv OverflowError')
            continue
        if chk_video == 'integv NotImplementedError':
            NotImplementedErrors.append(src)
            pass
        if chk_video == 'integv FileNotFoundError':
            FileNotFoundErrors.append(src)
            continue
        vmeta = get_vmeta_ffmpeg(src)
        if vmeta == 'not video file':
            continue
        if i in add_gif:
        # if (i in add_gif) and (os.path.isfile(src)):
            try:
                os.mkdir(split_file_name(src)['dir'] + GIF)
            except:
                pass
            n = count_gif_frame(vmeta['showtime'])
            cut_times = [int((vmeta['showtime'] - i*vmeta['showtime']/n)-vmeta['showtime']/(2*n)) for i in range(n)]
            cut_times.sort()
            dest = split_file_name(src)['dir'] + GIF + split_file_name(src)['stem'] + '.gif'
            [os.remove(TEMP_DIR + f) for f in os.listdir(TEMP_DIR) if not os.path.isdir(TEMP_DIR + f)]
            if vmeta['width'] >= vmeta['height']:
                gif = make_gif(src, dest, cut_times)
            else:
                gif = make_rotate_gif(src, dest, cut_times)
            if gif == False:
                gif_faile.append(src)
            else:
                add_gifs.append(cnv_gifpath(src))


        if i in add_webp:
            try:
                os.mkdir(split_file_name(src)['dir'] + WEBP)
            except:
                pass
            cut_time = vmeta['showtime']/2
            dest = split_file_name(src)['dir'] + WEBP + split_file_name(src)['stem'] + '.webp'
            if vmeta['width'] >= vmeta['height']:
                w = make_webp(src, dest, cut_time)
            else:
                w = make_rotate_webp(src, dest, cut_time)
            if w == False:
                # shutil.move(src, ROOT_DIR + WASTE_DIR + split_file_name(src)['name'])
                webp_faile.append(src)
            else:
                add_webps.append(cnv_webppath(src))

        if i in add_db:
            try:
                video = {
                    'dbid': i,
                    'width': vmeta['width'],
                    'height': vmeta['height'],
                    'showtime': vmeta['showtime'],
                    'bitrate': vmeta['bitrate'],
                    'filesize': vmeta['size'],
                    'cdate': vmeta['cdate'],
                    'date_posted': datetime.now().date(),
                }
            except KeyError:
                video = {
                    'dbid': i,
                    'width': vmeta['width'],
                    'height': vmeta['height'],
                    'showtime': vmeta['showtime'],
                    'bitrate': vmeta['bitrate'],
                    'filesize': vmeta['size'],
                    'date_posted': datetime.now().date(),
                }
            # video = CreateVideo(**video)
            # pprint(video)
            create_new_video(video=video, db=db)
            # video = Video(
            #     dbid = i,
            #     width = vmeta['width'],
            #     height = vmeta['height'],
            #     showtime = vmeta['showtime'],
            #     bitrate = vmeta['bitrate'],
            #     filesize = vmeta['size'],
            #     date_posted = datetime.now().date(),
            # )
            # db.add(video)
            # db.commit()
            # # db.rollback()
            add_dbs.append(i)
    file_size = count_dir_size()
    
    return {
        'videos': {'cnt': f'{len(videos):,}', 'size': file_size['videos']},
        'gif': {'cnt': f'{len(gif_videos):,}', 'size': file_size['gif']},
        'webp': {'cnt': f'{len(webp_videos):,}', 'size': file_size['webp']},
        'db': len(db.query(Video).all()),
        'add': {'add_gif': add_gifs,'add_webp': add_webps,'add_db': add_dbs,},
        'delete': {'wastes': wastes, 'del_db': del_dbs,},
        'integv_error': {
            'corrupted': corrupted,
            'OverflowError': OverflowErrors,
            'NotImplementedError': NotImplementedErrors,
            'FileNotFoundError': FileNotFoundErrors,
        },
        'opencv_error': {
            'webp_faile': webp_faile,
            'gif_faile': gif_faile,
        }
    }


