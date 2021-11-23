from dataclasses import dataclass


@dataclass
class Database():
    tables: list


@dataclass
class Table():
    name: str
    rows: list
    definition: list


# inefficient but the goal of this db was never to be efficient
@dataclass
class Row():
    type: str
    label: str
    value: str


db = Database([])


def create_table(name, fields):
    allowed_types = ["string"]
    definition = []

    if name in db.tables:
        raise Exception("Table already exists")

    for field in fields:
        if field["type"] not in allowed_types:
            raise Exception("Invalid field type")

        definition.append(field)

    db.tables.append(Table(name, [], definition))

    print(str(db))


def drop_table(name):
    if name == "*":
        db.tables = []
        return

    if name not in map(lambda x: x.name, db.tables):
        raise Exception("Table doesn't exist")

    db.tables = [table for table in db.tables if table.name != name]


def get_tables():
    return db.tables
