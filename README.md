<h1 align="center">
   Crypto Smart Candle - Candlestick data generator for crypto coins
</h1>

<p align="center">
  <a href="#page_with_curl-sobre">About</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#scroll-decisões-de-projeto">Project Decisions</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#books-requisitos">Requirements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#gear-instalação-de-requisitos">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
</p>

## :page_with_curl: About
This repository contains an environment automation, written in python, being responsible for fetching cryptocurrency data from an api and building a CandleStick database.

***Python***: The choice was made because it is a simple language and present on any platform. The JSON file contained in the project was chosen to make the project more independent, being able to modify the note at any time. In addition we also have a csv which contains information about the ids of each currency pair.

***Folder Structure***: The choice for this folder structure was mainly due to the scalability of the system! Trying to modularize the system so that in the future it can integrate more services.

## :scroll: Project Decisions

This project is built on Docker containers using an image that already has python, to facilitate the use of some dependencies.

## :scroll: Project Decisions

This project is built on Docker containers using an image that already has python, to facilitate the use of some dependencies.

***The project***: The data received is constant, so the use of the websocket where our program is listening to the poloniex platform was prioritized as the main data receiver. However, the main class that manages the program was built in an abstract way, enabling different types of implementation, currently we have websocket(DataManagerWebSocket) and api(DataManagerApi).

obs: websocket appeared unstable, losing connection a few times running in the docker.

***Points for improvement***: In this context, there are possible points for improvement to be discussed:

   1. Put the real or dollar as the default currency.
   2. Be able to exchange the default currency.
   3. Add more security to database management.
   4. Generate logs of possible errors.

## :books: Requirements
- Have [**Git**](https://git-scm.com/) to clone the project.
- Have [**Docker**](https://www.docker.com/) installed.

## :gear: Installation requirements
``` bash
   # Clone the project:
   $ git clone https://github.com/rubiotorres/CryptoSmartCandle.git
  
   # Run the Docker found at the root of the repository:
   $ docker-compose up --build

   # Replace on `env.json` with a valid host and database, if you want run on docker with localhost use `host.docker.internal` as host
   "database_destiny": {
    "host": "host.docker.internal",
    "port": "3306",
    "usr": "root",
    "pwd": "root",
    "db": "crypto_db"
  },

```
At the end you will have a service running in backgroud collecting data and recording it.

<h1></h1>

<p align="center">Rubio Viana</p>