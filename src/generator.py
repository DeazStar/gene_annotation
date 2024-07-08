def generate_query(requests, schema):
    query = []
    for request in requests:
        # TODO validate request
        predicate_schema = request['predicate']
        
        source = schema[predicate_schema]['source']
        target = schema[predicate_schema]['target']
        
        source_node = request['source']

        if source_node['id'].startswith("$"):
            match = "MATCH (source: {} {{id: $id,".format(source)
        else:
            match = "MATCH (source: {} {{".format(source)
        for property, value in request['source']['properties'].items():
            if isinstance(value, str):
                match += " " + f"{property}: '{value}',"
            elif isinstance(value, int):
                match += " " + f"{property}: {value},"
        match = match.rstrip(', ') + "})\n"

        match += "MATCH (target: {} {{".format(target)
        for property, value in request['target']['properties'].items():
            if isinstance(value, str):
                match += " " + f"{property}: '{value}',"
            elif isinstance(value, int):
                match += " " + f"{property}: {value}"        
        match = match.rstrip(', ') + "})\n"
        
        predicate = request['predicate'].replace(" ", "_")

        match += f"""MATCH (source)-[predicate:{predicate}]->(target)\nRETURN*"""

        match = match.strip(' ')

        query.append(match)
    return query

