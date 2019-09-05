# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import json


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

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "core"
    _build_subfolder = "build_subfolder"
    install_dir = None
    this_dir = os.path.dirname(os.path.realpath(__file__))

    requires = (
        "qt/5.12.2@bvanlew/stable",
        "bzip2/1.0.8@conan/stable"
    )
    #print(os.environ)
    access_token = os.environ["CONAN_BLDRVNLW_TOKEN"]
    validated_url = "https://{0}:{1}@github.com/hdps/core".format("bldrvnlw", access_token)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def _get_commit_sha(self, file_name):
        commit_sha = ""
        with open(file_name) as json_f:
            commit_info = json.load(json_f)
            commit_sha = ["head_commit"]["id"]
        return commit_sha
        
    
    def source(self):
        source_url = self.url
        self.run("git clone {0}.git".format(self.validated_url))
        os.chdir("./{0}".format(self._source_subfolder))
        commit_sha = self._get_commit_sha(os.path.join(os.getcwd(), "build_trigger.json"))
        self.run("git checkout {0}".format(commit_sha))
        os.chdir("..")
        with open("core/CMakeLists.txt",'r') as viewFileOpen:
            data = viewFileOpen.read()
        print(data)

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True            
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
