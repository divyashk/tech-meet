FROM python:3.8-slim-buster
# Install dependencies:
COPY ./requirements.txt .
COPY ./templates ./templates
COPY ./static ./static
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./app.py .
COPY ./blueprints ./blueprints
COPY ./creds.json .
# Run the application:
CMD python app.py

