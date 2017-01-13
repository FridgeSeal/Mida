import setuptools
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='mida',
    version='0.1.0.dev1',
    description=long_description,
    url='https://github.com/FridgeSeal/Mida',
    author='FridgeSeal',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers/Science/Research',
        'License ::  OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='greatcircledistance',
    packages=setuptools.find_packages(),
    install_requires=['numba']
)