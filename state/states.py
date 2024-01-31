import products.products
from admins.admin import *
from admins.admin_data import set_edit_id, get_edit_id
from products.products import *


class State:
    def __init__(self, name, send_message):
        self.name = name
        self.send_message = send_message

    def on_enter(self, user_id):
        pass

    def handle_input(self, user_id, message):
        pass

    def get_name(self):
        return self.name


class AdminMenuState(State):
    def __init__(self, send_message):
        super().__init__('AdminState', send_message)

    def on_enter(self, user_id):
        admins = load_admins()['list']
        if user_id in admins:
            self.send_message(user_id, "Вы являетесь администратором. Доступ разрешен.\n\n"
                                       "Доступные действия:\n"
                                       "1) Добавить товар\n"
                                       "2) Изменить товар\n"
                                       "3) Удалить товар")
            return AdminMenuState(self.send_message)
        else:
            self.send_message(user_id, "Вы НЕ являетесь администратором. Доступ запрещен.")
            return MenuState(self.send_message)

    def handle_input(self, user_id, message):
        if message.lower() == '1' or message.lower() == 'добавить товар':
            return AddProductState(self.send_message)
        elif message.lower() == '2' or message.lower() == 'изменить товар':
            return EditProductState(self.send_message)
        elif message.lower() == '3' or message.lower() == 'удалить товар':
            return DeleteProductsState(self.send_message)
        elif message.lower() == 'назад':
            return MenuState(self.send_message)
        elif message.lower() == 'menu':
            return MenuState(self.send_message)
        else:
            self.send_message(user_id, "Некорректный ввод. Попробуйте снова:")
            return None


class StartState(State):
    def __init__(self, send_message):
        super().__init__('StartState', send_message)

    def on_enter(self, user_id):
        pass

    def handle_input(self, user_id, message):
        if message.lower() == 'назад':
            return StartState(self.send_message)
        self.send_message(user_id, "successful load")
        return MenuState(self.send_message)


class MenuState(State):
    def __init__(self, send_message):
        super().__init__('MenuState', send_message)

    def on_enter(self, user_id):
        self.send_message(user_id, "menu: \n"
                                   "1) Товары\n"
                                   "2) Очередь\n"
                                   "3) Контакты\n")

    def handle_input(self, user_id, message):
        if message.lower() == '1' or message.lower() == 'товары':
            return ViewProductsState(self.send_message)
        elif message.lower() == 'назад':
            return StartState(self.send_message)
        elif message.lower() == 'admin':
            return AdminMenuState(self.send_message)
        elif message.lower() == 'menu':
            return MenuState(self.send_message)


class AddProductState(State):
    def __init__(self, send_message):
        super().__init__('AddProductState', send_message)
        self.state_data = {}

    def on_enter(self, user_id):
        self.send_message(user_id, "Введите название товара:")

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            set_edit_id(user_id, "0")
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            set_edit_id(user_id, "0")
            return AdminMenuState(self.send_message)
        if 'name' not in self.state_data:
            self.state_data['name'] = message
            self.send_message(user_id, "Введите описание товара:")
        elif 'description' not in self.state_data:
            self.state_data['description'] = message
            self.send_message(user_id, "Введите цену товара:")
        elif 'price' not in self.state_data:
            try:
                price = float(message)
                self.state_data['price'] = price
                add_product(self.state_data['name'], self.state_data['description'], price)
                self.send_message(user_id, f"Товар '{self.state_data['name']}' успешно добавлен!")
                self.state_data = {}  # Сбрасываем состояние после успешного добавления товара
                return AdminMenuState(self.send_message)  # Переходим в меню администратора
            except ValueError:
                self.send_message(user_id, "Некорректный формат цены. Попробуйте снова:")
        return None  # Возвращаем None, чтобы оставаться в текущем состоянии до успешного ввода цены


class DeleteProductsState(State):
    def __init__(self, send_message):
        super().__init__('DeleteProductsState', send_message)

    def on_enter(self, user_id):
        final_str = "Выберите товар для удаления:\n"
        product = load_products()
        for product_id, product_info in product.items():
            final_str += f"{product_id}. {product_info['name']} - {product_info['description']} - {product_info['price']}" + " RUB\n"
        self.send_message(user_id, final_str)

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            return AdminMenuState(self.send_message)
        elif message.isdigit():
            product_id = message
            success = delete_product(product_id)
            if success:
                self.send_message(user_id, f"Товар с ID {product_id} успешно удален!")
            else:
                self.send_message(user_id, f"Не удалось удалить товар с ID {product_id}. Товар с таким ID не найден.")
        else:
            self.send_message(user_id, "Некорректный ввод. Введите ID товара для удаления:")
        return None


class ViewProductsState(State):
    def __init__(self, send_message):
        super().__init__('ViewProductsState', send_message)

    def on_enter(self, user_id):
        product = load_products()
        final_str = "Список доступных товаров:\n"

        for product_id, product_info in product.items():
            final_str += f"{product_id}. {product_info['name']} - {product_info['description']} - {product_info['price']}" + " RUB\n"
        self.send_message(user_id, final_str)

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            return MenuState(self.send_message)
        elif message.isdigit():
            product_id = message
            products = load_products()
            if product_id in products:
                product_info = products[product_id]
                self.send_message(user_id, f"Название: {product_info['name']}\nОписание: {product_info['description']}\nЦена: {product_info['price']}" + " RUB\n")
            else:
                self.send_message(user_id, "Такого товара не существует.")
        else:
            self.send_message(user_id, "Некорректный ввод. Попробуйте снова:")
        return None


class EditProductState(State):
    def __init__(self, send_message):
        super().__init__('EditProductState', send_message)

    def on_enter(self, user_id):
        final_str = "Выберите товар для редактирования:\n"
        product = load_products()
        for product_id, product_info in product.items():
            final_str += f"{product_id}. {product_info['name']} - {product_info['description']} - {product_info['price']}" + " RUB\n"
        self.send_message(user_id, final_str)

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            return AdminMenuState(self.send_message)

        products = load_products()
        if message.isdigit() and message in products:
            selected_product_id = message
            set_edit_id(user_id, selected_product_id)
            self.send_message(user_id, f"Выбран товар с ID {selected_product_id}.")
            return EditMenuProductState(self.send_message)

        else:
            self.send_message(user_id, "Некорректный ввод. Попробуйте снова:")
            return None


class EditMenuProductState(State):
    def __init__(self, send_message):
        super().__init__('EditMenuProductState', send_message)

    def on_enter(self, user_id):
        self.send_message(user_id, "Выберите, что вы хотите изменить:\n"
                                    "1) Название\n"
                                    "2) Описание\n"
                                    "3) Цену")

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            set_edit_id(user_id, "0")
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            set_edit_id(user_id, "0")
            return AdminMenuState(self.send_message)
        elif message.lower() == '1' or message.lower() == 'название':
            return EditProductNameState(self.send_message)
        elif message.lower() == '2' or message.lower() == 'описание':
            return EditProductDescriptionState(self.send_message)
        elif message.lower() == '3' or message.lower() == 'цену':
            return EditProductPriceState(self.send_message)
        else:
            self.send_message(user_id, "Некорректный ввод. Попробуйте снова.")
            return None


class EditProductNameState(State):
    def __init__(self, send_message):
        super().__init__('EditProductNameState', send_message)

    def on_enter(self, user_id):
        self.send_message(user_id, "Введите новое название товара:")

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            return AdminMenuState(self.send_message)

        products = load_products()
        selected_product_id = get_edit_id(user_id)
        if selected_product_id in products:
            products[selected_product_id]['name'] = message
            save_products(products)
            self.send_message(user_id, f"Название товара успешно изменено на '{message}'.")
            return AdminMenuState(self.send_message)
        else:
            self.send_message(user_id, "Ошибка: товар с указанным ID не найден.")
            return None


class EditProductDescriptionState(State):
    def __init__(self, send_message):
        super().__init__('EditProductDescriptionState', send_message)

    def on_enter(self, user_id):
        self.send_message(user_id, "Введите новое описание товара:")

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            return AdminMenuState(self.send_message)

        products = load_products()
        selected_product_id = get_edit_id(user_id)
        if selected_product_id in products:
            products[selected_product_id]['description'] = message
            save_products(products)
            self.send_message(user_id, f"Описание товара успешно изменено на '{message}'.")
            return AdminMenuState(self.send_message)
        else:
            self.send_message(user_id, "Ошибка: товар с указанным ID не найден.")
            return None


class EditProductPriceState(State):
    def __init__(self, send_message):
        super().__init__('EditProductPriceState', send_message)

    def on_enter(self, user_id):
        self.send_message(user_id, "Введите новую цену товара:")

    def handle_input(self, user_id, message):
        if message.lower() == 'menu':
            return MenuState(self.send_message)
        elif message.lower() == 'назад':
            return AdminMenuState(self.send_message)

        products = load_products()
        selected_product_id = get_edit_id(user_id)
        if selected_product_id in products:
            try:
                price = float(message)
                products[selected_product_id]['price'] = price
                save_products(products)
                self.send_message(user_id, f"Цена товара успешно изменена на '{price}' RUB.")
                return AdminMenuState(self.send_message)
            except ValueError:
                self.send_message(user_id, "Некорректный формат цены. Попробуйте снова:")
                return None
        else:
            self.send_message(user_id, "Ошибка: товар с указанным ID не найден.")
            return None
