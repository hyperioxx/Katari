import os
import sys
from setuptools import setup,find_packages


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 4)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Katari requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "Katari",
    version = "0.0.9",
    author = "Aaron Parfitt",
    author_email = "aaronparfitt123@gmail.com",
    description = ("A SIP(Session Initiation Protocol) Application Framework"),
    license = "BSD",
    keywords = "voip",
    url = "http://packages.python.org/Katari",
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    scripts=['scripts/katari'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
