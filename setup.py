from setuptools import setup, find_packages

setup(
    name="deepseek_query_tool",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(exclude=["tests*", "logs*"]),
    include_package_data=True,
    package_dir={"": "."},
    install_requires=[
        line.strip() for line in open("requirements.txt").readlines() if line.strip()
    ],
    entry_points={
        "console_scripts": [
            "deepseek=main:main",  # Ajuste conforme o ponto de entrada
        ],
    },
)
