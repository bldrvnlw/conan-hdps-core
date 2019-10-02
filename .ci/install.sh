#!/usr/bin/env bash

set -ex

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    brew install cmake || brew upgrade cmake || true

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    pyenv install 3.7.1
    pyenv virtualenv 3.7.1 conan
    pyenv rehash
    pyenv activate conan
fi
# Add the citools to be able to set statuses on the original repo
pip install git+https://github.com/bldrvnlw/citools.git#egg=citools
pip install conan --upgrade
pip install conan_package_tools bincrafters_package_tools

conan user
