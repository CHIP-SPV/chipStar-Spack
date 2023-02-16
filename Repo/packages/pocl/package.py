# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.

from spack.pkg.builtin.pocl import Pocl as BuiltinPocl

class Pocl(BuiltinPocl):

    version('3.1', tag='v3.1')

    variant('spirv', default=False, description='Support SPIR-V')
    variant('cuda', default=False, description='Enable CUDA support')

    depends_on('spirv-llvm-translator', when='+spirv')
    depends_on('cuda', when='+cuda')

    def cmake_args(self):
        args = BuiltinPocl.cmake_args(self)

        if '+spirv' in self.spec:
            args.extend([
                '-DENABLE_SPIR=ON',
                '-DENABLE_SPIRV=ON',
                f'-DLLVM_SPIRV={join_path(self.spec["spirv-llvm-translator"].prefix.bin, "llvm-spirv")}'
            ])

        if '+cuda' in self.spec:
            args.extend([
                '-DENABLE_CUDA=ON'
            ])
        
        return args

