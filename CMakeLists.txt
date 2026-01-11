cmake_minimum_required(VERSION 3.15)

project(SiFileManager)

list(APPEND CMAKE_PREFIX_PATH
    "${GLFW_CMAKE_PREFIX}"
    "${IMGUI_CMAKE_PREFIX}"
)

find_package(OpenGL REQUIRED)

find_package(glfw3 REQUIRED)
find_package(imgui REQUIRED)

add_executable(${PROJECT_NAME}
    src/main.cpp
)
target_link_libraries(${PROJECT_NAME}
    PRIVATE
        imgui::core
        imgui::backend::glfw_opengl3
)
target_compile_options(SiFileManager PRIVATE /utf-8)


################################################################################
# LOG begin
# [[#
message(STATUS "================================================================================")
get_cmake_property(_variableNames VARIABLES)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()
message(STATUS "================================================================================")
#]]#
# LOG end
################################################################################
