"""Setup configuration for spool-shared package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spool-shared",
    version="0.1.0",
    author="Spool Team",
    author_email="team@spool.com",
    description="Shared utilities for Spool microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/G2-Spool/spool-shared",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "pydantic>=2.0.0",
        "fastapi>=0.104.0",
        "python-jose[cryptography]>=3.3.0",
        "structlog>=23.1.0",
        "httpx>=0.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
        ]
    },
)