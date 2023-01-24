from core.config import settings
from db.repository.videos import get_etcall


ROOT_DIR = settings.ROOT_DIR        #   /home/yadong/
WASTE_DIR = settings.WASTE_DIR      #   _waste/
GIF = settings.GIF                  #   gif/"
WEBP = settings.WEBP                #   webp/
PAGE = settings.PAGE                # 10
_PAGESIZE = settings._PAGESIZE      # 16


def get_pages(items):
    from math import ceil
    # PAGE = 10
    # total = 280
    # page = 16
    # size = 16
    itemspage = ceil(items.total/_PAGESIZE)
    # print(itemspage, '----------------', items.total, items.page, items.total/_PAGESIZE)
    pages = []
    for i in range(items.page-int(PAGE/2-1), items.page+int(PAGE/2)+1):
        # print (i)
        if i < 1:
            pages.append(PAGE + i)
            # print(PAGE+i, i)
        else:
            pages.append(i)
    pages_copy = pages.copy()
    for p in pages_copy:
        if p > ceil(items.total/_PAGESIZE):
            try:
                pages.remove(p)
            except ValueError as e:
                pass
    while (len(pages) < PAGE ) & (min(pages) != 1):
        pages.append(min(pages) - 1)

    pages.sort()
    return pages


def get_etc_keyword(db):
    etc_kwd = []
    for i in get_etcall(db):
        for j in i:
            for k in (j.strip()).split():
                etc_kwd.append(k.strip())
    etc_kwd_list = etc_kwd
    etc_kwd = list(set(etc_kwd))
    etc_kwd.sort()
    etc_kwd2 = []
    for i in etc_kwd:
        etc_kwd2.append( '#'+str(etc_kwd_list.count(i)).zfill(3) + ':' + i)
        # print( '#'+str(etc_kwd_list.count(i)) + ' ' + i)
        
        
    return etc_kwd2
    
    

