### How to install pyomo with Cython

First create and activate your virtual environment.

```shell
python -m venv .venv
source .venv/bin/activate
```

Next, install the Python development package corresponding to your Python version.

```shell
sudo apt update
sudo apt-get install python3.<X>-dev
```

Change `<X>` to your Python version.

Next, install the setuptools and cython packages 
(make sure your virtual envirnoment is active).

```shell
pip install setuptools
pip install cython
```

At the end, clone the pyomo repository to your location.

```shell
git clone https://github.com/Pyomo/pyomo.git
```

Navigate to the root folder of cloned pyomo repo and install pyomo by running

```shell
python setup.py install --with-cython
```

Make yourself comfortable, it will take some time...
