# metacsp
Software for analysis of metagenomes and metatranscriptomes from a JGI CSP

[![Build Status](https://travis-ci.org/dacb/metacsp.svg?branch=master)](https://travis-ci.org/dacb/metacsp)
[![Coverage Status](https://coveralls.io/repos/dacb/metacsp/badge.svg?branch=master)](https://coveralls.io/r/dacb/metacsp?branch=master)

---
Components
* metadata

   This module reads in a tab delimited file containing metadata for samples.  Each line should begin with a sample name and contain additional metadata fields.  E.g.
```
sample	oxygen	week	type
s1		low		1		metagenome
s2		high	1		metagenome
```

   The metadata are joined with subsequent analyses and used for output annotation.  This module also includes a function for parsing the metadata sample name from an output path.  The function, defaultSampleNameExtractionFunction, can be overridden by a user defined function and passed to the I/O routines for proper parsing.  See run.py for an example.

* phylodist

   This module reads in IMG formatted phylodist files that contain loci from the assembled input, alignment data such as percent identity and a taxonomy string of ; separated values denoting the kingdom, phylum, class, order, family, genus, species and strain names.  Tools exist to parse these into a dictionary with keys for the various taxonomy levels and for merging these data across samples. The resulting data frames can be joined to metadata loaded from the metadata module and written to Excel files or plotted directly.
