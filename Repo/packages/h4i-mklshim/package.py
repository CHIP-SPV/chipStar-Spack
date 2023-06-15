# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iMklshim(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-MKLShim'
    git = 'https://github.com/CHIP-SPV/H4I-MKLShim'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc']

    version('develop', branch='develop', preferred=True)
    version('main', branch='main')

    variant('mkl-threading',
                description='Which MKL threading mode to enable',
                values=('tbb_thread', 'sequential'),
                default='tbb_thread',
                multi=False)

    depends_on('intel-oneapi-compilers@2023:')
    depends_on('intel-oneapi-mkl@2023:')  # TODO verify that the Spack-installed MKL runs code on GPUs
    depends_on('oneapi-level-zero')

    # By design, we can *only* be built using %oneapi.
    # (At least until there are other SYCL compilers that can use the MKL
    # library to run code on Intel GPUs.)
    for curr_compiler in spack.compilers.supported_compilers():
        if curr_compiler != 'oneapi':
            conflicts(f'%{curr_compiler}')

    def cmake_args(self):

        # We depend on intel-oneapi-compiler but don't source its script
        # that sets environment variables.  Help CMake find the SYCL 
        # support.
        sycl_compiler_path = join_path(self.spec['intel-oneapi-compilers'].prefix, 'compiler', 'latest', 'linux')
        sycl_include_dir = join_path(sycl_compiler_path, 'include', 'sycl')
        sycl_library_dir = join_path(sycl_compiler_path, 'lib')

        args = [
            self.define_from_variant('MKL_THREADING', 'mkl-threading'),
            f'-DSYCL_INCLUDE_DIR={sycl_include_dir}',
            f'-DSYCL_LIBRARY_DIR={sycl_library_dir}'
        ]

        return args

