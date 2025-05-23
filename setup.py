from setuptools import setup, find_packages

setup(
    name="reservation_system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.27",
        "pydantic==2.6.1",
        "python-dotenv==1.0.1",
        "faker==22.6.0",
        "click==8.1.7",
        "pytest==8.0.0",
        "pytest-asyncio==0.23.5",
        "httpx==0.26.0",
    ],
) 