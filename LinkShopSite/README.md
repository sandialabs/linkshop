# LinkShop Tool Web Interface #

LinkShop is a tool for dynamically creating, modifying and analyzing linkographs. The tool provides functionality for working with linkographs.

The input and output format is JSON based and includes:

* Input data (sometimes called "commands" in LinkShop)
* Abstractions (a list of abstraction classes (essentially bins) and rules showing how to label the input data with correct abstraction class)
* Ontologies (a digraph showing relations between the various abstration classes)
* Linkographs (a graph of fore- and back-relations between time-series arranged nodes that represent the input data)

The LinkShop backend libraries provide functions for creating linkographs, analyzing linkographs using various metrics, and refining the ontology based on linkograph changes.

The LinkShop web framework is built using [python3](https://www.python.org/), [ThriftPy](https://thriftpy.readthedocs.org/en/latest/), [Node.js](https://nodejs.org/) with [Express](http://expressjs.com/), and [D3](http://d3js.org/). 

### Running ###

Simply clone this project and run the build script to install all necessary dependencies:

`./build.sh [-s] [-l] [-g]`

The build script is currently configured to get the full environment running. The configurable options are as follows:
* [-s] – specifies the build commands should be run with elevated privileges
* [-l] – specifies to only install the locally required packages and modules (all global environment packages are already installed)
* [-g] - specifies to generate a self signed certificate for the https portion of the website

Many of the commands require super-user privileges, so the [-s] and [-p] options will be necessary the majority of the time. After running the full build at least once on a system, the [-l] option should suffice in the case where the local modules need to be re-downloaded.

You can then start the project using the run script:

`./run.sh`

The run script starts all of the Linkshop services as background processes and awaits user to input the command 'q' to kill them. If you accidentally send the exit signal with ^c, the process ID's (PID) are printed when they are started so you can manually use the 'kill' command to exit them. 

Additionally, a clean script which deletes all large space intensive modules and saved data can be run via:

`./clean.sh [-s]`

The [-s] simply adds root priveleges to the delete commands in the case of errors. 

### Project Root Folder Descriptions  ###

* controllers/ – defines routes and their logic
* models/ – represents data, implements business logic and handles storage
* public/ – contains all web source files
* middlewares/ – all library modules and linking information
* docs/ – all relevant project documentation
* package.json – remembers all packages that your app depends on and their versions
