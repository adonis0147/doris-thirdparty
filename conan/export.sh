#!/bin/bash

find "$(pwd)" -mindepth 1 -maxdepth 1 -type d ! -name 'build' -exec bash -c "cd {}; conan export ." \;
