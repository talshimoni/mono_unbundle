from setuptools import setup, find_packages
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
pfile = Project(__file__).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
print(requirements)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'mono_unbundle',
    version='2019.03.10.dev0',
    description='Extract DLLs from Xamarin app bundles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tjg1/mono_unbundle',
    author='Tomasz J Goralczyk',
    author_email='tomg@fastmail.uk',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Software Development :: Disassemblers',
        'Topic :: System :: Archiving :: Packaging',
        'Operating System :: Android',
        'Programming Language :: C#'
        
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='reverse_engineering android xamarin apk',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mono_unbundle=mono_unbundle.cli:cli'
        ]
    }
)