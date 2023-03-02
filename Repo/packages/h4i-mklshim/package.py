# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class H4iMklshim(CMakePackage):

    homepage = 'https://github.com/CHIP-SPV/H4I-MKLShim'
    git = 'https://github.com/CHIP-SPV/H4I-MKLShim'

    # Maintainer of the Spack package, not necessarily the software itself.
    maintainers = ['rothpc@ornl.gov']

    version('develop', branch='develop')
    version('main', branch='main')

    variant('mkl-threading',
                description='Which MKL threading mode to enable',
                values=('tbb_thread', 'sequential'),
                default='tbb_thread',
                multi=False)

    depends_on('intel-oneapi-compilers')
    depends_on('intel-oneapi-mkl')  # TODO verify that the Spack-installed MKL runs code on GPUs
    depends_on('oneapi-level-zero')

    # Wish there were an easier way to say 
    # "only %oneapi is allowed" than to list
    # all other potential compiler families as conflicts.
    conflicts('%gcc')
    conflicts('%clang')
    conflicts('%intel')
    # TODO add all other compiler families, or find a way to specify the
    # way to say 'conflicted with everything *but* '%oneapi'

    def cmake_args(self):

        args = [
            self.define_from_variant('MKL_THREADING', 'mkl-threading'),
        ]

        return args

