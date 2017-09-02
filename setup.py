from setuptools import setup

setup(
    name = 'jizera',
    version = '170214',
    license = 'MIT',
    author = 'Dominik Gronkiewicz',
    author_email = 'gronki@gmail.com',
    url = 'https://github.com/gronki/jizera',
    packages = ['jizera'],
    install_requires = [
        'flask',
        'loremipsum',
    ],
    include_package_data = True,
    zip_safe = False,
)
