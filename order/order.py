import json
import uuid


class Order:
    def __init__(self, user_id, product, price, status='новый'):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.product = product
        self.price = price
        self.status = status

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'product': self.product,
            'price': self.price,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['user_id'],
            data['product'],
            data['price'],
            data['status']
        )

    @staticmethod
    def save_to_json(orders):
        with open('orders.json', 'w', encoding='cp1251') as f:
            json.dump([order.to_dict() for order in orders], f, indent=4)

    @staticmethod
    def load_from_json():
        try:
            with open('orders.json', 'r', encoding='cp1251') as f:
                data = json.load(f)
                return [Order.from_dict(order_data) for order_data in data]
        except FileNotFoundError:
            return None