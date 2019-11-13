 '''
This is merely a Python adaptation of Mark Adler's lzw decompression method
with some slight modifications regarding the input and output of the overall 
decompress() method.
'''
def decompress(file_name):
    try:
        with open(file_name, 'rb') as fh:
            compressed_bytes = fh.read()
    except EnvironmentError as err:
        raise ValueError(err)

    byte_decoder = ByteDecoder(compressed_bytes)

    return byte_decoder.decode()
    
class ByteDecoder:
    '''
    Takes in a stream of compressed bytes, then decodes and
    returns a stream of decompressed bytes. 
    '''

    def __init__(self, compressed_bytes):

        self._cb_len = len(compressed_bytes)
        self._flags = compressed_bytes[2]
        self._max = compressed_bytes[2] & 0x1f
        self._compressed_bytes = compressed_bytes

        self._prefix = [None] * 65536
        self._suffix = [None] * 65536

        # Utilized for clearing table, starts at nine bits per symbol
        self._bits = 9
        self._mask = 0x1ff
        self._clear_code = 256

        self._err_code_1 = "Compressed data was not created using the Unix Utility"
        self._err_code_2 = "Invalid end of stream"
        self._err_code_3 = "Invalid code detected"
        self._err_code_4 = "First code must be a literal"
    
    def decode(self):
        '''
        Decompression method based directly off of Mark Adler's C library
        for decoding lzw files.
        '''

        self.ensure_validity()

        bits = self._bits
        mask = self._mask
        end = 256 if self._flags else 255

        # Set up: get the first 9-bit code, which is the first ._data byte,
        # but don't create a table entry until the next code
        buf = self._compressed_bytes[3]
        buf += self._compressed_bytes[4] << 8
        final = prev = buf & mask
        buf >>= bits
        left = 16 - bits
        if prev > 255:
        raise ValueError(self._err_code_4)

        table = [final]

        mark = 3
        next_byte = 5
        while next_byte < self._cb_len:
        # If the table will be full after this, increment the code size
        if (end >= mask) and (bits < self._max):
            # Flush unused intable bits and bytes to next 8*bits bit boundary
            rem = (next_byte - mark) % bits

            if (rem):
                rem = bits - rem
                if rem >= self._cb_len - next_byte:
                    break
                next_byte += rem

            buf = 0
            left = 0
            mark = next_byte

            # increment the number of bits per symbol
            bits += 1
            mask <<= 1
            mask += 1

        # Get a code of bits bits
        buf += self._compressed_bytes[next_byte] << left
        next_byte += 1
        left += 8
        if left < bits:
            if next_byte == self._cb_len:
                raise ValueError(self._err_code_2)
            buf += self._compressed_bytes[next_byte] << left
            next_byte += 1
            left += 8
        code = buf & mask
        buf >>= bits
        left -= bits

        # process clear code (256)
        if code == self._clear_code and self._flags:
            rem = (next_byte - mark) % bits
            if rem:
                rem = bits - rem
                if rem > self._cb_len - next_byte:
                    break
                next_byte += rem
            buf = 0
            left = 0
            mark = next_byte

            # Go back to nine bits per symbol
            bits = self._bits
            mask = self._mask
            end = 255
            continue  # get next code

        # Process LZW code
        temp = code
        stack = []

        # Special code to reuse last match
        if code > end:
            if (code != end + 1) or (prev > end):
                raise ValueError(self._err_code_3)
            stack.append(final)
            code = prev

        # Walk through linked list to generate outtable in reverse order
        while code >= self._clear_code:
            stack.append(self._suffix[code])
            code = self._prefix[code]

        stack.append(code)
        final = code

        # Link new table entry
        if end < mask:
            end += 1
            self._prefix[end] = prev
            self._suffix[end] = final

        # Set previous code for next iteration
        prev = temp

        # Write stack to outtable in forward order
        table += stack[::-1]

        return bytes(bytearray(table))

    
    def ensure_validity(self):
        '''
        Processes header and flags to ensure validity of the
        compressed data and to ensure it was indeed created
        using the lzw compression algorithm
        '''

        # Process header
        if self._cb_len < 3 or self._compressed_bytes[0] != 0x1f or self._compressed_bytes[1] != 0x9d:
            raise ValueError(self._err_code_1)

        # Ensure flag validity
        if self._flags & 0x60:
            raise ValueError(self._err_code_1)
        
        if self._max < 9 or self._max > 16:
            raise ValueError(self._err_code_1)
        elif self._max == 9:
            self._max = 10

        # True for compressed block
        self._flags &= 0x80

        # Ensure stream is initially valid
        if self._cb_len == 3:
            return 0
        elif self._cb_len == 4:
            raise ValueError(self._err_code_2)
