# Use an official Python runtime as a parent image
FROM python:3.13.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY ../requirements.txt /app

# Install the Python virtual environment package
RUN python -m venv venv

# Install dependencies from the requirements file

# RUN venv/bin/pip install --upgrade pip && \
#     venv/bin/pip install -r requirements.txt && \
#     venv/bin/pip list
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip list


# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variable to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Run app.py when the container launches
# RUN . /app/venv/bin/activate 
# # CMD ["/app/venv/bin/python", "main.py"]
# CMD ["exec python", "main.py"]
CMD . venv/bin/activate && exec python myapp.py


