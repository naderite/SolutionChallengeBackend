# Problem Search API

## Overview

This API provides endpoints to search for problems based on specific criteria, such as category and difficulty score.

## API Endpoints

### `GET /api/problem-search/`

Fetch problems based on specified parameters.

#### Parameters

- `count` (integer): Number of problems to fetch.
- `category` (string): Problem category.
- `score` (integer): Difficulty score.

#### Example Request

```http
GET /api/problem-search/?count=1&category=Sample&score=3
```

#### Example Response

```json
{
  "id": 1,
  "problem": "Sample Problem",
  "rationale": "Sample Rationale",
  // ... other fields
}
```

## Usage

To get started, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-project
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure Django to accept requests from your Flutter app:

Update the ALLOWED_HOSTS setting in your Django project's settings.py file to include the IP address or domain of your Flutter app. For example:

   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-flutter-app-ip-or-domain']
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```
