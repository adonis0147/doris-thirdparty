#!/bin/bash

find "$(pwd)" -mindepth 1 -maxdepth 1 -type d \
	! -name 'build' ! -name 'profiles' ! -name 'tools' \
	-exec bash -c "cd {}; conan export ." \;
