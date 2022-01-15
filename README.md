# Groovy Code Executor Service Assignment


Groovy Code Executor is a REST service that accepts groovy code requests, executes them and provides the result to the end users. This is an automation project created to this Groovy Code Executor service.

## Prerequsites
* Python-
   * Python : version >= 3.7.*

## Usage

* The tests can be executed in following ways - 
	1. Using PyTest command: 

		a. Pre-requisite : To execute tests, install the required dependencies through command
    
        `pip3 install -r requirements.txt`

		b. Execute simple pytest command with additional flags(i.e. environment)
    
	  		python3 -m pytest --html=./reports/report.html -capture=tee-sys  --self-contained-html -vv -n 2 --environment=local .

	  		Here, 
	  		  --html                : Creates html report at given folder path
	  		  --capture             : Captures the logs generated during execution
	  		  --capture             : Captures the logs generated during execution
	  		  --self-contained-html : Creates single html file, which can be easily emailable
	  		  --environment=local   : Custom flag to execute test on local environment
	  		  -n 2                  : Executes test parallely where 2 represents 2 threads
	  		  .                     : This will run all the test from project, if you want to run specific tests then - 
	  		  	    Specific file : Add tests/test_defaults.py in place of .
	  		  	    Specific test : Add tests/test_multi_requests_user.py::TestDefaults::test_submit_null_code_and_check_status in place of .

	
	2. Using Make file: 
		To execute using make file follow below process -
    
			a. make environment : This will install all required dependencies and create a virual environment

			b. make test        : This will execute all the tests which are part of the project
			c. make clean       : This will clear the virual environment files
	  

## Preparing for Execution

To perform execution follow below steps:

1. Clone repository: `git clone https://github.com/rohittupe/GroovyExecutorServiceAssignment.git`
2. `cd` into the directory `GroovyExecutorServiceAssignment`
3. Run `make environment` to install the dpendencies and create a virtual environment
4. Run `make start-server` to start the application
5. Open another terminal and run `make test` to start the tests
6. Upon test completion, the reports will be generated under `reports` folder with name `report.html`
7. Open `report.html` file in a browser of your choice to view the execution report
8. Run `make clean` to clear the virtual environment files
9. Run `make stop-server` to stop the application

