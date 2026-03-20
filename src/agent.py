# Agent module
import sys
import os
from typing import List, Dict, Optional

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion import Ingestion
from extraction import Extraction, SourceClaims
from grouping import Grouping, ClaimGroup
from generation import Generation
from dotenv import load_dotenv

# Load environment variables (like GEMINI_API_KEY)
load_dotenv()

class ResearchDigestAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.extraction = Extraction(api_key=self.api_key)
        self.grouping = Grouping(api_key=self.api_key)

    def run(self, urls: List[str] = None, folder_path: str = None, output_dir: str = "output"):
        """Run the research digest agent."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        print(f"Starting research digest agent with {len(urls) if urls else 0} URLs and folder {folder_path}...")
        
        # 1. Content Ingestion
        sources = Ingestion.ingest_sources(urls=urls, folder_path=folder_path)
        if not sources:
            print("No sources found to process. Please check your URLs or data folder.")
            return

        print(f"Successfully ingested {len(sources)} sources.")

        # 2. Claim Extraction
        source_claims_list: List[SourceClaims] = []
        all_claims_for_grouping = []
        
        for source_data in sources:
            print(f"Extracting claims from {source_data['title']}...")
            source_claims = self.extraction.extract_claims(source_data)
            source_claims_list.append(source_claims)
            
            for c in source_claims.claims:
                all_claims_for_grouping.append({
                    "claim": c.claim,
                    "evidence": c.evidence,
                    "source": source_claims.source,
                    "title": source_claims.title
                })

        # 3. Deduplication & Grouping
        print(f"Grouping and deduplicating {len(all_claims_for_grouping)} claims...")
        groups: List[ClaimGroup] = self.grouping.group_claims(all_claims_for_grouping)

        # 4. Structured Digest Generation
        print(f"Generating output in {output_dir}...")
        digest_path = Generation.generate_digest(groups, output_dir=output_dir)
        json_path = Generation.generate_sources_json(source_claims_list, output_dir=output_dir)
        
        print(f"Research digest generated at {digest_path}")
        print(f"Sources JSON generated at {json_path}")
        return digest_path, json_path

if __name__ == "__main__":
    # Example usage for "Natural Disaster" topic
    default_urls = [
        "https://en.wikipedia.org/wiki/Natural_disaster",
        "https://www.britannica.com/science/natural-disaster",
        "https://outforia.com/types-of-natural-disasters/"
    ]
    
    # Check for local data folder
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    agent = ResearchDigestAgent()
    agent.run(urls=default_urls, folder_path=data_folder)
