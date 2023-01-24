from core.config import Settings

ROOT_DIR = Settings.ROOT_DIR    #= "/home/yadong/"
TEMP_DIR = Settings.TEMP_DIR    #= "/home/temp/"
WASTE_DIR = Settings.WASTE_DIR  #= "_waste/"
GIF = Settings.GIF              #= "gif/"
WEBP = Settings.WEBP            #= "webp/"

class Findpath:
    def __init__(self, src):
        self.src: str = src
    def dbid(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            return self.src.replace(GIF, '')[:-3]
        if self.src[self.src.rfind('.')+1:] == 'webp':
            return self.src.replace(WEBP, '')[:-4]
        else:
            return self.src.replace(ROOT_DIR, '')
    def video(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            return self.src.replace(GIF, '')[:-3]
        if self.src[self.src.rfind('.')+1:] == 'webp':
            return self.src.replace(WEBP, '')[:-4]
        else:
            return self.src.replace(ROOT_DIR, '')
    def gif(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            return self.src
        if self.src[self.src.rfind('.')+1:] == 'webp':
            return (self.src[:-4] + 'gif').replace(WEBP, GIF)
        else:
            d = self.src.replace(ROOT_DIR, '')
            return d[:d.find('/')+1] + GIF + d[d.find('/')+1:d.rfind('.')+1] + 'gif'
    def webp(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            return (self.src[:-3] + 'webp').replace(GIF, WEBP)
        if self.src[self.src.rfind('.')+1:] == 'webp':
            return self.src
        else:
            d = self.src.replace(ROOT_DIR, '')
            return d[:d.find('/')+1] + WEBP + d[d.find('/')+1:d.rfind('.')+1] + 'webp'
    def waste_video(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            d = self.src.replace(GIF, '')[:-3]
            return WASTE_DIR + d[d.rfind('/')+1:]
        if self.src[self.src.rfind('.')+1:] == 'webp':
            d = self.src.replace(WEBP, '')[:-4]
            return WASTE_DIR + d[d.rfind('/')+1:]
        else:
            d = self.src.replace(ROOT_DIR, '')
            return WASTE_DIR + d[d.find('/')+1:]
    def waste_gif(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            d = self.src.replace(GIF, '')
            return WASTE_DIR + d[d.rfind('/')+1:]
        if self.src[self.src.rfind('.')+1:] == 'webp':
            d = self.src.replace(WEBP, '')
            return WASTE_DIR + d[d.rfind('/')+1:-4] + 'gif'
        else:
            d = self.src.replace(ROOT_DIR, '')
            return WASTE_DIR + d[d.find('/')+1:d.rfind('.')+1] + 'gif'
    def waste_webp(self):
        if self.src[self.src.rfind('.')+1:] == 'gif':
            d = self.src.replace(GIF, '')
            return WASTE_DIR + d[d.rfind('/')+1:-3] + 'webp'
        if self.src[self.src.rfind('.')+1:] == 'webp':
            d = self.src.replace(GIF, '')
            return WASTE_DIR + d[d.rfind('/')+1:]
        else:
            d = self.src.replace(ROOT_DIR, '')
            return WASTE_DIR + d[d.find('/')+1:d.rfind('.')+1] + 'webp'


if __name__ == '__main__':
    src_webp = '0000/webp/99.webp'
    src_gif = '0000/gif/99.gif'
    src_dbid = '0000/99.mp4'
    src_video = '/home/yadong/0000/99.mp4'
    webp_path = Findpath(src_webp)
    gif_path = Findpath(src_gif)
    dbid_path = Findpath(src_dbid)
    video_path = Findpath(src_video)
    print('dbid       :', gif_path.dbid(), webp_path.dbid(), dbid_path.dbid(), video_path.dbid(),)
    print('video      :',gif_path.video(), webp_path.video(), dbid_path.video(), video_path.video(),)
    print('gif        :',gif_path.gif(), webp_path.gif(), dbid_path.gif(), video_path.gif(),)
    print('webp       :',gif_path.webp(), webp_path.webp(), dbid_path.webp(), video_path.webp(),)
    print('waste_video:',gif_path.waste_video(), webp_path.waste_video(),  dbid_path.waste_video(),  video_path.waste_video(),)
    print('waste_gif  :',gif_path.waste_gif(), webp_path.waste_gif(), dbid_path.waste_gif(), video_path.waste_gif(),)
    print('waste_webp :',gif_path.waste_webp(), webp_path.waste_webp(), dbid_path.waste_webp(), video_path.waste_webp(),)
    '''
    dbid       : 0000/99. 0000/99. 0000/99.mp4 0000/99.mp4
    video      : /home/yadong/0000/99. /home/yadong/0000/99. /home/yadong/0000/99.mp4 /home/yadong/0000/99.mp4
    gif        : /home/yadong/0000/gif/99.gif /home/yadong/0000/gif/99.gif /home/yadong/0000/gif/99.gif /home/yadong/0000/gif/99.gif
    webp       : /home/yadong/0000/webp/99.webp /home/yadong/0000/webp/99.webp /home/yadong/0000/webp/99.webp /home/yadong/0000/webp/99.webp
    waste_video: /home/yadong/_waste/99. /home/yadong/_waste/99. /home/yadong/_waste/99.mp4 /home/yadong/_waste/99.mp4
    waste_gif  : /home/yadong/_waste/99.gif /home/yadong/_waste/99.gif /home/yadong/_waste/99.gif /home/yadong/_waste/99.gif
    waste_webp : /home/yadong/_waste/99.webp /home/yadong/_waste/99.webp /home/yadong/_waste/99.webp /home/yadong/_waste/99.webp
    '''