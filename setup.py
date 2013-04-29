#
# Copyright Applied Language Solutions 2012
#
# This file is part of Pypeline.
#
# Pypeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pypeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pypeline.  If not, see <http://www.gnu.org/licenses/>.
#
from setuptools import setup, find_packages


setup(
    name = "pypeline",
    version = "0.2.2",
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
    install_requires = ['futures>=2.1.3'],

    test_suite = 'nose.collector',
)
