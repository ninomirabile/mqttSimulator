"""
Setup script for MQTT Simulator package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mqtt-simulator",
    version="0.1.0",
    author="MQTT Simulator Contributors",
    author_email="contributors@mqtt-simulator.com",
    description="A Python microservice/library for simulating real-time data publishing via MQTT",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mqtt-simulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mqtt-simulator=mqtt_simulator.cli:cli",
        ],
    },
    keywords="mqtt iot simulator weather agriculture energy real-time data",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mqtt-simulator/issues",
        "Source": "https://github.com/yourusername/mqtt-simulator",
        "Documentation": "https://github.com/yourusername/mqtt-simulator#readme",
    },
) 