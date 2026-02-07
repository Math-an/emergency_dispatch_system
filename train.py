import pandas as pd
import spacy
from spacy.pipeline import EntityRuler

def build_advanced_chennai_gazetteer(csv_path, model_name="chennai_gazetteer_model"):
    nlp = spacy.blank("en")
    df = pd.read_csv(csv_path)
    
    localities = df['Locality'].dropna().unique().tolist()
    streets = df['Street'].dropna().unique().tolist()
    areas = df['Area'].dropna().unique().tolist()

    config = {"phrase_matcher_attr": "LOWER", "overwrite_ents": True}
    ruler = nlp.add_pipe("entity_ruler", config=config)

    patterns = []


    for loc in localities:
        patterns.append({"label": "LOCALITY", "pattern": str(loc).strip()})
    for st in streets:
        patterns.append({"label": "STREET", "pattern": str(st).strip()})
    for ar in areas:
        patterns.append({"label": "AREA", "pattern": str(ar).strip()})


    aliases = [
        {"label": "STREET", "pattern": "OMR"},
        {"label": "STREET", "pattern": "ECR"},
        {"label": "STREET", "pattern": "GST Road"},
        {"label": "LOCALITY", "pattern": "T Nagar"},
        {"label": "LOCALITY", "pattern": "Velacherry"}, # Handling the double 'r' typo
    ]
    patterns.extend(aliases)

    ruler.add_patterns(patterns)
    nlp.to_disk(model_name)
    print(f"✅ Model '{model_name}' built with {len(patterns)} patterns.")

if __name__ == "__main__":
    build_advanced_chennai_gazetteer("3b816670-2d4b-47fb-a702-9946890d700a.csv")