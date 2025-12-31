from setuptools import find_packages, setup

package_name = 'nebula_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
        (f'share/{package_name}', ['package.xml']),
        (f'share/{package_name}/launch', files_if_exist('launch/*.launch.py') + files_if_exist('launch/*.py')),
        (f'share/{package_name}/config', files_if_exist('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alitalha',
    maintainer_email='alitqlhq@gmail.com',
    description='Bringup for Nebula UAV',
    license='MIT',
