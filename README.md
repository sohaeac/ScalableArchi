# Mandelbrot set viewer

This is a project for the Scalable Architecture course.

## Features

- Verify if a complex number belongs to the Mandelbrot set 
- Compute the Mandelbrot set pixel by pixel 
- Compute the Mandelbrot set at once behind the http server 




## How to run 

1. Run the loadbalancer server 
```sh
go run .
```
The loadbalancer runs on localhost:8000

2. Run the workers 
```sh
python worker.py worker1 5001
python worker.py worker2 5002
python worker.py worker3 5003
python worker.py worker4 5004
```
4. Run the CLI interface

```sh
python cli.py
```
## Gallery 

1. CLI

![alt text](https://github.com/sohaeac/ScalableArchi/blob/master/figures/cli_1.png?raw=true)

2. Some rendered Mandelbrot sets 

![alt text](https://github.com/sohaeac/ScalableArchi/blob/master/figures/Figure_1.png?raw=true)

![alt text](https://github.com/sohaeac/ScalableArchi/blob/master/figures/Figure_HOT.png?raw=true)

![alt text](https://github.com/sohaeac/ScalableArchi/blob/master/figures/Figure_2.png?raw=true)
