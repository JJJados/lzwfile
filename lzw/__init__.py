from lzw import LZW

file_name = "C:/Users/T947106/Documents/lzw/test.Z"

content = LZW(file_name)
print(content.decode())

f = open("test.csv", "wb")

f.write(content.decode())

f.close()