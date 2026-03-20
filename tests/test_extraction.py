# Extraction and grouping tests
import pytest
from unittest.mock import MagicMock, patch
from src.extraction import Extraction
from src.grouping import Grouping, ClaimGroup
import json

def test_deduplication_of_duplicate_claims():
    """Test that duplicate claims are grouped correctly."""
    all_claims = [
        {"claim": "AI is being regulated.", "source": "Source A", "evidence": "AI is regulated."},
        {"claim": "AI is being regulated.", "source": "Source B", "evidence": "Regulation of AI is happening."}
    ]
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "groups": [
            {
                "theme": "AI Regulation",
                "claims": [
                    {"claim": "AI is being regulated.", "source": "Source A", "evidence": "AI is regulated."},
                    {"claim": "AI is being regulated.", "source": "Source B", "evidence": "Regulation of AI is happening."}
                ],
                "sources": ["Source A", "Source B"]
            }
        ]
    })
    
    with patch('litellm.completion', return_value=mock_response):
        grouping = Grouping(api_key="fake-key")
        groups = grouping.group_claims(all_claims)
        
        assert len(groups) == 1
        assert groups[0].theme == "AI Regulation"
        assert len(groups[0].claims) == 2
        assert set(groups[0].sources) == {"Source A", "Source B"}

def test_preservation_of_conflicting_claims():
    """Test that conflicting claims are preserved."""
    all_claims = [
        {"claim": "AI is safe.", "source": "Source A", "evidence": "AI is safe."},
        {"claim": "AI is dangerous.", "source": "Source B", "evidence": "AI is dangerous."}
    ]
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "groups": [
            {
                "theme": "AI Safety",
                "claims": [
                    {"claim": "AI is safe.", "source": "Source A", "evidence": "AI is safe."},
                    {"claim": "AI is dangerous.", "source": "Source B", "evidence": "AI is dangerous."}
                ],
                "sources": ["Source A", "Source B"]
            }
        ]
    })
    
    with patch('litellm.completion', return_value=mock_response):
        grouping = Grouping(api_key="fake-key")
        groups = grouping.group_claims(all_claims)
        
        assert len(groups) == 1
        assert groups[0].theme == "AI Safety"
        # Both claims should be present in the group
        claims_text = [c['claim'] for c in groups[0].claims]
        assert "AI is safe." in claims_text
        assert "AI is dangerous." in claims_text
