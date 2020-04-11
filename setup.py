#  Drakkar-Software Package-Version-Manager
from setuptools import setup, find_packages

from package_version_manager import PROJECT_NAME, VERSION

with open('README.md', encoding='utf-8') as f:
    DESCRIPTION = f.read()

REQUIRED = open('requirements.txt').readlines()
REQUIRES_PYTHON = '>=3.7'

setup(
    name=PROJECT_NAME,
    version=VERSION,
    url='https://github.com/Drakkar-Software/Package-Version-Manager',
    license='MIT',
    author='Drakkar-Software',
    author_email='drakkar-software@protonmail.com',
    description='Package release tool',
    py_modules=['cli'],
    packages=find_packages(),
    data_files=['config.yml', 'logging_config.ini'],
    include_package_data=True,
    long_description=DESCRIPTION,
    zip_safe=False,
    setup_requires=REQUIRED,
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    entry_points={
        'console_scripts': [
            'pvg = cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
    ],
)
