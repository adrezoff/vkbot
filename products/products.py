import json


def load_products():
    with open('products/products.json', 'r', encoding='cp1251') as file:
        return json.load(file)


def save_products(products):
    with open('products/products.json', 'w', encoding='cp1251') as file:
        json.dump(products, file, indent=2, ensure_ascii=False)


def add_product(name, description, price):
    products = load_products()
    new_product_id = str(len(products) + 1)
    products[new_product_id] = {
        "name": name,
        "description": description,
        "price": price
    }
    save_products(products)


def delete_product(product_id):
    products = load_products()
    if product_id in products:
        del products[product_id]
        # Перестраиваем словарь, чтобы его ключи соответствовали порядковым номерам
        rebuilt_products = {}
        for idx, (key, value) in enumerate(products.items(), start=1):
            rebuilt_products[str(idx)] = value
        save_products(rebuilt_products)
        return True  # Возвращаем True, если товар успешно удален
    else:
        return False  # Возвращаем False, если товар с указанным ID не найден