# Stock-Market-Simulation
This is a small project I worked on over winter break. It uses a user class which interacts with three types of stock classes—a general stock class, a purchased stock class, and a sold stock class (in order of inhertiance)—to purchase and sell stocks. In addition, the user class hs a graph function which plots its money spent versus its portfolio worth. To validate input into functions and make the output of functions more readable, I used decorators. Lastly, I utilized various libraries: yahoo finance to get stock information, pandas to process stock history, matplotlib to visualize data, and built-in library Pickle for object sterilization.
![alt text](https://cdn.discordapp.com/attachments/752243157475000473/798782787788210226/StockMarketSimulationSampleGraph.png)
Below is an example of a graph the program can produce. This graph is especially useful because it provides the stocks purchased at every dot along the "dollars invested" line in the top left, and it also provides the exact closing numbers on the right side of the graph.
![alt text](https://cdn.discordapp.com/attachments/752243157475000473/798807892420853760/StockSim.png)

Here is a sample output of the client file where the username is Jamil and the initiated balance is 123456:

Welcome to the Stock Market Simulation Script. Enter your username to login or create a new account. Jamil
How much money would you like to put into your account? 123456
Account successfully created.
-
01/12/2021 21:08:10 - Stock Market Simulation
Your balance is currently $123456.0
-
01/12/2021 21:08:10 - Stock Market Simulation
Successfully purchased 3x Amazon.com, Inc. for $924.03. Your new balance is $122531.97.
-
01/12/2021 21:08:15 - Stock Market Simulation
Successfully purchased 3x Facebook, Inc. for $309.93. Your new balance is $122222.04.
-
01/12/2021 21:08:18 - Stock Market Simulation
Successfully purchased 3x Intel Corporation for $51.93. Your new balance is $122170.11.
-
01/12/2021 21:08:22 - Stock Market Simulation
Successfully purchased 3x Moderna, Inc. for $85.02. Your new balance is $122085.09.
-
01/12/2021 21:08:25 - Stock Market Simulation
Successfully purchased 3x Microsoft Corporation for $204.24. Your new balance is $121880.85.
-
01/12/2021 21:08:28 - Stock Market Simulation
Successfully purchased 3x Apple Inc. for $218.49. Your new balance is $121662.36.
-
01/12/2021 21:08:30 - Stock Market Simulation
Successfully purchased 12x DocuSign, Inc. for $3151.8. Your new balance is $118510.56.
-
01/12/2021 21:08:33 - Stock Market Simulation
Successfully purchased 1x DocuSign, Inc. for $262.65. Your new balance is $118247.91.
-
01/12/2021 21:08:36 - Stock Market Simulation
Successfully sold 1x Apple Inc. stock for 128.8 each or 128.8 total
-
01/12/2021 21:08:39 - Stock Market Simulation
Your balance is currently $118376.71 and you have the following holdings
3x Amazon.com, Inc. (AMZN - $3120.83) purchased on 2014-05-02 for $308.01 each or $924.03 total
3x Facebook, Inc. (FB - $251.09) purchased on 2015-11-02 for $103.31 each or $309.93 total
3x Intel Corporation (INTC - $53.24) purchased on 2013-01-15 for $17.31 each or $51.93 total
3x Moderna, Inc. (MRNA - $124.55) purchased on 2019-05-02 for $28.34 each or $85.02 total
3x Microsoft Corporation (MSFT - $214.93) purchased on 2017-06-02 for $68.08 each or $204.24 total
2x Apple Inc. (AAPL - $128.8) purchased on 2020-05-04 for $72.83 each or $145.66 total
13x DocuSign, Inc. (DOCU - $262.65) purchased on 2021-01-12 for $262.65 each or $3414.45 total
-
01/12/2021 21:08:41 - Stock Market Simulation
Error: Provided stock ticker is not valid. Please use a valid ticker from the National Market System
-
01/12/2021 21:08:44 - Stock Market Simulation
Your account does not have the funds to purchase 1000000x Alphabet Inc. stock for $1746.55 each or $1746550000.0 total.
-
01/12/2021 21:08:52 - Stock Market Simulation
Error: Provided date does not match the format YYYY-MM-DD
-
01/12/2021 21:08:52 - Stock Market Simulation
Error: Invalid quantity. Quantity must be of integer type and greater than 0
-
01/12/2021 21:08:52 - Stock Market Simulation
Error: Invalid quantity. Quantity must be of integer type and greater than 0
-
01/12/2021 21:08:52 - Stock Market Simulation
You do not own a stock with ticker XRX purchased on 2020-03-02
-
01/12/2021 21:08:54 - Stock Market Simulation
You only own 3x FB stock. Revise your quantity
-
01/12/2021 21:08:56 - Stock Market Simulation
Graph opened in new window

Process finished with exit code 0
