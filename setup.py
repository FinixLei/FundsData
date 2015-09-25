from setuptools import setup

PACKAGE = "fundsdata"
NAME = "fundsdata"
DESCRIPTION = "This package can download funds data from http://huobijijin.com and then analyze the data for giving valuable funds."
AUTHOR = "Finix Lei"
AUTHOR_EMAIL = "finixlei@gmail.com"
URL = "https://github.com/FinixLei/FundsData"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License, Version 2.0",
    url=URL,
    packages=["fundsdata"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'fundsdata = fundsdata.funds_data:main',
            ]
    },
    zip_safe=False,
)
