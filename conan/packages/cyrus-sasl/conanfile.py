from conans import python_requires
from conans.errors import ConanInvalidConfiguration
from conan.tools.files.patches import apply_conandata_patches, export_conandata_patches

base = python_requires("cyrus-sasl/2.1.27")


class CyrusSaslConan(base.CyrusSaslConan):
    name = "cyrus-sasl"
    version = "2.1.27"
    default_user = "doris"
    default_channel = "thirdparty"

    def validate(self):
        if self.info.settings.os == "Windows":
            raise ConanInvalidConfiguration("Cyrus SASL package is not compatible with Windows yet.")

    def requirements(self):
        base.CyrusSaslConan.requirements(self)
        if self.options.with_gssapi:
            self.requires("krb5/1.19")

    def export_sources(self):
        export_conandata_patches(self)
    
    def _patch_sources(self):
        base.CyrusSaslConan._patch_sources(self)
        apply_conandata_patches(self)

