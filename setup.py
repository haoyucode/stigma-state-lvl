from setuptools import find_namespace_packages, setup

setup(
    name='stigma_state_lvl',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    version='0.1.0',
    description='State level analyses of opioid use disorder (OUD) using the JCOIN MAARC Stigma Survey Protocol 2 ("in-depth")',
    author='norc',
    license='',
)
