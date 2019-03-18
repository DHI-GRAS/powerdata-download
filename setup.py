from setuptools import setup, find_packages

setup(
    name='powerdata_download',
    description='NASA EarthData download interface',
    author='Pantelis Kouris',
    author_email='pako@dhigroup.com',
    url='https://www.dhi-gras.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ]
)
