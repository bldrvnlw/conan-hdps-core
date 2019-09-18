#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os

if __name__ == "__main__":

    builder = build_template_default.get_builder() 
    #for b in builder.items:
    #    b.settings["compiler.cppstd"] = 14    
    builder.run()
