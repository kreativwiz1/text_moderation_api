import os
import re
import uuid
from flask import Flask, request, jsonify
from openai import OpenAI, OpenAIError
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OpenAI API Key is missing. Set the OPENAI_API_KEY environment variable.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Set up SQLAlchemy
engine = create_engine('sqlite:///feedback.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    request_id = Column(String(36), unique=True, nullable=False)
    original_text = Column(Text, nullable=False)
    moderation_result = Column(Text, nullable=False)
    user_feedback = Column(Boolean, nullable=True)
    user_comment = Column(Text, nullable=True)

Base.metadata.create_all(engine)

def check_additional_categories(text):
    text = text.lower()
    additional_categories = {
        "profanity": bool(re.search(r'(fuck|shit|ass)', text)),
        "discrimination": bool(re.search(r'(racist|sexist|homophobic)', text)),
        "bullying": bool(re.search(r'(loser|stupid|idiot)', text)),
        "spam": bool(re.search(r'(buy now|click here|limited offer)', text))
    }
    return additional_categories

@app.route('/')
def home():
    return "Content Moderation API is running!"

@app.route('/moderate', methods=['POST'])
def moderate_content():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data['text']
    request_id = str(uuid.uuid4())

    try:
        # Call OpenAI's moderation API
        response = openai_client.moderations.create(input=text)

        # Check if the content is flagged
        result = response.results[0]
        is_appropriate = not result.flagged

        # Convert categories and category_scores to dictionaries
        categories_dict = vars(result.categories)
        category_scores_dict = vars(result.category_scores)

        # Create a more detailed response
        detailed_response = {
            "request_id": request_id,
            "is_appropriate": is_appropriate,
            "categories": {
                "sexual": categories_dict.get("sexual"),
                "hate": categories_dict.get("hate"),
                "violence": categories_dict.get("violence"),
                "self_harm": categories_dict.get("self_harm"),
                "sexual_minors": categories_dict.get("sexual/minors"),
                "hate_threatening": categories_dict.get("hate/threatening"),
                "violence_graphic": categories_dict.get("violence/graphic")
            },
            "category_scores": {
                "sexual": category_scores_dict.get("sexual"),
                "hate": category_scores_dict.get("hate"),
                "violence": category_scores_dict.get("violence"),
                "self_harm": category_scores_dict.get("self_harm"),
                "sexual_minors": category_scores_dict.get("sexual/minors"),
                "hate_threatening": category_scores_dict.get("hate/threatening"),
                "violence_graphic": category_scores_dict.get("violence/graphic")
            }
        }

        # Add additional categories
        additional_categories = check_additional_categories(text)
        detailed_response["categories"].update(additional_categories)

        # Store the moderation result in the database
        with Session() as session:
            feedback = Feedback(
                request_id=request_id,
                original_text=text,
                moderation_result=str(detailed_response)
            )
            session.add(feedback)
            session.commit()

        return jsonify(detailed_response)

    except OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if not data or 'request_id' not in data or 'user_feedback' not in data:
        return jsonify({"error": "Missing 'request_id' or 'user_feedback' in request body"}), 400

    request_id = data['request_id']
    user_feedback = data['user_feedback']
    user_comment = data.get('user_comment', '')

    # Validate user_feedback is a boolean
    if not isinstance(user_feedback, bool):
        return jsonify({"error": "'user_feedback' must be a boolean value"}), 400

    with Session() as session:
        feedback = session.query(Feedback).filter_by(request_id=request_id).first()

        if feedback:
            feedback.user_feedback = user_feedback
            feedback.user_comment = user_comment
            session.commit()
            return jsonify({"message": "Feedback submitted successfully"}), 200
        else:
            return jsonify({"error": "Invalid request_id"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
