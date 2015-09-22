PACKAGE = "FundsData"
NAME = "FundsData"
DESCRIPTION = "This package can downloads funds data from http://huobijijin.com and then analyze the data for giving valuable funds."
AUTHOR = "Finix Lei"
AUTHOR_EMAIL = "finixlei@gmail.com"
URL = "https://github.com/FinixLei/FundsData"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache 2",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data=find_package_data(
            PACKAGE,
            only_in_packages=False
    ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache 2 License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
)
