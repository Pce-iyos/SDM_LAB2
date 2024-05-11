import csv
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD

def create_abox():
    g = Graph()
    pub = Namespace("http://example.com/")
    g.bind("pub", pub)
    
    # Load entities from CSV files and their properties
    entity_files = {
        'authors.csv': (pub.Author, 'authorId', ['name', 'email', 'department']),
        'organizations.csv': (pub.Organization, 'OrganizationID', ['affiliation_name', 'affiliationType']),
        'papers.csv': (pub.Paper, 'paperId', ['title', 'abstract','pages','DOI','link','citationCount','date']),
        'journal.csv': (pub.Journal, 'publicationId', ['publicationType','name','venue','year','issn','url','volume']),
        'conferences.csv': (pub.Conference, 'publicationId', ['name','year','venue','issn','url','edition']),
        'workshops.csv': (pub.Workshop, 'publicationId', ['name','year','venue','issn','url','edition']),
        'keywords.csv': (pub.Keyword, 'ID', ['name','domain']),
        'proceedings.csv': (pub.Proceedings, 'ID', ['name','city'])
    }

    
    
    for filename, (class_uri, id_field, attributes) in entity_files.items():
        with open(f'/home/pce/Documents/LAB1_SDM/DATA/CSV_files/{filename}', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entity = URIRef(pub[row[id_field]])
                g.add((entity, RDF.type, class_uri))
                for attr in attributes:
                    if row.get(attr):
                        g.add((entity, URIRef(pub[attr]), Literal(row[attr])))

    
    # Relationship files configuration
    relationship_files = {
        'organization_affiliated_with_author.csv': {
            'subjects': (pub.Author, 'start_id'),
            'objects': (pub.Organization, 'end_id'),
             'predicate': pub.affiliatedWith
        },
        'author_writes.csv': {
            'subjects': (pub.Author, 'start_id'),
            'objects': (pub.Paper, 'end_id'),
            'predicate': pub.writes,
            'extras': {
                'corresponding_author': (XSD.boolean, 'is_corresponding')
            }
        }, 
        'paper_cite_paper.csv': {
            'subjects': (pub.Paper, 'paper_id'),
            'objects': (pub.Paper, 'cited_paper_id'),
            'predicate': pub.cites
        },
        'paper_keyword.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Keyword, 'END_ID'),
            'predicate': pub.hasKeyword
        },
        'paper_published_in_journal.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Journal, 'END_ID'),
             'predicate': pub.publishedIn
        },
        'paper_presented_in_workshop.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Workshop, 'END_ID'),
            'predicate': pub.presentedInWork
        },
        'paper_presented_in_conference.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Conference, 'END_ID'),
            'predicate': pub.presentedIn
        },
        'conference_part_of_proceedings.csv': {
            'subjects': (pub.Conference, 'START_ID'),
            'objects': (pub.Proceedings, 'END_ID'),
            'predicate': pub.partOf
        },
        
        'workshop_part_of_proceedings.csv': {
            'subjects': (pub.Workshop, 'START_ID'),
            'objects': (pub.Proceedings, 'END_ID'),
            'predicate': pub.partOf
        },
        'reviews_with_decisions.csv': {
            'subjects': (pub.Reviewer, 'paperId'),
            'objects': (pub.Paper, 'reviewerId'),
            'predicate': pub.reviews,
            'extras': {
                'review_content': (XSD.string, 'reviewContent'),
                'decision': (XSD.string, 'decision'),
                'majority_decision': (XSD.string, 'majorityDecision')
            }
        }
    } 


    
    for file_name, config in relationship_files.items():
        with open(f'/home/pce/Documents/LAB1_SDM/DATA/CSV_files/{file_name}', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            subj_info = config['subjects']
            obj_info = config['objects']
            predicate = config['predicate']
            extras = config.get('extras', {})
            
            for row in reader:
                subject = URIRef(pub[row[subj_info[1]]])
                object = URIRef(pub[row[obj_info[1]]])
                g.add((subject, predicate, object))
                
                # print(f"Added relationship: {subject} {predicate} {object}")

                  
                for extra_key, (datatype, column) in extras.items():
                    if column in row and row[column]:  # Ensure column exists and has a value
                        extra_predicate = URIRef(pub[extra_key])
                        g.add((subject, extra_predicate, Literal(row[column], datatype=datatype)))

                        
                        # print(f"Added extra property: {subject} {extra_predicate} {Literal(row[column], datatype=datatype)}")


    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/chair_assign_reviewer.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            chair_id = URIRef(pub[row['START_ID']])
            reviewer_id = URIRef(pub[row['END_ID']])
            
            g.add((chair_id, RDF.type, pub.Chair))
            g.add((chair_id, pub.assignReviewer, reviewer_id))
            g.add((chair_id, pub.chair_name, Literal(row['conferenceChair'], datatype=XSD.string)))
            g.add((chair_id, pub.chair_review_policy, Literal(row['reviewPolicy'], datatype=XSD.integer)))

    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/editor_assign_reviewer.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            editor_id = URIRef(pub[row['START_ID']])
            reviewer_id = URIRef(pub[row['END_ID']])
            
            g.add((editor_id, RDF.type, pub.Editor))
            g.add((editor_id, pub.assignReviewer, reviewer_id))
            g.add((editor_id, pub.editor_name, Literal(row['editorName'], datatype=XSD.string)))
            g.add((editor_id, pub.editor_review_policy, Literal(row['reviewPolicy'], datatype=XSD.integer)))

    
    


    return g

# Create the ABox and serialize it
abox_graph = create_abox()
abox_graph.serialize(destination='/home/pce/Documents/LAB1_SDM/DATA/abox_output.ttl', format='turtle')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

