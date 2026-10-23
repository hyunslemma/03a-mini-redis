# 산출물 2 — 명령행 저장소 실행 기록

2026-10-23, Python 3.13.5에서 `main.py`를 실제 실행한 터미널 기록이다. 아래 코드 블록은 터미널의 입력 에코와 프로그램 출력이며 줄바꿈만 LF로 통일했다.

```text
$ python3 main.py
mini-redis> KEYS
(empty array)
mini-redis> DBSIZE
(integer) 0
mini-redis> sEt city Busan
OK
mini-redis> GET city
"Busan"
mini-redis> EXISTS city
(integer) 1
mini-redis> SET city Seoul
OK
mini-redis> GET city
"Seoul"
mini-redis> DBSIZE
(integer) 1
mini-redis> SET river Nakdong
OK
mini-redis> KEYS
1. "city"
2. "river"
mini-redis> DEL city
(integer) 1
mini-redis> DEL city
(integer) 0
mini-redis> GET city
(nil)
mini-redis> EXISTS city
(integer) 0
mini-redis> DEL river
(integer) 1
mini-redis> KEYS
(empty array)
mini-redis> DBSIZE
(integer) 0
mini-redis> LoOkUp
(error) ERR unknown command 'LoOkUp'
mini-redis> gEt
(error) ERR wrong number of arguments for 'gEt' command
mini-redis> SET onlykey
(error) ERR wrong number of arguments for 'SET' command
mini-redis> KEYS extra
(error) ERR wrong number of arguments for 'KEYS' command
mini-redis> SET place "New York"
OK
mini-redis> GET place
"New York"
mini-redis> SET empty ""
OK
mini-redis> GET empty
""
mini-redis> SET bad "unfinished
(error) ERR wrong number of arguments for 'SET' command
mini-redis> EXISTS bad
(integer) 0
mini-redis> exit
```

6종 명령어, 값 덮어쓰기 후 키 개수 유지, 존재/부재, 삭제 성공/실패, 빈 저장소, 두 표준 오류, 원래 명령어 대소문자 보존을 확인했다. 선택 기능인 따옴표로 감싼 공백·빈 값도 지원하며, 닫히지 않은 따옴표는 인자 오류로 처리한다.

재현: `python3 main.py` 실행 후 같은 명령어를 입력한다.
