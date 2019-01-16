from distutils.core import setup

with open('requirements.txt') as f:
      requirements = f.read().splitlines()

setup(name='bunchofutils',
      description='A bunch of utilities',
      author='Torben Fricke',
      author_email='mail@torben.co',
      packages=['bunchofutils'],
      package_data={'bunchofutils': ['styles/*']},
      install_requires=requirements,
     )