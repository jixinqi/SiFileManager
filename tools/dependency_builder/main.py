#!/usr/bin/env python3

import builder
import platform

import environment

def main():
    env = None
    system = platform.system()
    if system == "Windows" : env = environment.win(build_type=environment.BuildType.DEBUG, link_type=environment.LinkType.STATIC)
    elif system == "Linux" : pass # to do
    else                   : return

    builder.boost(env).build()
    builder.glfw(env).build()

if(__name__ == "__main__"):
    main()
