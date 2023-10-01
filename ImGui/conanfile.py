from conan import ConanFile
from conan.tools.cmake import CMake

import os

class Conan(ConanFile):
    name = 'imgui'
    version = '1.84.0-ext'
    homepage = 'https://github.com/ocornut/imgui'
    description = 'Bloat-free Immediate Mode Graphical User interface for C++ with minimal dependencies'
    topics = ('conan', 'imgui', 'gui', 'graphical')
    license = 'MIT'

    scm = {
        'type': 'git',
        'subfolder': 'src',
        'url': 'https://github.com/ocornut/imgui.git',
        'revision': '5a7d18a44171fd02f7b71df3e8416c1f87b93d75'
    }
    imgui_extensions = [
        ['https://github.com/BalazsJako/ImGuiColorTextEdit', 'master'],
        ['https://github.com/aiekick/ImGuiFileDialog', 'Lib_Only'],
        ['https://github.com/thedmd/imgui-node-editor', 'master'],
    ]
    requires = 'freetype/2.10.4', 'glfw/3.3.4'

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
    def src(self):
        return self.scm['subfolder']

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

    def source(self):
        for ext in self.imgui_extensions:
            self.run('git clone ' + ext[0] + '.git -b ' + ext[1] + ' extensions/' + os.path.basename(ext[0]))

    def build(self):
        self.build_tool.build()

    def package(self):
        self.build_tool.install()
        self.copy(pattern='LICENSE.txt', dst='licenses', src=self.src)

    def package_info(self):
        self.cpp_info.libs = ['imgui']
