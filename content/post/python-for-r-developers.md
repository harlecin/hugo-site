+++
date = "2018-03-17"
title = "Introduction to Python for R developers"
+++

I am a long time R user and I like R a lot. Coding in RStudio is a breeze and most every problem already has an associated package with a solution on CRAN. Nevertheless, I wanted to learn Python as well, because I firmly believe, if you only have a hammer, then every problem looks like a nail. Setting up a Python development workflow for data science proved to be a bit more work than I originally anticipated and that is why I wanted to provide a quick start guide for experienced R developers who want to get up to speed in Python.

First I will dive into setting up your coding environment on Windows 10 (macOS and Linux have similar, easier setups, but at work our laptops are Windows only, so here we go ...). Then I will quickly cover how to work with virtual environments, install packages, write your own Python package with unit tests, documentation, linting and how to debug your code. Since I like working with Docker a lot, I will also include some additional information on making your Python code work nicely with Docker.

## Getting started - VS Code as Python IDE
There are lots of great Python development environments out there, but personally I am very much in love with Visual Studio Code. I like a lightweight editor that I can customize to my hearts content. Plus, VS Code is available for Windows, macOS and Linux and is completely free to use. So this post will focus on VS Code. 

### Prerequisites

Before we begin, you need to:

1. [Download](https://code.visualstudio.com/) and install Visual Studio Code
2. [Download](https://www.anaconda.com/download/) and install Anaconda Python 3.6
3.  Install Microsoft's Python extension

Feel free to choose a different Python distribution, but I would recommend using Anaconda Python on Windows. Anaconda comes with most of the packages you are going to need for scientific computing and you do not need to build packages from source (which can be a pain on Windows).   

After you completed the steps above, create a file called `hello_world.py` with the following code:

```python
print("hello world")
``` 

Press `ctrl+shift+p` and type `Python: Run Python file in Terminal` and press Enter. You should now see *'hello world'* printed to the integrated terminal.

## Working with virtual environments and installing packages
When you work on multiple projects sooner or later you will run into dependency issues:

> Project A needs library XY version 1.1, but Project B needs library XY version 1.2 and there are lots of breaking changes between package versions

One way to resolve this kind of problem is to isolate project dependencies using virtual environments. A virtual environment specifies and isolates the Python interpreter you want to use for a given project and (depending on which virtual environment tool you use) most/all dependencies. As already mentioned before, we will focus on Continuum Analytics' package and dependency management system `conda` that is part of Anaconda Python. 

`conda` provides a couple of very nice benefits compared to other similar tools:

- It works on Windows, macOS and Linux
- While it was originally developed for Python, you can also use it for other languages such as R
- `conda` allows you to install and update packages easily and works with `pip install` (the Python equivalent to R's `install.packages()`)


**Note:** If you use Anaconda Python, do not change the default terminal in VS Code to PowerShell. Anaconda [cannot active environments](https://github.com/ContinuumIO/anaconda-issues/issues/2533) properly using Powershell.

Before we start, here is a high-level overview of how to use virtual environments:

![Overview][overview-conda-workflow]

Let's start by creating a virtual environment called `myenv`:

### Creating environments & installing packages
Open an integrated terminal in VS Code and type 
```
# create the environment
conda create --name myenv

# Active/deactivate the environment
activate myenv
deactivate myenv

# create environment with specific Python & package versions
conda create -n myenv python=x.y
conda install -n myenv pip scipy=a.b.c numpy matplotlib
```
**Note:** You have to use `source activate myenv` on macOS/Linux.

It is also possible to use `pip` to install packages in a `conda` environment:
```
# first install pip using conda
conda install pip -y
# then use pip to install scipy
pip install scipy
```

You can select an existing environment by pressing `ctrl+shift+p` and typing *'Python: Select Interpreter'* or clicking on the interpreter icon currently active on the right side of VS Code's menu bar at the bottom. 

You can also specify a default package list that is installed every time you create a new environment. Furthermore, it is possible to clone existing environments using:
```
conda create --name myclone --clone myenv
```
### Information about environments
Use 
```
conda info --envs
```
to get a list of all environments available.

You can easily see which environment is currently active by looking at your terminal.
```
(myenv) C:\your-working-directory
```
The active environment is shown in `()`. Alternatively, you can see an asterisk `*` in front of the active environment if you use `conda info --envs`.

To see which packages are currently installed in an environment run:
```
# to get a list of all packages
conda list -n myenv

# to check for a specific package (returns nothing or package version)
conda list -n myenv pip
```
### Exporting an environment
An environment can be exported using:
```
# writes a conda config to your current working directory
# that can handle both pip and conda packages
conda env export > file_name.yml

# Build environment based on file_name.yml:
# to create an environment from scratch
conda env create -f file_name.yml
# to build an environment based on a .yml config run in an existing environment
conda env update --file file_name.yml
```

### Deleting an environment
If you want to delete an environment and all associated content run:
```
conda remove --name myenv --all
```
**Note:** Don't forget, if you use a Linux based Docker image you have to run `source activate myenv`!

You can also use `conda` to save environment variables.

More detailed information is available on the `conda` [help pages](https://conda.io/docs/user-guide/tasks/manage-environments.html).


### Conda environments in Docker
Creating Docker containers with `pip install` is super easy. All you need to do is specify a *'requirements.txt'* file for pip to use in your Dockerfile:

```
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
```
However, conda always creates a virtual environment if you want to restore an *'environment.yml'* file. So you have three options:

1. Use `conda install` in your Dockerfile and specify all dependencies there
2. Use `pip freeze > requirements.txt` if everything can be installed using `pip`
3. Use conda inside your Docker container to setup a virtual environment in which to install the packages specified in your *'environment.yml'* and either do:

**Option 3.1**
which I found on [Docker and conda](https://beenje.github.io/blog/posts/docker-and-conda/) (shortened and modified):
```
FROM continuumio/miniconda3:latest
WORKDIR /app
COPY . /app/
COPY environment.yml /app/environment.yml

## create conda environment from environment.yml
RUN conda env create -n myapp -f environment.yml

## activate the myapp environment
ENV PATH /opt/conda/envs/myapp/bin:$PATH
```
Alternatively, you can try:  

**Option 3.2** from [Using Docker with Conda Environments](https://fmgdata.kinja.com/using-docker-with-conda-environments-1790901398) a bit shortened and modified:
```
FROM continuumio/miniconda3:latest
WORKDIR /app
COPY . /app/
COPY environment.yml /app/environment.yml
## Using bash! conda does NOT support sh, which is the Docker default (/bin/sh)! 
ENTRYPOINT [ “/bin/bash”, “-c” ]

CMD [ “source activate your-environment && exec python application.py” ]
```



[overview-conda-workflow]: /img/workflow-python-conda.png "Overview workflow Python + conda"