# Copyright 2022-2023 UT-Battelle
# See LICENSE.txt in the root of the source distribution for license info.
import sys
from spack import *

class SpirvTools(CMakePackage):

    homepage = 'https://github.com/KhronosGroup/SPIRV-Tools'
    git = 'https://github.com/KhronosGroup/SPIRV-Tools'
    url = 'https://github.com/KhronosGroup/SPIRV-Tools/archive/refs/tags/v2022.4.tar.gz'

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc@ornl.gov']

    version('2022.4', tag='v2022.4')
    version('2022.3', tag='v2022.3')
    version('2022.2', tag='v2022.2')
    version('2022.1', tag='v2022.1')

    depends_on('python@3')

    resource(
            name='spirv-headers',
            git='https://github.com/KhronosGroup/SPIRV-Headers',
            destination='external'
    )
    resource(
            name='re2',
            git='https://github.com/google/re2',
            destination='external'
    )
    resource(
            name='effcee',
            git='https://github.com/google/effcee',
            destination='external'
    )
    resource(
            name='googletest',
            git='https://github.com/google/googletest',
            destination='external'
    )

