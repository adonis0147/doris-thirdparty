from conan import ConanFile
from conan.tools.files.files import collect_libs, rm
from conan.tools.gnu import AutotoolsToolchain, Autotools
from conan.tools.layout import basic_layout
from conans.client.tools import get


class GperftoolsConan(ConanFile):
    name = "gperftools"
    version = "2.10"
    default_user = "doris"
    default_channel = "thirdparty"

    # Optional metadata
    license = "BSD-3-Clause"
    url = "https://github.com/apache/doris"
    description = "gperftools depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        basic_layout(self)

    def source(self):
        get(**self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        at_toolchain = AutotoolsToolchain(self)
        at_toolchain.configure_args.append("--disable-libunwind")
        at_toolchain.configure_args.append("--enable-frame-pointers")
        at_toolchain.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

        rm(self, "*.la", self.package_folder, recursive=True)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Gperftools")
        self.cpp_info.set_property("cmake_target_name", "Gperftools::Gperftools")
        self.cpp_info.set_property("cmake_find_mode", "both")
        for lib in collect_libs(self):
            self.cpp_info.components[lib].set_property("cmake_target_name", "Gperftools::{}".format(lib))
            self.cpp_info.components[lib].libs = [lib]

