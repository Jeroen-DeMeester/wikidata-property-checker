from argparse import ArgumentParser  # For easily parsing command-line arguments
import csv                           # For reading and writing CSV files
import time                          # For inserting pauses between batches
from rdflib.plugins.stores.sparqlstore import SPARQLStore  # For executing SPARQL queries against Wikidata

def get_property_links_batch(property_id: str, batch_size: int = 50, pause_sec: float = 0.5):
    """
    Retrieves a Wikidata property (e.g., ULAN, Rijksmuseum ID) for Q-codes in source.csv.
    Writes results to results.csv and prints them to the terminal.
    """

    endpoint = 'https://query.wikidata.org/sparql'
    csv_file = 'source.csv'
    output_csv = 'results.csv'

    # Connect to the SPARQL endpoint
    store = SPARQLStore(query_endpoint=endpoint)
    print(f"Using SPARQL endpoint: {endpoint}")
    print(f"Checking property: {property_id}")

    # Optional base URLs for certain properties (appears in output). 
    base_url_map = {
        'P245': 'http://vocab.getty.edu/ulan/',  # ULAN
        'P650': 'https://rkd.nl/artists/',  # rkdArtists
        'P1871': 'http://data.cerl.org/thesaurus/', # cerl.org
        'P214': 'http://viaf.org/viaf/', # viaf
        # Add more mappings here if needed
    }
    base_url = base_url_map.get(property_id, '')

    # Step 1: read all Q-codes and record numbers from CSV. The CSV should have a header with: "recordnumber" and "qcode"
    entries = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append({'recordnumber': row['recordnumber'], 'qcode': row['qcode']})

    # Step 2: open output CSV and write header
    with open(output_csv, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['recordnumber', 'qcode', 'prop_uri', 'full_url'])

        # Step 3: process Q-codes in batches
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]
            values_str = " ".join(f"wd:{e['qcode']}" for e in batch)

            # Step 4: SPARQL query for this batch
            query = f"""
            SELECT ?item ?prop_value
            WHERE {{
                VALUES ?item {{ {values_str} }}
                ?item wdt:{property_id} ?prop_value .
            }}
            """

            # Step 5: execute query
            result = store.query(query)

            # Step 6: map Q-code → found property URI
            prop_map = {str(r[0]).split('/')[-1]: str(r[1]) for r in result}

            # Step 7: write results to CSV and print
            for e in batch:
                code = e['qcode']
                prop_uri = prop_map.get(code, '')  # empty string if not found
                full_url = base_url + prop_uri.split('/')[-1] if prop_uri and base_url else ''
                if prop_uri:
                    print(f"{e['recordnumber']} ({code}): {prop_uri} -> {full_url}")
                else:
                    print(f"{e['recordnumber']} ({code}): No property found")
                writer.writerow([e['recordnumber'], code, prop_uri, full_url])

            # Step 8: pause between batches
            time.sleep(pause_sec)

# ----- CLI -----
if __name__ == '__main__':
    parser = ArgumentParser(description="Retrieve a Wikidata property for Q-codes in source.csv")
    parser.add_argument(
        '-p', '--property',
        type=str,
        default=None,  # if nothing provided, default to P245
        help='Wikidata property ID (e.g., P245 for ULAN). Include the P prefix.'
    )
    args = parser.parse_args()

    # Default to P245 if no property specified
    # For other codes, run: python3 get_match_from_wikidata.py -p P1871
    property_id = args.property if args.property else "P245"

    get_property_links_batch(property_id=property_id)
