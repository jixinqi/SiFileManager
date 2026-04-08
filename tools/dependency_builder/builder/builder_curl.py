#!/usr/bin/env python3

import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent)

import environment as environment

from .builder_base import builder_base

class builder_curl(builder_base):
    def __init__(self, env:environment.base):
        super().__init__("curl", env)

    def build_impl(self):
        self.env.run_commands(
            commands = [
                f'cmake -B "{self.module_build_dir}"'
                    f' -S "{self.module_pre_build_dir}"'
                    f' -DCMAKE_INSTALL_PREFIX="{self.module_install_dir}"'
                    f' -DCMAKE_CXX_FLAGS_INIT="/utf-8"'

                    f' -DBUILD_SHARED_LIBS='       f'OFF'
                    f' -DBUILD_STATIC_LIBS='       f'ON'
                    f' -DBUILD_TESTING='           f'ON'
                    f' -DCURL_TEST_BUNDLES='       f'ON'

                    f' -DCURL_USE_LIBPSL='         f'ON'
                    f' -DLIBPSL_INCLUDE_DIR='      f'"{ self.module_install_dir.parent / "libpsl"  / "include" }"'
                    f' -DLIBPSL_LIBRARY='          f'"{ self.module_install_dir.parent / "libpsl"  / "lib" / "psl.lib" }"'
                    f' -D_libpsl_CFLAGS='          f'"-DPSL_API="'
                    ,
                f'cmake --build   "{self.module_build_dir}" --config={self.env.build_type.value}',
                f'cmake --install "{self.module_build_dir}" --config={self.env.build_type.value}'
            ],
            cwd = self.module_pre_build_dir,
            log_file = self.module_install_dir / f"build__{self.module_name}.log"
        )

def main():
    pass

if(__name__ == "__main__"):
    main()

