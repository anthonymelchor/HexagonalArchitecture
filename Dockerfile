# Use the official Python 3.10 image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install the dependencies
RUN pip install Flask==3.0.0 SQLAlchemy==2.0.21 mysqlclient==2.2.0 PyJWT==2.8.0

# Expose the port your Flask app will run on
EXPOSE 5000

# Specify the command to run your application
CMD ["python3", "main.py"]