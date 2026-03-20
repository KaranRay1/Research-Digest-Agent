# Generation module
import json
import os
from typing import List, Dict, Any

class Generation:
    @staticmethod
    def generate_digest(groups: List[Any], output_dir: str = "output") -> str:
        """Generate digest.md and digest.txt with sectioned themes and source references."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        content = "# Research Digest\n\n"
        content += "## Executive Summary\n"
        # Flatten and count unique sources
        unique_sources = set()
        for g in groups:
            for s in g.sources:
                unique_sources.add(s)
        content += f"This digest summarizes research from {len(unique_sources)} sources.\n\n"
        
        for group in groups:
            content += f"### {group.theme}\n"
            for claim_data in group.claims:
                content += f"- **Claim:** {claim_data['claim']}\n"
                content += f"  - *Evidence:* \"{claim_data['evidence']}\"\n"
                content += f"  - *Source:* {claim_data['source']}\n"
            content += "\n"
        
        # Save as Markdown
        digest_path_md = os.path.join(output_dir, "digest.md")
        with open(digest_path_md, "w", encoding="utf-8") as f:
            f.write(content)
            
        # Save as Plain Text (Notepad compatible)
        digest_path_txt = os.path.join(output_dir, "digest.txt")
        # Strip markdown symbols for plain text version
        txt_content = content.replace("# ", "").replace("## ", "").replace("### ", "").replace("**", "").replace("- ", "• ")
        with open(digest_path_txt, "w", encoding="utf-8") as f:
            f.write(txt_content)
        
        return digest_path_txt

    @staticmethod
    def generate_sources_json(source_claims_list: List[Any], output_dir: str = "output") -> str:
        """Generate sources.json with claims and evidence per source."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        data = []
        for sc in source_claims_list:
            data.append({
                "source": sc.source,
                "title": sc.title,
                "claims": [c.dict() for c in sc.claims]
            })
        
        json_path = os.path.join(output_dir, "sources.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        return json_path
