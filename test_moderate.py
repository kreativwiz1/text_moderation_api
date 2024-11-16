import requests
import json

def test_moderate_endpoint():
    url = "http://localhost:5000/moderate"
    headers = {"Content-Type": "application/json"}

    test_cases = [
        {"text": "This is a test message.", "expected_categories": []},
        {"text": "This is a fucking violent message.", "expected_categories": ["profanity", "violence"]},
        {"text": "You're such a stupid loser!", "expected_categories": ["bullying"]},
        {"text": "That's so racist and sexist.", "expected_categories": ["discrimination", "hate"]},
        {"text": "Buy now! Limited offer! Click here!", "expected_categories": ["spam"]},
    ]

    for case in test_cases:
        try:
            response = requests.post(url, data=json.dumps({"text": case["text"]}), headers=headers)
            response.raise_for_status()
            result = response.json()
            
            print(f"\nTest case: {case['text']}")
            print("Response from /moderate endpoint:")
            print(json.dumps(result, indent=2))
            
            # Check if the response contains the expected fields
            expected_fields = ["is_appropriate", "categories", "category_scores"]
            all_fields_present = all(field in result for field in expected_fields)
            
            if all_fields_present:
                print("All expected fields are present in the response.")
            else:
                print("Some expected fields are missing from the response.")
            
            # Check if the expected categories are flagged
            flagged_categories = [cat for cat, flag in result["categories"].items() if flag]
            print("Flagged categories:", flagged_categories)
            
            missing_categories = set(case["expected_categories"]) - set(flagged_categories)
            unexpected_categories = set(flagged_categories) - set(case["expected_categories"])
            
            if not missing_categories and not unexpected_categories:
                print("All expected categories were correctly flagged.")
            else:
                if missing_categories:
                    print(f"Missing expected categories: {missing_categories}")
                if unexpected_categories:
                    print(f"Unexpected flagged categories: {unexpected_categories}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while testing the /moderate endpoint: {e}")

if __name__ == "__main__":
    test_moderate_endpoint()
