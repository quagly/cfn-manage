'''
cfn_manage
-----

Manage aws cloudformation templates
create/update/delete
pass parameters

'''
from setuptools import setup

# I think it is bad practice to name the package with - but module with _.
# I suspect this is why I cannot reference cfn-manage.__version__ in this script
setup(
    name='cfn-manage',
    version='0.1.0',
    url='https://github.com/quagly/cfn-manage',
    license='APACHE 2.0',
    author='Michael West',
    author_email='quagly@gmail.com',
    description='manage aws cloudformation templates'
                'create/update/delete and pass parameters',
    packages=['cfn_manage'],
    include_package_data=True,
    platforms='any',
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'boto3',
    ],
    extras_require={
        'dev': [
            'pytest>=3',
            'coverage',
            'tox',
            'sphinx',
            'moto',
        ],
    },
    tests_require=[
        'pytest>=3',
        'moto'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
