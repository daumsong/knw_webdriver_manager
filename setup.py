import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knw_Chromedriver_manager",
    version="0.1.1",
    install_requires=[
        "requests",
    ],
    author="OH nam kyun",
    author_email="daumsong@gmail.com",
    description="Chromedriver_manager for knw",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daumsong/knw_webdriver_manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)