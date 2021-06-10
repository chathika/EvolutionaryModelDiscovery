'''EvolutionaryModelDiscovery: Automated agent rule generation and 
importance evaluation for agent-based models with Genetic Programming.
Copyright (C) 2018  Chathika Gunaratne
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
from setuptools  import setup

setup(
    name='EvolutionaryModelDiscovery',
    version='2.0.0',
    author='Chathika Gunaratne',
    author_email='chathikagunaratne@gmail.com',
    packages=['EvolutionaryModelDiscovery'],
    url='https://github.com/chathika/EvolutionaryModelDiscovery/',
    license='GPL',
    description='EvolutionaryModelDiscovery: Automated agent rule generation and importance evaluation for agent-based models with Genetic Programming.',
    long_description="""https://github.com/chathika/EvolutionaryModelDiscovery""",
    long_description_content_type='text/markdown',
    project_urls={
    'Source': 'https://github.com/chathika/EvolutionaryModelDiscovery',
    'Thanks!': 'https://arxiv.org/abs/1802.00435',
    'Thanks!': 'http://complexity.cecs.ucf.edu/',
    },
    install_requires=[
        "nl4py>=0.9.0",
        "deap",
        "numpy",
        "pandas",
        "networkx",
        "scipy",
        "scikit-learn",
        "eli5"
    ]
)
