from setuptools import setup, find_packages

HYPEN_E_DOT = "-e ."

def get_requirements(filepath):
    requirements = []
    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name="Medicine Recommendation System",
    version="0.0.1",
    author="Latha",
    author_email="lathacharugundla@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)