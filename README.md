# Swabbie


## About

Swabbie is a command-line utility designed to help you manage your docker images and containers. 

Swabbie can clean up your containers and images, restore docker to a fresh install,
and keep track of containers and images more efficiently.

By using swabbie, you remove the need for shell scripts and bash aliases for all the 
docker image and container management commands.


## Installation

Currently to install swabbie as a package, download swabbie by cloning this repo, 
create a virtualenv, and run

    pip install --editable .
    
on the command line from inside the main swabbie folder.

In the future, I will add this package to the pypi server.


## Usage

`swabbie` will list all of the commands that swabbie supports, which are currently:

* `list`: lists images and containers (all or only running containers and correctly built images)
* `count`: tallies the total number of images and containers, as well as those that are functional
* `clean`: removes all dangling images and exited containers
* `nuke`: removes all images and containers; resets docker to fresh install state
* `shell`: reference guide for container and image access commands; has sub-arguments


## Development

To add features to swabbie, set up your virtualenv and run
    
    pip install -r requirements.txt

To install swabbie as a local package so that it will update automatically during development, run
   
    pip install --editable .

from the main folder.

### Testing

Swabbie uses nosetests for unit testing, so run `nosetests` from the
main folder.

To install dependencies for running the tests, use 

    pip install -r requirements-test.txt
    
    
## License 

MIT license, see LICENSE.txt.