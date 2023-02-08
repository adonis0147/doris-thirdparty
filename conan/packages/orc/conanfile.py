from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files.patches import apply_conandata_patches, export_conandata_patches
from conans.client.tools import get


class OrcConan(ConanFile):
    name = "orc"
    version = "1.7.2"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = "protobuf/3.21.9", "snappy/1.1.9", "lz4/1.9.4", "zlib/1.2.13", "zstd/1.5.2"

    # Optional metadata
    license = "Apache-2.0"
    url = "https://github.com/apache/doris"
    description = "Liborc depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(**self.conan_data["sources"][self.version], strip_root=True)

    def export_sources(self):
        export_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_JAVA"] = "OFF"
        tc.variables["BUILD_LIBHDFSPP"] = "OFF"
        tc.variables["BUILD_CPP_TESTS"] = "OFF"
        tc.variables["STOP_BUILD_ON_WARNING"] = "OFF"
        tc.variables["SNAPPY_HOME"] = self.deps_cpp_info["snappy"].rootpath
        tc.variables["ZLIB_HOME"] = self.deps_cpp_info["zlib"].rootpath
        tc.variables["ZSTD_HOME"] = self.deps_cpp_info["zstd"].rootpath
        tc.variables["LZ4_HOME"] = self.deps_cpp_info["lz4"].rootpath
        tc.variables["PROTOBUF_HOME"] = self.deps_cpp_info["protobuf"].rootpath
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "ORC")
        self.cpp_info.set_property("cmake_target_name", "ORC::ORC")
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.libs = ["orc"]

