# Algorithmia-New Relic - Temp space for colab work
Contains a simple load generation script for an algorithm on Algorithmia that streams its metrics to New Relic Account #3019600

## Story
Our user on Algorithmia has a Credit Card Approval algorithm. This algorithm is processing a user's demographic information as its input, and using an ML model to predict whether this credit card application should be approved or rejected. As its response, it returns a 1/0 value for approved/rejected, and this decision's `risk_score` as a probability between 0 and 1.

![](images/algorithm.png)

In order to detect anomalies in their model behavior, our algorithm owner wants to stream their metrics over Algorithmia Insights to New Relic. If their model suddenly (incorrectly) classifies a large percentage of applicants as high risk and denies their credit card applications, then they would like to be notified of this situation through New Relic's alerting features.

Our algorithm owner would also like to observe their model's operational metrics, such as the runtime duration of the algorithm, to keep an eye on their response times. 

## Input data

`data` folder contains a set of inputs to simulate load:
- `all.csv`: 25k records, as a mix of applications to be approved+rejected
- `reject.csv`: 5k records of applications to be rejected
- `approve.csv`: 20k records of applications to be approved


## Observed Algorithm output
The algorithm's streamed metrics are observed on this account's Credit Card Approval Dashboard as below:
![](images/dashboard.png)

Streamed data structure is as follows:
```json
[
  {
    "name": "algorithmia.approved",
    "timestamp": 1613707378916,
    "value": 1,
    "type": "gauge",
    "attributes": {
      "algorithm_name": "gradientboosting_creditcardapproval",
      "algorithm_version": "0.1.1",
      "algorithm_owner": "asli_algorithmia_trr",
      "request_id": "req-04c88db3-a0c1-4123-aaa1-6a096b59e4ec",
      "session_id": "rses-ec437101-e319-4123-8a4d-e65efdc86fd9"
    }
  },
  {
    "name": "algorithmia.risk_score",
    "timestamp": 1613707378916,
    "value": 0.43,
    "type": "gauge",
    "attributes": {
      "algorithm_name": "gradientboosting_creditcardapproval",
      "algorithm_version": "0.1.1",
      "algorithm_owner": "asli_algorithmia_trr",
      "request_id": "req-04c88db3-a0c1-4123-aaa1-6a096b59e4ec",
      "session_id": "rses-ec437101-e319-4123-8a4d-e65efdc86fd9"
    }
  },
  {
    "name": "algorithmia.n_features",
    "timestamp": 1613707378916,
    "value": 29,
    "type": "gauge",
    "attributes": {
      "algorithm_name": "gradientboosting_creditcardapproval",
      "algorithm_version": "0.1.1",
      "algorithm_owner": "asli_algorithmia_trr",
      "request_id": "req-04c88db3-a0c1-4123-aaa1-6a096b59e4ec",
      "session_id": "rses-ec437101-e319-4123-8a4d-e65efdc86fd9"
    }
  },
  {
    "name": "algorithmia.duration_milliseconds",
    "timestamp": 1613707378916,
    "value": 8,
    "type": "gauge",
    "attributes": {
      "algorithm_name": "kafka_insights_producer",
      "algorithm_version": "0.1.1",
      "algorithm_owner": "asli_algorithmia_trr",
      "request_id": "req-04c88db3-a0c1-4123-aaa1-6a096b59e4ec",
      "session_id": "rses-ec437101-e319-4123-8a4d-e65efdc86fd9"
    }
  }
]
```

## How to generate load

```
❯ python3 load.py -h                                  
usage: load.py [-h] [-s S] [-a A] [-v V] [-home HOME] [-phone PHONE] [-sleep SLEEP]

optional arguments:
  -h, --help    show this help message and exit
  -s S          Data segment to use:all, approve or reject. Defaults to all
  -a A          Algorithm name to call. Defaults to randomforest_creditcardapproval
  -v V          Algorithm version to call. Defaults to 0.1.1
  -home HOME    Overrides owns_home input feature with 0 or 1. Defaults to None (doesn't change the original value)
  -phone PHONE  Overrides has_work_phone input feature with 0 or 1. Defaults to None (doesn't change the original value)
  -sleep SLEEP  Num of seconds to increase the duration of the algorithm. Defaults to 0
```

### Examples 

#### Using defaults
To simulate "usual times", run `python3 load.py -s all`
This will send a mix set of credit card applications to randomforest_creditcardapproval algo, either to be approved or rejected.

To simulate "unusual times", run `python3 load.py -s reject`
This will only send credit card application requests that the randomforest_creditcardapproval algo will reject.

To normalize the stats, run `python3 load.py -s approve`
This will only send credit card application requests that the randomforest_creditcardapproval algo will approve.

### Loading a specific algo
If you don't provide the algo name, it will default to randomforest_creditcardapproval.
To send requests to gradientboosting_creditcardapproval, run: `python3 load.py -a gradientboosting_creditcardapproval`
To send applications to reject, add the -s reject flag: `python3 load.py -s reject -a gradientboosting_creditcardapproval`

### Overriding input features
This example sends a request to v0.1.1 of the `gradientboosting_creditcardapproval` algorithm, that approves all credit card applications, overrides the owns_home and has_work_phone input features with values "1" and makes the algorithm sleep for 2 seconds:
`python3 load.py -s approve -a gradientboosting_creditcardapproval -v 0.1.0 -home 1 -phone 1 -sleep 2`



## Requirements
- algorithmia --> `pip install algorithmia`
- pandas
