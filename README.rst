Swabbie
=======

About
-----

Swabbie is a command-line utility designed to help you manage your
`docker <https://www.docker.com/>`__ images and containers.

Swabbie can clean up your dangling containers and images, restore docker
to a fresh install, and keep track of containers and images more
efficiently.

By using swabbie, you remove the need for shell scripts and bash aliases
to manage docker images and containers. Let swabbie keep track of those
commands for you!

Installation
------------

Currently, to install swabbie as a package, download swabbie by cloning
this repo, create a virtualenv, and run

::

    pip install --editable .

on the command line from inside the main swabbie folder.

Usage
-----

``swabbie`` will list all of the commands that swabbie supports, which
are currently:

-  ``list``: lists images and containers (all or only running containers
   and correctly built images)
-  ``count``: tallies the total number of images and containers, as well
   as those that are functional
-  ``clean``: removes all dangling images and exited containers
-  ``nuke``: removes all images and containers; resets docker to fresh
   install state
-  ``shell``: reference guide for container and image access commands;
   has sub-arguments

Development
-----------

To add features to swabbie, set up your virtualenv and run

::

    pip install -r requirements.txt

To install swabbie as a local package so that it will update
automatically during development, run

::

    pip install --editable .

from the main folder.

Testing
~~~~~~~

Swabbie uses `nose <https://github.com/nose-devs/nose>`__ for unit
testing, so run ``nosetests`` from the main folder to execute the test
suite.

To install dependencies for running the tests, use

::

    pip install -r requirements-test.txt

Versioning
~~~~~~~~~~

Swabbie uses the
`bumpversion <https://github.com/peritus/bumpversion>`__ package for
versioning. The bumpversion.cfg file contains the necessary information
for updating the version, so just run

::

    bumpversion <major/minor/patch>

and bumpversion will do the rest.

Updating README
~~~~~~~~~~~~~~~

The readme is provided in both markdown and rst. One approach is to
write the readme in markdown, and then use pandoc to convert to rst:

::

    pandoc --from=markdown --to=rst --output=README.rst README.md

License
-------

MIT license, see LICENSE.txt.
