# Wikidata Property Checker

This script retrieves a specified Wikidata property for a list of Q-codes provided in a CSV file. It processes the Q-codes in batches to avoid overloading the Wikidata SPARQL endpoint and writes the results to a CSV file while printing them to the terminal. It is designed for batch processing and is particularly useful for collection management, data enrichment, and quality control workflows.

## What does this script do?

* Reads a CSV file named `source.csv` with columns `recordnumber` and `qcode`.
* Queries the Wikidata SPARQL endpoint to retrieve a specific property (P-code) for each Q-code.
* Processes the Q-codes in configurable batch sizes.
* Writes the results to an output CSV file `results.csv` with columns `recordnumber`, `qcode`, `prop_uri`, and `full_url`.
* Prints each result to the terminal.

## Features

* Handles large batches of Q-codes.
* Avoids overloading Wikidata with a configurable pause between batches.
* Supports any Wikidata property (P-code) by including the `P` prefix.
* Clearly indicates if a property is found or missing.
* Outputs results in CSV format ready for further processing.

## Input format

The input CSV must be named `source.csv` and have the following columns:

* **Column A (`recordnumber`)**: your internal record number or identifier.
* **Column B (`qcode`)**: the Wikidata Q-code.

Example:

```csv
recordnumber,qcode
140584,Q100116
165295,Q1000385
```


## Base URLs for properties

The script can append a base URL to certain properties to produce a full URL in the output. Currently supported properties:

* **P245 (`ULAN`)**: http://vocab.getty.edu/ulan/
* **P650 (`RKD artists`)**: https://rkd.nl/artists/

If a property is not listed here, the full_url column in the output CSV will remain empty.

You can extend the script by adding more mappings in base_url_map if needed:
```python
base_url_map = {
    'P245': 'http://vocab.getty.edu/ulan/',
    'P650': 'https://rkd.nl/artists/',
    # Add more mappings here if needed
}
```

## Requirements

- Python 3.9 or higher
- Python packages:

```bash
pip install rdflib
```

## Usage
Run the script via command line:

```bash
python get_property_links.py -p P245
```

`-p`, `--property`: the Wikidata property ID to retrieve. Always include the `P` prefix.  
If no property is specified, it defaults to `P245` (ULAN).

Retrieve ULAN links (default):

```bash
python get_property_links.py
```

Retrieve RKD artists IDs:
```bash
python get_property_links.py -p P650
```

## Output
The output CSV `results.csv` contains:

```csv
recordnumber,qcode,prop_uri,full_url
140584,Q100116,500115588,http://vocab.getty.edu/ulan/500115588
165295,Q1000385,,
```

If no property is found, `prop_uri` and `full_url` will be empty.

All results are also printed in the terminal.

## Typical workflow
Prepare `source.csv` with your Q-codes and record numbers.

Run the script with the desired property using the `-p` argument.

Review the `results.csv` file for found or missing properties.

## Recommended project structure

```
wikidata-property-checker/
│
├── get_match_from_wikidata.py
├── source.csv
├── results.csv
└── README.md
```

## Contributing

Contributions, improvements, and bug fixes are welcome. Please provide clear commit messages and usage examples.

## License

This project is released under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**.  
You are free to copy, modify, distribute, and use this work, even for commercial purposes, without asking for permission. No attribution is required.

**Author:** Jeroen De Meester  
**Repository:** [https://github.com/Jeroen-DeMeester/wikidata-property-checker](https://github.com/Jeroen-DeMeester/wikidata-property-checker)