from ast import keyword
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import videos
from sqlalchemy import or_, and_, not_
from sqlalchemy.sql import func
from typing import Dict
from datetime import datetime

from core.config import settings
from db.models.videos import Video

def get_test2(db: Session):
    return db.query(Video).filter(Video.dbid.like('%' + 'test2/' + '%')).all()

def get_etcall(db: Session):
    return db.query(Video.etc).filter(and_(Video.etc != None, Video.etc != 'None', Video.etc != ' ')).all()

def get_all_videos(db: Session):
    return db.query(Video).all()

def get_all_dbid(db: Session):
    return db.query(Video.dbid).all()

def get_all_videos_random(db: Session):
    return db.query(Video).order_by(func.random()).all()

def create_new_video(video: videos.CreateVideo, db: Session):
    from pprint import pprint
    # pprint(video)
    video = Video(**video)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video



def get_all_choice(db: Session):
    return db.query(Video).filter(Video.date_modified != None).all()

def get_all_choice_random(db: Session):
    return db.query(Video).filter(Video.date_modified != None).order_by(func.random()).all()


def get_all_nys(db: Session):
    return db.query(Video).filter(Video.date_modified == None).all()

def get_all_nys_random(db: Session):
    return db.query(Video).filter(Video.date_modified == None).order_by(func.random()).all()


def update_video(q: Dict, db: Session):
    
    video = db.query(Video).filter(Video.dbid == q['dbid'])
    if not video.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Video with id{q["dbid"]} not found')
    q.update({"date_modified": datetime.now()})
    video.update(q)
    db.commit()
    return 'update is completed'


def del_video_dbid(dbid: str, db: Session):
    video = db.query(Video).filter(Video.dbid == dbid)
    if not video.first():
        return f'db 없음  {dbid}'
    video.delete(synchronize_session=False)
    db.commit()
    return dbid


def get_video_query(query, db:Session):
    return set(db.query(Video).filter(query).all())
    # return query.all()



def search_videos(query: Dict, db: Session):
    RESOLUTION_HIGHT = settings.RESOLUTION_HIGHT
    RESOLUTION_LOW = settings.RESOLUTION_LOW

    # print(query)
    try:
        query['keyword'] = (query['keyword'].strip()).split()
    except AttributeError as e:
        pass
    def clean_query(query):
        query_copy = query.copy()
        for key in query_copy.keys():
            if type(query[key]) is list:
                query[key] = list(set(query[key]))
                try:
                    query[key].remove(None)
                except ValueError as e:
                    pass
                if len(query[key]) == 0:
                    del query[key]
            if query_copy[key] == None:
                del query[key]
        return query

    # print(clean_query(query))
    query = clean_query(query)
    # print('222222222\n' ,query)
    
    


    
    
    videos_and = []
    videos_or = []
    videos = None

    try:
        resolution = []
        for key in query.keys():
            if 'resolution' in key:
                if query[key] == 'high':
                    resolution.append(
                        (Video.width * Video.height) > RESOLUTION_HIGHT,
                        )
                elif query[key] == 'middle':
                    resolution.append(
                        ((Video.width * Video.height) <= RESOLUTION_HIGHT) & ((Video.width * Video.height) >= RESOLUTION_LOW),
                        )
                elif query[key] == 'low':
                    resolution.append(
                        (Video.width * Video.height) < RESOLUTION_LOW,
                        )
        resolution = or_(*resolution)
        
        if type(videos) is type(None):
            videos = resolution
        else:
            videos = and_(videos, resolution)
            
            
    except KeyError as e:
        pass






    try:
        if query['country_not'] == False:
            country = []
            for key in query.keys():
                if key in ['country1', 'country2', 'country3', 'country4', 'country5']:
                    country.append(Video.country == query[key])
            
            country = or_(*country)
            if type(videos) is type(None):
                videos = country
            else:
                videos = and_(videos, country)
            
        if query['country_not'] == True:
            country = []
            for key in query.keys():
                if key in ['country1', 'country2', 'country3', 'country4', 'country5']:
                    country.append(Video.country.isnot(query[key]))
            
            country = and_(*country)
            if type(videos) is type(None):
                videos = country
            else:
                videos = and_(videos, country)
            
    
    except KeyError as e:
        pass



    try:
        if query['age_not'] == False:
            age = []
            for key in query.keys():
                if key in ['age1', 'age2', 'age3', 'age4', 'age5']:
                    age.append(Video.age == query[key])
                    
            age = or_(*age)
            if type(videos) is type(None):
                videos = age
            else:
                videos = and_(videos, age)    
                
        if query['age_not'] == True:
            age = []
            for key in query.keys():
                if key in ['age1', 'age2', 'age3', 'age4', 'age5']:
                    age.append(Video.age.isnot(query[key]))
                    
            age = and_(*age)
            if type(videos) is type(None):
                videos = age
            else:
                videos = and_(videos, age)
                
    except KeyError as e:
        pass



    try:
        if query['face_not'] == False:
            face = []
            for key in query.keys():
                if key in ['face1', 'face2']:
                    face.append(Video.face == query[key])
                    
            face = or_(*face)
            if type(videos) is type(None):
                videos = face
            else:
                videos = and_(videos, face)
        if query['face_not'] == True:
            face = []
            for key in query.keys():
                if key in ['face1', 'face2']:
                    face.append(Video.face.isnot(query[key]))
                    
            face = and_(*face)
            if type(videos) is type(None):
                videos = face
            else:
                videos = and_(videos, face)
    except KeyError as e:
        pass



    try:
        if query['look_not'] == False:
            look = []
            for key in query.keys():
                if key in ['look1', 'look2', 'look3']:
                    look.append(Video.look == query[key])
            look = or_(*look)
            if type(videos) is type(None):
                videos = look
            else:
                videos = and_(videos, look)
        if query['look_not'] == True:
            look = []
            for key in query.keys():
                if key in ['look1', 'look2', 'look3']:
                    look.append(Video.look.isnot(query[key]))
            look = and_(*look)
            if type(videos) is type(None):
                videos = look
            else:
                videos = and_(videos, look)
    except KeyError as e:
        pass






    try:
        if query['display_quality_not'] == False:
            display_quality = []
            for key in query.keys():
                if key in ['display_quality1', 'display_quality2', 'display_quality3', 'display_quality4', 'display_quality5']:
                    display_quality.append(Video.display_quality == query[key])
            
            display_quality = or_(*display_quality)
            if type(videos) is type(None):
                videos = display_quality
            else:
                videos = and_(videos, display_quality)
        
        if query['display_quality_not'] == True:
            display_quality = []
            for key in query.keys():
                if key in ['display_quality1', 'display_quality2', 'display_quality3', 'display_quality4', 'display_quality5']:
                    display_quality.append(Video.display_quality.isnot(query[key]))
            
            display_quality = and_(*display_quality)
            if type(videos) is type(None):
                videos = display_quality
            else:
                videos = and_(videos, display_quality)
                
    except KeyError as e:
        pass



    try:
        if query['pussy_not'] == False:
            pussy = []
            for key in query.keys():
                if key in ['pussy1', 'pussy2']:
                    pussy.append(Video.pussy == query[key])
            
            pussy = or_(*pussy)
            if type(videos) is type(None):
                videos = pussy
            else:
                videos = and_(videos, pussy)
        
        if query['pussy_not'] == True:
            pussy = []
            for key in query.keys():
                if key in ['pussy1', 'pussy2']:
                    pussy.append(Video.pussy.isnot(query[key]))
            
            pussy = and_(*pussy)
            if type(videos) is type(None):
                videos = pussy
            else:
                videos = and_(videos, pussy)
                
    except KeyError as e:
        pass



    try:
        if query['ad'] == True:
            ad = or_(Video.ad_start != None, Video.ad_start != "None",Video.ad_finish != None, Video.ad_finish != "None",)
            
            if type(videos) == type(None):
                videos = ad
            else:
                videos = and_(videos, ad)
    
    except KeyError as e:
        pass






    try:
        if query['star_opt'] == True:
            star = Video.star >= query['star']
        else:
            star = Video.star == query['star']
            # star = or_(Video.star != None, Video.star != "None")
        if type(videos) == type(None):
            videos = star
        else:
            videos = and_(videos, star)
    except KeyError as e:
        pass



    etc2 = []
    try:
        if query['school_uniform'] == True:
            etc2.append(Video.school_uniform == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['hip'] == True:
            etc2.append(Video.hip == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['group'] == True:
            etc2.append(Video.group == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['pregnant'] == True:
            etc2.append(Video.pregnant == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['conversation'] == True:
            etc2.append(Video.conversation == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['lesbian'] == True:
            etc2.append(Video.lesbian == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['ani'] == True:
            etc2.append(Video.ani == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['oral'] == True:
            etc2.append(Video.oral == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['masturbation'] == True:
            etc2.append(Video.masturbation == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['massage'] == True:
            print(query['massage'])
            etc2.append(Video.massage == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['uniform'] == True:
            etc2.append(Video.uniform == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['family'] == True:
            etc2.append(Video.family == True)
        pass
    except KeyError as e:
        pass


    try:
        if query['etc2_and'] == True:
            if type(videos) == type(None):
                videos = and_(*etc2)
            else:
                videos = and_(videos, and_(*etc2))
        elif query['etc2_and'] == False:
            if type(videos) == type(None):
                videos = or_(*etc2)
            else:
                videos = and_(videos, or_(*etc2))
    except KeyError:
        pass
    #####################################################################



    etc2_not = []
    try:
        if query['not_school_uniform'] == True:
            etc2_not.append(or_(Video.school_uniform.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_hip'] == True:
            etc2_not.append(or_(Video.hip.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_group'] == True:
            etc2_not.append(or_(Video.group.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_pregnant'] == True:
            etc2_not.append(or_(Video.pregnant.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_conversation'] == True:
            etc2_not.append(or_(Video.conversation.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_lesbian'] == True:
            etc2_not.append(or_(Video.lesbian.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_ani'] == True:
            etc2_not.append(or_(Video.ani.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_oral'] == True:
            etc2_not.append(or_(Video.oral.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_masturbation'] == True:
            etc2_not.append(or_(Video.masturbation.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_massage'] == True:
            etc2_not.append(or_(Video.massage.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_uniform'] == True:
            etc2_not.append(or_(Video.uniform.isnot(True)))
        pass
    except KeyError as e:
        pass


    try:
        if query['not_family'] == True:
            etc2_not.append(or_(Video.family.isnot(True)))
        pass
    except KeyError as e:
        pass



    if type(videos) == type(None):
        videos = and_(*etc2_not)
    else:
        videos = and_(videos, and_(*etc2_not))
        
    #####################################################################


    try:
        keyword = []
        if query['keyword_not'] == False:
            if query['keyword_'] == 'or':
                for q in query['keyword']:
                    if (q != None) and (q != 'None'):
                        keyword.append(Video.etc.like('%'+q+'%'))
                        keyword.append(Video.dbid.like('%'+q+'%'))
                keyword = or_(*keyword)
                
                if type(videos) is None:
                    videos = keyword
                else:
                    videos = or_(videos, keyword)
                
            if query['keyword_'] == 'and':
                for q in query['keyword']:
                    if (q != None) and (q != 'None'):
                        keyword.append(Video.etc.like('%'+q+'%'))
                        keyword.append(Video.dbid.like('%'+q+'%'))
                keyword = or_(*keyword)
                
                if type(videos) is None:
                    videos = keyword
                else:
                    videos = and_(videos, keyword)
            
            
            
        if query['keyword_not'] == True:
            if query['keyword_'] == 'or':
                for q in query['keyword']:
                    if (q != None) and (q != 'None'):
                        keyword.append(Video.etc.notlike('%'+q+'%'))
                        keyword.append(Video.dbid.notlike('%'+q+'%'))
                keyword = or_(*keyword)
                if type(videos) is None:
                    videos = keyword
                else:
                    videos = or_(videos, keyword)
                
            if query['keyword_'] == 'and':
                for q in query['keyword']:
                    if (q != None) and (q != 'None'):
                        keyword.append(Video.etc.notlike('%'+q+'%'))
                        keyword.append(Video.dbid.notlike('%'+q+'%'))
                keyword = or_(*keyword)
                if type(videos) is None:
                    # print(videos, '+++++++++++++++++++++++')
                    videos = keyword
                else:
                    videos = and_(videos, keyword)
    except KeyError:
        pass
    
        
        
        
        
        
    
    # print('===============================')
    # print('len(videos): ', len(videos))
    # if type(videos) is list:
    #     for i, j in enumerate(and_(*videos)):
    #         print(i, '====', j)
    # print(and_(*videos))
    
    # if len(videos) > 0:
    #     for i, j in enumerate(videos):
    #         print(str(i).zfill(2), j)
    # print(videos)
    

    # if len(videos) == 1:
    #     return get_video_query(and_(videos[0]), db)
    # elif len(videos) > 1:
    #     return get_video_query(and_(*videos), db)
    # else:
    #     return get_video_query(and_(*videos), db)
    return get_video_query(videos, db)