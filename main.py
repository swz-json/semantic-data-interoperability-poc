import csv
from rdflib import Graph, Literal, RDF, URIRef, Namespace
# CORRECTION ICI : On retire 'SCHEMA' de l'import car il causait l'erreur
from rdflib.namespace import XSD 
import urllib.parse

def convert_csv_to_rdf(input_file, output_file):
    g = Graph()

    EX = Namespace("http://example.org/data/")
    
    # CORRECTION ICI : On définit manuellement le namespace Schema.org
    SCHEMA = Namespace("https://schema.org/")

    g.bind("ex", EX)
    g.bind("schema", SCHEMA)

    print(f"🔄 Lecture de {input_file}...")

    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            city_slug = urllib.parse.quote(row['City'].replace(' ', '_'))
            
            # Création du sujet
            city_uri = EX[city_slug]

            # Ajout des triples
            g.add((city_uri, RDF.type, SCHEMA.City))
            g.add((city_uri, SCHEMA.name, Literal(row['City'], datatype=XSD.string)))
            g.add((city_uri, SCHEMA.addressCountry, Literal(row['Country'])))
            g.add((city_uri, SCHEMA.population, Literal(row['Population'], datatype=XSD.integer)))
            g.add((city_uri, EX['pollutionIndex'], Literal(row['PollutionIndex'], datatype=XSD.integer)))

    print(f"💾 Sauvegarde du graphe dans {output_file}...")
    g.serialize(destination=output_file, format='turtle')
    print("✅ Conversion terminée !")

if __name__ == "__main__":
    convert_csv_to_rdf("data/pollution_data.csv", "output/knowledge_graph.ttl")