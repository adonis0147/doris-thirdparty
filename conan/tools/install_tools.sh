#!/bin/bash

set -e

current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

mkdir -p build

pushd build >/dev/null

conan export "${current_dir}/../ninja"
conan install "${current_dir}" --profile="${current_dir}/../profiles/doris_default" --build=missing

popd >/dev/null
