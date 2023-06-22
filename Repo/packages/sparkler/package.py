# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
from spack import *

class Sparkler(CMakePackage):

    homepage = 'https://github.com/olcf/sparkler'
    git = 'https://github.com/olcf/sparkler'
    # url = 'https://github.com/olcf/sparkler/archive/refs/tags - no tags defined yet.

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc']

    version('hiplz', branch='hiplz')
    version('hip', branch='hip')

    variant('cxxstd',
            description='Use the given C++ standard when compiling',
            values=('11', '14', '17'),
            default='17',
            multi=False)

    depends_on('mpi')
    depends_on('h4i-hipblas', when='^h4i-hipblas')
    depends_on('hipblas', when='^hipblas')


    def cmake_args(self):

        args = [
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            '-DCMAKE_CXX_EXTENSIONS=OFF',
            '-DCMAKE_CXX_STANDARD_REQUIRED=ON',
        ]

        return args

