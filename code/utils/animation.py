class Animation:
    def __init__(self, images, img_dur, loop = True):
        self.__images = images
        self.__img_duration = img_dur
        self.__loop = loop
        self.__done = False
        self.__frame = 0

    @property
    def images(self):
        return self.__images
    
    @images.setter
    def images(self, valor):
        self.__images = valor

    @property
    def img_duration(self):
        return self.__img_duration
    
    @img_duration.setter
    def img_duration(self, valor):
        self.__img_duration = valor

    @property
    def loop(self):
        return self.__loop
    
    @loop.setter
    def loop(self, valor):
        self.__loop = valor

    @property
    def done(self):
        return self.__done
    
    @done.setter
    def done(self, valor):
        self.__done = valor

    @property
    def frame(self):
        return self.__frame
    
    @frame.setter
    def frame(self, valor):
        self.__frame = valor

    def copy(self):
        return Animation(self.__images, self.__img_duration, self.__loop)
    
    def img(self):
        return self.__images[int(self.__frame / self.__img_duration)]
    
    def update(self):
        if self.__loop:
            self.__frame = (self.__frame + 1) % (self.__img_duration * len(self.__images))
        else:
            self.__frame = min(self.__frame + 1, self.__img_duration * len(self.__images) - 1)
            if self.__frame >= self.__img_duration * len(self.__images) - 1:
                self.__done = True
            

    
        
