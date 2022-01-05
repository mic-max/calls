# Python
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Pip
from google.protobuf.timestamp_pb2 import Timestamp

# Local
from call_data import CallData, CallType


class HistoryParser:
    @staticmethod
    def parse(infile):
        data = infile.read()
        infile.close()

        if infile.name.endswith('.xml'):
            return HistoryParser._parse_xml(data)
        elif infile.name.endswith('.aiob'):
            return HistoryParser._parse_aiob(data)
        elif infile.name.endswith('.bin'):
            return HistoryParser._parse_protobuf(data)
        raise Exception("Unsupported file type")

    @staticmethod
    def _parse_xml(data):
        result = []

        xml_data = ET.canonicalize(data, strip_text=True)
        root = ET.fromstring(xml_data)
        for child in root:
            number = child.findtext('phoneNumber')
            start = datetime.fromtimestamp(int(child.findtext('dateTime')) / 1000)
            end = start + timedelta(0, int(child.findtext('callDuration')))
            call_type = CallType(int(child.findtext('logType')))
            result.append(CallData(number, start, end, call_type))

        return result

    @staticmethod
    def _parse_aiob(data):
        result = []

        xml_data = ET.canonicalize(data, strip_text=True)
        root = ET.fromstring(xml_data).find('File').find('Data')
        for child in root:
            number = child.findtext('PhoneNumber')
            start = datetime.fromtimestamp(int(child.findtext('Timestamp')) / 1000)
            end = start + timedelta(0, int(child.findtext('Duration')))
            call_type = CallType(int(child.findtext('CallType')))
            result.append(CallData(number, start, end, call_type))

        return result

    @staticmethod
    def _parse_protobuf(data):
        from history_pb2 import CallHistory
        result = []

        call_history = CallHistory()
        call_history.ParseFromString(data)
        for call in call_history.calls:
            number = call.number
            # TODO timezone issues
            start = call.start.ToDatetime()
            end = Timestamp(seconds=call.start.seconds + call.duration.seconds).ToDatetime()
            call_type = CallType(call.type)
            result.append(CallData(number, start, end, call_type))

        return result
