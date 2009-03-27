# AutORM, fork of Autumn, a Python ORM

This is a derivative project of Autumn [Autumn](http://github.com/JaredKuolt/autumn/tree).  It adds a few features: Fields (e.g. type converters, validation), a few Django conventions (e.g. Model.objects.*), table creation from models, and ... TBD. Why Yet-[Yet Another Python ORM](http://superjared.com/entry/yet-another-python-orm/)? For the same reasons Jared Kuolt built the original Autumn ORM, but my use cases and preferences are slightly different.  I built my own system for use with sqlite that had much in common with Autumn, and a number of other features I needed, but ran into threading issues, so I merged the two projects as AutORM. Many thanks to him for the seed.

## What is Autumn (and by extension, AutORM)? 

Autumn exists as a super-lightweight Object-relational mapper (ORM) for Python. 
It’s an alternative to [SQLObject](http://www.sqlobject.org/), 
[SQLAlchemy](http://www.sqlalchemy.org/), [Storm](https://storm.canonical.com/),
etc. Perhaps the biggest difference is the ability for automatic population of fields as 
attributes (see the example below).

It is released under the MIT License (see LICENSE file for details).

This project is still under development.

## SQLite Example

Using these tables

    DROP TABLE IF EXISTS author;
    CREATE TABLE author (
        id INTEGER PRIMARY KEY autoincrement,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        bio TEXT,
        some_json_data TEXT
    );
    DROP TABLE IF EXISTS books;
    CREATE TABLE books (
        id INTEGER PRIMARY KEY autoincrement,
        title VARCHAR(255),
        other_json_data TEXT,
        author_id INT(11),
        FOREIGN KEY (author_id) REFERENCES author(id)
    );

We setup our objects like so:

    from autorm.db.connection import db
    from autorm.model import Model
    from autorm.fields import *
    from autorm.db.query import Query
    from autorm.db.relations import ForeignKey, OneToMany
    import datetime

    db.connect('sqlite', ':memory:')

    class Author(Model):
        books = OneToMany('Book')

        class Meta:
            defaults = {'bio': 'No bio available'}
            validations = {'first_name': lambda self, v: len(v) > 1}
            # do not inspect the database, use these fields to define the columns
            fields = [IdField('id'), TextField('first_name', length=40, notnull=True), 
                      TextField('first_name', length=40, notnull=True), 
                      TextField('last_name', notnull=True), TextField('bio'),
                      JSONField('some_json_data')]

    # Because we specify the fields, the table doesn't need to exist beforehand
    Author.objects.create_table()


    # for the following model, we rely on the db to define the fields
    Query.raw_sqlscript("""DROP TABLE IF EXISTS books;
    CREATE TABLE books (
        id INTEGER PRIMARY KEY autoincrement,
        title VARCHAR(255),
        other_json_data TEXT,
        author_id INT(11),
        FOREIGN KEY (author_id) REFERENCES author(id)
    );""")

    class Book(Model):
        author = ForeignKey(Author)

        class Meta:
            table = 'books'
            # fields = ...
            # don't define fields, at class creation, autorm inspect the database to get 
            # field names (so you need to have an open connection).   
            
            # Introspection uses the default field type (no-op) for all the columns, 
            # but you can override specific ones.
            field_overrides = [JSONField('other_json_data')]

Now we can create, retrieve, update and delete entries in our database.
Creation

    james = Author(first_name='James', last_name='Joyce', some_json_data={'key':['value',1,2,None]})
    james.save()

    u = Book(title='Ulysses', author_id=james.id)
    u.save()

### Retrieval

    a = Author.get(1)
    a.first_name # James
    a.books      # Returns list of author's books

    # Returns a list, using LIMIT based on slice
    a = Author.get()[:10]   # LIMIT 0, 10
    a = Author.get()[20:30] # LIMIT 20, 10

### Updating

    a = Author.get(1)
    a.bio = 'What a crazy guy! Hard to read but... wow!'
    a.save()

### Deleting

    a.delete()
