#!/bin/bash

set -e

current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

pushd "${current_dir}" >/dev/null

bash ./install-build-tools.sh
bash ./export-recipes.sh

mkdir -p build
cd build

profile="${current_dir}/profiles/doris_$(uname -s | awk '{ print(tolower($0)) }')"

conan install "${current_dir}" --build=missing --profile="${profile}"

arch="$(uname -m)"
if [[ "${arch}" == 'arm64' || "${arch}" == 'aarch64' ]]; then
	conanfile="${current_dir}/platforms/conanfile_arm64.txt"
else
	conanfile="${current_dir}/platforms/conanfile_$(uname -m).txt"
fi
conan install "${conanfile}" --build=missing --profile="${profile}"

popd >/dev/null
