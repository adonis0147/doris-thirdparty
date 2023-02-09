import json
from conan.tools.files import save
from conan.tools.gnu import AutotoolsToolchain, AutotoolsDeps
from conans import python_requires

base = python_requires("cmake/3.25.2")


class CMakeConan(base.CMakeConan):
    name = "cmake"
    version = "3.25.2"
    default_user = "doris"
    default_channel = "thirdparty"


    def configure(self):
        self.options.bootstrap = True

    def generate(self):
        if self.options.bootstrap:
            tc = AutotoolsToolchain(self)
            tc.generate()
            tc = AutotoolsDeps(self)
            tc.generate()
            bootstrap_cmake_options = ["--"]
            bootstrap_cmake_options.append(f'-DCMAKE_CXX_STANDARD={"11" if not self.settings.compiler.cppstd else self.settings.compiler.cppstd}')
            if self.options.with_openssl:
                openssl = self.dependencies["openssl"]
                bootstrap_cmake_options.append("-DCMAKE_USE_OPENSSL=ON")
                bootstrap_cmake_options.append(f'-DOPENSSL_USE_STATIC_LIBS={"FALSE" if openssl.options.shared else "TRUE"}')
                bootstrap_cmake_options.append('-DOPENSSL_ROOT_DIR={}'.format(self.deps_cpp_info['openssl'].rootpath))
            else:
                bootstrap_cmake_options.append("-DCMAKE_USE_OPENSSL=OFF")
            save(self, "bootstrap_args", json.dumps({"bootstrap_cmake_options": ' '.join(arg for arg in bootstrap_cmake_options)}))
        else:
            base.CMakeConan.generate(self)

