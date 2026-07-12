
# Shader Link 

It's a useful script to simplify GLSL shader compiling


## Features

- Massive shader compilation
- Shader export to C++ headers
- Export as constexpr std::array of binaries
- Flexible input and output paths
- Supports user-defined arguments
- Caches compilations 
- Very simple usage

## Setting Up

### Requirements:

- Installed [glslc](https://github.com/google/shaderc)
- The path to it in the `PATH` environment variable

### Install:

```bash
# clone the project
git clone https://github.com/seweex/shader-link.git
cd shader-link

# create a python environment if needed
python -m venv .venv

# activate it
# for windows:
.venv\bin\activate.bat
# for linux:
source .venv/bin/activate

# for tests
pip install pytest
```


## Usage 

```bash
python -m shader_link -f --input "path/to/file/or/dir" --output "result" --export "path/to/exports" --args "-O --target-env=vulkan1.4"
```

### Arguments:

- **--input** *or* **-i**: sets up the path to shader source code (file or folder), **required**
- **--output** *or* **-o**: sets up the path to output binaries (only folder), **required**
- **--export** *or* **-e**: sets up the path to hpp-export spv (only folder), **default=None**
- **--forced** *or* **-f**: replaces already compiled files (recompile all)
- **--args** *or* **-a**: adds user-defined arguments to the compiler.
  Note: if you specify only 1 argument, use `-a="-O"` instead of using  `-a "-O"`

### Shader Source Code Requirements:

- Files must have an extension that represents the shader stage (.vert, .frag etc.)


## Tests

In the root path call

```bash
pytest -v
```

## License

This project is under the MIT License - see the [LICENSE](LICENSE) file