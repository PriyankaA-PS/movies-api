# Movie Listing & Collection API

A Django REST Framework application that provides JWT-based authentication, movie listing through a third-party API, and authenticated movie collection management.

The project also includes unit tests, Behaviour-Driven Development (BDD) tests using Behave, code coverage, retry handling for the external movie API, Docker support, and PostgreSQL.

---

## Features

- User registration with username and password
- JWT authentication
- Login and logout APIs
- Protected APIs using JWT authentication
- Movie listing from a third-party movie API
- Retry mechanism for flaky third-party movie API requests
- Authenticated movie collections
- Create, list, retrieve and update collections
- Store movie information associated with collections
- User-specific collection access
- Top 3 favourite genres across a user's collections
- Unit/API tests
- BDD/integration tests using Behave
- Code coverage using `coverage.py`
- Dockerized Django application
- PostgreSQL database support

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| Django | Web framework |
| Django REST Framework | REST API |
| Simple JWT | JWT authentication |
| PostgreSQL | Database |
| Requests | Third-party API communication |
| Behave | BDD/integration testing |
| Coverage.py | Test coverage |
| Docker | Containerization |
| Docker Compose | Multi-container development |
| Git | Version control |

---

## Project Structure

```text
moviesListing/
│
├── accounts/
│   ├── views.py
│   ├── serializers.py
│   └── ...
│
├── movies/
│   ├── views.py
│   ├── services/
│   │   └── movie_api.py
│   └── ...
│
├── movie_collections/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
│
├── features/
│   ├── environment.py
│   ├── authentication.feature
│   ├── movies.feature
│   ├── collections.feature
│   └── steps/
│       ├── authentication_steps.py
│       ├── movie_steps.py
│       └── collection_steps.py
│
├── moviesListing/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

# API Documentation

Base URL:

```text
http://localhost:9000
```

When running Django locally without Docker, the port may be:

```text
http://127.0.0.1:8000
```

---

## Authentication

All APIs except registration require authentication.

Send the JWT access token using:

```http
Authorization: Bearer <access_token>
```

---

## 1. Register

Creates a new user and returns an access token.

### Request

```http
POST /register/
Content-Type: application/json
```

### Payload

```json
{
    "username": "testuser",
    "password": "TestPassword123"
}
```

### Response

```json
{
    "access_token": "<access-token>"
}
```

Expected status:

```text
201 Created
```

---

## 2. Login

Authenticates an existing user and returns access and refresh tokens.

### Request

```http
POST /login/
Content-Type: application/json
```

### Payload

```json
{
    "username": "testuser",
    "password": "TestPassword123"
}
```

### Response

```json
{
    "access": "<access-token>",
    "refresh": "<refresh-token>"
}
```

Expected status:

```text
200 OK
```

---

## 3. Logout

Invalidates the refresh token for an authenticated user.

### Request

```http
POST /logout/
Authorization: Bearer <access-token>
Content-Type: application/json
```

### Payload

```json
{
    "refresh": "<refresh-token>"
}
```

### Response

```json
{
    "message": "Logout successful"
}
```

Expected status:

```text
200 OK
```

---

# Movie APIs

## 4. Get Movies

Returns movies from the configured third-party movie API.

The movie data is **not read from the application's database**.

### Request

```http
GET /movies/
Authorization: Bearer <access-token>
```

### Third-party API

The project currently uses:

```text
https://api.sampleapis.com/movies/action-adventure
```

The original assignment API was unavailable/flaky during development, so this public API was used as the movie source.

Example third-party response:

```json
{
    "id": 84,
    "title": "Raiders of the Lost Ark",
    "posterURL": "https://example.com/poster.jpg",
    "imdbId": "tt0082971"
}
```

### Response

The local `/movies/` endpoint returns the movie data received from the configured third-party service.

Expected status:

```text
200 OK
```

### Retry mechanism

The external movie API is accessed through a `requests.Session` with retry support.

Retries are configured for:

```text
500
502
503
504
```

Only GET requests are retried.

A timeout is also configured to prevent the application from waiting indefinitely for the external service.

---

# Collection APIs

Collections belong to the authenticated user.

A user cannot access another user's collection.

---

## 5. Create Collection

### Request

```http
POST /collection/
Authorization: Bearer <access-token>
Content-Type: application/json
```

### Payload

```json
{
    "title": "Action Movies",
    "description": "My action movie collection",
    "movies": [
        {
            "title": "Raiders of the Lost Ark",
            "description": "An archaeologist searches for the Ark.",
            "genres": "Action, Adventure",
            "uuid": "84"
        },
        {
            "title": "Test Movie",
            "description": "A test movie",
            "genres": "Action, Thriller",
            "uuid": "85"
        }
    ]
}
```

### Response

```json
{
    "collection_uuid": "eabf96d7-2a5c-49d1-9b18-ac171a69d157"
}
```

Expected status:

```text
201 Created
```

Movie information supplied during collection creation is stored in the database.

---

## 6. Get User Collections

Returns collections belonging to the authenticated user.

### Request

```http
GET /collection/
Authorization: Bearer <access-token>
```

### Response

```json
{
    "is_success": true,
    "data": {
        "collections": [
            {
                "title": "Action Movies",
                "uuid": "eabf96d7-2a5c-49d1-9b18-ac171a69d157",
                "description": "My action movie collection"
            }
        ],
        "favourite_genres": "Action, Adventure, Thriller"
    }
}
```

The response does not include the movies inside each collection.

The movies are available through the collection detail API.

---

## Favourite Genres

The application calculates the user's top 3 favourite genres based on movies across all of the user's collections.

For example, if the stored movies contain:

```text
Action
Action
Action
Adventure
Adventure
Thriller
```

the result is:

```text
Action, Adventure, Thriller
```

Only the authenticated user's collections are considered.

---

## 7. Get Collection Details

Returns a single collection and its movies.

### Request

```http
GET /collection/<collection_uuid>/
Authorization: Bearer <access-token>
```

### Response

```json
{
    "title": "Action Movies",
    "description": "My action movie collection",
    "movies": [
        {
            "title": "Raiders of the Lost Ark",
            "description": "An archaeologist searches for the Ark.",
            "genres": "Action, Adventure",
            "uuid": "84"
        },
        {
            "title": "Test Movie",
            "description": "A test movie",
            "genres": "Action, Thriller",
            "uuid": "85"
        }
    ]
}
```

Expected status:

```text
200 OK
```

If the collection does not exist, or belongs to another user:

```text
404 Not Found
```

This ownership check prevents users from accessing another user's collections.

---

## 8. Update Collection

Updates an existing collection.

### Request

```http
PUT /collection/<collection_uuid>/
Authorization: Bearer <access-token>
Content-Type: application/json
```

### Payload

```json
{
    "title": "Updated Action Movies",
    "description": "Updated description",
    "movies": [
        {
            "title": "Updated Movie",
            "description": "Updated movie description",
            "genres": "Action",
            "uuid": "90"
        }
    ]
}
```

The fields are optional according to the assignment requirements.

Expected status:

```text
200 OK
```

The update must only affect the authenticated user's collection.

---

## 9. Delete Collection

The collection CRUD flow also supports deletion.

### Request

```http
DELETE /collection/<collection_uuid>/
Authorization: Bearer <access-token>
```

Expected response:

```text
204 No Content
```

Deleting a collection also removes its associated movies through the configured database relationship.

---

# Database Models

## Collection

A collection belongs to a Django user.

Conceptually:

```text
User
 │
 └── Collection
       │
       ├── title
       ├── description
       ├── uuid
       ├── created_at
       └── updated_at
```

## CollectionMovie

Movies stored inside a collection are represented separately.

```text
Collection
 │
 └── CollectionMovie
       ├── title
       ├── description
       ├── uuid
       └── genres
```

The relationship uses:

```python
related_name="movies"
```

so movies can be accessed using:

```python
collection.movies.all()
```

The movie data stored in collections is a snapshot of the movie information submitted when the collection is created/updated.

---

# External Movie API

The application uses:

```text
https://api.sampleapis.com/movies/action-adventure
```

The service is isolated behind a movie API service class rather than calling the external API directly from the view.

Conceptually:

```text
GET /movies/
     │
     ▼
MovieAPIService
     │
     ▼
Third-party Movie API
     │
     ▼
Movie response
     │
     ▼
Django API response
```

This separation makes the external integration easier to test and maintain.

---

# Retry Strategy

The movie service uses `requests.Session`, `HTTPAdapter`, and `urllib3 Retry`.

The retry configuration handles transient server errors:

```text
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

A backoff factor is used between retry attempts.

The request also has a timeout to prevent indefinitely hanging requests.

---

# Authentication Flow

```text
                    POST /register/
                           │
                           ▼
                      Django User
                           │
                           ▼
                     Access Token
                           │
                           ▼
                  Authorization Header
                           │
                           ▼
                  Protected API endpoint
                           │
                           ▼
                    Authenticated User
```

For login:

```text
POST /login/
     │
     ├── access token
     └── refresh token
```

The access token is sent with protected API requests:

```http
Authorization: Bearer <access-token>
```

---

# Local Development

## Prerequisites

Install:

- Python 3.12+
- PostgreSQL
- pip
- Docker Desktop (optional)
- Git

---

## Create Virtual Environment

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

For PostgreSQL, configure:

```text
DB_NAME=movies_listing
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

The project should read these values through environment variables rather than hardcoding database credentials.

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Start Django

```bash
python manage.py runserver
```

The development API will normally be available at:

```text
http://127.0.0.1:8000
```

---

# Docker Setup

The project supports Docker Compose with:

- Django
- PostgreSQL

Example architecture:

```text
┌──────────────────────────────┐
│ Django container             │
│                              │
│ runserver 0.0.0.0:9000      │
└──────────────┬───────────────┘
               │
               │ PostgreSQL
               ▼
┌──────────────────────────────┐
│ PostgreSQL container         │
│                              │
│ db:5432                      │
└──────────────────────────────┘
```

The Dockerized API is exposed on:

```text
http://localhost:9000
```

---

## Build Docker Images

```bash
docker compose build
```

---

## Start Containers

```bash
docker compose up
```

---

## Run Migrations in Docker

```bash
docker compose exec web python manage.py migrate
```

---

## Create Django Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Stop Containers

```bash
docker compose down
```

---

## PostgreSQL Data

PostgreSQL data is stored in a Docker volume so that database data survives container recreation.

---

# Testing

The project uses two main levels of testing:

```text
Unit/API Tests
       +
BDD / Integration Tests
```

---

## Unit Tests

Run all Django tests:

```bash
python manage.py test
```

Run a specific application:

```bash
python manage.py test accounts
```

```bash
python manage.py test movies
```

```bash
python manage.py test movie_collections
```

---

# BDD / Integration Testing

Behave tests are written using Gherkin feature files.

Example:

```gherkin
Scenario: Authenticated user can create a collection
    Given I have registered as "bdd_collection_user" with password "TestPassword123"
    And I login as "bdd_collection_user" with password "TestPassword123"
    When I create a collection titled "Action Movies"
    Then the collection response status should be 201
    And the response should contain a collection UUID
```

The Behave tests use real HTTP requests through `requests`.

Therefore the Django server must be running.

### Terminal 1

```bash
python manage.py runserver
```

### Terminal 2

```bash
behave
```

This produces:

```text
Behave
   │
   │ HTTP request
   ▼
Django server
   │
   ├── Authentication
   ├── Views
   ├── Serializers
   ├── Database
   └── External API
```

---

## Run a Specific Feature

```bash
behave features/authentication.feature
```

```bash
behave features/movies.feature
```

```bash
behave features/collections.feature
```

---

## Run a Specific Scenario

```bash
behave features/collections.feature --name "User can view collection details"
```

---

# BDD Test Data Cleanup

BDD users are created using the `bdd_` prefix, for example:

```text
bdd_owner
bdd_attacker
bdd_collection_user
bdd_movie_user
```

After each scenario, the test environment removes users whose usernames start with:

```text
bdd_
```

Their collections are removed as well.

This avoids deleting existing local development data while preventing test data from accumulating.

---

# Code Coverage

Install coverage if necessary:

```bash
pip install coverage
```

Run the unit tests with coverage:

```bash
coverage run manage.py test
```

View the terminal report:

```bash
coverage report
```

Generate an HTML report:

```bash
coverage html
```

Open it on macOS:

```bash
open htmlcov/index.html
```

You can also enforce a minimum coverage threshold:

```bash
coverage report --fail-under=80
```

---

# Recommended Testing Flow

Run unit tests first:

```bash
python manage.py test
```

Then start Django:

```bash
python manage.py runserver
```

Then run BDD:

```bash
behave
```

Finally generate coverage:

```bash
coverage run manage.py test
coverage report
coverage html
```

---

# API Test Flow

A typical end-to-end application flow is:

```text
1. Register
       │
       ▼
2. Login
       │
       ▼
3. Receive JWT
       │
       ▼
4. GET /movies/
       │
       ▼
5. Select movies
       │
       ▼
6. POST /collection/
       │
       ▼
7. GET /collection/
       │
       ▼
8. GET /collection/<uuid>/
       │
       ▼
9. PUT /collection/<uuid>/
       │
       ▼
10. DELETE /collection/<uuid>/
```

---

# Security Considerations

- Protected APIs require JWT authentication.
- Collection queries are scoped to the authenticated user.
- Users cannot retrieve another user's collection.
- Passwords are handled through Django's authentication system rather than stored as plain text.
- Third-party credentials should be provided through environment variables.
- External API calls use timeouts.
- External API failures are handled through retry logic.
- Database credentials should be supplied through environment variables.

---

# Future Improvements

Potential improvements include:

- API schema/documentation using OpenAPI/Swagger
- Pagination/normalization of the replacement movie API to match the original assignment contract
- Redis caching for the third-party movie API
- Rate limiting
- Structured application logging
- CI/CD pipeline
- Docker health checks
- Separate test database for BDD
- PostgreSQL integration tests in CI
- More comprehensive negative/security test scenarios

---

## Status

The project currently demonstrates:

- REST API development with Django REST Framework
- JWT authentication
- Third-party API integration
- Retry handling
- CRUD-oriented collection management
- Relational data modeling
- Unit/API testing
- BDD/integration testing
- Code coverage
- Docker
- PostgreSQL

