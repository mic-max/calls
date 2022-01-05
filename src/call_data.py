# Python
from datetime import datetime
from enum import Enum


class CallType(Enum):
    Incoming = 1
    Outgoing = 2
    Missed = 3
    Voicemail = 4
    Rejected = 5
    Blocked = 6
    AnsweredExternally = 7

class CallData:
    def __init__(self, number: str, start: datetime, end: datetime, call_type: CallType):
        self.number = number[-10:] # Excludes country code e.g. +1
        self.start = start
        self.end = end
        self.call_type = call_type
        self.duration = self.end - self.start
