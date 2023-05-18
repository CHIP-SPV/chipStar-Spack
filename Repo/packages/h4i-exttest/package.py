# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iExttest(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-ExtTest'
    git = 'https://github.com/CHIP-SPV/H4I-ExtTest'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop')
    version('main', branch='main')

    mkl_threading_values=('tbb_thread', 'sequential')
    variant('mkl-threading',
                description='Which MKL threading mode to enable',
                values=mkl_threading_values,
                default='tbb_thread',
                multi=False)

    depends_on('boost +program_options')

    for threading_value in mkl_threading_values:
        depends_on(f'h4i-hipblas mkl-threading={threading_value}', when=f'mkl-threading={threading_value}')

    # By design, we can *only* be built using %clang.
    # TODO is this really necessary?
    # TODO Do we need to specify 'hipcc' from chip-spv?
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'clang':
            conflicts(f'%{curr_compiler}')

    def cmake_args(self):

        args = [
            self.define_from_variant('MKL_THREADING', 'mkl-threading'),
        ]

        return args

