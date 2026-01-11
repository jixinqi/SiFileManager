#!/usr/bin/env python3

import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent)

import environment as environment

from .builder_base import builder_base

class builder_imgui(builder_base):
    def __init__(self, env:environment.base):
        super().__init__("imgui", env)

    def __gen_cmake_files(self):
        import shutil

        pathlib.Path(self.module_pre_build_dir / "cmake").mkdir(parents=True, exist_ok=True)
        shutil.copy(
            pathlib.Path(__file__).parent / "build_spec" / "imgui" / "imguiConfig.cmake.in",
            self.module_pre_build_dir / "cmake" / "imguiConfig.cmake.in"
        )
        shutil.copy(
            pathlib.Path(__file__).parent / "build_spec" / "imgui" / "CMakeLists.txt",
            self.module_pre_build_dir / "CMakeLists.txt"
        )

    def build_impl(self):
        self.__gen_cmake_files()

        self.env.run_commands(
            commands = [
                f'cmake -B "{self.module_build_dir}"'
                    f' -S "{self.module_pre_build_dir}"'
                    f' -DCMAKE_INSTALL_PREFIX="{self.module_install_dir}"'

                    f' -DCMAKE_PREFIX_PATH="{self.module_install_dir.parent / "glfw" / "lib" / "cmake"}"'
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

