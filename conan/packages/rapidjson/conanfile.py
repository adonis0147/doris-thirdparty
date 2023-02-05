import os
from conans import ConanFile, tools


class RapidjsonConan(ConanFile):
    name = "rapidjson"
    version = "master"
    default_user = "doris"
    default_channel = "thirdparty"

    license = "MIT"
    url = "https://github.com/apache/doris"
    description = "RapidJSON depended by Apache Doris"

    no_copy_source = True

    def source(self):
        git = tools.Git(self.name)
        git.clone(self.conan_data["sources"]["url"])
        git.checkout(self.conan_data["sources"]["commit"])

    def package(self):
        self.copy("include/*", src=os.path.join(self.source_folder, self.name), dst=self.package_folder)

