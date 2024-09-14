from setuptools import setup, find_packages

setup(
    name='mopidy-homeassistant-mixer',
    version='0.1.0',
    description='Mopidy mixer for Home Assistant media player control',
    author='Krzysztof Gorzelak',
    author_email='gorzelak@users.noreply.github.com',  # GitHub noreply email
    url='https://github.com/gorzelak/mopidy-homeassistant-mixer',
    packages=find_packages(),
    install_requires=[
        'mopidy>=3.0',
        'requests',
        'websockets',
    ],
    entry_points={
        'mopidy.ext': [
            'homeassistant = mopidy_homeassistant:Extension',
        ],
    },
)
