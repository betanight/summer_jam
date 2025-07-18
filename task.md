# Part 1. Rules & Criteria for Data Scientist

During the July Code Jam, you should create a model of an optimal route for your summer activity. 

You can receive a maximum of 35 points for your work. Your data part will be judged according to this criteria: 

## Part 1: Find and prepare data

In this stage of the project you need to collect data on locations that will be included. Each location should contain longitude and latitude as well as location name for later visualization. We recommend to select at maximum 9 locations to find the optimal route in the reasonable time.

You can use any source for locations but if you feel stuck you can try searching some datasets on Kaggle. There are many datasets with cities there which you can use for selecting the locations. Keep in mind that when you decide to take the dataset from Kaggle you need to check the quality and eventually preprocess the data, e.g. check incorrect values (if some points are out of reasonable range) or missing values.

## Part 2: Modeling

After your data is ready you need to create first route and visualize it. For this route you can select next location randomly. This will be your baseline model. Please remember that each route point should be visited only once. For each of the routes you create do not forget to compute the total distance after visiting all locations. This is important as it would allow to evaluate the improvement of the route by your optimization model.

After your baseline model (random) is established you need to come up with an approach how to optimize your route, i.e. find the route with the shortest total distance. Talking in terms of mathematical optimization the total distance is the objective function which should be minimized. The task to find the optimal distance is a little bit different from usual ML modeling which we talked about a lot in the platform. In this case there is no historic data which can be used for training to make the prediction. To minimize the distance you need to come up with algorithm that selects the next location to visit in such a way that the total distance is minimized (and no location was visited twice).

After your model is created and run please calculate the total distance for the optimized route as well as time needed to find this optimal route. It would be nice if both your baseline and optimized solution are visible on the screen for comparison.

## Part 3: Visualization (& explain the data to SE students)

The visualizations should be interactive, and you’ll need to work with your teammates to determine what elements will be interactive and how the end-user should interact with it. Please prepare the code in Python for visualizing the results of your modeling. You will need to share this Python code with SE teammates that will use it for website. For creating interactive visualizations you can use libraries such as plotly. For inspiration you can have a look at [these examples](https://plotly.com/python/maps/).

Each of your visualizations should be unique. For a refresher on the different types of graphs you can make (and the code to make them), you can use [this site](https://www.python-graph-gallery.com/) as a reference. These graphs can be used to visualize statistics for locations or travel times.

It is important that your visualizations include a map with locations and optimal route on this map as well as initial and optimized total distance and time needed for model to calculate the optimal route. Additionally you can include any visualizations you like.

## Part 4: Reporting Results - either part of a web page or a report goes

- technical staff
- where the data came from
- if use Python put report in readme

While visualizations are very useful for pointing out important features of a dataset, they are not sufficient for a full data analysis. The last stage of your work must be writing your results. These will be included in the repo you submit for grading.

You must write:

- An introduction to the dataset of a minimum of 100 words
    - What data do you have? How it was collected?
    - What did you do? Was preprocessing required?
    - How to read your report/what do you have in the report?
- A minimum of 100 words about the model that you created. Please describe how your algorithm works as well as which libraries you used to implement it. Describe the approaches that you experimented with and explain why the final approach was chosen.
- A minimum of 50 words for each visualization, explaining, giving broader context, and drawing conclusions
- A conclusion of at least 50 words, indicating what further explorations might be made into the dataset

## Reporting results for grading

Your team should submit a link to a Github public repo with all of your working materials to Denis. For assessing your work, there should be a Jupyter notebook containing:

- The code for your EDA work (Part 1)
- The code to calculate the optimal route and evaluate its quality (Part 2)
- The visualizations you created (Part 3)
- The texts for describing and reporting your results (Part 4)

Additionally, the files which you prepared for your SE teammates should also be present.

## Grading criteria for data science (35 points max)

- Code quality (5 points)
    - Does it follow established convention?
    - Is it easy to read?
    - Are there sufficient comments in the code?
    - Is it error-prone?
- Preprocessing (5 points)
    - Is the data suitable for modeling? Does it solve the required task?
    - Were problems/wrinkles discovered in the data? If so, how were they addressed?
    - Was the data grouped in a logical/useful manner?
- Modeling (15 points)
    - Have participants explored multiple approaches?
        - Can be described in a Jupiter file, add it to GitHub repo
    - Was the baseline model provided?
    - Is distance function defined correctly?
    - Does optimization help improve the route?
    - Is the model evaluated correctly?
- Results (10 points)
    - Does the introduction sufficiently describe the data?
    - Do each of the visualization descriptions fully explain the image?
    - The selected approach and selection criteria are explained.
    - Have clear conclusions been drawn?
    - Has it been indicated what next steps might be taken?