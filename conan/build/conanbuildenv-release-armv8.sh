echo "echo Restoring environment" > "/Users/adonis/Programs/doris-thirdparty/conan/build/deactivate_conanbuildenv-release-armv8.sh"
for v in PATH LD_LIBRARY_PATH DYLD_LIBRARY_PATH M4 PKG_CONFIG AUTOMAKE_CONAN_INCLUDES AC_MACRODIR autom4te_perllibdir AUTOCONF AUTORECONF AUTOHEADER AUTOM4TE
do
    is_defined="true"
    value=$(printenv $v) || is_defined="" || true
    if [ -n "$value" ] || [ -n "$is_defined" ]
    then
        echo export "$v='$value'" >> "/Users/adonis/Programs/doris-thirdparty/conan/build/deactivate_conanbuildenv-release-armv8.sh"
    else
        echo unset $v >> "/Users/adonis/Programs/doris-thirdparty/conan/build/deactivate_conanbuildenv-release-armv8.sh"
    fi
done


export PATH="/Users/adonis/.conan/data/libtool/2.4.7/_/_/package/163e4a3bdfbcfb21964a0ca9aad051981ad600e2/bin:/Users/adonis/.conan/data/automake/1.16.5/_/_/package/3c28ba69276b46fd46e9c2060ba991d725ccab43/bin:/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/bin:/Users/adonis/.conan/data/m4/1.4.19/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin:/Users/adonis/.conan/data/cmake/3.25.1/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin:/Users/adonis/.conan/data/pkgconf/1.9.3/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin:/Users/adonis/.conan/data/make/4.3/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin:$PATH"
export LD_LIBRARY_PATH="/Users/adonis/.conan/data/libtool/2.4.7/_/_/package/163e4a3bdfbcfb21964a0ca9aad051981ad600e2/lib:$LD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH="/Users/adonis/.conan/data/libtool/2.4.7/_/_/package/163e4a3bdfbcfb21964a0ca9aad051981ad600e2/lib:$DYLD_LIBRARY_PATH"
export M4="/Users/adonis/.conan/data/m4/1.4.19/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin/m4"
export PKG_CONFIG="/Users/adonis/.conan/data/pkgconf/1.9.3/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin/pkgconf"
export AUTOMAKE_CONAN_INCLUDES="/Users/adonis/.conan/data/pkgconf/1.9.3/_/_/package/3eb32b976fb0626f3c40a8b87ace72156aa44204/bin/aclocal:$AUTOMAKE_CONAN_INCLUDES"
export AC_MACRODIR="/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/res/autoconf"
export autom4te_perllibdir="/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/res/autoconf"
export AUTOCONF="/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/bin/autoconf"
export AUTORECONF="/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/bin/autoreconf"
export AUTOHEADER="/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/bin/autoheader"
export AUTOM4TE="/Users/adonis/.conan/data/autoconf/2.71/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/bin/autom4te"