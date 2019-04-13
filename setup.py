from setuptools import setup, find_packages

setup(
    name="jobmatcher",
    version="1.0",
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask_cors",
        "flask_restful",
        "pyjwt",
        "jsonify",
        "flask_httpauth",
        "flask_mongoengine",
        "marshmallow",
        "marshmallow-mongoengine",
        "flask-mail",
        "bs4",
        "googletrans",
        "nltk",  # to check if not work -> delete
        "singledispatch"   # to check if not work -> delete
    ]
)