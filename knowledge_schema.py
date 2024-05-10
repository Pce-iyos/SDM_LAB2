from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef, BNode

def create_enhanced_ontology():
    g = Graph()
    pub = Namespace("http://example.com/")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
    
    g.bind("pub", pub)
    g.bind("skos", SKOS)
    g.bind("xsd", XSD)

    # Define Classes
    classes = [
        pub.Publication, pub.Paper, pub.Proceedings, pub.Journal,
        pub.Event, pub.Workshop, pub.Conference,
        pub.Person, pub.Author, pub.Reviewer,
        pub.Establishment, pub.Organization,
        pub.Keyword
    ]
   
    
    # Add classes to the graph
    for cls in classes:
        g.add((cls, RDF.type, RDFS.Class))
    
    # Define subclass relationships
    g.add((pub.Author, RDFS.subClassOf, pub.Person))
    g.add((pub.Reviewer, RDFS.subClassOf, pub.Author))
    g.add((pub.Paper, RDFS.subClassOf, pub.Publication))
    g.add((pub.Proceedings, RDFS.subClassOf, pub.Publication))
    g.add((pub.Journal, RDFS.subClassOf, pub.Publication))
    g.add((pub.Workshop, RDFS.subClassOf, pub.Event))
    g.add((pub.Conference, RDFS.subClassOf, pub.Event))
    g.add((pub.Organization, RDFS.subClassOf, pub.Establishment))

    # Define Properties with domain and range
    properties = {
        "affiliatedWith": (pub.Author, pub.Organization),
        "writes": (pub.Author, pub.Paper),
        "presentedInWork": (pub.Paper, pub.Workshop),
        "publishedIn": (pub.Paper, pub.Journal),
        "partOf": (pub.Event, pub.Proceedings),
        "hasKeyword": (pub.Paper, pub.Keyword),  
        "cites": (pub.Paper, pub.Paper),
        "correspondingAuthor": (pub.Author, pub.Paper),
        "reviews": (pub.Reviewer, pub.Paper),
        "presentedIn": (pub.Paper, pub.Conference),
        
        
        
        "ID": (pub.Keyword, XSD.string),
        "name": (pub.Keyword, XSD.string),  
        "domain": (pub.Keyword, XSD.string),
        
        "paperId": (pub.Paper, XSD.string),
        "title": (pub.Paper, XSD.string),
        "abstract": (pub.Paper, XSD.string),
        "pages": (pub.Paper, XSD.string),
        "DOI": (pub.Paper,XSD.string),
        "link": (pub.Paper,XSD.string),
        "citationCount": (pub.Paper, XSD.integer),
        "date": (pub.Paper, XSD.date),
        
        
        "authorId": (pub.Author, XSD.string),
        "name": (pub.Author, XSD.string), 
        "email": (pub.Author, XSD.string), 
        "department": (pub.Author, XSD.string), 
        
                
        "OrganizationID": (pub.Organization, XSD.string),
        "affiliation_name": (pub.Organization, XSD.string),
        "affiliationType": (pub.Organization, XSD.string),
        
        
        "publicationId": (pub.Conference, XSD.string),
        "name": (pub.Conference, XSD.string),
        "year": (pub.Conference, XSD.integer),
        "venue": (pub.Conference, XSD.string),
        "issn": (pub.Conference, XSD.integer),
        "url": (pub.Conference, XSD.string),
        "edition": (pub.Conference, XSD.integer),
        
        
        "publicationId": (pub.Journal, XSD.string),
        "publicationType": (pub.Journal, XSD.string),
        "name": (pub.Journal, XSD.string),
        "venue": (pub.Journal, XSD.string),
        "year": (pub.Journal, XSD.integer),
        "issn": (pub.Journal, XSD.integer),
        "url": (pub.Journal, XSD.string),
        "volume": (pub.Journal, XSD.integer),
        
        
       
        "publicationId": (pub.Workshop, XSD.string),
        "name": (pub.Workshop, XSD.string),
        "year": (pub.Workshop, XSD.integer),
        "venue": (pub.Workshop, XSD.string), 
        "issn": (pub.Workshop, XSD.integer),
        "url": (pub.Workshop, XSD.string),
        "edition": (pub.Workshop, XSD.integer),
        
         
        "reviewerId": (pub.Reviewer, XSD.string),
        "reviewContent": (pub.Reviewer, XSD.string),
        "decision": (pub.Reviewer, XSD.string),
        "majorityDecision": (pub.Reviewer, XSD.string)
        
    }

    for prop, (dom, rng) in properties.items():
        p = URIRef(pub[prop])
        g.add((p, RDF.type, RDF.Property))
        g.add((p, RDFS.domain, dom))
        g.add((p, RDFS.range, rng))
        

    return g

# Generate and save the enhanced ontology
ontology_graph = create_enhanced_ontology()
with open("/home/pce/Documents/LAB1_SDM/DATA/kgtbox.ttl", "wb") as f:
    f.write(ontology_graph.serialize(format="turtle").encode('utf-8'))


# Save to JSON-LD
with open("/home/pce/Documents/LAB1_SDM/DATA/kgtbox.json", "w") as f:
    f.write(ontology_graph.serialize(format="json-ld"))
