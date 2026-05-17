
# Shader Link 

It's a useful script to simplify GLSL shader compiling


## Features

- Massive shader compilation
- Flexible input and output paths
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
```


## Usage 

```bash
python -m shader_link.main -f --input "path/to/file/or/dir" --output "result"
```

### Arguments:

- **--input** *or* **-i**: sets up the path to shader source code (file or folder), **required**
- **--output** *or* **-o**: sets up the path to output binaries (only folder), **required**
- **--forced** *or* **-f**: replaces already compiled files (recompile all) 

### Shader Source Code Requirements:

- Files must have an extension that represents the shader stage (.vert, .frag etc.)


## License

This project is under the MIT License - see the [LICENSE](LICENSE) file