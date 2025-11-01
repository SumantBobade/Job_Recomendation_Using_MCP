import os
from dotenv import load_dotenv  # For loading environment variables
from apify_client import ApifyClient

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))

def fetch_linkedin_jobs(search_quert, location = "india", rows = 60):
    run_input = {
        "title": search_quert,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        }
    }
    # Run the Actor and wait for it to finish
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

def fetch_naukri_jobs(search_quert, location = "india", rows = 60):
    run_input = {
        "keyword": search_quert,
        "maxJobs": rows,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    # Run the Actor and wait for it to finish
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs