# Python
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Pip
from google.protobuf.timestamp_pb2 import Timestamp

# Local
from call_data import CallData, CallType
from calls_pb2 import *


class HistoryParser:
    def __init__(self, infile):
        self.data = infile.read()
        self.file_name = infile.name
        infile.close()

    def parse(self):
        """ Returns a list of Call objects """
        if self.file_name.endswith('.xml'):
            return self.parse_xml()
        else:
            return self.parse_protobuf()

    def parse_protobuf(self):
        result = []

        call_history = CallHistory()
        call_history.ParseFromString(self.data)
        for call in call_history.calls:
            end = Timestamp()
            end.seconds = call.start.seconds + call.duration.seconds
            result.append(
                CallData(call.number, call.start.ToDatetime(), end.ToDatetime(), call.type))

        return result

    def parse_xml(self):
        result = []

        root = ET.fromstring(self.data)
        for child in root:
            # Note: Only takes the last 10 digits of the phone number
            number = child[0].text.strip()[-10:]
            if not number:
                continue
            start = datetime.fromtimestamp(int(child[1].text.strip()) / 1000)
            end = start + timedelta(0, int(child[2].text.strip()))
            call_type = CallType(int(child[3].text.strip()) - 1)
            result.append(CallData(number, start, end, call_type))

        return result

    # def parse_sqlite(self):
        # return []
