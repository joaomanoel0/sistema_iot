# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf_messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf_messages.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x17protobuf_messages.proto\"\x1c\n\tDiscovery\x12\x0f\n\x07message\x18\x01 \x01(\t\"_\n\x0eIdentification\x12\x13\n\x0b\x64\x65vice_type\x18\x01 \x01(\t\x12\x11\n\tdevice_ip\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65vice_port\x18\x03 \x01(\x05\x12\x10\n\x08protocol\x18\x04 \x01(\t\"#\n\x0bGatewayPort\x12\x14\n\x0cgateway_port\x18\x01 \x01(\x05\")\n\x16GatewayToDeviceMessage\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\"*\n\x16\x44\x65viceToGatewayMessage\x12\x10\n\x08response\x18\x01 \x01(\tb\x06proto3')
)




_DISCOVERY = _descriptor.Descriptor(
  name='Discovery',
  full_name='Discovery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='Discovery.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=55,
)


_IDENTIFICATION = _descriptor.Descriptor(
  name='Identification',
  full_name='Identification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_type', full_name='Identification.device_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_ip', full_name='Identification.device_ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_port', full_name='Identification.device_port', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='Identification.protocol', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=152,
)


_GATEWAYPORT = _descriptor.Descriptor(
  name='GatewayPort',
  full_name='GatewayPort',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gateway_port', full_name='GatewayPort.gateway_port', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=189,
)


_GATEWAYTODEVICEMESSAGE = _descriptor.Descriptor(
  name='GatewayToDeviceMessage',
  full_name='GatewayToDeviceMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='GatewayToDeviceMessage.command', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=191,
  serialized_end=232,
)


_DEVICETOGATEWAYMESSAGE = _descriptor.Descriptor(
  name='DeviceToGatewayMessage',
  full_name='DeviceToGatewayMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='DeviceToGatewayMessage.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=276,
)

DESCRIPTOR.message_types_by_name['Discovery'] = _DISCOVERY
DESCRIPTOR.message_types_by_name['Identification'] = _IDENTIFICATION
DESCRIPTOR.message_types_by_name['GatewayPort'] = _GATEWAYPORT
DESCRIPTOR.message_types_by_name['GatewayToDeviceMessage'] = _GATEWAYTODEVICEMESSAGE
DESCRIPTOR.message_types_by_name['DeviceToGatewayMessage'] = _DEVICETOGATEWAYMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Discovery = _reflection.GeneratedProtocolMessageType('Discovery', (_message.Message,), dict(
  DESCRIPTOR = _DISCOVERY,
  __module__ = 'protobuf_messages_pb2'
  # @@protoc_insertion_point(class_scope:Discovery)
  ))
_sym_db.RegisterMessage(Discovery)

Identification = _reflection.GeneratedProtocolMessageType('Identification', (_message.Message,), dict(
  DESCRIPTOR = _IDENTIFICATION,
  __module__ = 'protobuf_messages_pb2'
  # @@protoc_insertion_point(class_scope:Identification)
  ))
_sym_db.RegisterMessage(Identification)

GatewayPort = _reflection.GeneratedProtocolMessageType('GatewayPort', (_message.Message,), dict(
  DESCRIPTOR = _GATEWAYPORT,
  __module__ = 'protobuf_messages_pb2'
  # @@protoc_insertion_point(class_scope:GatewayPort)
  ))
_sym_db.RegisterMessage(GatewayPort)

GatewayToDeviceMessage = _reflection.GeneratedProtocolMessageType('GatewayToDeviceMessage', (_message.Message,), dict(
  DESCRIPTOR = _GATEWAYTODEVICEMESSAGE,
  __module__ = 'protobuf_messages_pb2'
  # @@protoc_insertion_point(class_scope:GatewayToDeviceMessage)
  ))
_sym_db.RegisterMessage(GatewayToDeviceMessage)

DeviceToGatewayMessage = _reflection.GeneratedProtocolMessageType('DeviceToGatewayMessage', (_message.Message,), dict(
  DESCRIPTOR = _DEVICETOGATEWAYMESSAGE,
  __module__ = 'protobuf_messages_pb2'
  # @@protoc_insertion_point(class_scope:DeviceToGatewayMessage)
  ))
_sym_db.RegisterMessage(DeviceToGatewayMessage)


# @@protoc_insertion_point(module_scope)
