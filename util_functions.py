

def reorder_columns_in_dataframe(df, columns_to_front, columns_to_back=[], columns_to_delete=[]):
    
    # Get original order of columns
    original = df.columns
    
    # Filter to present columns
    columns_to_front = [c for c in columns_to_front if c in original]
    columns_to_back = [c for c in columns_to_back if c in original and c not in columns_to_delete]
    
    # Keep the rest of the columns and sort it for consistency
    columns_other = list(set(original) - set(columns_to_front)- set(columns_to_back) - set(columns_to_delete))
    columns_other.sort()
    
    # Apply the order
    df = df.select(*columns_to_front, *columns_other, *columns_to_back)
    return df



def generate_dim_table_references(source, timestamp_key, dim_table_refs, print_output=True):
    
    query_first = "SELECT src.*"
    query_last = f"\nFROM {source} src"

    for ref in dim_table_refs:
        
        # Construct first part of query: Selects
        query_first += f""", {ref["table_name"]}.{ref["surrogate_key"]} """

        # Construct last part of query: Joins
        query_last += f"""\nLEFT JOIN {ref["table_name"]} ON {ref["table_name"]}.{ref["merge_key"]} = src.{ref["merge_key"]}
        AND src.{timestamp_key} BETWEEN {ref["table_name"]}.meta_valid_from AND {ref["table_name"]}.meta_valid_to"""

    # Print output
    if print_output:
        print(query_first + query_last)

    return query_first + query_last