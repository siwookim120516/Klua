# Klua
Klua는 한국어로 lua어를 코딩할 수 있게 만든 응용 프로그램 입니다.(ai를 사용한 프로그램 입니다.)
# 사용법
구글드라이브에서 klua.zip 파일을 다운로드 받습니다.(https://drive.google.com/drive/folders/1K33PmscGUwRlm5JpeIclz2QNxwvZ9eAg?usp=sharing)
먼저 압축을 풀어주세요. 그 다음 lua설치파일에 있는 루아를 설치 한 후 klua\dist\klua.exe 파일을 실행시켜 주세요(최초 실행은 관리자권환을 권장합니다.).

# 문법
케이루아는 기본적으로 루아와 같은 문법을 사용합니다. 하지만 한국어로 번역 한 것 뿐입니다.


"만일": "if", "이라면": "then", "아니면": "else", "그렇지않으면": "elseif", "끝": "end","반복": "for", "동안": "while", "반복하기": "repeat", "까지": "until", "반복멈추기": "break","돌려주기": "return", "하기": "do", "함수": "function", "지역": "local","출력": "print", "숫자로": "tonumber", "문자열로": "tostring", "자료형": "type", "요구": "require", "오류": "error", "확인": "assert", "추가": "table.insert", "제거": "table.remove", "정렬": "table.sort", "다음": "next","길이": "string.len", "부분문자열": "string.sub", "찾기": "string.find", "대체": "string.gsub", "형식": "string.format", "절댓값": "math.abs", "올림": "math.ceil", "버림": "math.floor", "최댓값": "math.max", "최솟값": "math.min", "거듭제곱": "math.pow", "무작위": "math.random", "제곱근": "math.sqrt", "코루틴_만들기": "coroutine.create", "코루틴_시작": "coroutine.resume", "코루틴_일시중지": "coroutine.yield", "코루틴_상태": "coroutine.status", "메타설정": "setmetatable", "메타가져오기": "getmetatable", "파일실행": "dofile", "파일읽기": "loadfile", "반복자_인덱스": "ipairs", "반복자_모두": "pairs", "참": "true", "거짓": "false", "또는": "or","그리고": "and", "아니다": "not"

### 예시코드

  출력하는 법
  ```sh
  출력("안녕 케이루아")
  ```
출력
  ```sh
  안녕 케이루아

  -- 실행 종료 --
  ```

-------

  반복문 응용

  ```sh
  지역 pl1 = "못생김"
  만일 pl1 == "못생김" 이라면
    반복 i=1, 10 하기
      출력("못생김 X ".. i)
    끝
  끝
  ```

  출력

  ```sh
  못생김 X 1
  못생김 X 2
  못생김 X 3
  못생김 X 4
  못생김 X 5
  못생김 X 6
  못생김 X 7
  못생김 X 8
  못생김 X 9
  못생김 X 10

  -- 실행 종료 --
  ```

-------

  리스트 응용

  ```sh
  지역 pls = {"파이썬", "자바", "케이루아", "루아", "어셈블리"}
   반복 i=1, #pls 하기
     만일 pls[i] == "케이루아" 이라면 
       출력("한국어를 사랑하는 언어 : " .. pls[i])
     아니면
       출력("그냥 일반적인 언어 : " .. pls[i])
    끝
  끝
  ```

  출력

  ```sh
  그냥 일반적인 언어 : 파이썬
  그냥 일반적인 언어 : 자바
  한국어를 사랑하는 언어 : 케이루아
  그냥 일반적인 언어 : 루아
  그냥 일반적인 언어 : 어셈블리

  -- 실행 종료 --
  ```


# 라이선스

이 프로그램은 MIT 라이선스에 따라 배포됩니다.

저작권자: 김트리0516 (2025)

본 소프트웨어는 자유롭게 사용, 수정, 배포할 수 있으나,  
모든 복제본 또는 중요 부분에 위 저작권 고지와 본 라이선스 내용을 포함해야 합니다.

본 소프트웨어는 어떠한 명시적 또는 묵시적 보증 없이 "있는 그대로" 제공됩니다.
