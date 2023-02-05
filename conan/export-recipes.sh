#!/bin/bash

find "$(pwd)/packages" -mindepth 1 -maxdepth 1 -type d -exec bash -c "cd {}; conan export ." \;
