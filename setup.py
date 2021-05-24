import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().split('\n')

setuptools.setup(
    name="img2text",
    version="0.0.1",
    author="Dhia HMILA",
    author_email="dhiahmila@gmail.com",
    description="A lightweight module to generate colorful ascii art from images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/hmiladhia/img2text",
    py_modules=['img2text'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords=['ascii', 'art', 'ascii-art', 'image', 'text', 'color', 'colour'],
)
