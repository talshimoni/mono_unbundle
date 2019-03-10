from elftools.elf.elffile import ELFFile
from io import BufferedReader
from pathlib import Path
from typing import Union, Tuple
import gzip
import magic
import sys


class MonoDll:
    def __init__(self, name: str, offset: int, size: int):
        self.name = name
        self.offset = offset
        self.size = size


class MonoBundle:
    little_endian = None

    def __init__(self, file: Union[str, BufferedReader], path: str = None, verbose: bool = False):
        self.path = path
        self.verbose = verbose
        self.file, self.elf_file = self.__open_elf(file)
        self.dlls = self.__parse_elf()

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def __open_elf(self, file: Union[str, BufferedReader]) -> Tuple[BufferedReader, ELFFile]:
        f = file if type(file) is BufferedReader else open(file, 'rb')
        m = magic.from_buffer(f.read(1024), mime=False)

        if m.startswith('PE32 '):
            raise NotImplementedError("PE bundles are not currently supported.")
        elif not m.startswith('ELF '):
            raise IOError("File is not an ELF library.")
        self.little_endian = "LSB" in m

        return f, ELFFile(f)

    def __parse_elf(self) -> [MonoDll]:
        # Shout out to maldrolyzer for independently arriving at the same solution
        # (https://github.com/maldroid/maldrolyzer/blob/master/plugins/z3core.py#L48)

        section = self.elf_file.get_section_by_name('.dynsym')
        dlls = []

        for symbol in section.iter_symbols():
            if symbol['st_shndx'] != 'SHN_UNDEF' and symbol.name.startswith('assembly_data_'):
                dll = dict()
                dll['name'] = symbol.name[14:].replace('_dll', '.dll')
                dll['offset'] = symbol['st_value']
                dll['size'] = symbol['st_size']
                dll = MonoDll(dll['name'], dll['offset'], dll['size'])

                if self.verbose:
                    print("found %s" % dll.name, file=sys.stderr)

                dlls.append(dll)

        return dlls

    def get_dlls(self) -> [MonoDll]:
        return self.dlls

    def extract(self, dll: MonoDll, path: str = None) -> bytes:
        self.file.seek(dll.offset)
        d = gzip.decompress(self.file.read(dll.size))

        if path is not None:
            p = Path(path)
            if p.exists() and not p.is_dir():
                raise IOError("PATH is not a directory")
            p.mkdir(parents=True, exist_ok=True)
            outfile = open(p.joinpath(dll.name), 'wb')
            outfile.write(d)
            outfile.close()

        return d

    def extract_all(self):
        for dll in self.dlls:
            self.extract(dll, self.path)
            if self.verbose:
                print("extracted %s" % dll.name)
