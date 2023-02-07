import os
from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake, cmake_layout
from conan.tools.files.files import mkdir, rename, replace_in_file
from conan.tools.files.patches import apply_conandata_patches, export_conandata_patches
from conans.client.tools import get, unix_path

class LibmysqlclientConan(ConanFile):
    name = "libmysqlclient"
    version = "5.7.18"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = "zlib/1.2.13", "boost/1.73.0"

    # Optional metadata
    license = "GPL-2.0-only with Universal-FOSS-exception-1.0"
    url = "https://github.com/apache/doris"
    description = "Libmysqlclient depended by Apache Doris"

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
        tc.variables["WITHOUT_SERVER"] = "ON"
        tc.variables["WITH_BOOST"] = self.deps_cpp_info["boost"].rootpath
        tc.variables["LOCAL_BOOST_DIR"] = self.deps_cpp_info["boost"].rootpath
        tc.variables["WITH_ZLIB"] = self.deps_cpp_info["zlib"].rootpath
        tc.variables["DISABLE_SHARED"] = "ON"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build(target="mysqlclient")

    def _patch_sources(self):
        apply_conandata_patches(self)

        replace_in_file(self, unix_path(os.path.join(self.source_folder, "cmake", "boost.cmake")),
                        "NOT BOOST_MINOR_VERSION EQUAL 59", "NOT BOOST_MINOR_VERSION EQUAL 73")

    def package(self):
        self.run("cmake --install libmysql")
        self.run("cmake --install include")
        include_folder = unix_path(os.path.join(self.package_folder, "include"))
        mysql_folder = unix_path(os.path.join(self.package_folder, "mysql"))
        rename(self, include_folder, mysql_folder)
        mkdir(self, include_folder)
        rename(self, mysql_folder, unix_path(os.path.join(include_folder, "mysql")))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "LibMySQLClient")
        self.cpp_info.set_property("cmake_target_name", "LibMySQLClient::LibMySQLClient")
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.libs = ["mysqlclient"]

