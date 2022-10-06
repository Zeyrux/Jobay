from collections import namedtuple

from .models import Message

# irrelevant da über relationship auf msgs zugegriffen werden kann
# TODO: überarbeiten / löschen
class User:
    def __init__(self, user_db) -> None:
        self.db = user_db
        self.messages = {}

    def get_msgs(self, other_user_id: int) -> tuple[list[Message], list[Message]]:
        msgs = self.messages.get(other_user_id, None)
        if not msgs:
            msgs_send = Message.query.filter_by(
                user_send=self.db.id, user_receive=other_user_id
            )
            msgs_receive = Message.query.filter_by(
                user_send=other_user_id, user_receive=self.db.id
            )
            msgs = namedtuple("Message", ["send", "receive"], [msgs_send, msgs_receive])
            self.messages[other_user_id] = msgs
        return msgs
