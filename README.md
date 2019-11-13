# LZWFILE
Python module for decoding lzw files. This is based directly off Mark Adler's C library for decoding lzw files.
Some slight modifications were done for my own use case.

## Getting Started

```Python
from lzwfile import decompress

# File name can be used if located within same directory,
# if not please use the absolute path.

file_name = 'compressed_file.Z'

decompressed_data = decompress(file_name)
```

## Notes

I'm planning on adding encoding functionality to this package as well to further my understanding
of the lzw compression algorithm. 
