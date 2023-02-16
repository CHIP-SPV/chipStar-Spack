# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class ChipSpv(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/chip-spv'
    git = 'https://github.com/CHIP-SPV/chip-spv'
    url = 'https://github.com/CHIP-SPV/chip-spv/archive/refs/tags/v0.9.tar.gz'

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc@ornl.gov']

    version('main', branch='main', submodules=True)
    version('0.9', tag='v0.9', submodules=True)

    variant('backend', description='Which backend to target',
                values=('level_zero', 'opencl'),
                default='level_zero',
                multi=False
        )

    variant('interop', description='Whether to build SYCL interoperability tests', default=True)

    depends_on('spirv-llvm-translator@15', when='^llvm@15')
    depends_on('spirv-llvm-translator@14', when='^llvm@14')

    depends_on('oneapi-level-zero', when='backend=level_zero')
    depends_on('ocl-icd', when='backend=opencl')

    depends_on('intel-oneapi-compilers', when='+interop')
    depends_on('intel-oneapi-mkl', when='+interop')

    patch('sycl_hip_interop-lz-noocl.patch', when='+interop backend=level_zero')

    def cmake_args(self):

        args = [
            f'-DLLVM_CONFIG={join_path(self.spec["llvm"].prefix.bin, "llvm-config")}',
            f'-DLLVM_LINK={join_path(self.spec["llvm"].prefix.bin, "llvm-link")}',
            f'-DCLANG_OFFLOAD_BUNDLER={join_path(self.spec["llvm"].prefix.bin, "clang-offload-bundler")}',
            f'-DLLVM_SPIRV_BINARY={join_path(self.spec["spirv-llvm-translator"].prefix.bin, "llvm-spirv")}'
        ]

        return args

