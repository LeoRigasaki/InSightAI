from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='insightai',  # Changed from bambooai
    version='0.1.0',   # Fresh version number for the new package
    description='A lightweight library for dataset insights using Groq and OpenAI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'openai',
        'tiktoken',
        'pandas',
        'termcolor',
        'groq',
        'sqlite3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)