<!---
Copyright 2022-2023 UT-Battelle
See LICENSE.txt in the root of the source distribution for license info.
-->
# Overview

[CHIP-SPV](https://github.com/CHIP-SPV/chip-spv) is software that
allows software written to use the [Heterogeneous-compute Interface for
Portability (HIP)](https://https://github.com/ROCm-Developer-Tools/HIP)
interface and kernel language to target GPUs via the 
[SPIR-V](https://registry.khronos.org/spir) intermediate language.
CHIP-SPV can use either the Intel Level Zero runtime or an OpenCL
runtime as a backend.

This repository contains support for building CHIP-SPV and its
dependencies via the [Spack](https://github.com/spack/spack) package
manager.

Note: most development to date has been done with the Level Zero 
environment, and it is expected that substantial work is needed for
the environment targeting the OpenCL backend to work.

# Prerequisites

* An x86_64 system running a common Linux distribution.  OpenSLES 15 is
  the best tested to date.
* A working Spack installation.
* Clang 15.x installed and registered as a Spack compiler.  Installing
  this compiler via Spack (i.e., by installing a package like `llvm@15.0.7`,
  and then using `spack compiler add`) is the approach that is currently
  best tested.

# Usage

0. Clone this repository to the target system.

```bash
$ git clone https://github.com/CHIP-SPV/CHIP-SPV-Spack
```

1. Verify that the compiler version is correctly represented in the
   desired environment's `spack.yaml` file.  For instance, if the Clang
   compiler to be used is version 15.0.7, ensure that the version
   numbers for the `compilers` definition, the `llvm` spec, and
   the `spirv-llvm-translator` spec are consistent.  In this instance,
   these should be `clang@15.0.7`, `llvm@15.0.7` and 
   `spirv-llvm-translator@15`, respectively.

2. Activate and concretize the environment.  E.g.,

```bash
$ cd CHIP-SPV-Spack/Environments/LevelZero
$ spack activate .
$ spack concretize -f
```

3. Build the environment.

```bash
$ spack install
```
If all goes well with the build, a `spack find` with the environment
active should show `chip-spv` available.

4. Use the installed software.  The easiest way to use the installed
software when compiling and running HIP code is to activate the 
environment and then build the software.  Because other packages like
`cmake` and `boost` are not roots in the Spack environments, they
are not automatically added to one's environment when one activates
the Spack environment.  To use these, one must load them before
activating the Spack environment, or ensure that they are available
using the `module` command.


# TODO

* Ensure the OpenCL-based environment can use any OpenCL implementation.
* Clean up and verify the OpenCL-based environment using POCL.
* Incorporate HIP libraries like HipBLAS into the environments.
* Support using the software installed by the environment via `module`

