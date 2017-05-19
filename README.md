LinkShop 1.0.0
==============

LinkShop provides a research playground for the field of Linkography.  This field was originally created by Gabriela
Goldschmidt in an attempt to clarify and quantify the design process.

LinkShop is a tool for dynamically creating, modifying and analyzing linkographs. The tool provides functionality
for working with linkographs.

The input and output format is JSON based and includes:

* Input data (sometimes called "commands" in LinkShop)
* Abstractions (a list of abstraction classes (essentially bins) and rules showing how to label the input data with correct abstraction class)
* Ontologies (a digraph showing relations between the various abstration classes)
* Linkographs (a graph of fore- and back-relations between time-series arranged nodes that represent the input data)

The LinkShop backend libraries provide functions for creating linkographs, analyzing linkographs using various
metrics, and refining the ontology based on linkograph changes.

| File / Dir           | Description                                                                           |
| -------------------- | ------------------------------------------------------------------------------------- |
| bin/                 | linkshop command line interface tools                                                 |
| frequencies/         | Enumerates linkographs and measures frequencies and Shannon entropy given an ontology |
| LICENSE              | License information                                                                   |
| linkograph/          | The linkshop linkograph functions python module                                       |
| LinkShopSite/        | The LinkShop web site                                                                 |
| markov/              | The linkshop markov python module                                                     |
| ontology/            | Example abstractions and ontologies                                                   |
| ontologyExtraction/  | Tools for ontology extraction / refinement                                            |
| README.md            | This file                                                                             |
| test                 | Simple functional tests                                                               |

For more information, see:

  * G. Goldschmidt. Linkography: Unfolding the Design Process. The MIT Press, 2014.
  * A. Fisher, K. Carson, D. Zage, and J. Jarocki. Using Linkography to Understand Cyberattacks. In IEEE Conference on Communications and Nework Security, Florence, Italy, September 2015.
  * R. Mitchell, A. Fisher, S. Watson and J. Jarocki, "Linkography ontology refinement and cyber security," 2017 IEEE 7th Annual Computing and Communication Workshop and Conference (CCWC), Las Vegas, NV, 2017, pp. 1-9.

Copyright (2017) National Technology and Engineering Solutions of Sandia, LLC . Under the terms of Contract DE-NA0003525 with National Technology and Engineering Solutions of Sandia, LLC , the U.S. Government retains certain rights in this software.
