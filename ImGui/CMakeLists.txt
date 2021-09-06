cmake_minimum_required(VERSION 3.4)
project(imgui CXX)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_STANDARD 17)

set(SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set(MISC_DIR ${SOURCE_DIR}/misc)
set(EXTRA_FONTS_DIR ${MISC_DIR}/fonts)
set(IMGUI_USER_CONFIG imgui_user_config.h)
set(EXTENSIONS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/extensions)

file(GLOB SOURCE_FILES
    ${SOURCE_DIR}/*.cpp
    ${SOURCE_DIR}/backends/imgui_impl_glfw.cpp
    ${MISC_DIR}/cpp/imgui_stdlib.cpp
    ${MISC_DIR}/freetype/imgui_freetype.cpp
    ${EXTENSIONS_DIR}/ImGuiColorTextEdit/TextEditor.cpp
    ${EXTENSIONS_DIR}/ImGuiFileDialog/ImGuiFileDialog.cpp
    ${EXTENSIONS_DIR}/imgui-node-editor/crude_json.cpp
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_canvas.cpp
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_node_editor.cpp
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_node_editor_api.cpp
)
file(GLOB HEADER_FILES
    ${SOURCE_DIR}/*.h
    ${SOURCE_DIR}/backends/imgui_impl_glfw.h
    ${MISC_DIR}/cpp/imgui_stdlib.h
    ${MISC_DIR}/freetype/imgui_freetype.h
    ${EXTENSIONS_DIR}/imgui-node-editor/crude_json.h
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_bezier_math.h
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_bezier_math.inl
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_canvas.h
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_extra_math.h
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_extra_math.inl
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_node_editor.h
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_node_editor_internal.h
    ${EXTENSIONS_DIR}/imgui-node-editor/imgui_node_editor_internal.inl
    ${EXTENSIONS_DIR}/ImGuiColorTextEdit/TextEditor.h
    ${EXTENSIONS_DIR}/ImGuiFileDialog/ImGuiFileDialog.h
    ${EXTENSIONS_DIR}/ImGuiFileDialog/ImGuiFileDialogConfig.h
)
file(GLOB EXTRA_FONTS_FILES ${EXTRA_FONTS_DIR}/*.ttf)
if (MSVC)
    file(GLOB EXTRA_NATVIS_FILES ${MISC_DIR}/natvis/*.natvis)
endif()

set(BINARY_TO_COMPRESSED_BIN binary_to_compressed_c)

add_executable(${BINARY_TO_COMPRESSED_BIN} ${EXTRA_FONTS_DIR}/binary_to_compressed_c.cpp)

add_library(${PROJECT_NAME} ${SOURCE_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
    )
include(GenerateExportHeader)
generate_export_header(${PROJECT_NAME}
    EXPORT_MACRO_NAME IMGUI_API
    EXPORT_FILE_NAME ${IMGUI_USER_CONFIG}
    )
target_include_directories(${PROJECT_NAME} PUBLIC
    $<BUILD_INTERFACE:${SOURCE_DIR}>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    $<INSTALL_INTERFACE:include>
    ${EXTENSIONS_DIR}/ImGuiColorTextEdit
    ${EXTENSIONS_DIR}/ImGuiFileDialog
    ${EXTENSIONS_DIR}/imgui-node-editor
)
target_compile_definitions(${PROJECT_NAME} PUBLIC "IMGUI_USER_CONFIG=\"${IMGUI_USER_CONFIG}\"")

include(GNUInstallDirs)

install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(TARGETS ${BINARY_TO_COMPRESSED_BIN}
    DESTINATION ${CMAKE_INSTALL_BINDIR})
install(FILES ${HEADER_FILES} ${CMAKE_CURRENT_BINARY_DIR}/${IMGUI_USER_CONFIG}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ)
install(FILES ${EXTRA_FONTS_FILES}
    DESTINATION ${CMAKE_INSTALL_PREFIX}/res/fonts
    PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ)
if (MSVC)
    install(FILES ${EXTRA_NATVIS_FILES}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/res/natvis
        PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ)
endif()
