from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.topic_state import TopicFSM
from filters.topic_filter import TopicFilter

router = Router()

@router.message(Command("topic"))
async def topic_handler(message: Message, state: FSMContext):
    await message.answer(
        'Enter news topic without "/" :\n\n' +
        '\n'.join(f'{topic}' for topic in TopicFilter.valid_topics)
    )
    await state.set_state(TopicFSM.choosing)

@router.message(TopicFSM.choosing, TopicFilter())
async def save_topic(message: Message, state: FSMContext):
    topic = message.text.lower()
    await state.update_data(topic=topic)
    await message.answer(f"Chosen topic: '{topic}'. Now you can use /latest")
    await state.set_state(None)

@router.message(TopicFSM.choosing)
async def invalid_topic(message: Message):
    await message.answer("Invalid topic. Please choose from the list.")
