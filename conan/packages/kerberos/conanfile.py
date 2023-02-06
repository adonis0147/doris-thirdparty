
import os

from conan import ConanFile
from conan.tools.files.files import collect_libs
from conan.tools.gnu import AutotoolsToolchain, Autotools, AutotoolsDeps
from conan.tools.layout import basic_layout
from conans.client.tools import get, unix_path
from conans import AutoToolsBuildEnvironment


class Krb5Conan(ConanFile):
    name = "krb5"
    version = "1.19"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = "bison/3.8.2", "openssl/1.1.1s"

    # Optional metadata
    license = "<Put the package license here>"
    url = "https://github.com/apache/doris"
    description = "Krb5 depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        basic_layout(self)

    def source(self):
        get(**self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.flags.append("-fcommon")
        env_build.configure(unix_path(os.path.join(self.source_folder, "src")),
                            ["--enable-static", "--disable-shared", "--with-crypto-impl=openssl"])
        env_build.make()
        env_build.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Krb5")
        self.cpp_info.set_property("cmake_target_name", "Krb5::Krb5")
        self.cpp_info.set_property("cmake_find_mode", "both")
        for lib in collect_libs(self):
            self.cpp_info.components[lib].set_property("cmake_target_name", "Krb5::{}".format(lib))
            self.cpp_info.components[lib].libs = [lib]

