from typing import List
from promptflow import tool
from promptflow.connections import CognitiveSearchConnection
from azure.search.documents import SearchClient
#from azure.search.documents.models import Vector
from azure.core.credentials import AzureKeyCredential

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def question_embedding(question: str, embedding: List[float], search: CognitiveSearchConnection):
    search_client = SearchClient(endpoint=search.api_base, 
                                 index_name="your-search-index",
                                 credential=AzureKeyCredential(search.api_key))
    results = search_client.search(
        search_text=question,
        top=10,
        search_fields=["content"],
 #       vector=Vector(value=embedding, k=2, fields=embedding)
    )
    return [{"id": doc["id"], "title": doc["title"], "content": doc["content"], "url": doc["url"]}
            for doc in results]
