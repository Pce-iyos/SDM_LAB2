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
        pub.Publication, pub.Paper, pub.Journal,
        pub.Event,
        pub.Workshop, pub.Conference,
        pub.Person, pub.Author, pub.Reviewer,
        pub.Establishment, pub.Organization,
        pub.Keyword, pub.CommitteeMember, pub.Volume, 
        pub.Conf_Proceedings, pub.Work_Proceedings
    ]
    
    # Add classes to the graph
    for cls in classes:
        g.add((cls, RDF.type, RDFS.Class))
    
    # Define subclass relationships
    
    g.add((pub.Author, RDFS.subClassOf, pub.Person))
    g.add((pub.Reviewer, RDFS.subClassOf, pub.Author))
    g.add((pub.Paper, RDFS.subClassOf, pub.Publication))
    g.add((pub.Organization, RDFS.subClassOf, pub.Establishment))
    

    # Define Properties with domain and range
    properties = {
        
        "affiliatedWith": (pub.Author, pub.Organization),
        "writes": (pub.Author, pub.Paper),
        
        "paperPartOfjour": (pub.Paper, pub.Volume),
        "paperPartOfconf": (pub.Paper, pub.Conf_Proceedings),
        "paperPartOfwork": (pub.Paper, pub.Work_Proceedings),

        "presentedInWork": (pub.Work_Proceedings, pub.Workshop),
        "publishedIn": (pub.Volume, pub.Journal),
        "presentedIn": (pub.Conf_Proceedings, pub.Conference),
        
        "WorkEventtype": (pub.Workshop, pub.Event),
        "ConfEventtype": (pub.Conference, pub.Event),
        
        "VolumeInPub": (pub.Volume, pub.Publication),
        "EventInPub": (pub.Event, pub.Publication),


        "hasKeyword": (pub.Paper, pub.Keyword),  
        "cites": (pub.Paper, pub.Paper),
        "correspondingAuthor": (pub.Author, pub.Paper),
        "reviews": (pub.Reviewer, pub.Paper),
        "assignReviewer": (pub.CommitteeMember, pub.Reviewer),
        
        
        "Conf_Proceedings_year": (pub.Conf_Proceedings, XSD.integer),
        "work_Proceedings_year": (pub.Work_Proceedings, XSD.integer),
        "volume_year": (pub.Volume, XSD.integer),
        
      
  
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
        p = URIRef(pub[prop])
        g.add((p, RDF.type, RDF.Property))
        g.add((p, RDFS.domain, dom))
        g.add((p, RDFS.range, rng))
        
    g.add((pub.EventInPub, RDF.type, RDF.Property))
    g.add((pub.EventInPub, RDFS.subPropertyOf, pub.paperPartOfconf))
    g.add((pub.EventInPub, RDFS.subPropertyOf, pub.paperPartOfwork))
    g.add((pub.EventInPub, RDFS.domain, pub.Event))
    g.add((pub.EventInPub, RDFS.range, pub.Publication))
    
    g.add((pub.VolumeInPub, RDF.type, RDF.Property))
    g.add((pub.VolumeInPub, RDFS.subPropertyOf, pub.paperPartOfjour))
    g.add((pub.VolumeInPub, RDFS.domain, pub.Volume))
    g.add((pub.VolumeInPub, RDFS.range, pub.Publication))
    
    g.add((pub.correspondingAuthor, RDF.type, RDF.Property))
    g.add((pub.correspondingAuthor, RDFS.subPropertyOf, pub.writes))
    g.add((pub.correspondingAuthor, RDFS.domain, pub.Author))
    g.add((pub.correspondingAuthor, RDFS.range, pub.Paper))
        

    return g

# Generate and save the enhanced ontology
ontology_graph = create_enhanced_ontology()
with open("/home/pce/Documents/LAB1_SDM/DATA/a_kgtbox.ttl", "wb") as f:
    f.write(ontology_graph.serialize(format="turtle").encode('utf-8'))


