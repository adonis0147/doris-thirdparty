import os
from conan.tools.files import rm
from conans import python_requires
from conans.client.tools import unix_path
from conans.client.tools.files import replace_in_file

base = python_requires("rocksdb/6.0.2")


class RocksdbConan(base.RocksDB):
    version = "5.14.2"
    default_user = "doris"
    default_channel = "thirdparty"

    def _patch_sources(self):
        base.RocksDB._patch_sources(self)
        replace_in_file(unix_path(os.path.join(self._source_subfolder, "CMakeLists.txt")), 
                        "LZ4_INCLUDE_DIR", "lz4_INCLUDE_DIR")
        replace_in_file(unix_path(os.path.join(self._source_subfolder, "CMakeLists.txt")), 
                        "LZ4_LIBRARIES", "lz4_LIBRARIES")
        replace_in_file(unix_path(os.path.join(self._source_subfolder, "CMakeLists.txt")), 
                        "SNAPPY_INCLUDE_DIR", "Snappy_INCLUDE_DIR")
        replace_in_file(unix_path(os.path.join(self._source_subfolder, "CMakeLists.txt")), 
                        "SNAPPY_LIBRARIES", "Snappy_LIBRARIES")

    def package(self):
        base.RocksDB.package(self)

        if self.options.shared == False:
            rm(self, "*.dylib", self.package_folder, recursive=True)
            rm(self, "*.so", self.package_folder, recursive=True)

