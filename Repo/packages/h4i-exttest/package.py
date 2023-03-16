# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iExttest(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-ExtTest'
    git = 'https://github.com/CHIP-SPV/H4I-ExtTest'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc@ornl.gov']

    version('develop', branch='develop')
    version('main', branch='main')

    variant('mkl-threading',
                description='Which MKL threading mode to enable',
                values=('tbb_thread', 'sequential'),
                default='tbb_thread',
                multi=False)

    depends_on('boost +program_options')

    # TODO Is it possible to specify this dependency without having to list all potential values?
    depends_on('h4i-hipblas mkl-threading=tbb_thread', when='mkl-threading=tbb_thread')
    depends_on('h4i-hipblas mkl-threading=sequential', when='mkl-threading=sequential')

    # depends_on('intel-oneapi-mkl')

    # How to specify that we must be compiled with clang, without
    # having to list all potential compiler families?
    # Is depends_on('llvm') what we need?
    conflicts('%gcc')
    conflicts('%oneapi')

    def cmake_args(self):

        args = [
            self.define_from_variant('MKL_THREADING', 'mkl-threading'),
        ]

        return args

