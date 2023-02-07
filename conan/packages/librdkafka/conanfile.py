from conans import python_requires

base = python_requires("librdkafka/1.8.2")


class LibrdkafkaConan(base.LibrdkafkaConan):
    name = "librdkafka"
    version = "1.8.2"
    default_user = "doris"
    default_channel = "thirdparty"

