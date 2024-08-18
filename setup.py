from setuptools import setup, find_packages

# Function to read the requirements from a file
def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

setup(
    name='pyfinmuni',
    version='0.0.1',
    description='A Python package containing finumi personal finance API',
    author='Ramachandra Vikas Chamarthi',
    author_email='x@navyaai.com',
    url='https://github.com/xadnavyaai/IndiaFinanceAPI',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'dev': read_requirements('requirements-dev.txt')
    },
    python_requires='>=3.6',
)
