import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SmartSpliter", 
    
    version="{{VERSION_PLACEHOLDER}}",

    author="alpaka",
    author_email="a1pakadeveloper@gmail.com",
   
    description="A balanced dataset splitter for multi-domain, multi-class AI tasks.",
    
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/a1paka12/SmartSpliter",
    
    packages=setuptools.find_packages(),
    
    python_requires=">=3.8",

    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
    ],

    entry_points={
        "console_scripts": [
            "SmartSplit=SmartSplit.cli:main",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Utilities",
    ],
)