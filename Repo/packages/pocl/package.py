
from spack.pkg.builtin.pocl import Pocl as BuiltinPocl

class Pocl(BuiltinPocl):

    version('3.1', tag='v3.1')

    variant('spirv', default=False, description='Support SPIR-V')

    depends_on('spirv-llvm-translator', when='+spirv')

    def cmake_args(self):
        args = BuiltinPocl.cmake_args(self)

        if '+spirv' in self.spec:
            args.extend([
                '-DENABLE_SPIR=ON',
                '-DENABLE_SPIRV=ON',
                f'-DLLVM_SPIRV={join_path(self.spec["spirv-llvm-translator"].prefix.bin, "llvm-spirv")}'
            ])
        
        return args

