from setuptools import find_packages, setup

setup(
    name='Mopidy-HomeAssistant',
    version='0.1.0',
    url='https://github.com/yourusername/mopidy-homeassistant',
    license='Apache License, Version 2.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Mopidy extension to control volume and mute through Home Assistant.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Mopidy >= 3.0',
        'requests',
    ],
    entry_points={
       'mopidy.ext': [
            'homeassistant = mopidy_homeassistant.extension:Extension',
        ],
    },
)
