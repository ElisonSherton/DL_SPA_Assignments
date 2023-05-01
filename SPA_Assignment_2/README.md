# SPA Assignment 2

This repo contains files organized for submission towards the second assignment of Stream Processing and Analytics Course offered as an elective in BITS-WILP programme MTech in DSE.

The folder structure is as follows
- **data**: This folder consists of the stock exchange instruments (In a real world this may be stored in a database like `Dynamo` or a File System storage like `S3` and there would be APIs to get the stock ticker information, but we've kept our solution low-key and simple and made a `json` file with a list of the three instruments for which we're allowing the trades.)
- **dynamic_generation**: This folder consists of `.py` scripts used to generate orders and the FIFO match making algorithm. The order generator might be thousands or lakhs of clients placing these orders through REST API Endpoints but in our case we have an `order_generation.py` script which does that job. Similarly for order matching, we could have on-prem servers or a `FaaS` like *AWS Lambda* which subscribes to a kafka cluster and does the order matching and executes trades. For our usecase, we have written a script `order_matching.py` which implements this simple algorithm locally.
- **images**: A folder which contains static images for showcasing the SMA query results.
- **logs**: Logs to demonstrate the trades happening in real time.
- **results**: Stores the orders and trades executed by the python scripts. In the real world, these would be persisted in a file system/database.
- **results_dynamic**: Similar to results only except this folder stores the output of the programs run through dynamic_generation scipts.
- **static_generation**: Similar to dynamic generation but since we can't wait for long periods of time for the sake of the demo, we are generating trades for two days in advance and computing the SMA/Profit calculation using the scripts `sma_computation.py` and `profit_calculator.py` respectively. These could also be implemented in real world using on-prem servers/FaaS services and subsequently their results could be persisted. The profit calculator would be run in a batch mode since needs the closing price of instruments and the SMA Computation could be done in stream mode.
- **playground.ipynb**: As a scratchpad of sorts to check the working of different components.
- **SPA-Assignment-2-2.pdf**: Problem Statement of the assignment.

Following resources contain a video and a document explaining the entire process step by step. Hope you find this useful.

|Contents|Link|
|--|--|
|Explanation Video|[spa_explanation_video_group_57.mp4](https://drive.google.com/file/d/1qwRtjtcnMP4seuS2cpRIvf2eFqSzP42f/view?usp=sharing)|
|Document describing submission|[SPA_Assignment_2.doc](https://docs.google.com/document/d/1_07-x-PGR6gvFvsXvHAJiYOBP_VA_6bds1B3BdQFl4c/edit?usp=sharing)|