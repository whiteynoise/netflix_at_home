movie_test_base_row = {
    '_id': 'd7bfb1fb-3157-4beb-a58a-7a58daa01845',
    'id': 'd7bfb1fb-3157-4beb-a58a-7a58daa01845',
    'imdb_rating': 8.5,
    'genres': ['Action', 'Sci-Fi'],
    'title': 'The Star',
    'description': 'New World',
    'directors_names': ['Stan'],
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'directors': [
        {
            'id': 'dc12b8fc-3c82-4d31-ad8e-72b69f4e3f95',
            'name': 'Stan'
        }
    ],
    'actors': [
        {
            'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95',
            'name': 'Ann'
        },
        {
            'id': 'fb111f22-121e-44a7-b78f-b19191810fbf',
            'name': 'Bob'
        }
    ],
    'writers': [
        {
            'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5',
            'name': 'Ben'
        },
        {
            'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6',
            'name': 'Howard'
        }
    ]
}

persons_test_base_row = {
    '_id': 'a5232057-cf81-47ca-9e46-5ccf27300678',
    'id': 'a5232057-cf81-47ca-9e46-5ccf27300678',
    'name': 'Elizabeth Kaufman',
    'films': [
        {
            'id': '10a10e2a-66dd-4398-a3ba-a22c3bb40db3',
            'roles': ['actor', 'director']
        },
        {
            'id': '0c98a005-fe93-4334-842e-0c3b1e532983',
            'roles': ['writer', 'actor']
        }
    ]
}

genre_test_base_row = {
    '_id': '5a4d46b8-07ba-4d8f-b376-25ed30944094',
    'id': '5a4d46b8-07ba-4d8f-b376-25ed30944094',
    'name': 'Horror',
    'description': 'Truly scary things, trust me'
}

base_row_by_name = {
    'movies': movie_test_base_row,
    'persons': persons_test_base_row,
    'genres': genre_test_base_row
}
