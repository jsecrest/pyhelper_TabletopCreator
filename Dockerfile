# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt /docker-temp/
RUN python -m pip install -r /docker-temp/requirements.txt
RUN rm -rf /docker-temp
