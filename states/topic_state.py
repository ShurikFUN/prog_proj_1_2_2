from aiogram.fsm.state import StatesGroup, State

class TopicFSM(StatesGroup):
    choosing = State()