This is an End to End chatbot which will answer user's queries based on the customized business data.

Modules:
1. Document Processing - In this step business data will be loaded. It provides the user option to upload data from various formats:
    .Doc
    .pdf
    .txt
    .csv
    website

2. Data loaded in step 1 will be split into chunks. This is required as LLMs has a token limit.

3. Chunks will then be embedded into the vector database.

Technology Stack:
Langchain
Open AI API
Chroma DB - for vector embedding

