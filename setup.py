from setuptools import setup, find_packages

setup(
    name="SmartSplit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas", "numpy", "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "SmartSplit=SmartSpliter.cli:main"
        ]
    },
    author="Your Name",
    description="Automatic multi-domain balanced dataset splitter for AI competitions",
    license="MIT",
)
