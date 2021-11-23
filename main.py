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
            fields.append({"name": current[0], "type": current[1][0]})
            break

        if result[i].text == ",":
            fields.append({"name": current[0], "type": current[1][0]})
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

        print(str(result[i]))

        if result[i].type == TokenType.STRING or result[i].type == TokenType.LITERAL:
            values.append(result[i].text)

    backend.insert_into(table_name, values)


test = True

if test:
    create_table(parse.parse_sql_str("CREATE_TABLE test ( name string , anothername string )"))
    # drop_table(parse.parse_sql_str("DROP_TABLE test"))
    insert_into(parse.parse_sql_str("INSERT_INTO test VALUES ( 'test' , 'test2' )"))

    import sys

    sys.exit()

while True:
    text = input('> ')
    if text == 'exit':
        break

    result = parse.parse_sql_str(text)

    print(str(result))

    if result[0].type != TokenType.KEYWORD:
        print("Invalid keyword")
        continue

    if result[0].text == "CREATE_TABLE":
        create_table(result)

    elif result[0].text == "DROP_TABLE":
        drop_table(result)
