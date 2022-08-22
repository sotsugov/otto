# set base image (host OS)
FROM python:3.10.6-slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# use environment variables for the api calls and authentication
ENV OTTO_URL=
ENV OTTO_KEY=
ENV OTTO_SECRET=
ENV OTTO_OTP=

# command to run on container start
CMD ["behave", "-f", "allure_behave.formatter:AllureFormatter", "-o", "./allure-results"]
