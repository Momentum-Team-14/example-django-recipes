# Recipes API

## Routes that don't require authentication

### GET `api/recipes/public`

List all public recipes

### POST `api/auth/token/login`

```json
{
  "username": "donkey",
  "password": "waffles"
}
```

## Routes that require authentication

### GET `api/users`

**restricted to admin users only**

List all users

### GET `api/recipes`

List all your own recipes

### POST `api/recipes`

Create a new recipe

### POST `api/recipes/<int:pk>/copy`

Make a copy of an existing public recipe

### GET `api/recipes/<int:pk>`

Detail about one recipe with all its ingredients

### PUT `api/recipes/<int:pk>` **TODO: TEST THIS**

Update details about a specific recipe

### POST `api/recipes/<int:pk>/ingredients`

Add an ingredient for a recipe

### GET `api/mealplans/<int:month>/<int:date>/<int:year>`

List URLs for recipes on a given date's mealplan

### POST `api/mealplans/<int:month>/<int:date>/<int:year>`

Add a recipe to a mealplan for a given date

