from setuptools import setup, find_packages


setup(
    name = "pypeline",
    version = "0.1",
    packages = find_packages("src", exclude = ["*tests"]),
    package_dir = {'': 'src'},

    # metadata for upload to PyPI
    author = "Ian Johnson",
    author_email = "languagetechnology@appliedlanguage.com",
    description = "A composable pipeline implementation using arrows.",
    license = "LGPLv3",
    keywords = "haskell arrow arrows monad monads computation pipeline pipelines",
    url = "http://www.appliedlanguage.com",

    setup_requires = ['nose>=1.0'],

    test_suite = 'nose.collector',
)
