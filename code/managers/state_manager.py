from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    VICTORY = auto()

class StateManager:
    def __init__(self):
        self.__current_state = GameState.MENU
        self.__state_handlers = {}
        self.__state_transitions = {}
        
    @property
    def current_state(self):
        return self.__current_state

    @current_state.setter
    def current_state(self, value):
        self.__current_state = value

    @property
    def state_handlers(self):
        return self.__state_handlers

    @state_handlers.setter
    def state_handlers(self, value):
        self.__state_handlers = value

    @property
    def state_transitions(self):
        return self.__state_transitions

    @state_transitions.setter
    def state_transitions(self, value):
        self.__state_transitions = value

    def register_state_handler(self, state, handler):
        """Registra um handler para um estado específico"""
        self.state_handlers[state] = handler

    def register_transition(self, from_state, to_state, transition_handler):
        """Registra uma transição entre estados"""
        if from_state not in self.state_transitions:
            self.state_transitions[from_state] = {}
        self.state_transitions[from_state][to_state] = transition_handler

    def change_state(self, new_state):
        """Muda para um novo estado executando a transição apropriada"""
        if self.current_state == new_state:
            return

        # Executa o handler de transição se existir
        if (self.current_state in self.state_transitions and 
            new_state in self.state_transitions[self.current_state]):
            self.state_transitions[self.current_state][new_state]()

        self.current_state = new_state

    def update(self):
        """Atualiza o estado atual"""
        if self.current_state in self.state_handlers:
            self.state_handlers[self.current_state]()

