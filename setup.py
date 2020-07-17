from setuptools import setup

setup(
    name='EC2Console',
    version="1.0.0",
    install_requires=["boto3", "fire", "bullet"],
    entry_points={
        "console_scripts": [
            "logic = logic:entry"
        ]
    }
)