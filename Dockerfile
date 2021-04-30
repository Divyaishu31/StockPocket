FROM python:3.8-slim

RUN apt-get update

# add user (change to whatever you want)
# prevents running sudo commands
RUN useradd -r -s /bin/bash mohit

# set current env
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

RUN chown -R mohit:mohit /app
USER mohit

# set app config option
ENV FLASK_ENV=production

# set argument vars in docker-run command
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# Avoid cache purge by adding requirements first
ADD ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt --user

# Add the rest of the files
COPY . /application
WORKDIR /application

# start web server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:application", "--workers=5"]
