import requests

from utils.config import USAJOBS_API_KEY, USAJOBS_EMAIL


def fetch_jobs(keyword="software developer", location="", results_per_page=5):
    url = "https://data.usajobs.gov/api/search"
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_EMAIL or "",
        "Authorization-Key": USAJOBS_API_KEY or ""
    }
    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results_per_page
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    items = data.get("SearchResult", {}).get("SearchResultItems", [])
    jobs = []

    for item in items:
        descriptor = item.get("MatchedObjectDescriptor", {})
        organization = descriptor.get("OrganizationName", "")
        locations = descriptor.get("PositionLocation", [])
        location_names = [location.get("LocationName", "") for location in locations]

        jobs.append({
            "title": descriptor.get("PositionTitle", "Untitled Job"),
            "agency": organization,
            "location": ", ".join(location_names),
            "url": descriptor.get("PositionURI", ""),
            "description": descriptor.get("UserArea", {}).get("Details", {}).get("JobSummary", ""),
            "qualifications": descriptor.get("QualificationSummary", "")
        })

    return jobs
