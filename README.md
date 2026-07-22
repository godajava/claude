# 개인 비서 에이전트

일정·할 일·메모를 관리하고 아침 브리핑을 생성하는 한국어 개인 비서 에이전트입니다.

## 구성

| 경로 | 설명 |
|---|---|
| `.claude/agents/personal-secretary.md` | 개인 비서 에이전트 정의 |
| `.claude/skills/daily-brief/SKILL.md` | 오늘의 일정·할 일 아침 브리핑 스킬 |
| `.claude/skills/remember/SKILL.md` | 자연어 입력을 일정/할 일/메모로 분류·기록하는 스킬 |
| `secretary/schedule.md` | 일정 데이터 |
| `secretary/todo.md` | 할 일 데이터 |
| `secretary/notes/` | 메모 |

## 사용법

- **기록**: "기억해줘", "일정 잡아줘", "할 일 추가" → `remember` 스킬이 `secretary/`에 기록
- **브리핑**: "오늘 브리핑", "아침 브리핑" → `daily-brief` 스킬이 오늘 일정·미완료 할 일을 요약

## 자동화

- 평일 08:00 KST 아침 브리핑 Routine이 `secretary/`를 읽어 브리핑을 생성합니다.
