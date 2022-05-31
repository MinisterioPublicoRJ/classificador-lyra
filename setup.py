from setuptools import setup, find_packages


__version__ = '0.0.0dev1'


setup(
    name='classificador-lyra',
    descripition='Classificação e análise de setenças e documentos judiciais.',
    url='https://github.com/MinisterioPublicoRJ/classificador-lyra',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    author='Felipe Ferreira & Rhenan Bartels',
    license='MIT',
    zip_safe=False
)
