import parse
from parse import TokenType

while True:
    text = input('> ')
    if text == 'exit':
        break

    result = parse.parse_sql_str(text)

    if result[0].type != TokenType.KEYWORD:
        print("Invalid keyword")
        continue

    if result[0].value == "CREATE_TABLE":
        if result[1].type != TokenType.IDENTIFIER or result[1].type != TokenType.STRING:
            print("Invalid table name")
            continue

        table_name = result[1].value

        if result[2].type != TokenType.SYMBOL or result[2].value != "(":
            print("Invalid table definition")
            continue

        i = 3
        failed = False

        fields = []

        while True:
            # TODO might have to tweak this
            if i + 3 >= len(result):
                break

            if result[i].type != TokenType.LITERAL or result[i+1].type != TokenType.LITERAL or result[i+2].type != TokenType.SYMBOL or result[i+2].value != ",":
                print(f"Invalid table definition at: "{result[i].text} {result[i+1].text} {result[i+2].text}")

                failed = True
                break

            #TODO now sanity check is done, iterate over, fill in the fields, then you can process it

        if failed:
            continue