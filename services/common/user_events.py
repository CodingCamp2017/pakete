import constants

class UserEvent:
    def __init__(self, email):
        self.email = email

    def toDict(self):
        return {'email':self.email}

class UserPacketEvent(UserEvent):
    def __init__(self, email, packet_id):
        super().__init__(email)
        self.packet_id = packet_id

    def toDict(self):
        d = super().toDict()
        d['packet_id'] = self.packet_id
        return d
