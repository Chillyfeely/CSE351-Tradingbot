# Overview

- From the start of our project we had a unswerving northstar and every step of our development journey clustered around this purpose. Which is `"Get rich quick"`. Anyone who has some experience in crypto ecosystem knows that in order to make money you need to be either:
  - Whale (a person or an organization that is capable of making high volume market manipulation)
  - Conman (comes with a various methods e.g., Rugpull, Pump and Dump schemes, Exit scams)
- Now that we now the various scams in this ecosystem lets talk about the main points of our project that diverse from these scams.
  - Our project is a subscription based curated information delivery sytem -how this information is curated explained later on the paper-
  - Only for `49$/month` you can get the newest tips for various crypto-exchanges in just matter of miliseconds as everyone in the project even me (owner)
  - We dont require any confidential information from you or make any transaction behalf you and the end decision is always up to you
- Lets elaborate the algorithms we use for predicting the market
  - We have various algorithms such as `MA`, `Momentum` and specially trained `SVM model` that can find the best moves even if the market is unpredictable
  - We've worked with the Akdeniz University's finest computer engineers and the economics professors to create these highly complex algorithms that works on the `ETH` currency and currently running this on the University's 2,746,360 PetaFLOPS super computer just for you to make some money.
  - After the calculations we will send you a Telegram message from `@cse351bot` that has the informations about the intended transactions to be made, after that it is up to you to take that lead and create value from it.

# Why Did We Used Python?

- Next section you will find that python is somewhat unorthodox when it comes to OOP and strict typing. Although we overcome these with `libraries` one may think its unnecessary and that we should've used a `better` language. For those who think like this way, all I want to say that is which language you are using probably does not have a `is-thirteen`[(See it for yourself)](https://pypi.org/project/is-thirteen/) library so probably you are wrong.
- Also learning the implementations for ML in java or some other horrible language is way harder than learning how to use 2 OOP libraries in python.

# Problems with Python and How We Fixed it

- As you know python does not enforce the strict access controls like some of the other languages such as Haskell, Lua etc. But there is a convention around the object oriented python programmers. That is `_` is used for protected entities and `__` is for privates. Using these knowladge programmers can understand other programmers intentions and preferably respect it.
- Also in order to implement Abstract classes we used `abc` (python abstract base classes library) and for interface we used `python-interface` libary (a wrapper around abc but stricter semantics and better error messages)
- We also used Typing library for safety (and also I am %99 percent sure that if we didn't it would resulted in point deduction)

# Design Patterns

## Template Pattern

- The Template pattern that is mandatory for this project is used in our TradingBot logic. We predicted the future and understood that our `run` function will always need `_get_market_info` and `get_time_stamp` steps wheter its running on `ETHEREUM` or another chain.
- Because of that we encapsulated them into protected functions and used them as steps in our `run` function

![bot.py](/images/bot.png)

## Strategy Method Pattern

- Strategy is the second and last mandatory pattern in our project and it was also crucial for this project in order to using different strategies based on a `metric` (more on that later) at `runtime`.
- We defined an interface named `TradingStrategyInterface` -resides at `strategies.py`- and implemented it in 3 different Strategy (2 of them uses solely algebra and one of them is using SVM which can be paraphrased as `fancy algebra`)
- Each of these strategies implements a execute method that returns either `BUY`, `SELL` or `HOLD` command where SVMStrategy also has an additional private method because of the complexity of running a ML model.

![strategies.py](/images/strategies.png)

## Observer Pattern

- According to our business plan the observer pattern was the obvious choice for finishing the trinity.
- We defined an interface named `Observer` and implemented on 3 different types of observer two of it has no practical value beside debugging whom are `ConsoleLogger` and `FileLogger`.
- The third observer, `TelegramLogger` is connected to our bot named `@cse351bot` that we created in telegram for sending our customers fast and reliable push notifications.
- Our subject in this project is the TradingBot -resides in `bot.py`- that has all the required functions for attaching, detaching and notifying observers

![observers.py](/images/observers.png)

## Abstract Factory & Singleton Pattern

- When we started to refactor the codebase into a better encapsulation and readability we encounter a structure that heavily resembles the `Abstract Factory` and `Singleton` pattern.

![factory.py](/images/factory.png)

- The need for this abstract class and its concrete implementations born from the better encapsulation for creation of Strategy instances.
- Also we implemented a Singleton logic for this in order to enhancing our credibility (we promised that everyone will get the same update)
- This `factory` implementation returns a concrete object implemented from TradingStrategyInterface.
- We use the `get_strategy` at runtime to change our strategy

## Main

- Below is the well documented main runner of our tradingbot

![main.py](/images/main.png)

# UML Diagram

![uml.py](/images/uml.png)
