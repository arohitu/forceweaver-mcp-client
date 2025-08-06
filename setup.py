#!/usr/bin/env python3
"""
Setup script for ForceWeaver MCP Client
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="forceweaver-mcp-client",
    version="1.1.0",
    author="ForceWeaver Team",
    author_email="support@forceweaver.com",
    description="Professional Salesforce Revenue Cloud health checking for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/forceweaver/mcp-client",
    project_urls={
        "Bug Tracker": "https://github.com/forceweaver/mcp-client/issues",
        "Homepage": "https://mcp.forceweaver.com",
        "Documentation": "https://github.com/forceweaver/mcp-client",
        "Support": "https://mcp.forceweaver.com/support",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Communications",
    ],
    keywords="salesforce mcp ai health-check revenue-cloud model-context-protocol",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "mcp>=1.12.0",
        "aiohttp>=3.8.0",
        "requests>=2.28.0",
        "certifi>=2022.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "forceweaver-mcp=forceweaver_mcp_client.client:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)