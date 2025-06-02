class Animation:
    def __init__(self, images, img_dur, loop = True):
        self._images = images
        self._img_duration = img_dur
        self._loop = loop
        self._done = False
        self._frame = 0

    @property
    def images(self):
        return self._images
    
    @images.setter
    def images(self, valor):
        self._images = valor

    @property
    def img_duration(self):
        return self._img_duration
    
    @img_duration.setter
    def img_duration(self, valor):
        self._img_duration = valor

    @property
    def loop(self):
        return self._loop
    
    @loop.setter
    def loop(self, valor):
        self._loop = valor

    @property
    def done(self):
        return self._done
    
    @done.setter
    def done(self, valor):
        self._done = valor

    @property
    def frame(self):
        return self._frame
    
    @frame.setter
    def frame(self, valor):
        self._frame = valor

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
            

    
        
