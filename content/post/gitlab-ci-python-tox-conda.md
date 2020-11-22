
+++ 
date = "2020-11-22" 
title = "Python Development with Jupyter, Gitlab CI and Tox" 
+++

In this post I want to give a brief overview how to structure a Python package, load it in Jupyter notebooks, setup continuous integration with Gitlab and `tox-conda` that I like to use for data science projects.

Most data scientists coming from R will probably ask themselves:

> What is *the* way to structure a Python package?

and:

> How can I get the `load_all()` behaviour from RStudio replicated in Jupyter to get access to my package in my notebooks?

While in R there is only one (admittedly sometimes limiting) way to structure a package, you have got quite a lot of options in the Python world.

Since data science workloads rely heavily on the `conda` packaging ecosystem (especially on Windows machines), I will focus on how to make everything play nicely with `conda`.

## Python Package

We begin setup by creating a new conda environment and specifying the interpreter we want to use and activating it:
```
conda create --name <environment_name> python=3.8 -y
conda activate <environment_name>
```

Now we need to setup our package structure. In R there is a function called `package.skeleton()` (or alternatively RStudio's GUI) that create a basic package with all necessary files. For Python there are different packages that provide similar functionality (such as `cookie-cutter`), but I will quickly outline a minimal setup here:

```
src/
    package_name/
        __init__.py
        python_file1.py
        ...
        python_fileN.py
tests/
notebooks/
data/
outputs/
setup.py
gitlab-ci.yml
tox.ini
config.yml
CHANGELOG.md
README.md
.gitignore
.env
```


Let's take a look at three important files:

- setup.py
- gitlab-ci.yml
- tox.ini

### setup.py

A simple `setup.py` file sufficient for small to medium sized projects can look like this:

```
from setuptools import setup
from setuptools import find_packages

setup(name='<pkg-name>',
      version='0.10',
      description='<package-description-here>',
      author='<your-name>',
      author_email='<your-email>',
      license='<your-license>',
      packages=find_packages("src"),
      package_dir={"": "src"},
      zip_safe=False,
      install_requires=[
          '<some-pkg>,
          ## Note: the space between the @ are acutally necessary!
          '<some-gitlab-package>  @  git+ssh://git@<package-url-with-slashes>.git@master',
      ],
      extras_require={
          'dev': [
              'pytest',
              'mypy',
              'pylint',
              'coverage',
              'python-dotenv',
              'tox-conda',
              'ipykernel',
              'matplotlib',
              'plotnine',
              'seaborn',
          ]
      }
)
```

For development purposes, you can install your package using:

```
pip install -e .[dev]
```

### gitlab-ci.yml

At work, IT only provides us with a basic Gitlab bash runner, so we need to be careful not to accidentially change our testing environment permanently.

As a work around, we use `tox-conda` which as the name suggests makes `tox` play nicely with conda environments. All test are run using `tox` in conda environments. 

A very simple gitlab-ci.yml can look like this:

```
stages:
# sample stages might include:
- test
- deploy

variables:
    # declare any variables here
    WORKSPACE: "../{CI_PROJECT_NAME}

before_script:
    # here you can run any commands before the pipelines start
    - echo $CONDA_PREFIX

after_script:
    # Do something after the pipeline is finished
    # Attention: if you do clean-up here and delete your junit output, Gitlab cannot upload the file 

test job:
    stage: test
    script:
    - tox
    artifacts:
        when: always
        reports: 
            junit: report.xml
        paths:
            - report.xml
        expire_in: 1 week

deploy job:
  stage: deploy
  script: <deploy>

last job:
  stage: .post
  script: <this will always be the last run job, so you can do for example clean-up here>

# Find more info here: https://docs.gitlab.com/ee/ci/yaml/
```

The next file we are going to cover ist `tox.ini` that helps us with running tests. Tox is a very convenient tool, as it takes care of automatically creating test environments (in our case conda environment, because we use `tox-conda`) and running any tests etc we want. Let's take a look:

### tox.ini

```
[tox]
envlist =
    {py37, py38}

[testenv]
passenv = *
deps=
    pytest-sugar
    python-dotenv
commands=
    pytest --junitxml=report.xml

[testenv:black]
deps=
    black
commands=
    black --check .
```

Note, the `passenv` part is necessary if you want to pass environment variables from Gitlab to tox. You can test multiple Python versions by passing them in `envlist`.


Don't forget to exclude your `.env` file from version control by putting it in `.gitignore` in case you have any api tokens or similar in your environment file.

You can specify environment variables in Gitlab to be used by your pipelines where you can mask them in log outputs.

## Jupyter Integration

Since I already included the `ipykernel` package in my `setup.py` file, we do not need to install it anymore. 

```
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

Last, but not least, I include the following code in my juypter notebook to get the mimic RStudio's `load_all()`, and load some environment variables:

```
# Load autoreload module 
# autoreload 1: reload modules imported with %aimport everytime before execution
# autoreload 2: reload all modules
%load_ext autoreload
%autoreload 2
%matplotlib inline
%load_ext dotenv

dotenv -o "../.env"
```

That's it, you should have working Python project structure ready to use :)

You can download a zip file containing a sample project from [here](post/python-sample-project.zip).
