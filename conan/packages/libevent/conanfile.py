from conans import python_requires


base = python_requires("libevent/2.1.12")

class LibeventConan(base.LibeventConan):
    version = "2.1.12"
    default_user = "doris"
    default_channel = "thirdparty"

