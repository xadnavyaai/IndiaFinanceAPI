from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pyfinmuni',
    version='0.0.1',
    description='A Python package containing finumi personal finance API',
    author='Ramachandra Vikas Chamarthi',
    author_email='x@navyaai.com',
    url='https://github.com/xadnavyaai/IndiaFinanceAPI',
    packages=find_packages(where='.'), 
    package_dir={'': '.'},  
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    python_requires='>=3.6',
)
