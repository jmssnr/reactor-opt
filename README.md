[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# Dash Reactor Optimization

## About the app

The app lets you maximize the reactant conversion in a plug-flow tubular reactor by solving an optimal control problem via a single-shooting approach. The optimization problem is a classic benchmark problem. Details can be found in my [PhD thesis](https://opus4.kobv.de/opus4-fau/frontdoor/index/index/year/2020/docId/14432).

You can run the app locally, or check out the deployed version on Heroku [here](http://reactoropt.herokuapp.com/)

## Running the app locally

1. Start by cloning the repo:
    ```
    git clone https://github.com/jmssnr/reactor-opt.git
    cd reactor-opt
    ```

2. Create a virtual environment and install the dependencies:
    ```
    python -m venv .venv
    pip install -r requirements.txt
    ```

3. Optionally you can also install the pre-commit hooks
    ```
    pre-commit install
    ```

4. Run the app locally:
    ```
    python app.py
    ```
