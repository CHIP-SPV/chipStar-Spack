# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class SpirvHeaders(CMakePackage):

    homepage = 'https://github.com/KhronosGroup/SPIRV-Headers'
    git = 'https://github.com/KhronosGroup/SPIRV-Headers'
    url = 'https://github.com/KhronosGroup/SPIRV-Headers/archive/refs/tags/sdk-1.3.250.0.tar.gz'

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc']

    version('main', branch='main')
    version('sdk-1.3.250.0', tag='sdk-1.3.250.0', preferred=True)

    variant('cxxstd',
            description='Use the given C++ standard when compiling',
            values=('11', '14', '17'),
            default='17',
            multi=False)

    def cmake_args(self):

        args = [
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            '-DCMAKE_CXX_EXTENSIONS=OFF',
            '-DCMAKE_CXX_STANDARD_REQUIRED=ON',
        ]

        return args

