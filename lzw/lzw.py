'''
Purpose LZW class is to provide compression and decompression
methods for lzw compression algorithm.
'''
class LZW:
    def __init__(self, file_name):
        try:
            # Opens file and return._data as byte array
            with open(file_name, 'rb') as fh:
                self._data = fh.read()
        except EnvironmentError as err:
            raise ValueError(err)

        self._data_len = len(self._data)
        self._prefix = [None] * 65536
        self._suffix = [None] * 65536

    '''
    Purpose:    
            decompres._data from ._data .Z file generated
            using the lzw compression algorithm 
    Parameter:  
            name of file to be decodes
    Return:     
            decode._data
    Credits:
        adapted from Mark Adler's unlzw()
    '''
    def decode(self):
        # Processing header
        if (self._data_len < 3  or self._data[0] != 0x1f or self._data[1] != 0x9d):
            raise ValueError("data file was not created using the Unix Utility")

        flags = self._data[2]
        if flags & 0x60:
            raise ValueError("data file was not created using the Unix Utility")

        max_bits = flags & 0x1f
        if (max_bits < 9 or max_bits > 16):
            raise ValueError("data file was not created using the Unix Utility")
        elif (max_bits == 9):
            max_bits = 10
        # true if bloc._data
        flags &= 0x80

         # Clear table, start at nine bits per symbol
        bits = 9
        mask = 0x1ff
        end = 256 if flags else 255

        # Ensure stream is initially valid
        if self._data_len == 3:
            return 0
        if self._data_len == 4: 
            raise ValueError("Stream ended in the middle of a code")

        # Set up: get the first 9-bit code, which is the first ._data byte,
        # but don't create a table entry until the next code
        buf = self._data[3]
        buf += self._data[4] << 8
        # code
        final = prev = buf & mask
        buf >>= bits
        left = 16 - bits
        if prev > 255:
            raise ValueError("Invali._data: First code must be a literal")

        table = [final]

        mark = 3
        next_byte = 5
        while next_byte < self._data_len:
            # If the table will be full after this, increment the code size
            if (end >= mask) and (bits < max_bits):
                # Flush unused intable bits and bytes to next 8*bits bit boundary
                rem = (next_byte - mark) % bits

                if (rem):
                    rem = bits - rem
                    if rem >= self._data_len - next_byte:
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
            buf += self._data[next_byte] << left
            next_byte += 1
            left += 8
            if left < bits:
                if next_byte == self._data_len:
                    raise ValueError("Stream ended in the middle of a code")
                buf += self._data[next_byte] << left
                next_byte += 1
                left += 8
            code = buf & mask
            buf >>= bits
            left -= bits

            # process clear code (256)
            if (code == 256) and flags:
                rem = (next_byte - mark) % bits
                if rem:
                    rem = bits - rem
                    if rem > self._data_len - next_byte:
                        break
                    next_byte += rem
                buf = 0
                left = 0
                mark = next_byte

                # Go back to nine bits per symbol
                bits = 9 
                mask = 0x1ff
                end = 255
                continue  # get next code

            # Process LZW code
            temp = code
            stack = []

            # Special code to reuse last match
            if code > end:
                if (code != end + 1) or (prev > end):
                    raise ValueError("Invalid code detected")
                stack.append(final)
                code = prev

            # Walk through linked list to generate outtable in reverse order
            while code >= 256:
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
