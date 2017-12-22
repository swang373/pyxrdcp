import ast
import re

from setuptools import setup, find_packages


VERSION_RE = re.compile(r'__version__\s+=\s+(.*)')


with open('pyxrdcp/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(VERSION_RE.search(f.read().decode('utf-8')).group(1)))


setup(
    name='pyxrdcp',
    version=version,
    packages=find_packages(),
    description='A wrapper for xrdcp implemented in Python',
    author='Sean-Jiun Wang',
    author_email='sean.jiun.wang@gmail.com',
    maintainer='Sean-Jiun Wang',
    maintainer_email='sean.jiun.wang@gmail.com',
    url='https://github.com/swang373/pyxrdcp',
    download_url='https://github.com/swang373/pyxrdcp/tarball/{0}'.format(version),
    license='MIT',
    python_requires='>=2.7, <3',
    install_requires = [
        'click',
        'futures',
        'tqdm',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    entry_points = {
        'console_scripts': [
            'pyxrdcp = pyxrdcp.pyxrdcp:cli',
        ],
    },
)

