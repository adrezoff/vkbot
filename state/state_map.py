# state_map.py

from state.states import *


def create_state_map(send_message):
    # Добавление состояний в ассоциативный массив
    state_map = {}
    state_map["StartState"] = StartState(send_message)

    state_map["MenuState"] = MenuState(send_message)
    state_map["ViewProductsState"] = ViewProductsState(send_message)

    state_map["AdminMenuState"] = AdminMenuState(send_message)

    state_map["AddProductState"] = AddProductState(send_message)
    state_map["DeleteProductsState"] = DeleteProductsState(send_message)
    state_map["EditProductState"] = EditProductState(send_message)
    state_map["EditMenuProductState"] = EditMenuProductState(send_message)
    state_map["EditProductNameState"] = EditProductNameState(send_message)
    state_map["EditProductDescriptionState"] = EditProductDescriptionState(send_message)
    state_map["EditProductPriceState"] = EditProductPriceState(send_message)



    return state_map


def get_state_from_map(state_map, state_name):
    return state_map.get(state_name)


def get_name_state_from_map(state_map, state_instance):
    for name, state in state_map.items():
        if state.get_name() == state_instance.get_name():
            return name
    return None



