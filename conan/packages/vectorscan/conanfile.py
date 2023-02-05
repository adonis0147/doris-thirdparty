from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, collect_libs, export_conandata_patches, get
from conans.errors import ConanInvalidConfiguration


class VectorscanConan(ConanFile):
    name = "vectorscan"
    version = "5.4.7"
    default_user = "doris"
    default_channel = "thirdparty"

    requires = "boost/1.73.0"
    build_requires = "pkgconf/1.9.3", "ragel/6.10"

    # Optional metadata
    license = "BSD-3-Clause"
    url = "https://github.com/apache/doris"
    description = "Vectorscan depended by Apache Doris"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def validate(self):
        if not self.settings.arch.value.startswith("arm"):
            raise ConanInvalidConfiguration("Vectorscan only supports arm architecture")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)

    def export_sources(self):
        export_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(cli_args=["-DBUILD_EXAMPLES=OFF"])
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Vectorscan")
        self.cpp_info.set_property("cmake_target_name", "Vectorscan::Vectorscan")
        self.cpp_info.set_property("cmake_find_mode", "both")
        for lib in collect_libs(self):
            self.cpp_info.components[lib].set_property("cmake_target_name", "Vectorscan::{}".format(lib))
            self.cpp_info.components[lib].libs = [lib]

