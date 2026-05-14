import arxiv
import json

client = arxiv.Client()

def searchTool(topic, amount):
    print("Search tool called for", amount, "papers about", topic)
    search = arxiv.Search(
        query = topic,
        max_results = amount,
        sort_by = arxiv.SortCriterion.Relevance
    )

    print("results recieved!")

    resultsData = [] #Hold dictionaries of our result papers

    for result in client.results(search):
        paper = {
            "title": result.title,
            "publish_date": str(result.published),
            "pdf_url": result.pdf_url,
            "summary": result.summary
        }
        resultsData.append(paper)
    return json.dumps(resultsData, indent = 4)