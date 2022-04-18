from conans import ConanFile, CMake, tools
import os

class Conan(ConanFile):
    name = 'DiligentEngineExt'
    version = '2.5'
    homepage = 'https://github.com/DiligentGraphics/DiligentEngine'
    description = 'A Modern Cross-Platform Low-Level 3D Graphics Library and Rendering Framework'
    topics = ('conan', 'DiligentEngine', '3d', 'graphics')
    license = 'Apache-2.0'

    requires = 'DiligentEngine/2.5', 'imgui/1.84.0-ext'

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
    }

    exports_sources = 'CMakeLists.txt'
    generators = 'cmake'
    _cmake = None

    @property
    def build_tool(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure(build_dir='build')
        return self._cmake

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def build(self):
        self.build_tool.build()

    def package(self):
        self.build_tool.install()
        self.copy(pattern='LICENSE.txt', dst='licenses')

    def package_info(self):
        self.cpp_info.libs = ['DiligentEngineExt']
