"""입력 파싱, 명령 검증/실행, 출력 형식을 담당하는 명령행 진입점."""

import shlex

from hash_map import HashMap


def quoted(value):
    """저장된 문자열을 한 줄의 큰따옴표 문자열로 표시한다."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return '"' + escaped + '"'


def wrong_arguments(command):
    """입력한 명령어의 원래 대소문자를 유지하는 인자 오류 형식."""
    return f"(error) ERR wrong number of arguments for '{command}' command"


def parse_line(line):
    """표준 문자열 파서로 따옴표를 지원한다. 닫히지 않은 따옴표도 검출한다."""
    try:
        return shlex.split(line), True
    except ValueError:
        # 명령어 이름은 보존하고, 별도 오류 형식을 추가하지 않는다.
        return line.split(maxsplit=1), False


def execute_line(store, line):
    """응답 문자열을 반환한다. 빈 입력은 빈 문자열, 정상 종료는 None이다."""
    tokens, valid = parse_line(line)
    if len(tokens) == 0:
        return ""
    original = tokens[0]
    command = original.upper()
    if command == "SET":
        expected = 3
    elif command == "GET" or command == "DEL" or command == "EXISTS":
        expected = 2
    elif command == "DBSIZE" or command == "KEYS" or command == "EXIT" or command == "QUIT":
        expected = 1
    else:
        return f"(error) ERR unknown command '{original}'"
    if not valid or len(tokens) != expected:
        return wrong_arguments(original)
    if command == "EXIT" or command == "QUIT":
        return None
    if command == "SET":
        store.put(tokens[1], tokens[2])
        return "OK"
    if command == "GET":
        value = store.get(tokens[1])
        return "(nil)" if value is None else quoted(value)
    if command == "DEL":
        return f"(integer) {int(store.delete(tokens[1]))}"
    if command == "EXISTS":
        return f"(integer) {int(store.contains(tokens[1]))}"
    if command == "DBSIZE":
        return f"(integer) {len(store)}"
    lines = []
    number = 1
    for key in store.keys():
        lines.append(f"{number}. {quoted(key)}")
        number += 1
    return "(empty array)" if len(lines) == 0 else "\n".join(lines)


def main():
    """하나의 메모리 저장소를 유지하며 종료 명령이나 입력 끝까지 대화한다."""
    store = HashMap()
    while True:
        try:
            line = input("mini-redis> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        response = execute_line(store, line)
        if response is None:
            break
        if response != "":
            print(response)


if __name__ == "__main__":
    main()
