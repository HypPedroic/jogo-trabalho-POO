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

    def register_state_handler(self, state, handler):
        """Registra um handler para um estado específico"""
        self.__state_handlers[state] = handler

    def register_transition(self, from_state, to_state, transition_handler):
        """Registra uma transição entre estados"""
        if from_state not in self.__state_transitions:
            self.__state_transitions[from_state] = {}
        self.__state_transitions[from_state][to_state] = transition_handler

    def change_state(self, new_state):
        """Muda para um novo estado executando a transição apropriada"""
        if self.__current_state == new_state:
            return

        # Executa o handler de transição se existir
        if (self.__current_state in self.__state_transitions and 
            new_state in self.__state_transitions[self.__current_state]):
            self.__state_transitions[self.__current_state][new_state]()

        self.__current_state = new_state

    def update(self):
        """Atualiza o estado atual"""
        if self.__current_state in self.__state_handlers:
            self.__state_handlers[self.__current_state]()

    @property
    def current_state(self):
        return self.__current_state