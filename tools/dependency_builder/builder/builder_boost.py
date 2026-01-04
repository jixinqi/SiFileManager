#!/usr/bin/env python3

import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent)

import environment as environment

from .builder_base import builder_base

class builder_boost(builder_base):
    def __init__(self, env:environment.base):
        super().__init__("boost", env)

    def build_impl(self):
        bootstrap_cmd = ""
        if(isinstance(self.env, environment.win)): bootstrap_cmd = "bootstrap.bat"

        b2_cmd = f'b2 install --prefix="{self.module_install_dir}"'
        if(self.env.build_type == environment.BuildType.DEBUG): b2_cmd += " variant=debug"
        else:                                                   b2_cmd += " variant=release"

        if(self.env.link_type == environment.LinkType.STATIC):  b2_cmd += " link=static runtime-link=static"
        else:                                                   b2_cmd += " link=shared runtime-link=shared"

        self.env.run_commands(
            commands = [
                bootstrap_cmd,
                b2_cmd
            ],
            cwd = self.module_pre_build_dir,
            log_file = self.module_install_dir / f"build__{self.module_name}.log"
        )

def main():
    pass

if(__name__ == "__main__"):
    main()

