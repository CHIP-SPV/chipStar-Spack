# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iHipblas(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-HipBLAS'
    git = 'https://github.com/CHIP-SPV/H4I-HipBLAS'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop', preferred=True)
    version('main', branch='main')

    depends_on('h4i-mklshim')
    depends_on('chip-spv')

    # By design, we can *only* be built using %clang.
    # TODO Do we need to specify 'hipcc' from chip-spv?  Don't seem to.
    # Do we need to be compiled with %clang at all?
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'clang':
            conflicts(f'%{curr_compiler}')

    def cmake_args(self):

        args = [
            f'-DHIP_PATH={self.spec["chip-spv"].prefix}',
        ]

        return args

