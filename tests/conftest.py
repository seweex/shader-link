from unittest.mock import MagicMock

import pytest
import unittest.mock
import unittest
import typing

import shutil
import subprocess

import shader_link.config
import shader_link.logger

@pytest.fixture
def shared_test_dir (tmp_path_factory):
    test_dir = tmp_path_factory.mktemp ("test_dir")
    return test_dir

@pytest.fixture
def _compiler (shared_test_dir):
    compiler_path = shared_test_dir / 'compiler.exe'
    compiler_path.touch ()

    compiler = unittest.mock.MagicMock ()
    compiler.compiler_path = compiler_path

    return typing.cast (shader_link.config.Compiler, compiler)

@pytest.fixture
def _arguments (shared_test_dir):
    input_path = shared_test_dir / 'input'
    output_path = shared_test_dir / 'output'
    export_path = shared_test_dir / 'export'

    input_path.mkdir ()
    output_path.mkdir ()
    export_path.mkdir ()

    arguments = unittest.mock.MagicMock()
    arguments.input_path = input_path
    arguments.output_path = output_path
    arguments.export_path = export_path

    arguments.forced = True

    return typing.cast (shader_link.config.Arguments, arguments)

@pytest.fixture
def good_compiler (monkeypatch):
    def fake_run (command, *args, **kwargs):
        try:
            out_index = command.index ("-o")
            output_file_path = command [out_index + 1]

            with open (output_file_path, "wb") as file:
                file.write(bytes([0x07, 0x23, 0x02, 0x03]))

        except (ValueError, IndexError):
            return subprocess.CompletedProcess (args=command, returncode=1, stderr="Failed")

        return subprocess.CompletedProcess (args=command, returncode=0)

    compiler = unittest.mock.MagicMock(side_effect=fake_run)
    monkeypatch.setattr ('subprocess.run', compiler)

    return compiler

@pytest.fixture
def bad_compiler (monkeypatch):
    result = unittest.mock.MagicMock()
    result.returncode = 1
    result.stderr = "Failed"

    monkeypatch.setattr('subprocess.run', result)

@pytest.fixture
def config (_arguments, _compiler):
    return shader_link.config.Config (_arguments, _compiler)

@pytest.fixture
def tracker (monkeypatch):
    mock = MagicMock(spec=shader_link.logger.Logger)
    monkeypatch.setattr ('shader_link.logger.Logger', mock)

    return mock

@pytest.fixture
def input_files (config):
    files = [
        config.input_path / 'triangle.vert',
        config.input_path / 'triangle.frag'
    ]

    for path in files:
        path.touch ()

        with open (path, 'w') as file:
            file.write (f'// fake code of {path.name}')

    return files