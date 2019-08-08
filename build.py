#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os

if __name__ == "__main__":

    builder = build_template_default.get_builder()
    print('In python vuild.py, token: ', os.environ["BLDRVNLW_TOKEN"]
    # pass access token to the docker conan runner
    builder.add({"BLDRVNLW_TOKEN": os.environ["BLDRVNLW_TOKEN"]})
    builder.run()
