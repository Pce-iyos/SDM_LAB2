
import urllib.parse    
import csv
from rdflib import Graph, Namespace, Literal, URIRef, RDF, XSD

def create_abox(pub):
    g = Graph()
    g.bind("pub", pub)
    
    # Load entities from CSV files and their properties
    entity_files = {
        'authors.csv': (pub.Author, 'authorId', ['name', 'email', 'department']),
        'organizations.csv': (pub.Organization, 'OrganizationID', ['affiliation_name', 'affiliationType']),
        'papers.csv': (pub.Paper, 'paperId', ['title', 'abstract', 'pages', 'DOI', 'link', 'citationCount', 'date', 'journalId', 'volume']),
        'workshops.csv': (pub.Workshop, 'publicationId', ['name', 'year', 'venue', 'issn', 'url', 'edition']),
        'proceedings.csv': (pub.Proceedings, 'ID', ['name', 'city']),
        'keywords.csv': (pub.Keyword, 'ID', ['name', 'domain']),
        'journal.csv': (pub.Journal, 'publicationId', ['publicationType', 'name', 'venue', 'year', 'issn', 'url', 'volume']),
        'conferences.csv': (pub.Conference, 'publicationId', ['name', 'year', 'venue', 'issn', 'url', 'edition'])
    }

    for filename, (class_uri, id_field, attributes) in entity_files.items():
        with open(f'/home/pce/Documents/LAB1_SDM/DATA/CSV_files/{filename}', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entity_uri = URIRef(f"{pub}{class_uri}/{urllib.parse.quote(row[id_field])}")
                g.add((entity_uri, RDF.type, class_uri))
                for attr in attributes:
                    if row.get(attr):
                        g.add((entity_uri,  URIRef(f"{pub}property/{urllib.parse.quote(attr)}"), Literal(row[attr])))

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
        'paper_presented_in_workshop.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Workshop, 'END_ID'),
            'predicate': pub.presentedInWork
        },
        'workshop_part_of_proceedings.csv': {
            'subjects': (pub.Workshop, 'START_ID'),
            'objects': (pub.Proceedings, 'END_ID'),
            'predicate': pub.paperPartOfwork
        },
        'paper_presented_in_conference.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Conference, 'END_ID'),
            'predicate': pub.presentedIn
        },
        'conference_part_of_proceedings.csv': {
            'subjects': (pub.Conference, 'START_ID'),
            'objects': (pub.Proceedings, 'END_ID'),
            'predicate': pub.paperPartOfconf
        },
        'paper_keyword.csv': {
            'subjects': (pub.Paper, 'START_ID'),
            'objects': (pub.Keyword, 'END_ID'),
            'predicate': pub.hasKeyword
        },
        'paper_cite_paper.csv': {
            'subjects': (pub.Paper, 'paper_id'),
            'objects': (pub.Paper, 'cited_paper_id'),
            'predicate': pub.cites
        },
        'reviews_with_decisions.csv': {
            'subjects': (pub.Reviewer, 'reviewerId'),
            'objects': (pub.Paper, 'paperId'),
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
                subject = URIRef(f"{pub}{subj_info[0]}/{urllib.parse.quote(row[subj_info[1]])}")
                object = URIRef(f"{pub}{obj_info[0]}/{urllib.parse.quote(row[obj_info[1]])}")
                g.add((subject, predicate, object))
                
                for extra_key, (datatype, column) in extras.items():
                    if column in row and row[column]:  
                        extra_predicate = URIRef(f"{pub}property/{urllib.parse.quote(extra_key)}")
                        g.add((subject, extra_predicate, Literal(row[column], datatype=datatype)))
                        
    # Handling chair and editor assignments
    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/chair_assign_reviewer.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            chair_id = URIRef(f"{pub}Chair/{urllib.parse.quote(row['START_ID'])}")
            reviewer_id = URIRef(f"{pub}Reviewer/{urllib.parse.quote(row['END_ID'])}")
           
            g.add((chair_id, RDF.type, pub.Chair))
            g.add((chair_id, pub.assignReviewer, reviewer_id))
            g.add((chair_id, pub.chair_name, Literal(row['conferenceChair'], datatype=XSD.string)))
            g.add((chair_id, pub.chair_review_policy, Literal(row['reviewPolicy'], datatype=XSD.integer)))

    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/editor_assign_reviewer.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            editor_id = URIRef(f"{pub}Editor/{urllib.parse.quote(row['START_ID'])}")
            reviewer_id = URIRef(f"{pub}Reviewer/{urllib.parse.quote(row['END_ID'])}")
            
            g.add((editor_id, RDF.type, pub.Editor))
            g.add((editor_id, pub.assignReviewer, reviewer_id))
            g.add((editor_id, pub.editor_name, Literal(row['editorName'], datatype=XSD.string)))
            g.add((editor_id, pub.editor_review_policy, Literal(row['reviewPolicy'], datatype=XSD.integer)))

    return g

def create_volume_instances(g, pub):
    volume_dict = {}
    # Extract volume and year from journal.csv
    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/journal.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            volume_id = f"{row['publicationId']}_volume_{row['volume']}"
            volume_uri = URIRef(f"{pub}Volume/{urllib.parse.quote(volume_id)}")
            journal_uri = URIRef(f"{pub}Journal/{urllib.parse.quote(row['publicationId'])}")
            
            # Create Volume instance and add properties
            g.add((volume_uri, RDF.type, pub.Volume))
            g.add((volume_uri, pub.name, Literal(row['volume'], datatype=XSD.string)))
            g.add((volume_uri, pub.year, Literal(row['year'], datatype=XSD.integer)))
            
            # Establish relationship between Volume and Journal
            g.add((volume_uri, pub.publishedIn, journal_uri))
            
            # Establish relationship between Volume and Publication
            publication_uri = URIRef(f"{pub}Publication/{urllib.parse.quote(row['publicationId'])}")
            g.add((volume_uri, pub.VolumeInPub, publication_uri))
            
            # Store volume information for later use
            volume_dict[(row['publicationId'], row['volume'])] = volume_uri

    return g, volume_dict

def add_event_types(g, pub):
    # Extract event types from proceedings.csv
    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/proceedings.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proceeding_uri = URIRef(f"{pub}Proceedings/{urllib.parse.quote(row['ID'])}")
            g.add((proceeding_uri, RDF.type, pub.Proceedings))
            g.add((proceeding_uri, pub.name, Literal(row['name'])))
            g.add((proceeding_uri, pub.city, Literal(row['city'])))
            
            # Determine and add event type
            if 'workshop' in row['name'].lower():
                g.add((proceeding_uri, pub.WorkEventType, Literal("WorkEventType")))
            elif 'conference' in row['name'].lower():
                g.add((proceeding_uri, pub.ConfEventType, Literal("ConfEventType")))

    return g

def extract_paper_info():
    paper_info = {}
    with open('/home/pce/Documents/LAB1_SDM/DATA/CSV_files/paper_published_in_journal.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            paper_id = row['START_ID']
            publication_id = row['END_ID']
            paper_info[paper_id] = publication_id
    return paper_info

def link_papers_to_volumes(g, pub, paper_info, volume_dict):
    # Link paper instances to volume instances using paperPartOfJour property
    for paper_id, publication_id in paper_info.items():
        paper_uri = URIRef(f"{pub}Paper/{urllib.parse.quote(paper_id)}")
        # Find the corresponding volume in volume_dict
        for (pub_id, vol), volume_uri in volume_dict.items():
            if pub_id == publication_id:
                g.add((paper_uri, pub.paperPartOfJour, volume_uri))
                break
    return g

def link_events_to_publications(g, pub):
    # Link event instances to publication instances using eventInPub property
    event_files = {
        'workshops.csv': pub.Workshop,
        'conferences.csv': pub.Conference
    }
    
    for filename, class_uri in event_files.items():
        with open(f'/home/pce/Documents/LAB1_SDM/DATA/CSV_files/{filename}', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                event_uri = URIRef(f"{pub}{class_uri}/{urllib.parse.quote(row['publicationId'])}")
                publication_uri = URIRef(f"{pub}Publication/{urllib.parse.quote(row['publicationId'])}")
                g.add((event_uri, pub.eventInPub, publication_uri))

    return g

# Create the ABox and serialize it
pub = Namespace("http://example.com/")
abox_graph = create_abox(pub)
abox_graph, volume_dict = create_volume_instances(abox_graph, pub)
abox_graph = add_event_types(abox_graph, pub)

paper_info = extract_paper_info()

# Link papers to volumes
abox_graph = link_papers_to_volumes(abox_graph, pub, paper_info, volume_dict)

# Link events to publications
abox_graph = link_events_to_publications(abox_graph, pub)

# Serialize the final graph to a file
abox_graph.serialize(destination='/home/pce/Documents/LAB1_SDM/DATA/abox_result.ttl', format='turtle')
