from fastapi import  Depends
from sqlalchemy.orm import Session
import os, shutil
import sqlalchemy
from db.session import get_db
from db.repository import videos as videos_crud
from core.config import settings

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
            # print(' ' + dbid, '\n', _dbid, '\n', video, '\n', _video, '\n', gif, '\n', _gif, '\n', webp, '\n', _webp, '\n\n')
            # for i in videos_crud.get_dbid(dbid=dbid, db=db):
            # print((title+_suffix) in os.listdir(video_dir))
            # print(video)
            # print(os.listdir(video_dir))
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
                    print('rollback================================================================')
                    db.rollback()
                    raise
                except sqlalchemy.exc.IntegrityError:
                    # print(sqlalchemy.exc.IntegrityError, "-------")
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
            #     print(j, '--------------------------------------------')
                
    print('end')    
        
        
'''
 dbid  20210220/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn - SpankBang - .mp4.mp4 
_dbid  20210220/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn.mp4 
video  /home/yadong/20210220/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn - SpankBang - .mp4.mp4 
_video /home/yadong/20210220/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn.mp4 
gif    /home/yadong/20210220/gif/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn - SpankBang - .mp4.gif 
_gif   /home/yadong/20210220/gif/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn.gif 
webp   /home/yadong/20210220/webp/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn - SpankBang - .mp4.webp 
_webp  /home/yadong/20210220/webp/Watch         - Japanese Uncensored Japanese Game Show Japanese College Japanese Groop Japanese Porn.webp 


# '''