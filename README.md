# LZWFILE
Python module for decoding lzw files. This is based directly off Mark Adler's C library for decoding lzw files.
Some slight modifications were done for my own use case.

## Getting Started

```Python
from lzwfile import decompress

fn = 'compressed_file.Z'

decompressed_data = decompress(fn)
```

## Notes

I'm planning on adding encoding functionality to this package as well to further my understanding
of the lzw compression algorithm. 
