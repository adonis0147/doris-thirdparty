from conan import ConanFile
from conan.tools.env import VirtualBuildEnv
from conan.tools.files.files import collect_libs, rm
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.layout import basic_layout
from conans.client.tools import get


class BinutilsConan(ConanFile):
    name = "binutils"
    version = "2.39"
    default_user = "doris"
    default_channel = "thirdparty"

    build_requires = "bison/3.8.2", "texinfo/7.0.2@doris/thirdparty"

    # Optional metadata
    license = "GPL-3.0-or-later"
    url = "https://github.com/apache/doris"
    description = "Binutils depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        basic_layout(self)

    def source(self):
        get(**self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        VirtualBuildEnv(self).generate()

        at_toolchain = AutotoolsToolchain(self)
        at_toolchain.configure_args.append("--enable-install-libiberty")
        at_toolchain.configure_args.append("--without-msgpack")
        at_toolchain.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install(target="install-bfd install-libiberty install-binutils")
        
        rm(self, "*.la", self.package_folder, recursive=True)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Binutils")
        self.cpp_info.set_property("cmake_target_name", "Binutils::Binutils")
        self.cpp_info.set_property("cmake_find_mode", "both")
        for lib in collect_libs(self):
            self.cpp_info.components[lib].set_property("cmake_target_name", "Binutils::{}".format(lib))
            self.cpp_info.components[lib].libs = [lib]

