import os

from setuptools import setup, find_packages, extension

# Read file contents
def read(file_name, encoding='utf-8'):

    full_path = os.path.join(os.path.dirname(__file__), file_name)
    
    with open(full_path, 'r', encoding=encoding) as fh:
        contents = fh.read().strip()
        return contents

setup(
    name='lzwfile',
    version='0.1.5',
    author='Jayden Laturnus',
    author_email='jaydenlaturnus@gmail.com',
    description='Python module for decoding compressed lzw files',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/JJJados/lzwfile',
    license='MIT',
    keywords='lzw',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">=3.6.0",
)