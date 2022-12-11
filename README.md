# Pic16A-Project
Pic16A Class project: Predict College Basketball Match

Group Members: Wei-Jen Lee, Haoyang Lyu, Adam Traut

Description: our project uses the college basketball match data in year 2020 to learn about the performance of each team and predicts their rankings as well as the winner of the match

Python package: numpy 1.21.5, pandas 1.4.2, matplotlib 3.5.1 and random

Demo File:
![1670800953059](https://user-images.githubusercontent.com/119776543/206935032-a6733060-da44-4497-a411-91d2b0af692c.png)
The data we are working on with is the college basketball match outcome of previous years. We want to predict the rankings of each team, which is only included in the year 2020 data. In addition to that, we also want to predict the final winner of the basketball match.

![1670801171098](https://user-images.githubusercontent.com/119776543/206935189-cde8e737-b294-44de-a011-4177b18fb1aa.png)
To determine which columns to use, we defined this function the get column correlations. We used it to select columns that are not very intercorrelated but also strongly correlates to the ranking. User can change the specified column names to get correlations between different columns.
In our model, we conlcuded that "W","ADJOE","ADJDE" are the 3 most relevant columns to ranking.

![1670801320432](https://user-images.githubusercontent.com/119776543/206935298-3cc5153d-fb29-4f95-abf7-42592f5f173f.png)
By performing a linear regression, we can get the newly predicted team rankings.

![1670801426146](https://user-images.githubusercontent.com/119776543/206935383-4d88e42f-a1d1-444d-907a-6e2a0248e910.png)
This model can also be veryfied in data from other years. Since they lack the ranking column, we used "BARTHAG" column to obtain model score. Our model has a score of 0.97 which is relatively good.

![1670801529726](https://user-images.githubusercontent.com/119776543/206935466-122f3b7f-4878-4297-b7ca-1e419cb0a424.png)
And in the end there is this march_madness function which simulates basketball match between 64 teams and produces the final winner.

Scope and Limitation: the code can similarly be applied to predict the outcome of other sport matches like football, soccer etc, with modification of parameters and class definition. However it cannot automatically generate the desired parameters and requires the user to have a relatively good understanding of the specific sports to use.

References and acknowledgement: Prof Lee, UCLA 22Fall Pic16A Lec2 Lecture Notes.
                                We sincerely thank Prof Lee, the TAs and the LAs for their instructions
                              
Source of the dataset: https://www.kaggle.com/datasets/andrewsundberg/college-basketball-dataset

