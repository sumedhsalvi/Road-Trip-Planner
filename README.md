# Road-Trip-Planner

## Goal
Goal is to find the best route according to the specified cost
function, as well as the number of segments, number of miles, 
number of hours for a car driver, and expected number of hours for the delivery driver.
###Given Conditions-

- Dataset of major highway segments of the United States including 
one line per road segment connecting two cities. The space delimited 
fields are: first city, second city, length (in miles), speed limit (in miles per hour),
 name of highway.
- Dataset of cities and towns with corresponding latitude-longitude 
positions including one line per city, with three fields per line, 
delimited by spaces. The first field is the city, followed by the latitude,
followed by the longitude.
- Inconsistencies and mistakes in datasets - For the fields, First City and Second City
in road segment dataset contains highway names instead of the name of a town. Some cities
will not have latitude-longitude coordinates in city gps dataset.

## Running the code
python3 ./route.py [start-city] [end-city] [cost-function]

## Search Abstraction

### initial state:

A list of cities with their gps coordinates and road segments with their length, 
speed limit and name of highway.

### successor function:
Successor function finds all possible next cities in the dataset that can reached 
from the given city.

### cost function:
We have implemented A* algorithm by adding the next cost to the total cost travelled, 
and added heuristic value to this value which is being used as a priority for priority 
queue. This also includes pop and push operations on the priority queue which has been 
used as a fringe.

Initially, we processed the dataset files and stored the data in dictionaries. The key of 
road-segments dataset in a dictionary is city name and values are stored as the string of values 
needed for our code and separated by ':' The key of city-gps dataset in a dictionary 
is city name and latitude and longitude fields are stored in the values.

We have implemented fringe which has been used as priority queue. The priority can be computed 
based on the cost function parameters and manhattan distance between cities. First we check whether the 
current city in the path is the end city and apply relevant logic to store route-taken which can be 
used to generate output in the expected format. If the current city is not the end city then our 
logic check for the successors of the current city and push values to the fringe by keeping 
track of the visited cities.

To calculate the heuristics, we have used manhattan distance and the relevant parameter 
from the respective cost function.

In addition, we have attempted to solve the statetour cost function. We have stored all the state 
names in a list and also added functions to return visited states count and not-visited 
states count. If we reach end city with all the states explored then the logic returns 
whole route taken, otherwise set the priority by not-visited states count, current segment 
length and distance between cities, and push the parameters to the fringe by keeping 
track of visited cities.

### goal state:
Reach the end city by taking the best route based on the cost function. 

## Algorithm:

1. Store the dataset of road-segments in a dictionary
2. Transform the list into a heap using heapify
3. Define the fringe as a priority queue (lowest score will be popped first)
4. Add the start city to the fringe along with other parameters.
5. Loop that pops the best state from the fringe and apply below logic, <br/>
   a. Find manhattan distance between start city and end city<br/>
   b. Find the successor states based on road-segments dataset stored in a dictionary<br/>
   c. Iterate over successors,<br/>
     - If we reach goal state (end city) then return the whole route taken.<br/>
     - Else append the current segment to the path taken to reach this successor, calculate the 
priority that is being pushed onto the fringe which we used as a priority queue, and keep 
track of the current city as a visited state.
