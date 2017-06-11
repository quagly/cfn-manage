'''
cfn_manage
-----

Manage aws cloudformation templates
create/update/delete
pass parameters

'''
from setuptools import setup

setup(
    name='cfn-manage',
    version='0.1.0',
    url='https://github.com/quagly/cfn-manage',
    license='APACHE 2.0',
    author='Michael West',
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
    tests_require=[
        'pytest',
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
