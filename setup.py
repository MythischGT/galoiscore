from setuptools import setup, find_packages

setup(
    name="galois_core",
    version="0.1.0",
    description="A pure Python implementation of Finite Fields and Elliptic Curves for educational cryptography.",
    author="Tugrahan Gorkem Turkmen",
    author_email="tugrahan.gorkem@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        # No external dependencies for the math core! 
        # Keeping it pure makes it portable and auditable.
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",    # For code formatting
            "mypy>=1.0",      # For static type checking
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Security :: Cryptography",
        "Programming Language :: Python :: 3",
    ],
)