# salad-generator

Generating salads using flavour matching techniques (i.e. how to choose ingredients for salads for the indecisive people).

Data is sourced from [FlavorDB](https://cosylab.iiitd.edu.in/flavordb/) and licenced under [Creative Commons](https://creativecommons.org/licenses/by-nc-sa/3.0/).

## Usage

Still a work in progress. Currently you can:

* Preprocess JSON data files in the `/data` directory into tuples containing ingredient pairs and the number of common molecules.
* Generate a [NetworkX](https://networkx.github.io/) graph from the list of tuples.
* Perform simple operations on the graph, like retrieving a node by the ingredient name and then returning the nearest neighbours of that node.

## Todo

* [ ] Create graph traversal algorithm so we can start at any ingredient and then keep walking to adjacent ingredients until enough ingredients have been selected to complete a salad.
* [ ] Create CLI for traversal. User can select the starting ingredient and is asked to select from the next best pairings until a salad is complete.
* [ ] Create GUI for traversal. Same as above but visual...
