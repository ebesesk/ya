from datetime import datetime
from pydantic import BaseModel
from typing import Union, Optional
from datetime import date 


class VideoItem(BaseModel):
    dbid:  Union[None, str] = None
    width: Union[None, int] = None
    height: Union[None, int] = None
    showtime: Union[None, int] = None
    bitrate: Union[None, int] = None
    filesize: Union[None, int] = None
    cdate: Union[None, date] = None
    
    display_quality:  Union[None, str] = None
    country:  Union[None, str] = None
    face:  Union[None, str] = None
    look:  Union[None, str] = None
    age:  Union[None, str] = None
    pussy:  Union[None, str] = None

    etc:  Union[None, str] = None

    school_uniform: Union[None, bool] = None
    hip: Union[None, bool] = None
    group: Union[None, bool] = None
    pregnant: Union[None, bool] = None
    conversation: Union[None, bool] = None
    lesbian: Union[None, bool] = None
    ani: Union[None, bool] = None
    oral: Union[None, bool] = None
    masturbation: Union[None, bool] = None
    massage: Union[None, bool] = None
    uniform: Union[None, bool] = None
    family: Union[None, bool] = None
    
    ad_start: Union[None, int] = None
    ad_finish: Union[None, int] = None
    star: Union[None, int] = None
    
    date_posted: Union[None, date] = None
    date_posted: Union[None, date] = None

    class Config:
        orm_mode = True


class CreateVideo(BaseModel):
    dbid:  Union[None, str] = None
    width: Union[None, int] = None
    height: Union[None, int] = None
    showtime: Union[None, int] = None
    bitrate: Union[None, int] = None
    filesize: Union[None, int] = None
    cdate: Union[None, date] = None
    
    # class Config:
    #     orm_mode = True


class UpdateVideo(BaseModel):
    dbid:  Union[None, str]
    display_quality:  Union[None, str]
    country:  Union[None, str]
    age:  Union[None, str]
    face:  Union[None, str]
    look:  Union[None, str]
    pussy:  Union[None, str]

    ad_start: Union[None, int] 
    ad_finish: Union[None, int] 
    star: Union[None, int] 

    school_uniform: Union[None, bool]
    hip: Union[None, bool]
    group: Union[None, bool]
    pregnant: Union[None, bool]
    conversation: Union[None, bool]
    lesbian: Union[None, bool]
    ani: Union[None, bool]
    oral: Union[None, bool]
    masturbation: Union[None, bool]
    massage: Union[None, bool]
    uniform: Union[None, bool]
    family: Union[None, bool]
    etc:  Union[None, str]


class SearchVideos(BaseModel):
    keyword: Optional[str] = None
    keyword_: Optional[str] = None
    keyword_not: Optional[bool] = False
    
    resolution1: Optional[str] = None
    resolution2: Optional[str] = None
    resolution3: Optional[str] = None
    
    country1: Optional[str] = None
    country2: Optional[str] = None
    country3: Optional[str] = None
    country4: Optional[str] = None
    country5: Optional[str] = None
    country_not: Optional[bool] = False
    
    age1: Optional[str] = None
    age2: Optional[str] = None
    age3: Optional[str] = None
    age4: Optional[str] = None
    age5: Optional[str] = None
    age_not: Optional[bool] = False
    
        
    face1: Optional[str] = None
    face2: Optional[str] = None
    face3: Optional[str] = None
    face_not: Optional[bool] = False
    
    look1: Optional[str] = None
    look2: Optional[str] = None
    look3: Optional[str] = None
    look4: Optional[str] = None
    look_not: Optional[bool] = False
    
    
    display_quality1: Optional[str] = None
    display_quality2: Optional[str] = None
    display_quality3: Optional[str] = None
    display_quality4: Optional[str] = None
    display_quality5: Optional[str] = None
    display_quality6: Optional[str] = None
    display_quality_not: Optional[bool] = False

    
    pussy1: Optional[str] = None
    pussy2: Optional[str] = None
    pussy3: Optional[str] = None
    pussy_not: Optional[bool] = False
    
    
    ad: Optional[bool] = None
    is_ad: Optional[bool] = False
    
    star: Optional[int] = None
    star_opt: Optional[bool] = False
    # ad_start: Optional[int] = None
    # ad_finish: Optional[int] = None
    

    school_uniform: Optional[bool] = None
    hip: Optional[bool] = None
    group: Optional[bool] = None
    pregnant: Optional[bool] = None
    conversation: Optional[bool] = None
    lesbian: Optional[bool] = None
    ani: Optional[bool] = None
    oral: Optional[bool] = None
    masturbation: Optional[bool] = None
    massage: Optional[bool] = None
    uniform: Optional[bool] = None
    family: Optional[bool] = None
    etc2_and: Optional[bool] = False
    
    not_school_uniform: Optional[bool] = None
    not_hip: Optional[bool] = None
    not_group: Optional[bool] = None
    not_pregnant: Optional[bool] = None
    not_conversation: Optional[bool] = None
    not_lesbian: Optional[bool] = None
    not_ani: Optional[bool] = None
    not_oral: Optional[bool] = None
    not_masturbation: Optional[bool] = None
    not_massage: Optional[bool] = None
    not_uniform: Optional[bool] = None
    not_family: Optional[bool] = None
    not_etc2_and: Optional[bool] = None
    
    