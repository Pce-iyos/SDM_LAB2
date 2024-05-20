
from rdflib import Graph, Namespace, RDF, RDFS

def load_and_link_graphs(tbox_path, abox_path, output_path, infer=True):
    # Define namespaces
    pub = Namespace("http://example.com/")
    
    # Load TBOX
    tbox = Graph()
    try:
        tbox.parse(tbox_path, format='turtle')
    except Exception as e:
        print(f"Failed to load TBOX: {e}")
        return
    
    # Load ABOX
    abox = Graph()
    try:
        abox.parse(abox_path, format='turtle')
    except Exception as e:
        print(f"Failed to load ABOX: {e}")
        return
    
    if infer:
        for s, p, o in abox.triples((None, RDF.type, None)):
            for super_class in tbox.transitive_objects(o, RDFS.subClassOf):
                if super_class != o:  
                    abox.add((s, RDF.type, super_class))
                    

    # Merge TBOX and ABOX into a single graph
    combined_graph = tbox + abox

    # Save the combined graph
    try:
        combined_graph.serialize(destination=output_path, format='turtle')
        print("Combined graph saved successfully.")
    except Exception as e:
        print(f"Failed to save combined graph: {e}")
        
def compute_statistics(graph):
    pub = Namespace("http://example.com/")
    
    # Count the number of classes
    num_classes = len(set(graph.subjects(RDF.type, RDFS.Class)))
    
    # Count the number of properties
    num_properties = len(set(graph.subjects(RDF.type, RDF.Property)))
    
    # Count the number of instances for each main class
    classes_of_interest = {
        "Author": pub.Author,
        "Paper": pub.Paper,
        "Conference": pub.Conference,
        "Journal": pub.Journal,
        "Workshop": pub.Workshop,
        "Organization": pub.Organization,
        "Proceedings": pub.Proceedings,
        # "Reviewer": pub.Reviewer,
        "Keyword": pub.Keyword
    }
    
    instance_counts = {}
    for class_label, class_uri in classes_of_interest.items():
        num_instances = len(set(graph.subjects(RDF.type, class_uri)))
        instance_counts[class_label] = num_instances

    # Count total number of triples
    total_triples = len(graph)
    
    # Print or return the results
    print(f"Number of Classes: {num_classes}")
    print(f"Number of Properties: {num_properties}")
    for class_label, count in instance_counts.items():
        print(f"Number of {class_label} Instances: {count}")
    print(f"Total Number of Triples: {total_triples}")


# Paths to your TBOX and ABOX files
tbox_path = '/home/pce/Documents/LAB1_SDM/DATA/kgtbox.ttl'
abox_path = '/home/pce/Documents/LAB1_SDM/DATA/abox_result.ttl'
output_path = '/home/pce/Documents/LAB1_SDM/DATA/combined_graph_test.ttl'

# Run the function with inference enabled
load_and_link_graphs(tbox_path, abox_path, output_path, infer=True)


combined_graph = Graph()
combined_graph.parse('/home/pce/Documents/LAB1_SDM/DATA/combined_graph_test.ttl', format='turtle')

# Compute and display statistics
compute_statistics(combined_graph)
