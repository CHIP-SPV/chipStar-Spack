# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class SpirvTools(CMakePackage):

    homepage = 'https://github.com/KhronosGroup/SPIRV-Tools'
    git = 'https://github.com/KhronosGroup/SPIRV-Tools'
    url = 'https://github.com/KhronosGroup/SPIRV-Tools/archive/refs/tags/v2022.4.tar.gz'

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc']

    version('2023.2', tag='v2023.2')
    version('2023.1', tag='v2023.1')
    version('2022.4', tag='v2022.4')
    version('2022.3', tag='v2022.3')
    version('2022.2', tag='v2022.2')
    version('2022.1', tag='v2022.1')

    variant('cxxstd',
            description='Use the given C++ standard when compiling',
            values=('11', '14', '17'),
            default='17',
            multi=False)

    depends_on('python@3')
    depends_on('spirv-headers')

    conflicts('cxxstd=11', when='@:2023.1')
    conflicts('cxxstd=14', when='@:2023.2')

    def cmake_args(self):

        args = [
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            '-DCMAKE_CXX_EXTENSIONS=OFF',
            '-DCMAKE_CXX_STANDARD_REQUIRED=ON',
            f'-DSPIRV-Headers_SOURCE_DIR={self.spec["spirv-headers"].prefix}',
            '-DSPIRV_SKIP_TESTS=ON',    # TODO consider supporting tests
        ]

        return args

