# KiwoomClient 라이브러리 사용 가이드

`kiwoom_client.py`는 키움증권 OpenAPI (REST 방식)를 파이썬에서 가장 직관적이고 편리하게 사용할 수 있도록 설계된 독립적인 SDK 모듈입니다. 이 파일 하나만 본인의 프로젝트로 복사해 가면 언제 어디서든 강력한 기능들을 활용할 수 있습니다.

## ✨ 핵심 기능 (Features)

1. **완전 자동화된 토큰 관리**: 첫 호출 시 알아서 Access Token을 발급받으며, 만료되거나 세션이 끊어지면 백그라운드에서 자동으로 새 토큰을 갱신(Renew)하여 기존 요청을 재시도합니다.
2. **High-Level API 호출 (`call` 메서드)**: `apis.json` 스펙을 참조하여 Header와 Body/Param을 개발자가 구분할 필요 없이, 파라미터만 쭉 나열하면 라이브러리가 알아서 분류하고 통신합니다.
3. **하이픈(`-`) 키워드 자동 매핑**: 파이썬 문법상 불가능한 `cont-yn` 같은 키움증권 특유의 파라미터들을 `cont_yn`으로 입력해도 알아서 원래 스펙에 맞게 변환해 줍니다.
4. **빈 값(Default) 자동 채움**: 키움 API 특성상 모든 파라미터를 누락 없이 보내야 합니다. 사용자가 입력하지 않은 파라미터는 스펙을 참조하여 기본값(`""`)으로 빈 공간을 꽉 채워서 전송해 줍니다.

---

## 🚀 퀵 스타트 (Quick Start)

### 1. 모듈 임포트 및 초기화
`kiwoom_client.py` 와 `static/apis.json` 파일을 본인 프로젝트에 복사한 뒤 임포트합니다.

```python
from kiwoom_client import KiwoomClient

# 클라이언트 초기화 (토큰은 API 첫 호출 시점에 알아서 발급받습니다)
client = KiwoomClient(
    appkey="본인의_APP_KEY", 
    secretkey="본인의_SECRET_KEY",
    base_url="https://openapi.kiwoom.com:8282", # 실전투자 URL (모의투자는 https://openapivts.kiwoom.com:29443)
    acc_id="12345678"  # 내 계좌번호 (선택사항, 자동 주입용)
)
```

### 2. 마법의 `call` 메서드 사용법
가장 추천하는 사용법입니다. API ID와 필요한 값만 던지면 끝납니다.

```python
# [예시 1] 주식기본정보 조회 (현재가 등)
# - API ID : ka10001
# - 스펙상 'api-id'는 필수 헤더지만, call()에서는 api_id를 던졌으므로 생략해도 자동 주입됩니다.
res_price = client.call(
    api_id="ka10001", 
    stk_cd="005930"      # 삼성전자 종목코드
)
# 응답은 HTTP 헤더와 응답 바디가 하나로 합쳐진 딕셔너리로 반환됩니다.
import json
print(json.dumps(res_price, indent=2, ensure_ascii=False))

# [예시 2] 파이썬 친화적인 하이픈 변환 (cont_yn)
# 스펙의 'cont-yn'을 파이썬 문법에 맞게 'cont_yn'으로 던지면 알아서 'cont-yn' Header로 변환됩니다.
res_account = client.call(
    api_id="kt00018",     # 계좌평가잔고내역요청
    cont_yn="N",          
    next_key="",          
    qry_tp="1",
    dmst_stex_tp="KRX"    
)

# [예시 3] 주식 매수 주문 (POST 방식)
# - 생략된 나머지 파라미터들은 빈 문자열("")로 알아서 채워져 전송됩니다.
res_order = client.call(
    api_id="kt10000",      # 주식 매수주문
    dmst_stex_tp="KRX",    # 국내거래소구분
    stk_cd="005930",       # 종목코드
    ord_qty="10",          # 주문수량 (10주)
    ord_uv="0",            # 주문단가 (시장가 0원)
    trde_tp="3"            # 매매구분 (3: 시장가)
)
```

---

## 🛠 저수준 (Low-Level) 수동 제어

가이드 문서에 없는 커스텀 API를 호출하거나, Header와 Param을 직접 엄격하게 통제하고 싶을 때는 `get`, `post` 래퍼 메서드를 사용합니다.

```python
# GET 요청 수동 제어
response = client.get(
    path="/api/dostk/stkinfo",
    headers={"api-id": "ka10001", "cont-yn": "N"},
    params={"stk_cd": "005930"}
)

# POST 요청 수동 제어
response = client.post(
    path="/api/dostk/ordr",
    headers={"api-id": "kt10000"},
    json_data={
        "dmst_stex_tp": "KRX",
        "stk_cd": "005930",
        "ord_qty": "10",
        "ord_uv": "0",
        "trde_tp": "3",
        "cond_uv": ""
    }
)
```

---

## 📦 응답 (Response) 포맷

### High-Level `call` 메서드 사용 시
**JSON 응답 바디 전체**와 `apis.json` 스펙에 정의된 **핵심 응답 헤더(api-id, cont-yn 등)만 필터링**되어 하나의 딕셔너리로 합쳐진(Merged) 형태로 반환됩니다. 쓰레기 HTTP 헤더들이 제거되어 깔끔합니다.

> 💡 **에러(Exception) 처리 안내**
> 서버가 정상 응답(200 OK)을 주었더라도 인증 실패나 키움증권 내부 로직 에러(예: 장 종료, 잔고 부족 등)로 인해 `return_code` 값이 `"0"`이 아닌 경우, 결괏값을 반환하지 않고 즉시 커스텀 예외인 **`KiwoomException`을 발생(raise)시킵니다.**
> 이 예외 객체에서는 `e.return_code`와 `e.return_msg`를 속성으로 직접 꺼내어 세밀한 핸들링이 가능합니다.

```python
from kiwoom_client import KiwoomException

try:
    res = client.call(api_id="kt10000", ...)
except KiwoomException as e:
    print(f"에러코드: {e.return_code}")
    print(f"에러메시지: {e.return_msg}")
    print(f"HTTP상태: {e.status_code}")
```

### Low-Level `request`, `get`, `post` 메서드 사용 시
가공되지 않은 상태로 헤더 딕셔너리와 바디 딕셔너리가 분리되어 반환됩니다.
```python
{
    "headers": { ... }, # 모든 HTTP 응답 헤더 포함 (Date, Server 등)
    "body": { ... }     # JSON 응답 바디
}
```

---

## 🔒 로그아웃 (토큰 즉시 폐기)

사용이 끝난 후 보안을 위해 발급된 토큰을 즉시 폐기하고 싶을 때 사용합니다.

```python
client.revoke_token()
```