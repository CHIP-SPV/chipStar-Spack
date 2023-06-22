# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iHipblas(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-HipBLAS'
    git = 'https://github.com/CHIP-SPV/H4I-HipBLAS'
    url = 'https://github.com/CHIP-SPV/H4I-HipBLAS/archive/refs/tags/v0.1.0.tar.gz'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop', preferred=True)
    version('main', branch='main')
    version('0.1.0', sha256='6f8cc622ad7c532eecb1d241e979496ef4471bc00a31845f11156531f9959273')

    depends_on('h4i-mklshim')
    depends_on('chipstar')

    # By design, we can *only* be built using %clang.
    # TODO Do we need to specify 'hipcc' from chipstar?  Don't seem to.
    # Do we need to be compiled with %clang at all?
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'clang':
            conflicts(f'%{curr_compiler}')

    def cmake_args(self):

        args = [
            f'-DHIP_PATH={self.spec["chipstar"].prefix}',
        ]

        return args

