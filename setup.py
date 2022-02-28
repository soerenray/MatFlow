from distutils.core import setup

setup(name='matflow',
      version='1.0',
      url='https://git.scc.kit.edu/pse-2021/team-2/pse-worfklow-project',
      packages=['', 'database', 'exceptionpackage', 'frontendapi', 'hardwareadministration', 'useradministration',
                'workflow'],
      package_dir={'': 'matflow'},
      data_files=[('', ['README.md', 'docker-compose.yaml'])]
      )
