from setuptools import setup, find_packages

setup(
    name='powerdata_download',
    description='NASA EarthData download interface',
    version='0.3.0',
    author='Pantelis Kouris',
    author_email='pako@dhigroup.com',
    url='https://www.dhi-gras.com',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
    extras_require={
        'test': [
            'pytest'
        ]}
)
