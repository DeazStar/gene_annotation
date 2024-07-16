def generate_query(data):
    nodes = data['nodes']
    node_map = {node['node_id']: node for node in nodes}
    match_statements = []
    return_statements = []

    node_without_predicate = None
    predicates = None
    if "predicates" not in data:
        node_without_predicate = nodes
    else:
        predicates = data['predicates']
        node_with_predicate = set()
        for predicate in predicates:
            node_with_predicate.add(predicate["source"])
            node_with_predicate.add(predicate["target"])
        node_without_predicate = [node for node in nodes if node["node_id"] not in node_with_predicate]
        
    if "predicates" not in data or (node_without_predicate is not None and len(node_without_predicate) != 0):
        for node in node_without_predicate:
            node_type = node["type"]
            node_properties_str = ", ".join([f"{k}: '{v}'" for k, v in node["properties"].items()])
            if node['id']:
                match_statement = f"({node['node_id']}:{node_type} {{id: '{node['id']}'}})"
            else:
                match_statement = f"({node['node_id']}:{node_type} {{{node_properties_str}}})"

            return_statements.append(node['node_id'])
            return_statements = list(set(return_statements))
            match_statements.append(match_statement)

    if predicates is None:
        match_query = "MATCH " + ", ".join(match_statements)
        return_query = "RETURN " + ", ".join(return_statements)
        cypher_output = f"{match_query} {return_query}"
        print("OUTPUT", cypher_output)
        return cypher_output

    for predicate in predicates:
        predicate_type = predicate['type'].replace(" ", "_")
        source_id = predicate['source']
        print("source_id", source_id)
        target_id = predicate['target']
        print("target_id", target_id)

        # get source node
        source_node = node_map[source_id]
        print("source_node", source_node)
        source_node_type = source_node["type"]
        source_node_properties_str = ", ".join([f"{k}: '{v}'" for k, v in source_node["properties"].items()])
        if source_node['id']:
            source_match = f"({source_node['node_id']}:{source_node_type} {{id: '{source_node['id']}'}})"
        else:
            source_match = f"({source_node['node_id']}:{source_node_type} {{{source_node_properties_str}}})"
            
        #get target node
        target_node = node_map[target_id]
        print("target_node", target_node)
        target_node_type = target_node["type"]
        target_node_properties_str = ", ".join([f"{k}: '{v}'" for k, v in target_node["properties"].items()])
        if target_node['id']:
            target_match = f"({target_node['node_id']}:{target_node_type} {{id: '{target_node['id']}'}})"
        else:
            target_match = f"({target_node['node_id']}:{target_node_type} {{{target_node_properties_str}}})"
        return_statements.append(source_node['node_id'])
        return_statements.append(target_node['node_id'])
        return_statements = list(set(return_statements))
        match_statement = f" {source_match}-[:{predicate_type}]-{target_match}"
        match_statements.append(match_statement)
    match_query = "MATCH " + ", ".join(match_statements)
    return_query = "RETURN " + ", ".join(return_statements)
    cypher_output = f"{match_query} {return_query}"
    return cypher_output

