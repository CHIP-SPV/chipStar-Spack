# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class Chipstar(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/chipStar'
    git = 'https://github.com/CHIP-SPV/chipStar'
    url = 'https://github.com/CHIP-SPV/chipStar/archive/refs/tags/v0.9.tar.gz'

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc@ornl.gov']

    version('main', branch='main', submodules=True, preferred=True)
    version('0.9', tag='v0.9', submodules=True)

    variant('backend', description='Which backend to target',
                values=('level_zero', 'opencl'),
                default='level_zero',
                multi=False
        )

    variant('interop', description='Whether to build SYCL interoperability tests', default=True)

    # By design, we can *only* be built using %clang.
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'clang':
            conflicts(f'%{curr_compiler}')

    for supported_version in [14, 15, 16]:
        with when(f'%clang@{supported_version}:{supported_version}.999'):
            depends_on(f'llvm@{supported_version}')
            depends_on(f'spirv-llvm-translator@{supported_version}', type=('build', 'link', 'run'))

    depends_on('oneapi-level-zero', when='backend=level_zero')
    depends_on('opencl', when='backend=opencl')

    with when('+interop'):
        depends_on('intel-oneapi-compilers')
        depends_on('intel-oneapi-mkl')

    def cmake_args(self):

        # Chipstar uses a heavily modified version of a HIP repository,
        # which in turn uses an internal, modified version of Catch2 for tests that
        # knows how to build HIP executables.
        # Chipstar will not even configure correctly without using this modified Catch2,
        # even if we aren't building tests.
        # So force it to find its internal, modified Catch2.
        # Note that this isn't necessarily simple: the Chipstar CMakeLists.txt files
        # will define a variable CATCH2_PATH that makes one think it is where it will
        # find Catch2, and the actual find_package() command specifies the internal
        # path using a PATH keyword, but CMake treats that as a hint that is overridden
        # if there's another Catch2 to be found using its higher-priority checks.
        # Unfortunately for us, that's the case when building with Spack, if Catch2
        # is already loaded or available in the environment.
        internal_catch2_path = join_path(self.stage.source_path, 'HIP', 'tests', 'catch', 'external', 'Catch2', 'cmake', 'Catch2')

        args = [
            f'-DLLVM_CONFIG={join_path(self.spec["llvm"].prefix.bin, "llvm-config")}',
            f'-DLLVM_LINK={join_path(self.spec["llvm"].prefix.bin, "llvm-link")}',
            f'-DCLANG_OFFLOAD_BUNDLER={join_path(self.spec["llvm"].prefix.bin, "clang-offload-bundler")}',
            f'-DLLVM_SPIRV_BINARY={join_path(self.spec["spirv-llvm-translator"].prefix.bin, "llvm-spirv")}',
            f'-DCatch2_ROOT:PATH={internal_catch2_path}'
        ]

        return args



    def setup_build_environment(self, env):

        if self.spec.satisfies('+interop'):
            # We want to build the HIP-SYCL interop examples,
            # but just depending on the OneAPI compiler and MKL packages
            # isn't enough for this project's CMake scripts to decide
            # that it has the support it needs to build those examples.
            # Update the environment so CMake will find them.
            env.set('MKLROOT', self.spec['intel-oneapi-mkl'].prefix)
            env.prepend_path('PATH',
                join_path(self.spec['intel-oneapi-compilers'].prefix, 'compiler', 'latest', 'linux', 'bin'))


    def setup_dependent_build_environment(self, env, dependent_spec):

        # For some reason, our dependency on spirv-llvm-translator with type=(build, link, run)
        # doesn't seem to be sufficient for dependent packages to use llvm-spirv.
        # TODO is there a more Spack-ic idiom for doing this?
        env.prepend_path('PATH', join_path(self.spec["spirv-llvm-translator"].prefix.bin))

