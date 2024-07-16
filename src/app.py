from flask import Flask, request, jsonify
from  biocypher import BioCypher
import logging
from generator import  generate_query 

logging.basicConfig(level=logging.DEBUG)

bcy = BioCypher(schema_config_path='./config/schema_config.yaml', biocypher_config_path='./config/biocypher_config.yaml')
schema = bcy._get_ontology_mapping()._extend_schema()

from neo4j import GraphDatabase

def read_queries_from_file(script_path):
    with open(script_path, 'r') as file:
        queries = file.read().split(';')
    return [query.strip() for query in queries if query.strip()]

def execute_queries(tx, queries):
    results = []
    previous_results = []
    for query in queries:
        if query:
            if "$id" in query:
                if len(previous_results) == 0:
                    return
                temp = []
                for previous_result in previous_results:
                    source_id = previous_result['target']['id']
                    rs = tx.run(query, id=source_id)
                    data = rs.data()
                    results.append(data)
                    temp.extend(data)
                previous_results = temp
            else:
                rs = tx.run(query)
                data = rs.data()
                previous_results = data
                results.append(data)
    return results

def load_data():
    uri = "neo4j+s://2838a353.databases.neo4j.io"
    user = "neo4j"
    password = "_xmUcjpnF0ZKDOVeRY6dSZ_tfFGLDvW8mDVF0eC1p6w" 
    
    driver = GraphDatabase.driver(uri, auth=(user, password))

#    queries = read_queries_from_file('./data/data.cypher')

#    with driver.session(database="neo4j") as session:
 #       session.write_transaction(execute_queries, queries)

    return driver

driver = load_data()

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    queries = generate_query(data["requests"])
    
    #response = []

    #with driver.session(database="neo4j") as session:
        #for query in queries:
            #result = session.run(query)
            #data = result.data()
            #print(data)
            #response.extend(data)
            #print("result")
            #print(response)
    print(queries) 
    with driver.session(database="neo4j") as session:
        result = session.run(queries)
        result = result.data()
   
    res = []
    for nodes in result:
        res.extend([{"data": node} for node in nodes.values()])
    #response = [{"data": node} for node in response]
    
    return jsonify({"nodes": res})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
