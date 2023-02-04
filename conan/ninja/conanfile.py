import os
from conan import ConanFile, conan_version
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import copy, get
from conan.tools.scm import Version

required_conan_version = ">=1.52.0"


class NinjaConan(ConanFile):
    name = "ninja"
    version = "1.11.1"

    build_requires = "cmake/3.25.1"

    package_type = "application"
    description = "Ninja is a small build system with a focus on speed"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/ninja-build/ninja"
    topics = ("ninja", "build")
    settings = "os", "arch", "compiler", "build_type"

    def layout(self):
        cmake_layout(self, src_folder="src")

    def package_id(self):
        del self.info.settings.compiler

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def configure(self):
        self.options["cmake"].bootstrap = True
        self.options["cmake"].with_openssl = False

    def generate(self):
        VirtualBuildEnv(self).generate()

        tc = CMakeToolchain(self)
        tc.variables["BUILD_TESTING"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "COPYING", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

        self.buildenv_info.define("CONAN_CMAKE_GENERATOR", "Ninja")

        # TODO: to remove in conan v2
        if Version(conan_version).major < 2:
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            self.env_info.CONAN_CMAKE_GENERATOR = "Ninja"
