# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
from spack import *

class H4iExttest(CMakePackage, ROCmPackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-ExtTest'
    git = 'https://github.com/CHIP-SPV/H4I-ExtTest'
    url = 'https://github.com/CHIP-SPV/H4I-ExtTest/archive/refs/tags/v0.1.0.tar.gz'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop', preferred=True)
    version('main', branch='main')
    version('0.1.0', sha256='ca1db3f8e9f26e0c754d44c4dee860a499920845f399d5070beca46476211fe2')

    depends_on('catch2@3')
    depends_on('hip', when='+rocm')
    depends_on('hipblas', when='+rocm')
    depends_on('h4i-hipblas', when='~rocm')

    requires('%clang', '%cce', policy='one_of', msg='Package must be built with a Clang-based compiler')


    def cmake_args(self):

        args = [
            self.define_from_variant('H4I_USE_ROCM_LIBS', 'rocm')
        ]

        if self.spec.satisfies('+rocm'):
            args.extend([
                self.define_from_variant('AMDGPU_TARGETS', 'amdgpu_target')
            ])

        if self.spec.satisfies('~rocm'):
            args.extend([
                f'-DHIP_PATH={self.spec["chipstar"].prefix}',
            ])

        return args


    def flag_handler(self, name, flags):

        if name == 'cppflags':
            if self.spec.satisfies('^hipblas+rocm'):
                flags.append('-D__HIP_PLATFORM_AMD__')
            elif self.spec.satisfies('^hipblas+cuda'):
                flags.append('-D__HIP_PLATFORM_NVIDIA__')

        return (None, None, flags)

