# CoffeeTracker
Analysing my co-workers' coffee consumption!

## Context
As part of the day-long Second Genome 2018 Hackathon, this project was developped to track coffee consumption in the SG office. 

## Usefulness
Absolutely none.


## Architecture
The goal was to design a system to visualize Second Genome’s coffee consumption in real time.

![architecture](images/arch.png)

* The SG coffee machine offers two choices of coffee beans: BlueBottle or Stumptown brand
* Coffee drinkers vote by pressing one of two programmable AWS IoT "dash" buttons.
* A button press triggers the _Coffee Tracker Lambda_ which collects the votes and sends them for storage in a dynamoDB table
* A second lambda, the _Coffee Calculator Lambda_ is listening to the dynamo table stream and aggregates new votes to the dataset and plots them
* The plots are then sent to S3 where a static HTML page is generated and served as a webpage.
* Display the results on office screens!

![](images/hour_line.jpeg)
![](images/weekday.jpeg)


Note: this project was never fully completed, hence the missing link between _Coffee Calc Lambda_ and the R script to generate these plots _trendseekers_plots.R_
