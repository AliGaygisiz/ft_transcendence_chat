import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import AcceptConnection
from asgiref.sync import async_to_sync


class ChatUser:
    id = 0
    username = ""
    main_channel = ""


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("connect")
        # create a new user and add it to the list
        self.room_group_name = "GlobalChat"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("message:", message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"type": "chat", "message": message}))
