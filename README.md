# ChillStream content service
ASEE Project, content service part.
This project provides an API for managing contents and their associated actors.
The service is built using Python, Flask, and MongoDB, leveraging a modular architecture for handling
routes and validations.

## Features
### Content Management
- Create a Content: Add new film.
- Retrieve Contents: Fetch all contents or a specific content by ID.
- Update Content: Modify content details.
- Delete Content: Remove a content.

## Actor Management
- Add Actor: Add a new actor.
- Retrieve Actors: Fetch all actors and fins a specific actor by ID.
- Update Actor: Modify the details of an actor.
- Delete Actor: Remove an actor and update the content's actor list.

## API Endpoints
### Contents
``` GET /films```: Retrieve all contents.

```POST /films```: Create a new content.

```GET /films/<filmId>```: Retrieve details of a specific content.

```PUT /films/<filmId>```: Update details of a specific content.

```DELETE /films/<filmId>```: Delete a content.

### Actors
```GET /actors```: Retrieve all actors.

```POST /actors```: Add a new actor.

```GET /actors/<actorsId>```: Retrieve a specific actor.

```PUT /actors/<actorId>```: Update a specific actor.

```DELETE /actors/<actorId>```: Delete an actor.

## Usage
### Example Requests

#### Create a Content
```
{
 "filmId": 5,
  "title": "La banda",
  "actors": "1",
  "release_year": 2020,
  "genre": "Action",
  "rating": 10,
  "description": "The film tells the story of an alienated... ",
  "image_path": "/default_film_image.png"
}
```
#### Add a Actor
```
{
  "actorId": 1,
  "name": "Bella ",
  "surname": "Rella",
  "date_of_birth": "05-03-2000",
  "films": ""
}
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.