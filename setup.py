import re
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().split('\n')


reg = re.compile(r"!\[(?P<alt_text>.*?)\]\((?P<path>.*)\)")
long_description = re.sub(reg, r"![\g<alt_text>](https://raw.githubusercontent.com/hmiladhia/img2text/master/\g<path>)",
                          long_description)

setuptools.setup(
    name="img2text",
    version="0.1.0",
    author="Dhia Hmila",
    author_email="dhiahmila.dev@gmail.com",
    description="A lightweight module to generate colorful ascii art from images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/hmiladhia/img2text",
    py_modules=['img2text'],
    install_requires=requirements,
    entry_points={
        'console_scripts': ['img2text=img2text:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords=['ascii', 'art', 'ascii-art', 'image', 'text', 'color', 'colour'],
)
