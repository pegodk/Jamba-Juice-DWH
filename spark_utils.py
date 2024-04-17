def generate_dim_table_references(source, target, timestamp_key, dim_table_refs, delta_load_column, print_output=False):
    
    query_first = "SELECT s.*"
    query_last = f"\nFROM {source} s"

    for ref in dim_table_refs:
        
        # Construct first part of query: Selects
        query_first += f""", {ref["table_name"]}.{ref["surrogate_key"]} """

        # Construct last part of query: Joins
        query_last += f"""\nLEFT JOIN {ref["table_name"]} ON {ref["table_name"]}.{ref["merge_key"]} = s.{ref["merge_key"]}
        AND s.{timestamp_key} BETWEEN {ref["table_name"]}.meta_valid_from AND {ref["table_name"]}.meta_valid_to"""

    # Add delta load logic if the target table already exists
    if delta_load_column:
        query_last += f"\n WHERE s.{delta_load_column} > (SELECT COALESCE(MAX({delta_load_column}), '1970-01-01') FROM {target})"
    
    # Print output
    if print_output:
        print(query_first + query_last)

    return query_first + query_last