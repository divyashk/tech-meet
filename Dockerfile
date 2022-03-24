FROM python:3.8-slim-buster
# Install dependencies:
COPY requirements.txt .
COPY templates ./templates
COPY static ./static
RUN pip install -r requirements.txt
EXPOSE 5000
COPY main.py .
RUN mkdir blueprints
COPY ./blueprints/__init__.py ./blueprints/__init__.py
COPY ./blueprints/apis.py ./blueprints/apis.py
COPY creds.json .
# Run the application:
CMD python main.py