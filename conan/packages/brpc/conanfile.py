import os
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, replace_in_file
from conans.client.tools import unix_path


class BrpcConan(ConanFile):
    name = "brpc"
    version = "1.2.0"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = 'protobuf/3.21.9', 'leveldb/1.23', 'gflags/2.2.2', 'openssl/1.1.1s'

    # Optional metadata
    license = "Apache-2.0"
    url = "https://github.com/apache/doris"
    description = "Apache bRPC depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False], 
        "fPIC": [True, False], 
        "with_glog": [True, False],
        "build_tools": [True, False]}

    default_options = {
        "shared": False, 
        "fPIC": True, 
        "with_glog": False,
        "build_tools": False,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def requirements(self):
        if self.options.with_glog:
            self.requires("glog/0.6.0")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["gflags"].nothreads = False

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)

    def export_sources(self):
        export_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["WITH_GLOG"] = "ON" if self.options.with_glog else "OFF"
        tc.variables["BUILD_BRPC_TOOLS"] = "ON" if self.options.build_tools else "OFF"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Brpc")
        self.cpp_info.set_property("cmake_target_name", "Brpc::Brpc")
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.libs = ["brpc"]

