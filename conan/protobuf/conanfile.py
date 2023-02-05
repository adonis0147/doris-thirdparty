from conans import python_requires
from conan.tools.files import copy

base = python_requires("protobuf/3.15.8")

class ProtobufConan(base.ProtobufConan):
    version = "3.15.0"
    default_user = "doris"
    default_channel = "thirdparty"

