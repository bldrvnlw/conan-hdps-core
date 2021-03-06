# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import json
import subprocess


class HdpsCoreConan(ConanFile):
    name = "hdps-core"
    version = "0.1.0"
    description = "Core libraries and plugind for the High Dimensional Plugin System a.k.a. TBD"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "analysis", "n-dimensional", "plugin")
    url = "https://github.com/hdps/core"
    branch = "develop"  # should come from profile
    author = "B. van Lew <b.van_lew@lumc.nl>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt", "build_trigger.json"]
    generators = "cmake"

    # Options may need to change depending on the packaged library
    settings = {"os": None, "build_type": None, "compiler": None, "arch": None}
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "core"
    _build_subfolder = "build_subfolder"
    install_dir = None
    this_dir = os.path.dirname(os.path.realpath(__file__))

    requires = (
        "qt/5.14.2@lkeb/stable",
        "bzip2/1.0.8@conan/stable"
    )
    #print(os.environ)
    access_token = os.environ["CONAN_BLDRVNLW_TOKEN"]
    validated_url = "https://{0}:{1}@github.com/hdps/core".format("bldrvnlw", access_token)
# "libssl-dev", "libxcursor-dev", "libxcomposite-dev", "libxdamage-dev", "libxrandr-dev", "libdbus-1-dev", "libfontconfig1-dev", "libcap-dev", "libxtst-dev", "libpulse-dev", "libudev-dev", "libpci-dev", "libnss3-dev", "libasound2-dev", "libxss-dev", "libegl1-mesa-dev", "gperf", "bison"])       

    def system_requirements(self):
        if tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                installer.install('mesa-common-dev')
                installer.install('libgl1-mesa-dev')
                installer.install('libxcomposite-dev')
                installer.install('libxcursor-dev')
                installer.install('libxi-dev')
                installer.install('libnss3-dev')
                installer.install('libnspr4-dev')
                installer.install('libfreetype6-dev')
                installer.install('libfontconfig1-dev')
                installer.install('libxtst-dev')
                installer.install('libasound2-dev')
                installer.install('libdbus-1-dev')
                min_cmake_version = os.environ.get('CONAN_MINIMUM_CMAKE_VERSION')
                if min_cmake_version is not None:
                    subprocess.run(f"pip3 install cmake>={min_cmake_version}".split())
                    print('Path is: ', os.environ['PATH'])
                    result = subprocess.run("which cmake".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    os.environ['CONAN_CMAKE_PROGRAM'] = result.stdout.decode('utf-8').rstrip()
                    print(f'Cmake at {os.environ["CONAN_CMAKE_PROGRAM"]}')
        if tools.os_info.is_macos: 
            installer = tools.SystemPackageTool()    
            installer.install('libomp')              
                
    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def _get_commit_sha(self, file_name):
        commit_sha = ""
        with open(file_name) as json_f:
            commit_info = json.load(json_f)
            commit_sha = commit_info["head_commit"]["id"]
        return commit_sha     
    
    def source(self):
        source_url = self.url
        commit_sha = self._get_commit_sha("build_trigger.json")
        self.run("git clone {0}.git".format(self.validated_url))
        os.chdir("./{0}".format(self._source_subfolder))                       
        self.run("git checkout {0}".format(commit_sha))
        self.run("git submodule init && git submodule sync && git submodule update")                             
        os.chdir("..")
        with open("core/CMakeLists.txt",'r') as viewFileOpen:
            data = viewFileOpen.read()
        print(data)

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            # cmake.definitions["CMAKE_CXX_STANDARD"] = 14
            cmake.definitions["CMAKE_CXX_STANDARD_REQUIRED"] = "ON"
        cmake.configure(source_folder="core")
        cmake.verbose = True
        return cmake

    def build(self):
        # If the user has no preference in HDPS_INSTALL_DIR simply set the install dir
        if not os.environ.get('HDPS_INSTALL_DIR', None):
            os.environ['HDPS_INSTALL_DIR'] = os.path.join(self.build_folder, "install")
        print('HDPS_INSTALL_DIR: ', os.environ['HDPS_INSTALL_DIR']) 
        self.install_dir = os.environ['HDPS_INSTALL_DIR']
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        self.copy(pattern="*", src=os.path.join(self.install_dir, 'Release'))


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
