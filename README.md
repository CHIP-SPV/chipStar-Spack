<!---
Copyright 2022-2023 UT-Battelle
See LICENSE.txt in the root of the source distribution for license info.
-->
# Overview

[chipStar](https://github.com/CHIP-SPV/chipStar) (formerly CHIP-SPV)
is software that allows software written to use the
[Heterogeneous-compute Interface for Portability
(HIP)](https://https://github.com/ROCm-Developer-Tools/HIP)
interface and kernel language to target GPUs via the 
[SPIR-V](https://registry.khronos.org/spir) intermediate language.
chipStar can use either the Intel Level Zero runtime or an OpenCL
runtime as a backend.

This repository contains support for building chipStar and its
dependencies via the [Spack](https://github.com/spack/spack) package
manager.

Note: most development to date has been done with the Level Zero 
environment, and it is expected that substantial work is needed for
the environment targeting the OpenCL backend to work.

# Prerequisites

* An x86_64 system running a common Linux distribution.  OpenSLES 15 is
  the best tested to date.
* A working Spack installation.
* A recent Clang installation that is registered with Spack as a compiler.
  Versions 15 and 16 are best tested, but 14 might work.  We suggest
  installing the compiler via Spack (i.e., by installing something like
  `llvm@16.0.2` and then using `spack compiler add` with the llvm
  package's install location), because the `chipstar` package defined
  in this repository depends on the `llvm` package anyway.
* A recent (at least version 2023.1) Intel OneAPI compiler installation
  that is registered with Spack as a compiler.  The recommended way
  of doing this is by installing the Spack `intel-oneapi-compilers`
  package, then registering the location of its compilers with Spack.
  E.g., 

```bash
$ spack install intel-oneapi-compilers@2023
$ spack compiler add $(spack location -i intel-oneapi-compilers@2023)/compiler/latest/linux
```

# Usage

0. Clone this repository to the target system.

```bash
$ git clone https://github.com/CHIP-SPV/CHIP-SPV-Spack
```

2. Activate the environment you want to build.  E.g., for the
environment that just builds chipStar with Level Zero backend:

```bash
$ cd CHIP-SPV-Spack/Environments/LevelZero
$ spack env activate .
```

3. Concretize the active environment.  (In Spack terminology, 
"to concretize" means to let Spack examine the package specifications
it has been asked to build, plus the available package repositories, 
resolve dependencies and check constraints, and decide exactly which
packages it will build, in which order, and with which configuration.)

```bash
$ spack concretize -f -U
```

We suggest examining the output from running the `spack concretize` 
command to make sure that Spack's concretizer has truly decided to
use the configuration options and especially the compilers that you
want it to use.  Note that the environment and related configuration 
are purposefully not overly constrained to use the given compiler
for every dependency package, so even though there are some packages
that must be built with `%clang`, there are others that may be
built (or re-used from already-installed packages) using `%gcc` such
as the system's GCC installation.

If Spack's concretizer  didn't do what you want, you can re-concretize
the environment and be more explicit about what you want using command-line
configuration options (recommended) or by editing the environment's
`spack.yaml` file or other configuration options that your Spack installation
is using.  (Use `spack config blame` to see which configuration files Spack is
using.)  For instance, if you have both `clang@16.0.2` and `clang@15.0.7`
installed and registered as Spack compilers, and you want to build
using `clang@15.0.7`, you may have to use a concretize command like the
following:

```bash
$ spack -c "packages:chipstar:require:'%clang@15.0.7'" concretize -f -U
```

As before, verify from the output of the `spack concretize` command that it
is using the compiler version you want, `clang@15.0.7` in this example.


4. Build the environment.

```bash
$ spack install
```
Spack supports some options for controlling the build and installation,
such as `-j` to limit the number of processes used for parallel builds,
useful for being a good citizen on shared systems by not allowing Spack
to use all available cores (its default).  See the Spack documentation for
more information.

Assuming all goes well with the build and install, a `spack find`
should show the packages that you just built.

5. Use the installed software.  There are several ways you might
update your environment to use the software, including:

* `spack load chipstar`
* Activating the environment that you used to build the software
* If your Spack configuration is such that it can generate module files
and module files have been generated for the software you built
via this environment, `module load chipstar`

Note that you may need to modify your environment to be able to run
programs produced using chipStar and the H4I libraries built
using this Spack repository.  For instance, on some systems,
one must load the `intel_compute_runtime` module before being
able to run programs that use the Intel Level Zero runtime.


# TODO

* Clean up and verify the OpenCL-based environment.
* Ensure the OpenCL-based environment can use any OpenCL implementation.
* Incorporate H4I HIP libraries like H4I-HipBLAS into an environments.
* Support using the software installed by the environment via 
`module` command.

