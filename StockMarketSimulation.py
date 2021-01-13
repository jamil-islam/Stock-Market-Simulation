import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime

"""
Notes:
This program uses closing prices and only supports stocks from the National Market System (Nasdaq, NYSE, ETC.)
This means stocks can only be purchased on days when the market is open. For this reason, if you, for example, purchase
a stock on the weekend it will actually be purchased on Friday.
"""


class Stock:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.name = self.stock.info["longName"]

    @property
    def history(self) -> pd.Series:
        return self.stock.history(period="max", rounding=True)["Close"]

    @property
    def latest_price(self):
        return self.history[-1]

    @property
    def stock(self):
        return yf.Ticker(self.ticker)

    def __str__(self):
        return f"{self.name} ({self.ticker} - ${self.latest_price})"


class PurchasedStock(Stock):
    def __init__(self, ticker: str, quantity: int, purchased_date: str = "now"):
        super().__init__(ticker)
        if purchased_date == "now":
            purchased_date = self.get_closest_date()
        try:
            purchased_price = np.float64(self.history[purchased_date])
        except KeyError:
            raise Exception('''Error: Inputting dates in the past or future is a feature intended for developers only.
            The date you have inputted is not in the history of the stock.''')
        self.purchased_date = purchased_date
        self.purchased_price = purchased_price
        self.quantity = np.int64(quantity)

    # Provides history since purchase date
    @property
    def recent_history(self) -> pd.Series:
        return self.history[self.purchased_date::]

    def get_purchased_total(self):
        return round(self.purchased_price * self.quantity, 2)

    def get_current_total(self):
        return round(self.quantity * self.latest_price, 2)

    def get_closest_date(self) -> datetime.datetime:
        return self.history.index[-1].to_pydatetime()

    def __lt__(self, other):
        return self.purchased_date < other.purchased_date

    def __str__(self):
        return "{}x {} purchased on {} for ${} each or ${} total".format(self.quantity, super().__str__(),
                                                                         self.purchased_date.date(),
                                                                         self.purchased_price,
                                                                         self.get_purchased_total())


class SoldStock(PurchasedStock):
    def __init__(self, ticker: str, quantity: int, purchased_date: str, sold_date: str = "now"):
        super().__init__(ticker, quantity, purchased_date)
        if sold_date == "now":
            sold_date = self.get_closest_date()
        self.sold_price = np.float64(self.history[sold_date])
        self.sold_date = sold_date

    def __str__(self):
        return "{} and sold on {} for ${} each or ${} total".format(super().__str__(), self.sold_date.date(),
                                                                    self.sold_price,
                                                                    self.get_sold_total())

    def get_sold_total(self):
        return round(self.quantity * self.sold_price, 2)


class User:
    class Decorators:
        @classmethod
        def validate_input(cls, user_action_function):
            def wrapper(self, ticker, quantity, date="now"):
                _DTM_FORMAT = "%Y-%m-%d"
                ticker = ticker.upper()
                if date != "now":
                    try:
                        date = datetime.datetime.strptime(date, _DTM_FORMAT)
                    except ValueError:
                        return cls.error("Provided date does not match the format YYYY-MM-DD")
                if not cls.is_valid_quantity(quantity):
                    return cls.error("Invalid quantity. Quantity must be of integer type and greater than 0")
                if not cls.is_valid_ticker(ticker):
                    return cls.error(
                        "Provided stock ticker is not valid. Please use a valid ticker from the National Market System")
                index = self.check_for_holding(ticker, date)
                return user_action_function(self, ticker, quantity, index, date)

            return wrapper

        @staticmethod
        def add_aesthetics(original_function):
            def wrapper(*args):
                return "-\n{} - Stock Market Simulation\n{}".format(
                    datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), original_function(*args))

            return wrapper

        @staticmethod
        def is_valid_quantity(quantity):
            if type(quantity) != int or quantity < 1:
                return False
            else:
                return True

        @staticmethod
        def error(error_message):
            return "Error: " + error_message

        @staticmethod
        def is_valid_ticker(ticker):
            # Checks to see if provided stock is valid and in the National Market System (NMS)
            try:
                stock_info = yf.Ticker(ticker).info
                if stock_info["exchange"] in ["NMS", "NYQ"]:
                    return True
            except ValueError:
                pass
            return False

    def __init__(self, name: str, balance: float):
        self.holdings = []
        self.previous_holdings = []
        self.name = name
        self.balance = np.float64(balance)

    @property
    def balance(self):
        return round(self.__balance, 2)

    @balance.setter
    def balance(self, balance):
        self.__balance = balance

    @Decorators.add_aesthetics
    @Decorators.validate_input
    def purchase(self, ticker, quantity, index, date):
        purchased_stock = PurchasedStock(ticker, quantity, date)
        cost = purchased_stock.get_purchased_total()
        if not self.verify_funds(cost):
            return "Your account does not have the funds to purchase {}x {} stock for ${} each or ${} total.".format(
                quantity, purchased_stock.name, purchased_stock.purchased_price, cost)
        if index is None:  # Groups together stocks purchased for the same closing price.
            self.holdings.append(purchased_stock)
        else:
            self.holdings[index].quantity += quantity
        self.balance -= cost
        return "Successfully purchased {}x {} for ${}. Your new balance is ${}.".format(quantity, purchased_stock.name,
                                                                                        cost, self.balance)

    @Decorators.add_aesthetics
    @Decorators.validate_input
    def sell(self, ticker, quantity, index, date):
        if index is None:
            return f"You do not own a stock with ticker {ticker} purchased on {date.date()}"
        purchased_stock = self.holdings[index]
        if quantity > purchased_stock.quantity:
            return "You only own {}x {} stock. Revise your quantity".format(purchased_stock.quantity, ticker)
        if quantity == purchased_stock.quantity:
            self.holdings.remove(purchased_stock)
        else:
            self.holdings[index].quantity -= quantity
        sold_stock = SoldStock(purchased_stock.ticker, quantity, date)
        self.previous_holdings.append(sold_stock)
        self.balance += sold_stock.get_sold_total()
        return "Successfully sold {}x {} stock for {} each or {} total".format(quantity, sold_stock.name,
                                                                               sold_stock.sold_price,
                                                                               sold_stock.get_sold_total())

    @Decorators.add_aesthetics
    def save(self):
        filename = self.name + " Stock Market Simulation Account.pickle"
        pickle_out = open(filename, "wb")
        pickle.dump(self, pickle_out)
        return f"Successfully saved account data:\n{self.__str__()}"

    @Decorators.add_aesthetics
    def graph_account(self):
        plt.style.use(["ggplot", "seaborn-dark-palette"])
        fig, ax1 = plt.subplots()
        spent_history = pd.Series(dtype=np.float64)
        holdings = sorted(self.holdings)
        portfolio_history = pd.Series(data=0.0, index=holdings[0].recent_history.index, dtype=np.float64)
        bbox_props = dict(boxstyle="round", fc="w", ec="k")
        y = 0.9
        for stock in holdings:
            date = stock.purchased_date
            try:  # Adds the previous money spent to get the total and filters out if it is the first date
                money_spent = spent_history[-1] + stock.get_purchased_total()
            except IndexError:
                money_spent = stock.get_purchased_total()
            spent_history[date] = money_spent
            ax1.text(0.01, y, f"+ {stock.quantity}x {stock.ticker}", bbox=bbox_props,
                     transform=ax1.transAxes)
            portfolio_history[stock.purchased_date::] += stock.recent_history * stock.quantity
            y -= .03
        ax1.plot(portfolio_history, label="Portfolio Worth")
        ax1.plot(spent_history, marker="o", ls="--", label="Dollars Invested")
        for series in [portfolio_history, spent_history]:
            ax1.text(.963, series[-1], str(round(series[-1], 2)),
                     bbox=bbox_props,
                     transform=ax1.get_yaxis_transform())
        ax1.set_title("Portfolio Worth Compared to Dollars Invested Over Time")
        ax1.set_ylabel("Dollars")
        ax1.set_xlabel("Date")
        ax1.legend()
        plt.show()
        return "Graph opened in new window"

    @Decorators.add_aesthetics
    def __str__(self):
        account_info = f"Your balance is currently ${self.balance}"
        if len(self.holdings) > 0:
            holdings = [stock.__str__() for stock in self.holdings]
            account_info += " and you have the following holdings\n" + "\n".join(holdings)
        return account_info

    def check_for_holding(self, ticker, date):
        for index, stock in enumerate(self.holdings):
            if date == "now":
                date = stock.get_closest_date()
            if stock.ticker == ticker and stock.purchased_date == date:
                return index
        return None

    def verify_funds(self, cost):
        return self.balance - cost >= 0

    @classmethod
    def login(cls):
        username = input(
            "Welcome to the Stock Market Simulation Script. Enter your username to login or create a new account. ")
        filename = username + " Stock Market Simulation Account.pickle"
        try:
            pickle_in = open(filename, "rb")
            user = pickle.load(pickle_in)
            print("Successfully logged in")
        except FileNotFoundError:
            money = np.float64(input("How much money would you like to put into your account? "))
            if money <= 0:
                print("Error: Please provide a balance greater than 0")
                return cls.login()

            user = User(username, money)
            print("Account successfully created.")
        print(user)
        return user


# Sample Code
if __name__ == '__main__':
    user = User.login()
    print(user.purchase("amzn", 3, "2014-5-2"))
    print(user.purchase("fb", 3, "2015-11-2"))
    print(user.purchase("intc", 3, "2013-1-15"))
    print(user.purchase("mrna", 3, "2019-5-2"))
    print(user.purchase("msft", 3, "2017-6-2"))
    print(user.purchase("aapl", 3, "2020-5-4"))
    print(user.purchase("docu", 12))
    print(user.sell("aapl", 1, "2020-5-4"))
    print(user)
    print(user.graph_account())
# Uncomment this line if you wish to save your account
# print(user.save())
