#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os

if __name__ == "__main__":

    builder = build_template_default.get_builder()
    # force the build items to use c++14
    adjusted_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        settings["compiler.cppstd"] = "14"
        adjusted_builds.append([settings, options, env_vars, build_requires, reference])
    builder.items = adjusted_builds    
    builder.run()
