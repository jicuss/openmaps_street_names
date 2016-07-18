# OpenMaps Street Name Tool
###### A library to estimate the most common street names in the continental US.
---
#
This library uses the Openmaps API to estimate the top 10 most common street names. It will iteratively download ways data from Openmaps, count the occurrences of street names and present statistics about the relative probability of common street names.


##### Objective:
Write a program that uses the Open Street Maps API to build a list of the 20 most commonly used street names in the United States.

The output should include the street name and number of times it occures. It would look something like this:

    Jefferson Street 1500
    Walnut Street  1000
    Terre Haute Road  900

##### Requirements:
#
Library | Docs | Install
--- | --- | ---
Overpass Python Wrapper | https://github.com/DinoTools/python-overpy | pip install overpy

##### Helpful Links:
#
Link | Description
--- | ---
[Overpass Turbo](http://overpass-turbo.eu/) | Overpass Turbo is a helpful tool to test Overpass QL Queries for testing
[BoundingBox](http://boundingbox.klokantech.com/) | This tool will provide lat long box coordinates in a format similar to what Openmaps accepts
[Openmaps Metadata Reference](https://www.openstreetmap.org/relation/253832#map=10/32.8259/-117.1074) | Openmaps Reference. You can use this tool to search Openmaps and look at the metadata returned by a node
[Openmaps QL Examples](http://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL) | Some examples of the Overpass QL query language
[Openmaps Language Guide](https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide) | The docs for the Overpass QL query language
[538 Most Common Streets in America](http://fivethirtyeight.com/datalab/whats-the-most-common-street-name-in-america/) | A similar study done by 538. The street counts returned by this library and the 538 study were not identical, though relative occurances of the street names was mostly consistent.


##### Installation:
#
Clone this repo to your local drive
Navigate to the location of the cloned repo
Install using the command pip install -e .[dev]

##### Usage:
#
* Run the main library using the command count_street_names
* Alternatively you can use the command download_map_data first then the count_street_names.
    - This will download the Openmaps ways data first, then collect descriptive statistics about the street name occurrences as a second pass.
    - In practice this is a more convenient approach as you will likely have to leave the library running overnight to be able to fully download the input dataset.

