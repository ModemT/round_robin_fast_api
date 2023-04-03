# Round Robin Load Balancer FastAPI

This is a simple implementation of a Round Robin load balancer using FastAPI and requests library. The round robin API is an approach to load balancing that distributes incoming requests evenly across a set of backend servers or applications in a cyclic manner. Each incoming request is forwarded to the next server in the list of servers in a sequential manner, with the first server being used again once the last server has been used. This approach ensures that no single server is overloaded with too many requests and that the overall workload is evenly distributed across all servers, leading to optimal utilization of the available resources.

## Installation

1. Install Python in an Virtual Environment (Reccomended Version 3.9)
2. Clone the repository
3. Activate Python Environment 
4. Install the required packages with `pip install -r requirements.txt`.

## Run the app
Using bash run the endpoint services

```sh
uvicorn app:app --port 8001
uvicorn app:app --port 8002
uvicorn app:app --port 8003
```

Run the Round-Robin Balancer

```sh
uvicorn balancer:app --port 8080
```

## Test the app 

There are two major scenarios which this app considered.
### 1. How would my round robin API handle it if one of the application APIs goes down?

If one of the application APIs goes down, the round-robin API will mark that application API as failed and move on to the next application API in the list. It will continue to cycle through the list of application APIs, skipping any that are marked as failed, until it finds an application API that is not marked as failed or the retry downtime for a failed application API has passed. This way, the round-robin API can still distribute the incoming requests among the available application APIs and minimize the impact of a single application API going down. Once the failed application API is back up and running, the round-robin API will automatically start using it again.

To test the round-robin load balancing behavior, the AlternatingFailureApp is used in place of the actual endpoint application API. Each time a request is made to the FastAPI endpoint, the handle_request method is called, and the failure_counter of the AlternatingFailureApp is incremented.

Since the AlternatingFailureApp is designed to fail every other request, testing this functionality would involve sending a series of requests and verifying that the response alternates between the expected data and the "App failure" exception message at a interval of retry downtime.

To test set one endpoint to the AlternatingFailureApp and execute the request through the round robin. The response would be a skipped endpoint at the response header (x-app-url) on the client side. Which the failed endpoint would reappear when the retry downtime has passed.

```sh
uvicorn app:app --port 8001
uvicorn alterfailed:app --port 8002
uvicorn app:app --port 8003
```

Example of the header received.

```
 content-length: 16 
 content-type: application/json 
 date: Mon,03 Apr 2023 02:55:56 GMT 
 server: uvicorn 
 x-app-url: http://localhost:8003 
```




### 2.How would my round robin API handle it if one of the application APIs starts to go slowly?

If one of the application APIs starts to respond slowly, the Round Robin API will still attempt to use it for requests. This is because the Round Robin algorithm simply cycles through the list of application APIs in order, without taking into account their response times.

As a result, if one application API is slow, the Round Robin API will wait until the max delay response time is exceeded. This could result in slow response times for clients, as they may need to wait for each slow request to time out before moving on to the next application API. The max delay response could be lowered to match the client expectation of maximum wait time. However, there would have to be a monitoring of services that if the endpoint is becoming too slow it would have to be diagnosed.

To test this issue, a mock timeout instance of the endpoint would be created. The delay from the timeout instance need to be more than the max_delay_reponse of the round robin. The run script would be similar with a replaced service of the timeout instance.


```sh
uvicorn app:app --port 8001
uvicorn timeout:app --port 8002
uvicorn app:app --port 8003
```

In this case, the round robin would skip port 8002 always if the timeout instance time delay exceeds the configured max_delay_response of the round robin.



## TODO

1. Health Monitoring of Services
2. Configuration Management
3. Testing configuration
4. Additional logic in the Round Robin API to monitor the response times of each application API and adjust the round robin algorithm accordingly.