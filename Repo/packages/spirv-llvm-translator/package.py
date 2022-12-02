import sys
from spack import *

class SpirvLlvmTranslator(CMakePackage):

    homepage = 'https://github.com/KhronosGroup/SPIRV-LLVM-Translator'
    git = 'https://github.com/KhronosGroup/SPIRV-LLVM-Translator'
    url = 'https://github.com/KhronosGroup/SPIRV-LLVM-Translator/archive/refs/tags/v15.0.0.tar.gz'

    # Maintainer of the Spack package, not the software itself.
    maintainers = ['rothpc@ornl.gov']

    version('15.0.0', tag='v15.0.0')
    version('14.0.0', tag='v14.0.0')

    variant('tools', default=True, description='Integrate SPIRV-Tools')

    depends_on('llvm@15', when='@15.0.0')
    depends_on('llvm@14', when='@14.0.0')
    depends_on('spirv-tools', when='+tools')

    def setup_build_environment(self, env):
        if '+tools' in self.spec:
            env.append_path("PKG_CONFIG_PATH", self.spec['spirv-tools'].prefix.lib.pkgconfig)

