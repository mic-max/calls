# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: calls.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x63\x61lls.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x82\x02\n\x04\x43\x61ll\x12\x0e\n\x06number\x18\x01 \x01(\t\x12)\n\x05start\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\x08\x64uration\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x1c\n\x04type\x18\x04 \x01(\x0e\x32\x0e.Call.CallType\"t\n\x08\x43\x61llType\x12\x0c\n\x08Incoming\x10\x00\x12\x0c\n\x08Outgoing\x10\x01\x12\n\n\x06Missed\x10\x02\x12\r\n\tVoicemail\x10\x03\x12\x0c\n\x08Rejected\x10\x04\x12\x0b\n\x07\x42locked\x10\x05\x12\x16\n\x12\x41nsweredExternally\x10\x06\"#\n\x0b\x43\x61llHistory\x12\x14\n\x05\x63\x61lls\x18\x01 \x03(\x0b\x32\x05.Callb\x06proto3')



_CALL = DESCRIPTOR.message_types_by_name['Call']
_CALLHISTORY = DESCRIPTOR.message_types_by_name['CallHistory']
_CALL_CALLTYPE = _CALL.enum_types_by_name['CallType']
Call = _reflection.GeneratedProtocolMessageType('Call', (_message.Message,), {
  'DESCRIPTOR' : _CALL,
  '__module__' : 'calls_pb2'
  # @@protoc_insertion_point(class_scope:Call)
  })
_sym_db.RegisterMessage(Call)

CallHistory = _reflection.GeneratedProtocolMessageType('CallHistory', (_message.Message,), {
  'DESCRIPTOR' : _CALLHISTORY,
  '__module__' : 'calls_pb2'
  # @@protoc_insertion_point(class_scope:CallHistory)
  })
_sym_db.RegisterMessage(CallHistory)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CALL._serialized_start=81
  _CALL._serialized_end=339
  _CALL_CALLTYPE._serialized_start=223
  _CALL_CALLTYPE._serialized_end=339
  _CALLHISTORY._serialized_start=341
  _CALLHISTORY._serialized_end=376
# @@protoc_insertion_point(module_scope)