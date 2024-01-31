products_user_data = {}


def get_product_id(user_id):
    _id = products_user_data[user_id]
    if _id:
        return _id
    else:
        return None

def set_product_id(user_id, selected_product_id):
    if selected_product_id == "0":
        products_user_data[user_id] = "0"
        del products_user_data[user_id]
    else:
        products_user_data[user_id] = selected_product_id