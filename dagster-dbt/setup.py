from setuptools import find_packages, setup

setup(
    name="ecommerce_dm",
    packages=find_packages(),
    install_requires=[
        "dagster==1.6.6",
        "dagster-dbt==0.22.6",
        "dbt-core==1.7.0",
        "dbt-postgres==1.7.0"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
