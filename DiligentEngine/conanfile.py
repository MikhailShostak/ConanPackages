from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = 'DiligentEngine'
    version = '2.5'
    homepage = 'https://github.com/DiligentGraphics/DiligentEngine'
    description = 'A Modern Cross-Platform Low-Level 3D Graphics Library and Rendering Framework'
    topics = ('conan', 'DiligentEngine', '3d', 'graphics')
    license = 'Apache-2.0'

    settings = 'os', 'compiler', 'build_type', 'arch'

    def source(self):
        tools.get('https://github.com/DiligentGraphics/DiligentEngine/releases/download/v2.5/DiligentEngine_v2.5.zip', destination='src', strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir='build', source_dir='../src')
        cmake.build(target='Diligent-GraphicsEngineVk-static')
        cmake.build(target='Diligent-GraphicsTools')

    def package(self):
        for ext in ['.h', '.hpp', '.inl']:
            self.copy('*/interface/*' + ext, 'include/DiligentCore', 'src/DiligentCore', keep_path=True)
            self.copy('*/interface/*' + ext, 'include/DiligentTools', 'src/DiligentTools', keep_path=True)

        self.copy('ImGuiDiligentRenderer.cpp', 'res', 'src/DiligentTools/Imgui/src', keep_path=False)
        self.copy('ImGuiImplDiligent.cpp', 'res', 'src/DiligentTools/Imgui/src', keep_path=False)

        self.copy('*.lib', 'lib', 'build/DiligentCore', keep_path=False)
        self.copy('*.pdb', 'lib', 'build/DiligentCore', keep_path=False)

    def package_info(self):
        if self.settings.os == 'Windows':
            self.cpp_info.defines = ['PLATFORM_WIN32=1']
        elif self.settings.os == 'Macos':
            self.cpp_info.defines = ['PLATFORM_MACOS=1']
        elif self.settings.os == 'Linux':
            self.cpp_info.defines = ['PLATFORM_LINUX=1']
        elif self.settings.os == 'Android':
            self.cpp_info.defines = ['PLATFORM_ANDROID=1']
        elif self.settings.os == 'iOS':
            self.cpp_info.defines = ['PLATFORM_IOS=1']

        self.cpp_info.defines.append('DILIGENT_NO_DIRECT3D11')
        self.cpp_info.defines.append('DILIGENT_NO_DIRECT3D12')
        self.cpp_info.defines.append('DILIGENT_NO_OPENGL')

        self.cpp_info.includedirs = []
        for (root, dirs, files) in os.walk('include'):
            for d in dirs:
                if d == 'interface':
                    self.cpp_info.includedirs.append(root.replace('\\', '/') + '/' + d)

        self.cpp_info.libs = []
        for (root, dirs, files) in os.walk('lib'):
            for f in files:
                if f.endswith('lib'):
                    self.cpp_info.libs.append(f)
