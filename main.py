import parse
from parse import TokenType
import backend


def create_table(result):
    if result[1].type != TokenType.LITERAL and result[1].type != TokenType.STRING:
        raise Exception("Invalid table name")

    table_name = result[1].text

    if result[2].type != TokenType.SYMBOL or result[2].text != "(":
        raise Exception("Invalid table definition")

    i = 2

    fields = []
    current = []
    increment = 1

    while True:
        i += 1

        if i + increment >= len(result):
            current.append([result[i].text])
            fields.append({"name": current[0][0], "type": current[1][0]})
            break

        if result[i].text == ",":
            fields.append({"name": current[0][0], "type": current[1][0]})
            current = []
            continue

        current.append([result[i].text])

    backend.create_table(table_name, fields)


def drop_table(result):
    if result[1].type != TokenType.LITERAL and result[1].type != TokenType.STRING and result[1].text != "*":
        raise Exception("Invalid table name")

    table_name = result[1].text

    backend.drop_table(table_name)


def insert_into(result):
    if result[1].type != TokenType.LITERAL and result[1].type != TokenType.STRING:
        raise Exception("Invalid table name")

    if result[1].text not in map(lambda x: x.name, backend.get_tables()):
        raise Exception("Table does not exist")

    table_name = result[1].text

    if result[2].text != "VALUES" or result[2].type != TokenType.KEYWORD:
        raise Exception("Invalid insert statement")

    if result[3].type != TokenType.SYMBOL or result[3].text != "(":
        raise Exception("Invalid table definition")

    i = 2

    table = [table for table in backend.get_tables() if table.name == table_name][0]
    fields = table.definition
    maxLength = len(fields)

    values = []

    while True:
        i += 1
        if i >= len(result):
            break

        if len(values) > maxLength:
            raise Exception("Too many values")

        if result[i].type == TokenType.STRING or result[i].type == TokenType.LITERAL:
            values.append(result[i].text)

    backend.insert_into(table_name, values)


def select(result):
    if result[1].type != TokenType.LITERAL and result[1].type != TokenType.STRING and result[1].text != "*":
        raise Exception("Invalid selector")

    toSelect = []

    endIndex = 0

    for index, i in enumerate(result[1:]):
        if i.type == TokenType.LITERAL or i.type == TokenType.STRING or i.text == "*":
            toSelect.append(i.text)

        if i.type == TokenType.KEYWORD:
            endIndex = index - 1
            break

    if result[endIndex + 2].text != "FROM":
        raise Exception("Expected 'FROM', got " + str(result[endIndex + 1].text))

    if result[endIndex + 3].type != TokenType.LITERAL and result[endIndex + 2].type != TokenType.STRING:
        raise Exception("Invalid table name " + str(result[endIndex + 3].text))

    if result[endIndex + 3].text not in map(lambda x: x.name, backend.get_tables()):
        raise Exception("Table does not exist " + str(result[endIndex + 3].text))

    table_name = result[endIndex + 3].text

    try:
        result[endIndex + 4].text
    except IndexError:
        return backend.select(table_name, toSelect)

    # filters

    if result[endIndex + 4].text != "WHERE":
        raise Exception("Expected 'WHERE', got " + str(result[endIndex + 4].text))

    # send filters to func
    filters = {}
    print(str(result[endIndex + 5:]))

    identifier = None
    content = None

    for index, value in enumerate(result[endIndex + 5:]):
        if value.type == TokenType.LITERAL:
            raise Exception("Got literal in where specifier; literals are illegal in this context. Literal: '" + str(
                value.text) + "'")

        if value.type == TokenType.IDENTIFIER:
            identifier = value.text

        if value.type == TokenType.SYMBOL and value.text == "=":
            continue

        if value.type == TokenType.STRING:
            content = value.text

        if identifier is not None and content is not None:
            filters[identifier] = content
            identifier = None
            content = None

    return backend.select(table_name, toSelect, filters)


test = True

if test:
    create_table(parse.parse_sql_str("CREATE_TABLE test ( name string , secondname string )"))
    # drop_table(parse.parse_sql_str("DROP_TABLE test"))
    insert_into(parse.parse_sql_str("INSERT_INTO test VALUES ( 'name1' , 'secondname2' )"))
    insert_into(parse.parse_sql_str("INSERT_INTO test VALUES ( 'name3' , 'secondname2' )"))
    print(str(select(parse.parse_sql_str("SELECT * FROM test"))))
    print(str(select(parse.parse_sql_str("SELECT name FROM test"))))
    print("---------------------")
    print(str(select(parse.parse_sql_str("SELECT secondname FROM test WHERE name = 'name1'"))))
    # print(str(select(parse.parse_sql_str("SELECT name , secondname FROM test WHERE name='name3'"))))

    import sys

    sys.exit()

while True:
    text = input("> ")
    if text == "exit":
        break

    result = parse.parse_sql_str(text)

    if result[0].type != TokenType.KEYWORD:
        print("Invalid keyword")
        continue

    if result[0].text == "CREATE_TABLE":
        create_table(result)

    elif result[0].text == "DROP_TABLE":
        drop_table(result)

    elif result[0].text == "INSERT_INTO":
        insert_into(result)

    elif result[0].text == "SELECT":
        select(result)

    else:
        print("Invalid operation")
