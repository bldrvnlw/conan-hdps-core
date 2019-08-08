# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


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
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "core"
    _build_subfolder = "build_subfolder"

    requires = (
        "qt/5.12.4@bincrafters/stable"
    )
    print(os.environ)
    access_token = os.environ["BLDRVNLW_TOKEN"]
    validated_url = "https://{0}:{1}@github.com/hdps/core".format("bldrvnlw", access_token)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = self.url
        self.run("git clone {0}.git".format(self.validated_url))
        os.chdir("./{0}".format(self._source_subfolder))
        self.run("git checkout {0}".format(self.branch))
        os.chdir("..")

    def _configure_cmake(self):
        cmake = CMake(self)
        #cmake.definitions["BUILD_TESTS"] = False  # example
        #cmake.configure(build_folder=self._build_subfolder)
        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True            
        cmake.configure(source_folder="core")
        cmake.verbose = True
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
