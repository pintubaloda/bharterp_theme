from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="bharterp_theme",
    version="1.0.0",
    description="BhartERP Theme — Branding, Print Templates, Email Templates and India Compliance for ERPNext",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Paisape Techfin Private Limited",
    author_email="dev@paisape.org",
    url="https://github.com/paisape-techfin/bharterp_theme",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=["frappe"],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Frappe",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
)
