import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysse",
    version="0.0.1",
    author="sj",
    author_email="root@mail.codeorder.cn",
    description="获取上海证券交易所网站数据的Python包。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/songjian/pysse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests==2.27.1',
        'pandas==1.3.5',
        'beautifulsoup4==4.10.0',
        ],
    python_requires='>=3'
)
