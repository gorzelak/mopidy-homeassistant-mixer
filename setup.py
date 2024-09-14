from pathlib import Path
from setuptools import setup, find_packages

# Read the README.md file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='mopidy-homeassistant-mixer',
    version='0.1.1',
    description='Mopidy mixer for Home Assistant media player control',
    long_description=long_description,
    long_description_content_type='text/markdown', 
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
