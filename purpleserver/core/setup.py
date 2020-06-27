from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='purplship-server.core',
      version='2020.7.0',
      description='Multi-carrier shipping API Core module',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship-server',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='AGPLv3',
      packages=find_packages("."),
      install_requires=[
            'purplship',
            'purplship.package'
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
      ],
      zip_safe=False
)
