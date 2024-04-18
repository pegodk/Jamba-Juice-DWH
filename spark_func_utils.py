def generate_dim_table_references(source_table, timestamp_key, dim_table_refs, print_output=False):
    
    query_first = "SELECT s.*"
    query_last = f"\nFROM {source_table} s"

    for ref in dim_table_refs:
        
        # Construct first part of query: Selects
        query_first += f""", COALESCE({ref["table_name"]}.{ref["surrogate_key"]}, 'N/A') AS {ref["surrogate_key"]} """

        # Construct last part of query: Joins
        query_last += f"""\nLEFT JOIN {ref["table_name"]} ON {ref["table_name"]}.{ref["join_key"]} = s.{ref["join_key"]}
        AND s.{timestamp_key} BETWEEN {ref["table_name"]}.meta_valid_from AND {ref["table_name"]}.meta_valid_to"""

    # Print output
    if print_output:
        print(query_first + query_last)

    return query_first + query_last