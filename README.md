# Content Moderation API 🛡️

A sophisticated Flask-based content moderation service that combines OpenAI's moderation capabilities with custom category detection and user feedback collection. This service provides real-time content analysis for identifying inappropriate content across multiple categories.

## ✨ Features

- **Content Analysis**
  - Real-time moderation using OpenAI
  - Custom category detection
    - Profanity
    - Discrimination
    - Bullying
    - Spam
  - Confidence scoring
  - Result persistence

- **Feedback System**
  - User feedback collection
  - Comment support
  - Historical tracking

- **API Features**
  - RESTful endpoints
  - CORS support
  - Comprehensive error handling
  - Request tracking via UUIDs

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key
- Poetry for dependency management

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/content-moderation-api.git
cd content-moderation-api
```

2. Install dependencies:
```bash
poetry install
```

3. Configure environment:
```bash
export OPENAI_API_KEY='your-api-key'
```

## 📡 API Reference

### Moderate Content

Analyzes text content for inappropriate material across multiple categories.

#### Endpoint
```
POST /moderate
Content-Type: application/json
```

#### Request
```json
{
  "text": "Content to moderate"
}
```

#### Response
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_appropriate": true,
  "categories": {
    "sexual": false,
    "hate": false,
    "violence": false,
    "profanity": false,
    "discrimination": false,
    "bullying": false,
    "spam": false
  },
  "category_scores": {
    "sexual": 0.001,
    "hate": 0.002,
    "violence": 0.001,
    "profanity": 0.003,
    "discrimination": 0.001,
    "bullying": 0.002,
    "spam": 0.001
  }
}
```

### Submit Feedback

Provides feedback on moderation results for system improvement.

#### Endpoint
```
POST /feedback
Content-Type: application/json
```

#### Request
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_feedback": true,
  "user_comment": "Accurate detection of profanity"
}
```

## 💾 Database Schema

```sql
CREATE TABLE feedback (
  id INTEGER PRIMARY KEY,
  request_id VARCHAR(36) UNIQUE NOT NULL,
  original_text TEXT NOT NULL,
  moderation_result TEXT NOT NULL,
  user_feedback BOOLEAN,
  user_comment TEXT
);
```

## 📁 Project Structure

```
content-moderation-api/
├── app.py              # Core application and API endpoints
├── test_moderate.py    # Moderation endpoint tests
├── test_feedback.py    # Feedback system tests
├── pyproject.toml      # Project dependencies
├── README.md          # This file
└── .env.example       # Environment variable template
```

## 🧪 Testing

Run the test suites:
```bash
# Run all tests
poetry run pytest

# Run specific test files
python test_moderate.py
python test_feedback.py
```

### Example Test Cases
```python
def test_moderation_endpoint():
    response = client.post('/moderate', 
                         json={'text': 'Test content'})
    assert response.status_code == 200
    assert 'request_id' in response.json

def test_feedback_submission():
    response = client.post('/feedback',
                         json={'request_id': 'test-uuid',
                              'user_feedback': True})
    assert response.status_code == 200
```

## 🔍 Error Handling

| Status Code | Description | Example |
|-------------|-------------|----------|
| 400 | Bad Request | Missing text parameter |
| 404 | Not Found | Invalid request_id |
| 500 | Server Error | OpenAI API failure |

Error Response Format:
```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "status": 400
}
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Cloud Run)
The service is configured for Cloud Run deployment via `.replit` configuration:
```yaml
run: gunicorn app:app --bind 0.0.0.0:$PORT
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|-----------|
| OPENAI_API_KEY | OpenAI API key | Yes |
| FLASK_ENV | Development/Production mode | No |
| DATABASE_URL | SQLite database path | No |

## 📊 Performance Considerations

- **Rate Limiting**
  - OpenAI API limits apply
  - Implement client-side rate limiting

- **Database**
  - Regular cleanup of old feedback
  - Index on request_id column

## 🛡️ Security

- Input sanitization
- Request size limits
- API key protection
- CORS configuration
- SQL injection prevention

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📮 Support

For support or feature requests:
- Open an issue in the GitHub repository
- Contact the maintainers

## 📚 Additional Resources

- [OpenAI Moderation API Documentation](https://platform.openai.com/docs/guides/moderation)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)