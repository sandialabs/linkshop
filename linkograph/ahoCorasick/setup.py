"""Installation script for the module ahoCorasick."""
from distutils.core import setup, Extension
import platform  # For determining the os type, i.e. linux, windows, etc.

osType = platform.system()

flags=["-O2"]

if osType.lower().startswith('windows'):
    flags.extend(['/EHsc', '/O2'])

ahoCModule = Extension('ahoCorasick',
                       sources=['src/acPython.cpp', 'src/ahoCorasick.cpp'],
                       extra_compile_args=flags)
setup(name='AhoCorasick',
      version='1.0',
      description='Implementation of the Aho-Corasick Algorithm',
      long_description=" ".join("""
        Module to accelerate substring matching using the Aho-Corasick
        algorithm.
       """.strip().split()),
      author='Carson Kent',
      author_email='ckent@sandia.gov',
      platforms=['POSIX'],
      package_dir={'': 'src'},
      ext_modules=[ahoCModule])
