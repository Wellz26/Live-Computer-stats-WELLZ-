#!/usr/bin/env python3
"""Setup script for Wellz - Gaming PC Stats Dashboard"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wellz",
    version="1.0.0",
    author="Wellz26",
    author_email="wellz26@github.com",
    description="A visually artistic gaming PC stats dashboard for your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wellz26/Live-Computer-stats-WELLZ-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "wellz=wellz.cli:main",
            "wellz-gui=wellz.gui:main",
        ],
    },
    keywords="system monitor gaming pc stats terminal cli dashboard",
)
