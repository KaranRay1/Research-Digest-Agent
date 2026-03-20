# Research Digest Agent

An autonomous research digest agent that ingests multiple sources, extracts key information, removes redundancy, and produces a structured, evidence-backed brief.

## How the Agent Processes Sources Step-by-Step

1.  **Ingestion**: The agent accepts a list of URLs or a folder of local text/HTML files. It uses `requests` and `BeautifulSoup4` to fetch and clean the text, removing scripts and styles.
2.  **Claim Extraction**: Using an LLM (via `litellm`), the agent extracts key claims and insights from each source. For each claim, it identifies a supporting quote or snippet from the source text.
3.  **Deduplication & Grouping**: The agent takes all extracted claims and uses an LLM to group them into themes. This process identifies overlapping claims, groups similar insights, and tracks which sources support each theme.
4.  **Digest Generation**: The agent produces two files:
    *   `digest.md`: A structured markdown report with sectioned themes and source references.
    *   `sources.json`: A structured JSON file containing all claims and evidence per source.

## How Claims are Grounded

Claims are grounded by requiring the extraction step to identify a direct "supporting quote/snippet" from the source text for every claim. This ensures that every insight presented in the final digest is directly linked to the original source.

## How Deduplication/Grouping Works

The deduplication and grouping process uses an LLM to analyze the entire pool of extracted claims. The LLM is prompted to:
- Identify overlapping or repeated claims.
- Group similar claims under a common descriptive "theme".
- Track which sources support each group.
- Preserve conflicting viewpoints with correct attribution.

## Limitation

The current implementation relies on a fixed context window for the LLM during claim extraction and grouping. Very large sources or a very high number of claims may exceed this limit, leading to truncated data or incomplete grouping.

## Improvement with More Time

A significant improvement would be implementing a vector database (like Chroma or FAISS) for initial similarity-based clustering before LLM-based grouping. This would allow the agent to handle much larger datasets more efficiently and provide a more robust deduplication process.

## Installation Requirements

To install and run the Research Digest Agent, you need:
- **Python 3.8+**
- The following Python libraries:
  - `requests`: For fetching web content.
  - `beautifulsoup4`: For parsing and cleaning HTML.
  - `litellm`: For interfacing with LLMs (Gemini, OpenAI, etc.).
  - `pydantic`: For data validation.
  - `python-dotenv`: For managing environment variables.
  - `pytest` & `responses`: For running tests.

## Run Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Environment Variables**:
    Create a file named `.env` in the project root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
    *Note: Do not paste the actual key directly into the code. The agent is designed to securely read it from this `.env` file.*

3.  **Run the Agent**:
    ```bash
    python src/agent.py
    ```
    The agent will process the default AI Regulation sources and output the results to the `output/` directory.

4.  **Local Files**:
    Place HTML or text files in the `data/` directory to include them in the research.

## Tests

Run the tests using pytest:
```bash
pytest tests/
```
The tests cover:
- Empty/unreachable source handling.
- Deduplication of duplicate content.
- Preservation of conflicting claims.
