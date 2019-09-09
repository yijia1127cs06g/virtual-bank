# virtual-bank

## Overview
For inter process communication, there are two mechanisms can meet the need that includes message passing and shared memmory approaches. In distributed computer environment, we can also use distributed shared memory and message broker to meet the need of cross-machine communication. In this assignment, we are going to implement a client-server communication service, which is based on a distributed shared memory architecture.
## Virtual Bank
We are the owner of a digital bank in network and provide financial services to the customers. For serving, there are 
- multiple available web ATMs (called socket server) 
- specific client (called socket client).

Customers can access them via specific client. To make sure that accounts' data can be consistent across different ATMs, you need a sharable account manager system to handle it.

## Procedure
User client <----> ATM <------> Account System

## Account System
- Account system is a distributed shared memory service that used to manage all sharing data. e.g. transaction logs, and accounts' deposits.
- Redis database as distributed data sharing mechanism to build the account system.

## User client
- User client are represented customers whom want to access your web ATMs and manage and manipulate thier deposits.
- There are 4 actions that customers would wnat to do:
  - init <account> <initial deposits>: Registering a user account with initial money.
  - save <account> <money>: Saving money to a specific account.
  - load <account> <deposits>: Loading their deposits from a specific account.
  - remit <src_account> <des_account> <money>: Remitting money from their account to a specific account.

## Web ATM server
- Web ATM server is represented as a indivisual financial service agent that processs customers' requests and check if these requests are legal or not. 
- When the ATM server recieve a request, it should to validat the request and does coresponding actions.
