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
    "title": "Interstellar",
    "actors": ["Rossi"],
    "release_year": 2014,
    "genre": "Sci-Fi",
    "rating": 8.6,
    "description": "A journey beyond space and time.",
    "image_path": "/images/interstellar.jpg"
}
```
#### Add a Actor
```
{
    "name": "Gianmaria",
    "surname": "Rossi
    ",
    "date_of_birth": "1969-11-04"
}
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.