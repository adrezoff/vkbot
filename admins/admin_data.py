import admins.admin

admin_map = {}


def create_admin_data_map():
    for admin in admins.admin.load_admins():
        admin_map[admin] = "0"  # Устанавливаем начальное значение 0 для каждого администратора
    return admin_map


def get_edit_id(user_id):
    return admin_map[user_id]


def set_edit_id(user_id, selected_product_id):
    admin_map[user_id] = selected_product_id