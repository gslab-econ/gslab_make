# GSLab Make Library

Overview
--------
This repository contains the `gslab_make` Python library. 

Information about this package is available in its internal documentation. 

Requirements
------------
- Python 2.7, 3.7
- `setuptools` ([installation instructions](https://packaging.python.org/installing/))

Installation
------------

The preferred installation method is to use [pip](https://pypi.python.org/pypi/pip):
```
pip install git+ssh://git@github.com/gentzkow/gslab_make.git@master
```
or
```
pip install git+https://git@github.com/gentzkow/gslab_make.git@master
```
which are the SSH and HTTPS protocol versions, respectively.

The package at any tagged release, branch, or commit can be installed with the same commands, just changing `master` to the desired target; e.g., 
```
pip install git+ssh://git@github.com/gentzkow/gslab_make.git@<tag, branch name, or commit hash>
```

Note that this installation procedure may require obtaining machine privileges through,
say, a `sudo` command.

Alternatively, one may install the local version of `gslab_make` by running (from the root of the repository)

```
pip install .
```

We do not recommend that these packages be installed by executing
```bash
python setup.py install
```
This method of installation uses egg files rather than wheels, which can cause conflicts with previous versions of `gslab_tools`. If this method of installation is executed, some files need to be removed from the directory with a `clean` argument. `clean` removes `/build`,`/dist`, and `GSLab_Make.egg-info`, which are built upon installation. This argument can be called by executing 

```bash
python setup.py clean
```

License
-------
See [here](https://github.com/gentzkow/gslab_make/blob/master/LICENSE.txt).

FAQs
-------

Q: What if I want to install a different branch called `dev` of `gslab_make` rather than `master`?

A: Either `git checkout dev` that branch of the repo before installing, or change `@master` to `@dev` in the `pip install` instruction.

