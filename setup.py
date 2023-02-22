from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Version number
exec(open('sphinx_exec_directive/version.py').read())
version = __version__

setup(
    name='sphinx-exec-directive',
    version=__version__,
    description='Run Python code blocks and display the output directly within Sphinx documentation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yongrenjie/sphinx-exec-directive',
    author='Jonathan Yong',
    author_email='yongrenjie@gmail.com',
    license='MIT',
    packages=['sphinx_exec_directive'],
    python_requires='>=3.7',
    install_requires=["docutils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
