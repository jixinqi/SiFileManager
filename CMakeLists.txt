cmake_minimum_required(VERSION 3.15)

project(SiFileManager)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(GLOB _third_party_children RELATIVE "${THIRD_PARTY_DIR}" "${THIRD_PARTY_DIR}/*")
foreach(_child ${_third_party_children})
    if(IS_DIRECTORY "${THIRD_PARTY_DIR}/${_child}")
        list(APPEND CMAKE_PREFIX_PATH "${THIRD_PARTY_DIR}/${_child}")
    endif()
endforeach()
find_package(Boost CONFIG REQUIRED COMPONENTS system filesystem)
find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)
find_package(imgui REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(spdlog REQUIRED)

add_executable(${PROJECT_NAME}
    src/sifm/window/window_main.cpp
    src/sifm/imgui_components/backend_base.cpp
    src/sifm/imgui_components/backend_glfw_opengl3.cpp
    src/sifm/auto_increment_id.cpp
    src/sifm/config.cpp
    src/sifm/environment.cpp
    src/sifm/log.cpp
    src/main.cpp
)
target_include_directories(${PROJECT_NAME}
    PRIVATE
        src/sifm/imgui_components/
        src/sifm/
        src/
)
target_link_libraries(${PROJECT_NAME}
    PRIVATE
        Boost::system
        Boost::filesystem
        imgui::core
        imgui::backend::glfw_opengl3
        nlohmann_json::nlohmann_json
        spdlog::spdlog
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
