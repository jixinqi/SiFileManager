#!/usr/bin/env python3

import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent)

import environment as environment

from .builder_base import builder_base

class builder_zstd(builder_base):
    def __init__(self, env:environment.base):
        super().__init__("zstd", env)

    def build_impl(self):
        self.env.run_commands(
            commands = [
                f'cmake -B "{self.module_build_dir}"'
                    f' -S "{self.module_pre_build_dir}"'
                    f' -DCMAKE_INSTALL_PREFIX="{self.module_install_dir}"'

                    f' -DZSTD_BUILD_CONTRIB=OFF'
                    f' -DZSTD_BUILD_TESTS=OFF'
                    f' -DZSTD_LEGACY_SUPPORT=OFF'
                    f' -DZSTD_BUILD_PROGRAMS=OFF'
                    f' -DZSTD_PROGRAMS_LINK_SHARED=OFF'
                    f' -DZSTD_BUILD_SHARED=OFF'
                    f' -DZSTD_BUILD_STATIC=ON'
                    f' -DZSTD_MULTITHREAD_SUPPORT=ON'
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

