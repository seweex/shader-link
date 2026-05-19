
import pathlib
import struct
import re

class Exporter:
    @staticmethod
    def _make_varname (name: str) -> str:
        valid_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        clean_name = re.sub(r'_+', '_', valid_name).strip('_')

        while clean_name.startswith ('_'):
            clean_name = clean_name [1:]

        return 'spv_' + clean_name

    @staticmethod
    def _read_words (path : pathlib.Path):
        bytecode = None

        with open (path, 'rb') as file:
            bytecode = file.read()

        words = struct.unpack(f'<{len(bytecode) // 4}I', bytecode)
        return words

    @staticmethod
    def _format_words (words) -> str:
        formatted = str ()
        newline = "\n" + (" " * 8)

        for i, word in enumerate (words):
            if i % 5 == 0:
                formatted += newline

            formatted += f'0x{word:08X}U, '

        return formatted[:-2]

    @staticmethod
    def _write_header (formatted_words, path : pathlib.Path, varname : str):
        with open (path, 'w') as file:

            file.write (
f"""
#pragma once

#include <cstdint>
#include <array>

namespace shader_link_compiled 
{{
    inline constexpr std::array {varname} = {{ {formatted_words} }};                                      
}}
"""
            )

    @staticmethod
    def export (spv : pathlib.Path, out: pathlib.Path, name : str):
        raw = Exporter._read_words (spv)
        formatted = Exporter._format_words (raw)
        varname = Exporter._make_varname (name)

        Exporter._write_header (formatted, out, varname)
