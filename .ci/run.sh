#!/usr/bin/env bash

set -ex

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
    export CONAN_CMAKE_PROGRAM=`which cmake`
    cmake --version
fi

python -c "from citools.githubtools import set_build_status, State; set_build_status('build_trigger.json', '$CONAN_BLDRVNLW_TOKEN', '$TRAVIS_BUILD_WEB_URL', 'Travis', State.pending)"
python build.py
