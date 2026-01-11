cmake_minimum_required(VERSION 3.15)

project(imgui
    VERSION 1.0.0
    LANGUAGES CXX
)

include(GNUInstallDirs)
include(CheckIncludeFile)
include(CheckLibraryExists)
include(CMakePackageConfigHelpers)

set(${PROJECT_NAME}_LIB_TARGETS "")
set(${PROJECT_NAME}_EXE_TARGETS "")

# ============================================================
# Common paths
# ============================================================

set(IMGUI_ROOT     ${CMAKE_CURRENT_LIST_DIR})
set(IMGUI_BACKENDS ${IMGUI_ROOT}/backends)

# ============================================================
# imgui::core
# ============================================================

add_library(imgui_core)
add_library(imgui::core ALIAS imgui_core)
set_target_properties(imgui_core PROPERTIES EXPORT_NAME core)
list(APPEND ${PROJECT_NAME}_LIB_TARGETS imgui_core)
target_sources(imgui_core
    PRIVATE
        ${IMGUI_ROOT}/imgui.cpp
        ${IMGUI_ROOT}/imgui_demo.cpp
        ${IMGUI_ROOT}/imgui_draw.cpp
        ${IMGUI_ROOT}/imgui_tables.cpp
        ${IMGUI_ROOT}/imgui_widgets.cpp
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${IMGUI_ROOT}
        FILES
            ${IMGUI_ROOT}/imconfig.h
            ${IMGUI_ROOT}/imgui.h
            ${IMGUI_ROOT}/imgui_internal.h
            ${IMGUI_ROOT}/imstb_rectpack.h
            ${IMGUI_ROOT}/imstb_textedit.h
            ${IMGUI_ROOT}/imstb_truetype.h
)
target_include_directories(imgui_core
    PUBLIC
        $<BUILD_INTERFACE:${IMGUI_ROOT}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
target_compile_features(imgui_core PUBLIC cxx_std_11)

# ============================================================
# Dependencies
# ============================================================

find_package(glfw3 QUIET)
find_package(OpenGL QUIET)

set(IMGUI_HAS_GLFW_OPENGL OFF)
if (glfw3_FOUND AND OpenGL_FOUND)
    set(IMGUI_HAS_GLFW_OPENGL ON)
endif()

# ============================================================
# imgui::backend::glfw_opengl2
# ============================================================

if (IMGUI_HAS_GLFW_OPENGL)

    add_library(imgui_backend_glfw_opengl2)
    add_library(imgui::backend::glfw_opengl2 ALIAS imgui_backend_glfw_opengl2)
    set_target_properties(imgui_backend_glfw_opengl2 PROPERTIES EXPORT_NAME backend::glfw_opengl2)
    list(APPEND ${PROJECT_NAME}_LIB_TARGETS imgui_backend_glfw_opengl2)
    target_sources(imgui_backend_glfw_opengl2
        PRIVATE
            ${IMGUI_BACKENDS}/imgui_impl_glfw.cpp
            ${IMGUI_BACKENDS}/imgui_impl_opengl2.cpp
    )
    target_include_directories(imgui_backend_glfw_opengl2
        PUBLIC
            $<BUILD_INTERFACE:${IMGUI_BACKENDS}>
            $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/backends>
    )
    target_link_libraries(imgui_backend_glfw_opengl2
        PUBLIC
            imgui::core
            glfw
            OpenGL::GL
    )

    add_executable(imgui_example_glfw_opengl2
        examples/example_glfw_opengl2/main.cpp
    )
    list(APPEND ${PROJECT_NAME}_EXE_TARGETS
        imgui_example_glfw_opengl2
    )
    target_link_libraries(imgui_example_glfw_opengl2
        PRIVATE
            imgui::backend::glfw_opengl2
    )

endif()

# ============================================================
# imgui::backend::glfw_opengl3
# ============================================================

if (IMGUI_HAS_GLFW_OPENGL)

    add_library(imgui_backend_glfw_opengl3)
    add_library(imgui::backend::glfw_opengl3 ALIAS imgui_backend_glfw_opengl3)
    set_target_properties(imgui_backend_glfw_opengl3 PROPERTIES EXPORT_NAME backend::glfw_opengl3)
    list(APPEND ${PROJECT_NAME}_LIB_TARGETS imgui_backend_glfw_opengl3)
    target_sources(imgui_backend_glfw_opengl3
        PRIVATE
            ${IMGUI_BACKENDS}/imgui_impl_glfw.cpp
            ${IMGUI_BACKENDS}/imgui_impl_opengl3.cpp
    )
    target_include_directories(imgui_backend_glfw_opengl3
        PUBLIC
            $<BUILD_INTERFACE:${IMGUI_BACKENDS}>
            $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/backends>
    )
    target_link_libraries(imgui_backend_glfw_opengl3
        PUBLIC
            imgui::core
            glfw
            OpenGL::GL
    )

    add_executable(imgui_example_glfw_opengl3
        examples/example_glfw_opengl3/main.cpp
    )
    list(APPEND ${PROJECT_NAME}_EXE_TARGETS
        imgui_example_glfw_opengl3
    )
    target_link_libraries(imgui_example_glfw_opengl3
        PRIVATE
            imgui::backend::glfw_opengl3
    )

endif()

# ============================================================
# Windows DLL export
# ============================================================

if (WIN32 AND BUILD_SHARED_LIBS)
    target_compile_definitions(imgui_core
        PRIVATE   IMGUI_API=__declspec(dllexport)
        INTERFACE IMGUI_API=__declspec(dllimport)
    )
endif()

# ============================================================
# Install
# ============================================================

if (${PROJECT_NAME}_LIB_TARGETS)
    install(TARGETS
        ${${PROJECT_NAME}_LIB_TARGETS}
        EXPORT imguiTargets
        FILE_SET HEADERS
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
endif()

if (${PROJECT_NAME}_EXE_TARGETS)
    install(TARGETS
        ${${PROJECT_NAME}_EXE_TARGETS}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

install(
    DIRECTORY ${IMGUI_BACKENDS}/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/backends
    FILES_MATCHING PATTERN "*.h"
)

install(EXPORT imguiTargets
    NAMESPACE imgui::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/imgui
)
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/imguiConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/imguiConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/imgui
)
write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/imguiConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/imguiConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/imguiConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/imgui
)

################################################################################
# LOG begin
#[[#
message(STATUS "================================================================================")
get_cmake_property(_variableNames VARIABLES)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()
message(STATUS "================================================================================")
#]]#
# LOG end
################################################################################
