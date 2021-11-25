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
    values: list


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


def insert_into(table, values):
    if table not in map(lambda x: x.name, db.tables):
        raise Exception("Table doesn't exist")

    table = next(filter(lambda x: x.name == table, db.tables))

    table.rows.append(Row(values))


def select(tableName, toSelect, where=None):
    # TODO make this. return only the indexes defined in the list of selectors using the definition in the table
    def get_from_row_with_selectors(row, selectors, table):

    if tableName not in map(lambda x: x.name, db.tables):
        raise Exception("Table doesn't exist")

    table = next(filter(lambda x: x.name == tableName, db.tables))

    if where is None:
        if len(toSelect) == 1 and toSelect[0] == "*":
            return [row.values for row in table.rows]

        output = []
        for row in table.rows:
            output.append(get_from_row_with_selectors(row, toSelect, table))

        return output
