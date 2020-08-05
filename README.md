# Portfolio Tracker

## Important Links:
Postman Collection of all the endpoints with valid request/responses :
https://documenter.getpostman.com/view/5364090/T1Dv9F6G

GitHub Repository Link : https://github.com/khatryshikha/smallcase.git


## Introduction
A portfolio tracking API is a collection containing single portfolio for a single user. This set of APIs implements adding/deleting/updating trades and can do basic return calculations. In which each trade contains 2 operation i.e. Selling and Buying. With the details of the trade that are :

- ticker_symbol for the traded security.
- buy price of the trade at that point of time.
- total shares brought/sell
- trade operation : Buy or Sell

This documenetation contains following requests:
1. [API for Adding trade](#1-api-for-adding-trade)
2. [API for Updating a trade](#2-api-for-updating-trade)
3. [API for Removing a trade](#3-api-for-removing-trade)
4. [API for Fetching portfolio](#4-api-for-fetching-portfolio)
5. [API for Fetching holdings](#5-api-for-fetching-holdings)
6. [API for Fetching returns](#6-api-for-fetching-returns)


Technologies used:
-----------------------------
  - Python/ Django framework
  - MongoDB
  - Mongoengine ORM

## Move To

- [Installation Instructions](#installation-instructions)
- [API for Adding trade](#api-for-adding-trade)
- [API for Updating a trade](#api-for-updating-trade)
- [API for Removing a trade](#api-for-removing-trade)
- [API for Fetching portfolio](#api-for-fetching-portfolio)
- [API for Fetching holdings](#api-for-fetching-holdings)
- [API for Fetching returns](#api-for-fetching-returns)
  

## Installation Instructions
  1. clone the project
  `git clone https://github.com/khatryshikha/smallcase.git`
  2. cd to project folder `cd csv_browser_project` and create virtual environment
  `python3 -m venv venv`
  3. activate virtual environment
  `source venv/bin/activate`
  4. install requirements
  `pip install -r requirements.txt`
  5. run the server
  `cd trader/ & python manage.py runserver`


## API for Adding trade
  This API to adds a trade​ for a security, and updating the portfolio accordingly.

  API - `http://127.0.0.1:8000/api/trade`

  Methods : POST

  ### API Response
   ```
  1. Successful response
    {
        "status": "success",
        "message": "Trade successfully done"
    }

  2. Failed response
    {
        "status": "fail",
        "message": "Trade failed due to server error"
    }
``` 

## API for Updating a trade
  This API to update either shares count or buy price of the particular trade and portfolio accordingly.


  API - `http://127.0.0.1:8000/api/trade`

  Methods : PUT

  ### API Response
   ```
  1. Successful response
    {
        "status": "success",
        "message": "Trade updated Successfully"
    }

  2. Failed response

    i)  Due to Internal server error

    {
        "status": "fail",
        "message": "Trade update failed due to server error",
    }

    ii) If no such trade pre-exist to update
  
     {
        "status": "fail",
        "message": "No such trade exist for {ticker_symbol}",
    },

``` 

## API for Removing a trade
  This API to delete the particular trade from portfolio.


  API - `http://127.0.0.1:8000/api/trade`

  Methods : DELETE

  ### API Response
   ```
  1. Successful response
    {
        "status": "success",
        "message": "Trade deletion successfully"
    }

  2. Failed response

    i)  Due to Internal server error

    {
        "status": "fail",
        "message": "Trade deletion failed due to server error",
    }

    ii) If no such trade pre-exist to update
  
    {
        "status": "fail", 
        "message": "No such trade exist"
    }

``` 


## API for Fetching portfolio
 This API fetches all the securities and trades corresponding to it i.e. complete portfolio.


  API - `http://127.0.0.1:8000/api/fetch`

  Methods : GET

  ### API Response
   ```
  1. Successful response
    {
      "portfolio": [
          {
              "_id": "5f26cab3cefd9bd32bd3ffb1",
              "uid": "340bf0e0-fefe-49f9-a4fc-2f99bde724f2",
              "average_buy_price": 319.25,
              "total_shares_count": 5,
              "trades": [
                  {
                      "operation": "Buy",
                      "ticker_symbol": "WIPRO",
                      "shares_count": 10,
                      "buy_price": 319.25,
                      "timestamp": "2020-08-02T14:16:16.099"
                  },
                  {
                      "operation": "Sell",
                      "ticker_symbol": "WIPRO",
                      "shares_count": 5,
                      "buy_price": 400,
                      "timestamp": "2020-08-02T14:19:03.980"
                  }
              ],
              "created_at": "2020-08-02T14:16:16.296",
              "updated_at": "2020-08-02T14:16:16.296"
          },
          {
              "_id": "5f26cad4cefd9bd32bd3ffb2",
              "uid": "58521941-7e9f-4efe-a4f5-6074ca8710f6",
              "average_buy_price": 1833.45,
              "total_shares_count": 5,
              "trades": [
                  {
                      "operation": "Buy",
                      "ticker_symbol": "TCS",
                      "shares_count": 5,
                      "buy_price": 1833.45,
                      "timestamp": "2020-08-02T14:16:52.330"
                  }
              ],
              "created_at": "2020-08-02T14:16:52.352",
              "updated_at": "2020-08-02T14:16:52.352"
          },
          {
              "_id": "5f26caf0cefd9bd32bd3ffb3",
              "uid": "cc515e5b-f9a6-4940-b79a-864c3f5ebc87",
              "average_buy_price": 438.57,
              "total_shares_count": 7,
              "trades": [
                  {
                      "operation": "Buy",
                      "ticker_symbol": "GODREJIND",
                      "shares_count": 2,
                      "buy_price": 535,
                      "timestamp": "2020-08-02T14:17:20.437"
                  },
                  {
                      "operation": "Buy",
                      "ticker_symbol": "GODREJIND",
                      "shares_count": 5,
                      "buy_price": 400,
                      "timestamp": "2020-08-02T14:18:22.193"
                  }
              ],
              "created_at": "2020-08-02T14:17:20.438",
              "updated_at": "2020-08-02T14:17:20.438"
          }
      ],
      "status": "success"
    }

  2. Failed response

    {
        "status": "fail",
        "message": "Failed to fetch portfolio",
    }

``` 

## API for Fetching holdings
  This API to get an aggregate view of all securities in the portfolio with its final quantity and average buy price.


  API - `http://127.0.0.1:8000/api/trade/holdings`

  Methods : GET

  ### API Response
   ```
  1. Successful response
    {
        "total securities": 3,
        "holdings": 13833.49,
        "status": "success"
    }

  2. Failed response
    {
        "status": "fail",
        "message": "Failed to fetch holdings"
    }
``` 

## API for Fetching returns
  This API to get cumulative returns at any point of time of a particular portfolio.


  API - `http://127.0.0.1:8000/api/trade/returns`

  Methods : GET

  ### API Response
   ```
  1. Successful response
    {
        "returns": -13333.49,
        "status": "success"
    }

  2. Failed response
    {
        "status": "fail",
        "message": "Failed to fetch returns"
    }
``` 
