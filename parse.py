from dataclasses import dataclass


@dataclass
class Token():
    text: str
    quote: bool


def tokenise(string):
    output = []

    inQuotes = False
    current = ""

    string = string.strip()

    splitters = [" "]

    for index, char in enumerate(string):
        if char == '"' or char == "'":
            inQuotes = not inQuotes
            output.append(Token(current, inQuotes))
            current = ""

            continue

        print(str(inQuotes))

        if char in splitters and not inQuotes:
            output.append(Token(current, inQuotes))
            current = ""

        else:
            current += char

    output = [token for token in output if token.text != ""]

    return output


def parse_sql_str(sql_str):
    sql_str = tokenise(sql_str)


def tests():
    print(str(tokenise("SELECT * FROM thing WHERE name='stuff and things'")))


if __name__ == "__main__":
    tests()
