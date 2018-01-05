FROM python:2.7-jessie

RUN mkdir -p /app/logs

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Instalo dependencias
RUN apt-get update
RUN apt-get -y install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8

RUN pip install --no-cache-dir -r requirements.txt

RUN rm -f db.sqlite3
RUN python manage.py migrate

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000