FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/
# Install any dependencies
RUN pip install -r requirements.txt

RUN apt-get update -y \
    && apt-get install -y \
       netcat \
       libgdal-dev \
       python3-gdal \
       libgl1 \
       libglib2.0-0 \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*


# Copy the current directory contents into the container at /app
COPY . /app/