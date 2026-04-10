#!/usr/bin/env python3

import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent)

import environment as environment

from .builder_base import builder_base

class builder_zlib(builder_base):
    def __init__(self, env:environment.base):
        super().__init__("zlib", env)

    def build_impl(self):
        build_args = ""
        if(self.env.link_type == environment.LinkType.STATIC):
            build_args += " -DZLIB_BUILD_SHARED=OFF -DZLIB_BUILD_STATIC=ON"
        elif(self.env.link_type == environment.LinkType.DYNAMIC):
            build_args += " -DZLIB_BUILD_SHARED=ON  -DZLIB_BUILD_STATIC=OFF"

        self.env.run_commands(
            commands = [
                f'cmake -B "{self.module_build_dir}"'
                    f' -S "{self.module_pre_build_dir}"'
                    f' -DCMAKE_INSTALL_PREFIX="{self.module_install_dir}"'

                    f' -DCMAKE_CXX_FLAGS_INIT="/utf-8"'

                    f' -DZLIB_BUILD_TESTING=OFF'
                    f'{build_args}'
                    ,
                f'cmake --build   "{self.module_build_dir}" --config={self.env.build_type.value} -j',
                f'cmake --install "{self.module_build_dir}" --config={self.env.build_type.value}',
            ],
            cwd = self.module_pre_build_dir,
            log_file = self.module_install_dir / f"build__{self.module_name}.log"
        )

def main():
    pass

if(__name__ == "__main__"):
    main()

