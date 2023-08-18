from setuptools import setup, find_packages

setup(
    name='MultiCleaningSystem',
    version='1.0',
    description='Paquete para modelar un sistema multiagente destinado a la limpieza automática de una ubicación',
    author='José Armando Rosas Balderas, Ramona Najera Fuentes',
    author_email='a01704132@tec.mx, a01423596@tec.mx',
    url='https://github.com/ArmandoRosasB/Proyecto_WALL-E',
    packages=find_packages(),
    scripts =['main.py'],
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()]
)