FROM ubuntu
COPY . /application
WORKDIR /application
RUN install pip | pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python" ]
CMD [ "application.py" ]
