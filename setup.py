"""
pytest-tap is a reporting plugin for pytest that outputs
`Test Anything Protocol (TAP) <http://testanything.org/>`_ data.
TAP is a line based test protocol for recording test data in a standard way.

Follow development on `GitHub <https://github.com/python-tap/pytest-tap>`_.
Developer documentation is on
`Read the Docs <https://tappy.readthedocs.io/>`_.
"""

from setuptools import find_packages, setup


if __name__ == "__main__":
    with open("docs/releases.rst", "r") as f:
        releases = f.read()

    long_description = __doc__ + "\n\n" + releases

    setup(
        name="pytest-tap",
        version="3.3",
        url="https://github.com/python-tap/pytest-tap",
        license="BSD",
        author="Matt Layman",
        author_email="matthewlayman@gmail.com",
        description="Test Anything Protocol (TAP) reporting plugin for pytest",
        long_description=long_description,
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        entry_points={"pytest11": ["tap = pytest_tap.plugin"]},
        include_package_data=True,
        zip_safe=False,
        platforms="any",
        install_requires=["pytest>=3.0", "tap.py>=3.0,<4.0"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Framework :: Pytest",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Testing",
        ],
        keywords=["TAP", "unittest", "pytest"],
    )
