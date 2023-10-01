from conan import ConanFile, tools
from conan.tools.cmake import CMake

import os

class Conan(ConanFile):
    name = 'diligentengine'
    version = '2.5.4'
    homepage = 'https://github.com/DiligentGraphics/DiligentEngine'
    description = 'A Modern Cross-Platform Low-Level 3D Graphics Library and Rendering Framework'
    topics = ('conan', 'DiligentEngine', '3d', 'graphics')
    license = 'Apache-2.0'
    generators = "CMakeToolchain", "CMakeDeps"

    settings = 'os', 'compiler', 'build_type', 'arch'

    def source(self):
        tools.files.get(self, f'https://github.com/DiligentGraphics/DiligentEngine/releases/download/v{self.version}/DiligentEngine_v{self.version}.zip', destination='src', strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder='src')
        cmake.build(target='Diligent-GraphicsEngineVk-static')
        cmake.build(target='Diligent-GraphicsTools')

    def package(self):
        for ext in ['.h', '.hpp', '.inl']:
            tools.files.copy(self, '*/interface/*' + ext, 'src/DiligentCore', 'include/DiligentCore', keep_path=True)
            tools.files.copy(self, '*/interface/*' + ext, 'src/DiligentTools', 'include/DiligentTools', keep_path=True)

        tools.files.copy(self, 'ImGuiDiligentRenderer.cpp', 'src/DiligentTools/Imgui/src', 'res', keep_path=False)
        tools.files.copy(self, 'ImGuiImplDiligent.cpp', 'src/DiligentTools/Imgui/src', 'res', keep_path=False)

        for ext in ['.a', '.lib', '.dll', '.so', '.dylib', '.pdb', '.dsym']:
            tools.files.copy(self, '*' + ext, 'lib', 'build/DiligentCore', keep_path=False)

    def package_info(self):
        diligent_platform = None
        if self.settings.os == 'Windows':
            self.cpp_info.defines = ['PLATFORM_WIN32=1']
            diligent_platform = 'Win32'
        elif self.settings.os == 'Macos':
            self.cpp_info.defines = ['PLATFORM_MACOS=1']
            diligent_platform = 'Apple'
        elif self.settings.os == 'Linux':
            self.cpp_info.defines = ['PLATFORM_LINUX=1']
            diligent_platform = 'Linux'
        elif self.settings.os == 'Android':
            self.cpp_info.defines = ['PLATFORM_ANDROID=1']
            diligent_platform = 'Android'
        elif self.settings.os == 'iOS':
            self.cpp_info.defines = ['PLATFORM_IOS=1']
            diligent_platform = 'Apple'

        self.cpp_info.defines.append('DILIGENT_NO_DIRECT3D11')
        self.cpp_info.defines.append('DILIGENT_NO_DIRECT3D12')
        self.cpp_info.defines.append('DILIGENT_NO_OPENGL')

        self.cpp_info.includedirs = []
        for (root, dirs, files) in os.walk('include'):
            for d in dirs:
                if d == 'interface':
                    self.cpp_info.includedirs.append(root.replace('\\', '/') + '/' + d)

        need_debug_sufix = self.settings.os == 'Windows' and self.settings.build_type == 'Debug'
        self.cpp_info.libs = [
            'Diligent-GraphicsEngineVk-static',
            'Diligent-GraphicsEngineNextGenBase',
            'Diligent-ShaderTools',
            'Diligent-HLSL2GLSLConverterLib',
            'Diligent-GraphicsEngine',
            'spirv-cross-cored' if need_debug_sufix else 'spirv-cross-core',
            'SPIRVd' if need_debug_sufix else 'SPIRV',
            'glslangd' if need_debug_sufix else 'glslang',
            'MachineIndependentd'  if need_debug_sufix else 'MachineIndependent',
            'GenericCodeGend' if need_debug_sufix else 'GenericCodeGen',
            'OGLCompilerd' if need_debug_sufix else 'OGLCompiler',
            'OSDependentd' if need_debug_sufix else 'OSDependent',
            'SPIRV-Tools-opt',
            'SPIRV-Tools',
            'Diligent-GraphicsTools',
            'Diligent-GraphicsAccessories',
            'Diligent-Common',
            'Diligent-' + diligent_platform + 'Platform',
            'Diligent-BasicPlatform',
            'Diligent-Primitives',
        ]
