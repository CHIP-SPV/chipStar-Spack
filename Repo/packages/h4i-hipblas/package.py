# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iHipblas(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-HipBLAS'
    git = 'https://github.com/CHIP-SPV/H4I-HipBLAS'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop')
    version('main', branch='main')

    # TODO do we need to specify that we're compiling with CHIP-SPV's hipcc?
    depends_on('chip-spv')

    # By design, we can *only* be built using %clang.
    # TODO is this really necessary?
    # TODO Do we need to specify 'hipcc' from chip-spv?
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'clang':
            conflicts(f'%{curr_compiler}')

