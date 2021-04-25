# Transportastic
###### TUM Junge Akademie Science Hack 2021


*Backup of Devpost Readme*
## Inspiration
Public transportation providers in many cities are facing increasing problems with the **peak usage** of their services **during the rush hours** which will only increase in the future due to urbanization.
This is not only a problem for the providers but also for the millions of people using these services. This is especially true during the current pandemic where it can be life threatning to use overcrowded means of transportation.
Consequently, **our goal is to flatten the curve around the rush hour usage peaks** which can also help to flatten the curve in the pandemic.

## What it does
We use **WiFi probe requests** to analyze the **occupancy of transportation** services.
Based on this data, we provide services to both the provider and the customer.
The provider can view the occupancy in **real-time in a web dashboard** and use this data to react quickly to unexpected growth of passengers, e.g. by sending additional buses.
Moreover, historic occupancy data can be viewed for any line and **predictions generated with machine learning** are provided to improve the route planning.
By introducing a **reward based system**, we give the passenger an incentive to use less occupied means of transportation io order to reduce the load on the main transportation systems. The reward comes in form of **bonus kilometers** depending on the occupancy during the trip - "*the lower the occupancy, the higher the reward*". These bonus kilometers **can be used to get free trips** in the future.
To provide this information to the customer, we add information regarding occupancy and expected reward to the common information of a trip search.

## How we built it
The progam design satisfies the **Model-View-Control (MVC)** architecture. On a flask server, WiFi probe requests were stored and analyszed by our algorithms. Through a controller and under the use of HTTP-Requests, the data was transferred threadedly to the client in JSON packages. The client - a single-page-webapplication - was built on the Javascript-Framework **vue.js** and extended by the **bootstrap** CSS-Framework. **@@@TODO** 
- MAPs integration api 
- Models and Algorithms (with references)

In the sitemap a homepage, an about us and two distinct use case demo-pages exist. On the one hand, the **Company Page** showed simulated real-time bus positions and their respective occupancies. Users could then interact with the busses in order to get more detailed trip information from a heatmap widget. On the other hand, the **Passenger Page** implemented a simple trip planner, where users could get propositions based on their origin, destination, time and personal preference (fast or rewarding). The solutions were fetched from the **MVG-API** and displayed in a list view widget. 

For the **backend** we used **Python 3.7** to analyze the WiFi probe request data and to predict future occupancy with machine learning. The algorithms for these tasks were adapted from research papers providing the state of the art.

**Frontend**
**Interface**

## Challenges we ran into
Due to the widely used randomization of MAC adresses which are captured by the WiFi sniffer it is difficult to provide accurate numbers of the passenger count.


## Accomplishments that we're proud of
We are proud that we were able to identify and use the skillset of each member to form a well working unit. We discussed and agreed on all important ideas while giving all members the flexibility to come up with great solutions in their field of work.
Regarding the project, we not only identified a major problem of current and future transportation but provided an intuitive solution to reduce the extreme peaks during rush hours. If applied, this idea could increase the number of transported passengers while still flattening the peaks while benefitting provider and customer. We generated this idea while developing algorithms and building a fully functional web page as well as the data interface to visualize our data.

## What we learned


## What's next for Transportastic


Text formatting
## Headline
**bold**
_ italics _
[link](http://foo.bar)
![Alt text](/path/to/img.jpg)
Code block example
```ruby
puts "Hello World!"
```