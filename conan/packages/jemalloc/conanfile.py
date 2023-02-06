from conan import ConanFile
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import apply_conandata_patches, export_conandata_patches
from conan.tools.gnu import AutotoolsToolchain, Autotools
from conan.tools.layout import basic_layout
from conans.client.tools import get


class JemallocConan(ConanFile):
    name = "jemalloc"
    version = "5.2.1"
    default_user = "doris"
    default_channel = "thirdparty"

    # Optional metadata
    license = "BSD-2-Clause"
    url = "https://github.com/apache/doris"
    description = "Jemalloc depended by Apache Doris"

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

    def export_sources(self):
        export_conandata_patches(self)

    def generate(self):
        VirtualBuildEnv(self).generate()

        at_toolchain = AutotoolsToolchain(self)
        at_toolchain.configure_args.append("--with-jemalloc-prefix=je")
        at_toolchain.configure_args.append("--enable-prof")
        at_toolchain.configure_args.append("--disable-cxx")
        at_toolchain.configure_args.append("--disable-libdl")
        at_toolchain.generate()

    def build(self):
        apply_conandata_patches(self)
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["jemalloc"]

