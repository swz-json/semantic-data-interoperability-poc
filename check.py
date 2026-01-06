from rdflib import Graph

# 1. On charge le fichier que tu as créé
g = Graph()
g.parse("output/knowledge_graph.ttl", format="turtle")

print(f"✅ Succès ! Le graphe contient {len(g)} informations (triples).")

# 2. On affiche tout ce qu'on a trouvé pour prouver que l'ordinateur le comprend
print("\n--- Liste des villes et leur pollution ---")
query = """
    SELECT ?name ?pollution
    WHERE {
        ?city schema:name ?name .
        ?city ex:pollutionIndex ?pollution .
    }
"""

# Exécution de la requête (C'est du SPARQL, le SQL du Web Sémantique)
for row in g.query(query):
    print(f"🏙️  {row.name} a un indice de pollution de {row.pollution}")