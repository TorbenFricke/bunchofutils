from distutils.core import setup

with open('requirements.txt') as f:
      requirements = f.read().splitlines()

setup(name='torbotils',
      description='A bunch of utilities',
      author='Torben Fricke',
      author_email='mail@torben.co',
      packages=['torbotils'],
      package_data={'torbotils': ['styles/*']},
      install_requires=requirements,
     )