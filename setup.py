import setuptools

with open("README.md") as f:
    readme = f.read()

setuptools.setup(
    name="duckpy",
    version="2.1.1",
    packages=["duckpy"],
    url="https://github.com/Gelbpunkt/duckpy",
    author="Amano Team",
    author_email="contact@amanoteam.com",
    license="MIT",
    description="A simple module for searching on DuckDuckGo",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp"],
)
