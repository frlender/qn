from setuptools import setup

setup(name='qn',
      version='0.2.2',
      description='Handy functions I use everyday.',
      url='https://github.com/frlender/qn',
      author='Qiaonan Duan',
      author_email='geonann@gmail.com',
      license='MIT',
      packages=['qn'],
      package_data={
          'configs':['*.py']
      },
      # install_requires=[
      #       'matplotlib',
      #       'seaborn',
      #       'numpy',
      #       'scipy',
      #       'pandas',
      #       'PyYAML',
      #       'matplotlib-venn',
      #       'scikit-learn'
      # ],
      zip_safe=False)
