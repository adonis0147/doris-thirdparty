import os
from conan import ConanFile
from conan.tools.gnu import AutotoolsToolchain, Autotools, AutotoolsDeps
from conan.tools.layout import basic_layout
from conans.client.tools import get
from conans.tools import unix_path


class TexinfoConan(ConanFile):
    name = "texinfo"
    version = "7.0.2"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = "libgettext/0.21"

    # Optional metadata
    license = "GPL-3.0-or-later"
    url = "https://github.com/apache/doris"
    description = "Texinfo depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        basic_layout(self)

    def source(self):
        get(**self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        libiconv_prefix = unix_path(self.deps_cpp_info["libiconv"].rootpath)

        at_toolchain = AutotoolsToolchain(self)
        at_toolchain.configure_args.append("--with-libiconv-prefix={}".format(libiconv_prefix))
        at_toolchain.generate()

        deps = AutotoolsDeps(self)
        deps.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.buildenv_info.prepend_path("PATH", bindir)
        self.buildenv_info.define("MAKEINFO", unix_path(os.path.join(bindir, "makeinfo")))

