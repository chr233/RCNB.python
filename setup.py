import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="rcnb",
    version="1.0.2",
    author="chr_",
    author_email="chr@chrxw.com",
    description="Everything can be encoded into RCNB with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chr233/RCNB.python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
