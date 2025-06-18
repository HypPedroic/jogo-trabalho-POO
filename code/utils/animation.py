class Animation:
    def __init__(self, images, img_dur, loop = True):
        self.__images = images
        self.__img_duration = img_dur
        self.__loop = loop
        self.__done = False
        self.__frame = 0
        self.__current_state = 'default'
        self.__state_transitions = {}
        self.__on_complete_callback = None

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
                if self.__on_complete_callback:
                    self.__on_complete_callback()
                if self.__current_state in self.__state_transitions:
                    self.transition_to(self.__state_transitions[self.__current_state])
    
    def add_state_transition(self, from_state, to_state):
        """Adiciona uma transição automática entre estados de animação"""
        self.__state_transitions[from_state] = to_state
    
    def set_on_complete(self, callback):
        """Define uma função de callback para quando a animação terminar"""
        self.__on_complete_callback = callback
    
    def transition_to(self, new_state):
        """Realiza a transição para um novo estado"""
        self.__current_state = new_state
        self.__frame = 0
        self.__done = False
    
    def reset(self):
        """Reseta a animação para o frame inicial"""
        self.__frame = 0
        self.__done = False
            

    
        
