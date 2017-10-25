from setuptools import setup

setup(name='PythonPokedex',
      version='0.2',
      description='Python+Flask Frontend for Veekun PokeDex DB',
      url='https://github.com/ObamaNYoMama/pythonpokedex',
      author='Zach Bresser',
      author_email='github@chbresser.com',
      license='MIT',
      packages=['PythonPokedex'],
      install_requires=[
          'flask', 'sqlite3'
      ],
      zip_safe=False)