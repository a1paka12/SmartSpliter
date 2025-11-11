from setuptools import setup, find_packages

setup(
    name="smart-split",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pandas", "numpy", "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "smart-split=smart_split.cli:main"
        ]
    },
    author="Your Name",
    description="Automatic multi-domain balanced dataset splitter for AI competitions",
    license="MIT",
)
