from setuptools import setup, find_packages

setup(
    name='stock_visualizer_backend',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A Django app to visualize stock data',
    install_requires=[
        'Django>=3.2',
        # Add other dependencies as needed
    ],
)