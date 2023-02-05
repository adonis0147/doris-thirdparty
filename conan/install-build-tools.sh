#!/bin/bash

set -e

current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

mkdir -p build

pushd build >/dev/null

conan export "${current_dir}/packages/ninja"

temp_folder=$(mktemp -d)
# shellcheck disable=2064
trap "rm -rf ${temp_folder}" EXIT

cat >"${temp_folder}/conanfile.txt" <<EOF
[requires]
EOF

conan install "${temp_folder}" --profile="${current_dir}/profiles/doris_default" --build=missing

popd >/dev/null
