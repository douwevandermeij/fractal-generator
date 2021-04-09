# Fractal-generator

Fractal-generator is a code generator for projects using Fractal.

## Demo

First install Fractal itself:

    pip install git+https://github.com/douwevandermeij/fractal.git@master#egg=fractal

To generate a demo Shop, copy the examples and run:

    python generator_shop.py && black shop && isort shop

To test the application run:

    python shop_test.py

Or run FastAPI, but first install some dependencies:

    pip install fastapi uvicorn sentry_sdk
    python shop/contrib/fastapi/main.py