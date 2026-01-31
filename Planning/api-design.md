# RESTful API Design – Subscribed Articles

## Purpose
The REST API allows authenticated third-party clients to retrieve approved articles from publishers and journalists that a reader has subscribed to.

## Authentication
API access requires authentication using the same user credentials as the main application.

## Base URL
/api/

## Endpoint

### GET /api/articles/
Returns all approved articles from subscribed publishers and journalists.

- Method: GET
- Permissions: Authenticated users only
- Access Level: Read-only

## Business Rules
- Only approved articles are returned
- Articles are filtered based on user subscriptions
- Users cannot retrieve articles from unsubscribed sources

## Response Format
The API supports:
- JSON (default)
- XML (via custom renderer)

## Example Response
```json
[
  {
    "id": 1,
    "title": "Breaking News",
    "content": "Article content",
    "approved": true
  }
]
