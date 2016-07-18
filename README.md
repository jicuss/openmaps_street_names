# OpenMaps Street Name Tool
###### A library to estimate the most common street names in the continental US
---
#
This library uses the Openmaps API to estimate the top 10 most common street names. It will iteratively download ways data from Openmaps, count the occurrences of street names and present statistics about the relative probability of common street names.


##### Objective:
Write a program that uses the Open Street Maps API to build a list of the 10 most commonly used street names in the United States.

The output should include the street name and number of times it occurs. It would look something like this:

    Jefferson Street 1500
    Walnut Street  1000
    Terre Haute Road  900

##### Requirements:
#
Library | Docs | Install
--- | --- | ---
[Overpass Python Wrapper](https://github.com/DinoTools/python-overpy)| https://github.com/DinoTools/python-overpy | pip install overpy
[Redis](http://redis.io/)| http://redis.io/documentation | brew install redis

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
* Clone this repo to your local drive
* Navigate to the location of the cloned repo
* Install using the command:
```
$ pip install -e .[dev]
```

##### Usage:
#
* Run the main library using the command count_street_names
```
$ count_street_names
```
* Alternatively you can use the command download_map_data first then the count_street_names.
    - This will download the Openmaps ways data first without the additional overhead of processing the Openmaps response data. The count_street_names will then use the cached Openmaps response data and collect descriptive statistics about the street name occurrences as a second pass.
    - In practice this is a more convenient approach, as you will likely have to leave the library running overnight to be able to fully download the input dataset.
```
$ download_map_data
$ count_street_names
```

The count_street_names command will attempt to download the Openmaps ways datasets for the continental US. It does this by drawing a rectangular box around the US, breaking it into lat long coordinate boxes of length / width 1 then rastering from the Southwest to the Northeast using a depth first approach. After downloading the Openmaps data it will count instances of street names and print the top 10 results.
* You can start and stop the data harvesting process at anytime. The results of each Openmaps API query are cached to the disk for later retrival.
* The full result datasets will be stored in the root of the directory where the commands were run, in tab deliminated format. This makes it easy to copy those results directly into Excel if you want to look at the results further.
* In addition to a simple count of the streets, it also counts word occurrences and a ‘normalized’ street name count. The normalization process removes common street suffixes such as street, circle, or way to estimate the occurrences of the root street name alone.

