# Provider Read me

- my-sdk is provider
- pyproject.toml is configuration file used by packaging tools
  - build-systems in that hatchling, tool used to build package
  - indicate the packaging tool , where to find the version of the package [tool.hatch.version]
  - project details
  - get_provider_info() returns information regarding the provider and this allow us to transform our python package into compatiable airflow provider

- my_sdk is package
  - __init__.py - defint that get provider info function in this python file
  - get_provider_info() return a dictionary , this dict will conatin some fields describing your airflow provider
    - task-decorators, the decorators we want to make available from our airflow providers. this list can have different dictonaries, but for this task we will have only one dictonary as we gonna create one decorator.
    - if we dont provide this function then our python package wont be an airflow provider and this function is actually the entry point of our airflow provider as defined in the pyproject.toml file

- we will build custom_operator our decorator will use, so we will create new decorator, not a new operator, we will use the existing SQLoperator to work so please check the python file in decorators folder, i have commented the information what each line is doing.

- we are going to create the python function corresponding to our decorator and decorator will use "_SQLDecoratedOperator" class

- so to install our provider, as it is not available in pypi, so we will create a docker image that will copy this my-sdk folder and then we will install the provider by exectuing the command pip install and a local path
  - dockerffile
  - moidfy the yaml file to create an image, instead of extract the airflow image we will create an image using docker build