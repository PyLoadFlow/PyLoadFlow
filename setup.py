from distutils.core import setup

setup(
    name="pyloadflow",
    packages=["pyloadflow"],
    version="0.1.0",
    license="MIT",
    description="A simple and powerful load calculations library for python 3",
    author="Luis Miguel Pintor Olivares",
    author_email="contact.pyloadflow@gmail.com",
    url="https://github.com/PyLoadFlow/pyloadflow",
    download_url="https://github.com/PyLoadFlow/pyloadflow/archive/v_01.tar.gz",
    keywords=[
        "electric",
        "fast decoupled",
        "load flow",
        "newton raphson",
        "power flow",
    ],
    install_requires=[
        "numpy",
        "scipy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
