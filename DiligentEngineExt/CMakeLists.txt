cmake_minimum_required(VERSION 3.20)
project(DiligentEngineExt CXX)

include(${CMAKE_SOURCE_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(DiligentEngineExt
    ${CONAN_RES_DIRS_DILIGENTENGINE}/ImGuiImplDiligent.cpp
    ${CONAN_RES_DIRS_DILIGENTENGINE}/ImGuiDiligentRenderer.cpp
)

include(GNUInstallDirs)

install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
