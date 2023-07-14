# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
from spack import *

class H4iExttest(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-ExtTest'
    git = 'https://github.com/CHIP-SPV/H4I-ExtTest'
    url = 'https://github.com/CHIP-SPV/H4I-ExtTest/archive/refs/tags/v0.1.0.tar.gz'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop', preferred=True)
    version('main', branch='main')
    version('0.1.0', sha256='ca1db3f8e9f26e0c754d44c4dee860a499920845f399d5070beca46476211fe2')

    depends_on('catch2@3')
    depends_on('hipblas')

    # By design, we can *only* be built using %clang.
    # TODO is this really necessary?
    # TODO Do we need to specify 'hipcc' from chipStar?
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'clang':
            conflicts(f'%{curr_compiler}')

    def cmake_args(self):

        args = [
            f'-DHIP_PATH={self.spec["chipstar"].prefix}'
        ]

        return args

