# Problem
Calls to 2 3rd party apis with limits to the number of daily requests that can be made.

Unreliable services which may go up and down at any time.

# Description
The application consists of 3 services
ranking, pricing and http

The services form a pipeline task with ranking data pulled down continuously and pushed into a topic called ranking.
That topic is read by pricing which then populates the entries with upto date pricing data then pushes into a rankingwithpricing.
The http service pulls the latest data down from the last topic and displays it for the user.

The service is designed to pull data down periodically and add the data to topics so that the service will still operate 
if the 3rd party services are down. Communication between services is done with eventual consistency in mind so that the 
system will continue to operate if one or 2 services are down.

# starting the application
This will build and tag the images and launch the services

`make app.up`

# things to do
Separate out api keys, urls from REPO into env variables. 

Improve scraping job for flask server by utilising background threads.
