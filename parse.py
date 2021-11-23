from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    STRING = 3
    LITERAL = 4


@dataclass
class Token():
    text: str
    quote: bool


@dataclass
class EnhancedToken():
    text: str
    type: TokenType


def tokenise(string):
    output = []

    inQuotes = False
    current = ""

    string = string.strip()

    splitters = [" "]

    for index, char in enumerate(string):
        if char == '"' or char == "'":
            output.append(Token(current, inQuotes))

            inQuotes = not inQuotes
            current = ""

            continue

        if char in splitters and not inQuotes:
            output.append(Token(current, inQuotes))
            current = ""

        else:
            current += char

    output.append(Token(current, inQuotes))

    output = [token for token in output if token.text != ""]

    for index, token in enumerate(output):
        if not token.quote:
            if token.text[-1] == "=" and len(token.text) > 1:
                token.text = token.text[:-1]

                output.insert(index + 1, Token("=", False))

            elif token.text[-1] == "," and len(token.text) > 1:
                token.text = token.text[:-1]

                output.insert(index + 1, Token(",", False))

    return output


def categorise(tokens):
    output = []
    keywords = ["SELECT", "FROM", "WHERE", "CREATE", "CREATE_TABLE", "DROP_TABLE", "INSERT_INTO", "VALUES"]
    symbols = ["=", "*", "(", ")", ","]

    for index, token in enumerate(tokens):
        if token.text in keywords:
            output.append(EnhancedToken(token.text, TokenType.KEYWORD))
        elif token.text in symbols:
            output.append(EnhancedToken(token.text, TokenType.SYMBOL))
        elif token.quote:
            output.append(EnhancedToken(token.text, TokenType.STRING))
        elif index != len(tokens) - 1 and tokens[index + 1].text == "=":
            output.append(EnhancedToken(token.text, TokenType.IDENTIFIER))
        else:
            output.append(EnhancedToken(token.text, TokenType.LITERAL))

    return output


def parse_sql_str(sql_str):
    sql_str = tokenise(sql_str)
    return categorise(sql_str)


def tests():
    # print(str(tokenise("SELECT * FROM thing WHERE name='stuff and things'")))
    # print(str(categorise(tokenise("SELECT * FROM thing WHERE name='stuff and things'"))))
    print(parse_sql_str("CREATE_TABLE People ( PersonID string, PersonName string, location string )"))


if __name__ == "__main__":
    tests()
