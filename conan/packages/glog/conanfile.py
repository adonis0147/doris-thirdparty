from conans import python_requires

base = python_requires("glog/0.4.0")

class GlogConan(base.GlogConan):
    version = "0.4.0"
    default_user = "doris"
    default_channel = "thirdparty"

