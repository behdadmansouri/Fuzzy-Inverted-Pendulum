# Fuzzy Inverted Pendulum

This project consists of an inverted pendulum simulator and a fuzzy controller. The main goal was to develop a simple yet useful simulator to model the environment, so that you are enabled to easily create a fuzzy controller for the inverted pendulum problem.
It was implemented using **pygame** and **pyfuzzy** in *python2.7*.

## What's new
As a coursework, the controller.py is changed. The content of the **decide** function have been commented and there's a
call to a **my_decide_function** that implements the fuzzy logic solution without using the fuzzy library.

What that **decide** function does, is basically returning a force value between -100 and 100 to be applied to the cart.

### How it's done

1. fuzzification
   1. We use the fcl file to calculate the function for the pendulum and the cart. They're all triangle shaped so a linear function should do it
2. inference
   1. using the rules in fcl file to infer how much belonging is there to any what rule.
3. Defuzzification
   1. Here we find the final value of force. This is done via finding the inference result's center of mass (by integration).

## Getting Started


### Install

    $ sudo pip install virtualenv
    $ virtualenv -p python2.7 venv
    $ source venv/bin/activate
    $ ./libraries/install-deps.sh

### Run

    $ ./main.py

Also, you can run the project using custom configurations located in the **configs** directory.
Changing the physical parameters of simulator. That is, cart mass, pendulum length, etc...

	$ ./main.py configs/full.ini


## Usage


### Physical parameters of simulator

> **M**: cart mass, *kg*
> 
> **m**: pendulum mass, *kg*
> 
> **l**: pendulum length, *m*
> 
> **x**: cart position, *m*
> 
> **v**: cart velocity, *m/s*
> 
> **a**: cart acceleration, *m/s^2*
> 
> **theta**: pendulum central angle, *radian*
> 
> **omega**: pendulum angular velocity, *m/s*
> 
> **alpha**: pendulum angular acceleration, *m/s^2*
> 
> **g**: gravity acceleration, *m/s^2*
> 
> **b**: cart coefficient of friction, *newton/m/s*
> 
> **I**: moment of inertia, *kg.m^2*
> 
> **min_x**: cart minimum x, *m*
> 
> **max_x**: cart maximum x, *m*
> 
> **force**: force applied on cart, *newton*

You can see all the parameters in **world.py** module.
Also these parameters can be modified using configuration files located in **configs** directory.

### Fuzzy Control Language (FCL)
The *FuzzyController* class in **controller.py** module, loads an *FCL* file to decide how much force needs to be applied to the cart in each cycle of simulation.
*FCL* files can be found in **controllers** directory. You can create your own controller by writing a new *FCL* file and specifying it in the *config* files by changing the *fcl_path* item.

**configs/default.ini**:

	[simulator]
	dt = 0.1
	fps = 60


	[controller]
	fcl_path = controllers/simple.fcl


	[world]
	theta = -90.0

### Simple FCL Controller

There is a simple controller that works just fine and can be found in **controllers** directory. You can also checkout
the fuzzy variables chart, available in the same directory.
