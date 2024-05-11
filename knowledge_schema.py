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
        pub.Keyword, pub.CommitteeMember, pub.Chair, pub.Editor,
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
    g.add((pub.Chair, RDFS.subClassOf, pub.CommitteeMember))
    g.add((pub.Editor, RDFS.subClassOf, pub.CommitteeMember))
    

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
        "assignReviewer": (pub.CommitteeMember, pub.Reviewer),
        
        "chair_id": (pub.Chair, XSD.string),
        "chair_name":(pub.Chair, XSD.string),
        "chair_review_policy": (pub.Chair, XSD.integer),
        
        "editor_id": (pub.Editor, XSD.string),
        "editor_name":(pub.Editor, XSD.string),
        "editor_review_policy": (pub.Editor, XSD.integer),
        
        
        "keyword_ID": (pub.Keyword, XSD.string),
        "keyword_name": (pub.Keyword, XSD.string),  
        "domain": (pub.Keyword, XSD.string),
        
        "paperId": (pub.Paper, XSD.string),
        "paper_title": (pub.Paper, XSD.string),
        "abstract": (pub.Paper, XSD.string),
        "paper_pages": (pub.Paper, XSD.string),
        "DOI": (pub.Paper,XSD.string),
        "paper_link": (pub.Paper,XSD.string),
        "citationCount": (pub.Paper, XSD.integer),
        "paper_date": (pub.Paper, XSD.date),
        
        
        "authorId": (pub.Author, XSD.string),
        "author_name": (pub.Author, XSD.string), 
        "author_email": (pub.Author, XSD.string), 
        "author_department": (pub.Author, XSD.string), 
        
                
        "OrganizationID": (pub.Organization, XSD.string),
        "affiliation_name": (pub.Organization, XSD.string),
        "affiliationType": (pub.Organization, XSD.string),
        
        
        "conf_publicationId": (pub.Conference, XSD.string),
        "conf_name": (pub.Conference, XSD.string),
        "conf_year": (pub.Conference, XSD.integer),
        "conf_venue": (pub.Conference, XSD.string),
        "conf_issn": (pub.Conference, XSD.integer),
        "conf_url": (pub.Conference, XSD.string),
        "conf_edition": (pub.Conference, XSD.integer),
        
        
        "jour_publicationId": (pub.Journal, XSD.string),
        "publicationType": (pub.Journal, XSD.string),
        "jour_name": (pub.Journal, XSD.string),
        "jour_venue": (pub.Journal, XSD.string),
        "jour_year": (pub.Journal, XSD.integer),
        "jour_issn": (pub.Journal, XSD.integer),
        "jour_url": (pub.Journal, XSD.string),
        "jour_volume": (pub.Journal, XSD.integer),
        
        
       
        "work_publicationId": (pub.Workshop, XSD.string),
        "work_name": (pub.Workshop, XSD.string),
        "work_year": (pub.Workshop, XSD.integer),
        "work_venue": (pub.Workshop, XSD.string), 
        "work_issn": (pub.Workshop, XSD.integer),
        "work_url": (pub.Workshop, XSD.string),
        "work_edition": (pub.Workshop, XSD.integer),
        
         
        "reviewerId": (pub.Reviewer, XSD.string),
        "reviewContent": (pub.Reviewer, XSD.string),
        "decision": (pub.Reviewer, XSD.string),
        "majorityDecision": (pub.Reviewer, XSD.string)
        
    }

    for prop, (dom, rng) in properties.items():
        # p = URIRef(f"{str(pub)}{prop}")  
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
