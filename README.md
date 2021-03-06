# ltv-analytic-INT20H
This repository contains code for solving the second task on INT20H

## Structure
+ implementation of LTV you can find in file **src/ltv.py**
+ our dataset places in file **data/data_analytics.csv**
+ In file **config.yaml** you can find different parameters like:
    + path to folder with data
    + dataset filename
    + etc

## How to run a project ?

### 1️⃣ method
1. Open your GitBush console and put following command:
```bash
git clone https://github.com/welcome-pack-only/ltv-analytic-INT20H.git
```
2. Open your console in root project directory
3. Execute following command:
```bash
pip install -r requirements
```
4. Run computing LTV using following command:
```bash
python main.py
```
And then you will see something like that:
```bash
LTV: 9.3400127
```

### 2️⃣ method
1. Open your GitBush console and put following command:
```bash
git clone https://github.com/welcome-pack-only/ltv-analytic-INT20H.git
```
2. Open your console in root project directory
3. Execute following command to build our application:
```bash
docker build -t ltv-analytic-int20h .
```
4. Next, execute following command to run computing LTV:
```bash
docker run --rm ltv-analytic-int20h
```