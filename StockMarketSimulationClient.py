import StockMarketSimulation as sms

user = sms.User.login()
"""Inputting dates when purchasing stocks is not advised and can cause errors because the program functioning off of
only closing prices"""
# The following code gives you a good base portfolio
print(user.purchase("amzn", 3, "2014-5-2"))
print(user.purchase("fb", 3, "2015-11-2"))
print(user.purchase("intc", 3, "2013-1-15"))
print(user.purchase("mrna", 3, "2019-5-2"))
print(user.purchase("msft", 3, "2017-6-2"))
print(user.purchase("aapl", 3, "2020-5-4"))
print(user.purchase("docu", 12))
print(user.purchase("docu", 1))  # This line tests group for stocks with same price
print(user.sell("aapl", 1, "2020-5-4"))
print(user)
# Testing all error cases:
# Trying to buy a stock that does not exist
print(user.purchase("msftttt", 12))
# Trying to spend money money than I have
print(user.purchase("goog", 1000000))
# Purchasing stock with invalid date
print(user.purchase("aapl", 3, "20/15/2003"))
# Purchasing stock with invalid quantity
print(user.purchase("aapl", -1))
print(user.purchase("aapl", 7.6))
# Trying to sell a stock I do not own
print(user.sell("xrx", 12,"2020-3-2"))
# Trying to sell more quantity of a stock than I own
print(user.sell("fb", 4, "2015-11-2"))
# Graphing the users account
print(user.graph_account())
# Save user if you wish to do so
# print(user.save())
