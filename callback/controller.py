# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

confirmation_token = "hwgfASD2391das"

@app.route('/callback', methods=['POST'])
def callback_handler():
    data = request.json

    if 'type' in data:
        # Если тип уведомления - "confirmation", возвращаем строку подтверждения
        if data['type'] == 'confirmation':
            return confirmation_token

        # Если тип уведомления - "message_new", это новое сообщение от пользователя
        elif data['type'] == 'message_new':
            # Проверяем, является ли сообщение уведомлением о платеже через VK Pay
            if 'object' in data and 'action' in data['object'] and data['object']['action']['type'] == 'vkpay_transaction':
                handle_vkpay_transaction(data['object'])

    # Возвращаем OK, чтобы VK не пытался отправить уведомление снова
    return 'OK'


def handle_vkpay_transaction(transaction_data):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
