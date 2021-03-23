FROM python:3.7-slim-buster


# Copy all the code to a directory called app
ADD . /app

#  Set working directory to /app so we can execute commands in it
WORKDIR /app

# STEP 2: Install required dependencies.
RUN pip install -r requirements.txt

ENV SQLALCHEMY_DATABASE_URI=sqlite:///database.db
ENV SECRET_KEY=

# STEP 6: Expose the port that Flask is running on
EXPOSE 5000

# STEP 7: Run Flask!
CMD ["flask", "run", "--host=0.0.0.0"]