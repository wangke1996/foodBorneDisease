from py2neo import Graph,Node,Relationship
graph = Graph("http://localhost:7474",auth=("neo4j","ohahaha"))
a = Node("Person", name="Alice")
b = Node("Person", name="Bob")
ab = Relationship(a, "KNOWS", b)
graph.create(ab)