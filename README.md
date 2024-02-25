# Project APIs Overview

## Table of Contents

1. [Problem Search API](#1-problem-search-api)
   - [Overview](#overview)
   - [API Endpoints](#api-endpoints)
     - [GET /api/problem-search/](#get-apiproblem-search)
       - [Parameters](#parameters)
       - [Example Request](#example-request)
       - [Example Response](#example-response)
2. [User Scores & History API](#2-user-scores--history-api)
   - [Overview](#overview-1)
   - [API Endpoints](#api-endpoints-1)
     - [1. User Scores](#1-user-scores)
       - [GET /user/scores/](#get-userscores)
       - [POST /user/scores/](#post-userscores)
       - [PATCH /user/scores/](#patch-userscores)
     - [2. User History](#2-user-history)
       - [GET /user/history/](#get-userhistory)
       - [PATCH /user/history/](#patch-userhistory)
     - [3. User Stats](#3-user-stats)
       - [GET /user/stats/](#get-userstats)
   - [How to Use](#how-to-use)
     - [Setting Up Locally](#setting-up-locally)
     - [Running the Django API](#running-the-django-api)

## 1. Problem Search API

### Overview

The Problem Search API facilitates problem retrieval based on specific criteria such as category and difficulty score.

### API Endpoints

#### `GET /api/problem-search/`

Fetch problems based on specified parameters.

##### Parameters

- `count` (integer): Number of problems to fetch.
- `category` (string): Problem category.
- `score` (integer): Difficulty score.
- `new` (integer): 0 or 1 to indicate a new user.

##### Example Request

```http
GET /api/problem-search/?count=1&category=Sample&score=3
```

##### Example Response

```json
{
  "id": 1,
  "problem": "Sample Problem",
  "rationale": "Sample Rationale",
  // ... other fields
}
```

## 2. User Scores & History API

### Overview

The User Scores & History API manages user scores and history, providing endpoints for retrieving, creating, and updating user scores and history based on specific categories.

### API Endpoints

#### 1. User Scores

##### `GET /user/scores/`

Retrieve user scores based on the specified user ID and optional category parameter.

###### Parameters

- `user_id` (string): The unique identifier for the user.
- `category` (string, optional): Specific category for which you want to retrieve scores.

###### Example Request

```http
GET /user/scores/?user_id=123&category=gain
```

###### Example Response

```json
{
  "gain": 85.5,
  "general": 90.0,
  "probability": 78.2,
  // ... other category scores
}
```

##### `POST /user/scores/`

Create new user scores by providing data in the request body.

###### Request Body

```json
{
  "user_id": "123",
  "gain": 85.5,
  "general": 90.0,
  "probability": 78.2,
  // ... other category scores
}
```

###### Example Response

```json
{
  "user_id": "123",
  "gain": 85.5,
  "general": 90.0,
  "probability": 78.2,
  // ... other category scores
}
```

##### `PATCH /user/scores/`

Update a specific category score for a user by providing the necessary parameters.

###### Request Body

```json
{
  "user_id": "123",
  "category": "gain",
  "new_score": 12,
}
```

###### Example Response

```json
{
  "message": "Category gain updated successfully."
}
```

#### 2. User History

##### `GET /user/history/`

Retrieve user history based on the specified user ID and optional category parameter.

###### Parameters

- `user_id` (string): The unique identifier for the user.
- `category` (string, optional): Specific category for which you want to retrieve history.

###### Example Request

```http
GET /user/history/?user_id=123&category=gain
```

###### Example Response

```json
{
  "gain": 10,
  "general": 6,
  "probability": 78,
  // ... other category scores
}
```

##### `PATCH /user/history/`

Update a specific category history for a user by providing the necessary parameters.

###### Request Body

```json
{
  "user_id": "123",
  "category": "gain",
  "new_history": 12,
}
```

###### Example Response

```json
{
  "message": "Category gain updated successfully."
}
```

#### 3. User Stats

##### `GET /user/stats/`

Retrieve various statistics for a user based on the specified user ID and data type.

###### Parameters

- `user_id` (string): The unique identifier for the user.
- `type` (string): Type of statistics to retrieve (`score`, `history`, `favorites`, `recent`).

###### Example Request

```http
GET /user/stats/?user_id=123&type=score
```

###### Example Response

Returns statistics based on the specified type.

### How to Use

Integrate these API endpoints into your application to manage and track user scores dynamically. Retrieve existing scores, add new scores, and update category scores based on user interactions. Follow the steps outlined in each API section for a smooth integration process.

#### Setting Up Locally

Follow these steps to set up the Django API locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/naderite/SolutionChallengeBackend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SolutionChallengeBackend
   ```

3. Create a virtual environment if you don't already have one named "venv".

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### Running the API

Run the file `./start_env.bat` to start the servers.

Copy the Django API tunnel link (forwarded to localhost:8000) and paste it in the `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in the Django project `settings.py`.
