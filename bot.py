import random
import os
from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from admins.admin_data import create_admin_data_map
from state.state_map import *
from users.users import *
from admins import admin_data


def send_message(user_id, message):
    vk.messages.send(
        user_id=user_id,
        random_id=random.randint(0, 2 ** 64),  # Генерируем случайное целое число
        message=message
    )


# Инициализация сессии VK API
load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

state_map = create_state_map(send_message)

if __name__ == "__main__":
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.from_user and event.to_me:
            user_id = event.user_id
            message = event.text.lower()

            if not user_in_db(user_id):
                insert_user(user_id)

            user_data = get_data(user_id)

            if user_data[1] is None:
                state = get_state_from_map(state_map, 'StartState')

            if message == 'end':
                set_state(user_id, 'StartState')
                user_data = get_data(user_id)
            state = get_state_from_map(state_map, user_data[1])

            next_state = state.handle_input(user_id, message)

            if next_state:
                set_state(user_id, get_name_state_from_map(state_map, next_state))
                next_state.on_enter(user_id)
