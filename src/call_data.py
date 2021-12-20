# Python
from datetime import datetime
from enum import Enum


class CallType(Enum):
    Incoming = 0
    Outgoing = 1
    Missed = 2
    Voicemail = 3
    Rejected = 4
    Blocked = 5
    AnsweredExternally = 6


class CallData:
    def __init__(self, number: str, start: datetime, end: datetime, call_type: CallType):
        self.number = number
        self.start = start
        self.end = end
        self.call_type = call_type
        self.duration = self.end - self.start

    def __str__(self):
        return f'{self.call_type.name}: {self.number} - {self.start} - {self.duration}'
