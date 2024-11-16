import requests
import json
import time

def test_feedback():
    base_url = "http://localhost:5000"
    headers = {"Content-Type": "application/json"}

    # Test the /moderate endpoint
    moderate_url = f"{base_url}/moderate"
    text_to_moderate = "This is a test message for feedback."
    moderate_data = {"text": text_to_moderate}

    try:
        response = requests.post(moderate_url, data=json.dumps(moderate_data), headers=headers)
        response.raise_for_status()
        result = response.json()
        
        print("Response from /moderate endpoint:")
        print(json.dumps(result, indent=2))
        
        # Check if the response contains the expected fields
        expected_fields = ["request_id", "is_appropriate", "categories", "category_scores"]
        all_fields_present = all(field in result for field in expected_fields)
        
        if all_fields_present:
            print("All expected fields are present in the /moderate response.")
        else:
            print("Some expected fields are missing from the /moderate response.")
        
        # Test the /feedback endpoint
        feedback_url = f"{base_url}/feedback"
        request_id = result["request_id"]
        feedback_data = {
            "request_id": request_id,
            "user_feedback": True,
            "user_comment": "This message is appropriate."
        }
        
        time.sleep(1)  # Wait for a second to ensure the database transaction is complete
        
        feedback_response = requests.post(feedback_url, data=json.dumps(feedback_data), headers=headers)
        feedback_response.raise_for_status()
        feedback_result = feedback_response.json()
        
        print("\nResponse from /feedback endpoint:")
        print(json.dumps(feedback_result, indent=2))
        
        if "message" in feedback_result and feedback_result["message"] == "Feedback submitted successfully":
            print("Feedback submitted successfully.")
        else:
            print("Error submitting feedback.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while testing the endpoints: {e}")

if __name__ == "__main__":
    test_feedback()
