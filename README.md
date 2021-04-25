# Transportastic
###### TUM Junge Akademie Science Hack 2021

# Workflow
How to use:

1. Clone repository

2. Check if data contains bus trips

3. Install requirements

```
#Open cmd
pip install -r requirements.txt
cd ../webserver/pixida-web-ui
Npm install
Npm run build
cd ../..
```

4. Start application with controller.py with python3.7


*Backup of Devpost Readme*
## Inspiration
Public transportation providers in many cities are facing increasing problems with the **peak usage** of their services **during the rush hours** which will only increase in the future due to urbanization.
This is not only a problem for the providers but also for the millions of people using these services. This is especially true during the current pandemic where it can be life threatening to use overcrowded means of transportation.
Consequently, **our goal is to flatten the curve around the rush hour usage peaks** which can also help to flatten the curve in the pandemic.

## What it does
We are using **WiFi probe requests** to analyze the **occupancy of transportation** services.
Based on this data, we provide services to both the provider and the customer.
The provider can view the occupancy in **real-time in a web dashboard** and use this data to react quickly to the unexpected growth of passengers, e.g. by sending additional buses.
Moreover, historic occupancy data can be viewed for any bus line and **predictions generated with machine learning** are provided to improve the route planning.
By introducing a **reward based system**, we intent to incentivize passengers to use less occupied means of transportation in order to reduce the load on the main transportation systems. The reward comes in the form of **bonus kilometers** depending on the occupancy during the trip - "*the lower the occupancy, the higher the reward*". These bonus kilometers **can be used to get free trips** in the future.
To provide this information to the customer, we add information regarding occupancy and expected reward to the common information of a trip search.

## How we built it
The progam design satisfies the **Model-View-Control (MVC)** architecture. On a flask server, WiFi probe requests are stored and analyszed by our algorithms. Through a controller and under the use of HTTP-Requests, the data is transferred threadedly to the client in JSON packages. The client - a single-page-webapplication - is built on the Javascript-Framework **vue.js** and extended by the **bootstrap** CSS-Framework.

To count the number of people inside a mean of transportation, the following algorithm was abstracted from [this paper](http://www.kresttechnology.com/krest-academic-projects/krest-mtech-projects/ECE/M-TECH%20EMBEDDED%20%202019-20/2019%20IEEE%20BASE%20PAPERS/32.Occupancy%20Estimation%20using%20WiFi%20A%20Case%20Study.pdf).
- Input: MAC adresses, GPS position, speed
- 1: Identify a bus station
- 2: Count number of MAC adresses for each subsequent station
- 3: compare MAC adresses between subsequent stations and identify those present at both stations
The above-mentioned algorithm was evaluated based on Mean Absolute Error(MAE) metric and the algorithm achieved MAE score of 4.8


To predict the passenger load for next 24h, we adapted an idea from [this paper](http://statweb.stanford.edu/~tibs/lasso/lasso.pdf)
- Input: GPS position, speed, heading, timestamp
- Model: choose between Random Forrest, Support Vector Regression (SVR) and Linear Regression with L2 regularization (LASSO)

Random Forest was the best performing algorithm with the MAE score of 5.7


In the sitemap a homepage, an about us and two distinct use case demo-pages exist. On the one hand, the **Company Page** visualizes real-time bus positions and their respective occupancies. Users can interact with the busses in order to get more detailed trip information from a heatmap widget. On the other hand, the **Passenger Page** contains a simple trip planner, where users can get propositions based on their origin, destination, time and personal preference (fast or rewarding). The solutions are fetched from the **MVG-API** and displayed in a list view widget. 

For the **backend** we use **Python 3.7** to analyze the WiFi probe request data and to predict future occupancy with machine learning. The algorithms for these tasks were adapted from research papers providing the state of the art results.

## Challenges we ran into
Due to the widely used randomization of MAC addresses that are captured by the WiFi sniffer, it is difficult to provide accurate numbers of the passenger count. Another challenge was to identify when a bus is at a station. We have the speed and GPS position of the bus but it is not possible to detect whether the bus stops at a red light, in a traffic jam, or it is at a station. This could be solved by providing the GPS position of all stations.
Regarding the web page development, it was difficult to use a fully functional map underlay to show where the busses drive. This was due to the fact that the most used and documented tool which is GoogleMaps was recently moved behind a paywall.
In general it was difficult to find a good balance between using already implemented code snippets and implementing new code.

## Accomplishments that we're proud of
We are proud that we were able to identify and use the skillset of each member to form a well working unit. We discussed and agreed on all important ideas while giving all members the flexibility to come up with great solutions in their field of work.
Regarding the project, we not only identified a major problem of current and future transportation but provided an intuitive solution to reduce the extreme peaks during rush hours. If applied, this idea could increase the number of transported passengers while still flattening the peaks and moreover benefitting provider and customer. We generated this idea while developing sophisticated algorithms and building a fully functional web page as well as the data interface to visualize our data.

## What we learned
We learned that despite not working at one location it is possible to come together and create a productive and open-minded working environment.
To do so, the usage of agile project management was key.
Regarding the realization we learned how to set up a good interface between our python environment and the web dashboard.
Additionally, we learned about the usage of MAC addresses to count passenger data and that it is key to not only generate the algorithms but to also integrate these algorithms in use cases in order to show the need for this product. 

## What's next for Transportastic
We worked together on a GitHub repository and made it publicly available. With this, we ensure that not only our idea can be shared and further researched but that with the power of the open source community we can truly redefine mobility. 
