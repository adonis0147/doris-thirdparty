from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake, cmake_layout
from conan.tools.files.patches import apply_conandata_patches, export_conandata_patches
from conans.client.tools import collect_libs, get


class ArrowConan(ConanFile):
    name = "arrow"
    version = "7.0.0"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = ("thrift/0.13.0", "orc/1.7.2@doris/thirdparty", "glog/0.4.0@doris/thirdparty", "gflags/2.2.2",
                "re2/20210202", "boost/1.73.0")

    # Optional metadata
    license = "Apache-2.0"
    url = "https://github.com/apache/doris"
    description = "Libarrow depended by Apache Doris"

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
        tc.variables["ARROW_BUILD_SHARED"] = "OFF"
        tc.variables["ARROW_PARQUET"] = "ON"
        tc.variables["ARROW_ORC"] = "ON"
        tc.variables["ARROW_JSON"] = "ON"
        tc.variables["ARROW_ZSTD_USE_SHARED"] = "OFF"
        tc.variables["ARROW_PROTOBUF_USE_SHARED"] = "OFF"
        tc.variables["ARROW_WITH_BROTLI"] = "ON"
        tc.variables["Brotli_SOURCE"] = "BUNDLED"
        tc.variables["ARROW_BROTLI_USE_SHARED"] = "OFF"
        tc.variables["utf8proc_SOURCE"] = "BUNDLED"
        tc.variables["ARROW_UTF8PROC_USE_SHARED"] = "OFF"
        tc.variables["ARROW_USE_GLOG"] = "ON"
        tc.variables["ARROW_BOOST_REQUIRED"] = "ON"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder="cpp")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Arrow")
        self.cpp_info.set_property("cmake_target_name", "Arrow::Arrow")
        self.cpp_info.set_property("cmake_find_mode", "both")
        for lib in collect_libs(self):
            if lib == "arrow_bundled_dependencies":
                self.cpp_info.components[lib].set_property("cmake_target_name", "Arrow::bundled_dependencies")
            else:
                self.cpp_info.components[lib].set_property("cmake_target_name", "Arrow::{}".format(lib))
            self.cpp_info.components[lib].libs = [lib]

