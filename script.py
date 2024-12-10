import requests
import json
import csv

def fetch_bug_discussions(tags, page=1, page_size=100):
    """
    Fetches questions tagged with specific tags from Stack Overflow.
    
    Args:
    - tags: Semicolon-separated tags (e.g., 'c;bug').
    - page: Page number to fetch.
    - page_size: Number of questions per page.
    
    Returns:
    - JSON response with questions.
    """
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",          # Descending order
        "sort": "creation",       # Sort by creation date
        "tagged": tags,           # Tags filter
        "site": "stackoverflow",  # Target Stack Overflow
        "pagesize": page_size,    # Number of results per page
        "page": page              # Page number
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def save_to_csv(data, filename):
    """
    Converts JSON data to CSV and saves it to a file.
    
    Args:
    - data: JSON response containing Stack Overflow questions.
    - filename: Name of the CSV file to save.
    """
    if not data.get("items"):
        print("No items found in the data.")
        return

    # Extract relevant fields from JSON
    questions = data["items"]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Question ID", "Title", "Creation Date", "Link", "Tags", "Score"])
        
        # Write rows
        for question in questions:
            writer.writerow([
                question.get("question_id"),
                question.get("title"),
                question.get("creation_date"),
                question.get("link"),
                ", ".join(question.get("tags", [])),
                question.get("score")
            ])
    
    print(f"Data saved to {filename}!")

# Fetch questions tagged with 'c'
tags = "c"
data = fetch_bug_discussions(tags, page=1, page_size=50)

# Save data to CSV
if data:
    save_to_csv(data, "c_bug_discussions.csv")


