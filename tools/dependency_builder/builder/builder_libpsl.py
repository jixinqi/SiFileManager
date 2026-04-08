#!/usr/bin/env python3

import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent)

import shutil

import environment as environment

from .builder_base import builder_base

class builder_libpsl(builder_base):
    def __init__(self, env:environment.base):
        super().__init__("libpsl", env)

    def __generate_suffixes_dafsa_h(self):
        self.env.run_commands(
            commands = [
                "python3 src/psl-make-dafsa --output-format=cxx+ list/public_suffix_list.dat suffixes_dafsa.h",
            ],
            cwd = self.module_pre_build_dir,
            log_file = self.module_install_dir / f"build__{self.module_name}.log"
        )

    def __generate_libpsl_h(self):
        psl_version        = ""
        psl_version_major  = ""
        psl_version_minor  = ""
        psl_version_patch  = ""
        psl_version_number = ""

        with open(self.module_pre_build_dir / "version.txt") as version_file:
            psl_version = version_file.read().strip()
            psl_version_major, psl_version_minor, psl_version_patch = psl_version.split(".")
            psl_version_number = f"0x{int(psl_version_major):02X}{int(psl_version_minor):02X}{int(psl_version_patch):02X}"

        libpsl_h_content = ""
        with open(self.module_pre_build_dir / "include" / "libpsl.h.in") as libpsl_h_in_file:
            libpsl_h_in_file_lines = libpsl_h_in_file.readlines()
            for line in libpsl_h_in_file_lines:
                line = line.replace("@LIBPSL_VERSION@",        f"{psl_version}")
                line = line.replace("@LIBPSL_VERSION_MAJOR@",  f"{psl_version_major}")
                line = line.replace("@LIBPSL_VERSION_MINOR@",  f"{psl_version_minor}")
                line = line.replace("@LIBPSL_VERSION_PATCH@",  f"{psl_version_patch}")
                line = line.replace("@LIBPSL_VERSION_NUMBER@", f"{psl_version_number}")
                libpsl_h_content += line

        with open(self.module_pre_build_dir / "include" / "libpsl.h", "w") as libpsl_h_file:
            libpsl_h_file.write(libpsl_h_content)

    def __generate_cmake_file(self):
        shutil.copy(
            pathlib.Path(__file__).parent / "build_spec" / "libpsl" / "CMakeLists.txt",
            self.module_pre_build_dir / "CMakeLists.txt"
        )

    def build_impl(self):
        self.__generate_suffixes_dafsa_h()
        self.__generate_libpsl_h()
        self.__generate_cmake_file()

        self.env.run_commands(
            commands = [
                f'cmake -B "{self.module_build_dir}"'
                    f' -S "{self.module_pre_build_dir}"'
                    f' -DCMAKE_INSTALL_PREFIX="{self.module_install_dir}"'

                    f' -DCMAKE_CXX_FLAGS_INIT="/utf-8"'
                    ,
                f'cmake --build   "{self.module_build_dir}" --config={self.env.build_type.value} -j',
                f'cmake --install "{self.module_build_dir}" --config={self.env.build_type.value}'
            ],
            cwd = self.module_pre_build_dir,
            log_file = self.module_install_dir / f"build__{self.module_name}.log"
        )

def main():
    pass

if(__name__ == "__main__"):
    main()

