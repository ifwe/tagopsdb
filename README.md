# tagopsdb - Site Operations Database Library

## Authors
Kenneth Lareau, Karandeep Nagra

## Description
tagopsdb is a library to interface with a Site Operations database
used at if(we) to manage various infrastructure information.

**\*\*WARNING\*\***: Consider this code **EXPERIMENTAL**.  It has
not been fully prepared for use outside If(we) though we will be
working on this.  In particular, the schemas themselves are still
being cleaned up in preparation to move from MySQL to PostgreSQL.
If you have any questions or suggestions, please email
<tagopsdb@ifwe.co>

## License
<a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License, Version 2.0</a>

## Installation
To install all necessary dependencies and tagopsdb:

```bash
$ ./setup.py
```

## Dependencies

### PyPI packages
See `requirements.txt`. To install (NOTE: `setup.py` will do this for you):

```bash
$ pip install -r requirements.txt
```

### Other required packages
* OurSQL (MySQL interface in Python)

## Testing
First, install development requirements
(again, `setup.py` automatically does this for you):

```bash
$ pip install -r requirements-dev.txt
```

### Unit tests
The following command will run all unit tests:

```bash
$ ./run_tests.py
```

-----

README.md: Copyright 2016 Ifwe Inc.

README.md is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
