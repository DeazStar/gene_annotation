def generate_query(requests, schema):
    # TODO validate request
    predicates = requests['predicates']
    nodes = requests['nodes']

    node_map = {node['node_id']: node for node in nodes}

    query = "MATCH"
    for predicate in predicates:
        relationship = predicate['type'].replace(' ', '_')
        source = predicate['source']
        target= predicate['target']

        
        source_node = node_map[source]

        node_type = source_node["type"]
        node_id = source_node["node_id"]
        query += " " + f"({node_id}: {node_type} {{"
        for property, value in source_node['properties'].items():
            if isinstance(value, str):
                query += " " + f"{property}: '{value}',"
            elif isinstance(value, int):
                query += " " + f"{property}: {value},"
        query = query.rstrip(', ') + "}),"
        
        target_node = node_map[target]

        node_type = target_node["type"]
        node_id = target_node["node_id"]
        query += " " + f"({node_id}: {node_type} {{"
        for property, value in target_node['properties'].items():
            if isinstance(value, str):
                query += " " + f"{property}: '{value}',"
            elif isinstance(value, int):
                query += " " + f"{property}: {value},"
        query = query.rstrip(', ') + "}),"

        query += " " + f"({source})-[:{relationship}]->({target}),"
        query = query.strip(' ')
    query = query.rstrip(', ')
    query += " RETURN *"
    return query

