### How to install pyomo with Cython

Create your virtual environment and install project dependencies.

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements
```

Install the Python development package corresponding to your Python version.

```shell
sudo apt update
sudo apt-get install python3.<X>-dev
```

Change `<X>` to your Python version.

Clone the pyomo repository.

```shell
git clone https://github.com/Pyomo/pyomo.git
```

Navigate to the root folder of cloned pyomo repo and (with your venv activated) 
install pyomo by running the following command.

```shell
python setup.py install --with-cython
```

Make yourself comfortable, it will take some time...
