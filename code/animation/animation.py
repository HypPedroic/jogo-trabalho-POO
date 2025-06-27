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
        
    @property
    def current_state(self):
        return self.__current_state

    @current_state.setter
    def current_state(self, valor):
        self.__current_state = valor

    @property
    def state_transitions(self):
        return self.__state_transitions

    @state_transitions.setter
    def state_transitions(self, valor):
        self.__state_transitions = valor

    @property
    def on_complete_callback(self):
        return self.__on_complete_callback

    @on_complete_callback.setter
    def on_complete_callback(self, valor):
        self.__on_complete_callback = valor

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def img(self):
        # Verificação de segurança para evitar erro de índice
        if len(self.images) == 0:
            return None
        return self.images[int(self.frame / self.img_duration)]
    
    def update(self):
        # Verificação de segurança para evitar divisão por zero
        if len(self.images) == 0:
            return
            
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
                if self.on_complete_callback:
                    self.on_complete_callback()
                if self.current_state in self.state_transitions:
                    self.transition_to(self.state_transitions[self.current_state])
    
    def add_state_transition(self, from_state, to_state):
        """Adiciona uma transição automática entre estados de animação"""
        self.state_transitions[from_state] = to_state
    
    def set_on_complete(self, callback):
        """Define uma função de callback para quando a animação terminar"""
        self.on_complete_callback = callback
    
    def transition_to(self, new_state):
        """Realiza a transição para um novo estado"""
        self.current_state = new_state
        self.frame = 0
        self.done = False
    
    def reset(self):
        """Reseta a animação para o frame inicial"""
        self.frame = 0
        self.done = False
            

    
        
