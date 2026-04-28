from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Dict, Any, List, Type, Annotated, Callable, Union
from .core import KiwoomCore

# ====================================================================
# 0. Type Validators (키움증권 예외 타입 처리기)
# ====================================================================
def _force_str(v: Any) -> str:
    if v == [] or v is None:
        return ""
    if isinstance(v, list):
        return ",".join(str(x) for x in v)
    return str(v)

def _force_list(v: Any) -> Any:
    if v == "" or v is None:
        return []
    if not isinstance(v, list):
        return [v]
    return v

def _force_int(v: Any) -> int:
    if v == "" or v is None:
        return 0
    try:
        return int(v)
    except ValueError:
        return 0

SafeStr = Annotated[str, BeforeValidator(_force_str)]
SafeInt = Annotated[int, BeforeValidator(_force_int)]
SafeListStr = Annotated[List[str], BeforeValidator(_force_list)]

# ====================================================================
# 1. API Models (입력 및 출력 모델)
# ====================================================================

class IssueAccessTokenRequest(BaseModel):
    """[au10001] 접근토큰 발급 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    grant_type: SafeStr = Field(default="", description="grant_type client_credentials 입력")
    appkey: SafeStr = Field(default="", description="앱키")
    secretkey: SafeStr = Field(default="", description="시크릿키")

class IssueAccessToken(BaseModel):
    """[au10001] 접근토큰 발급 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    expires_dt: SafeStr = Field(default="", description="만료일")
    token_type: SafeStr = Field(default="", description="토큰타입")
    token: SafeStr = Field(default="", description="접근토큰")

class RevokeAccessTokenRequest(BaseModel):
    """[au10002] 접근토큰폐기 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    appkey: SafeStr = Field(default="", description="앱키")
    secretkey: SafeStr = Field(default="", description="시크릿키")
    token: SafeStr = Field(default="", description="접근토큰")

class RevokeAccessToken(BaseModel):
    """[au10002] 접근토큰폐기 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    pass

class AccountNumberRequest(BaseModel):
    """[ka00001] 계좌번호조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class AccountNumber(BaseModel):
    """[ka00001] 계좌번호조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acctNo: SafeStr = Field(default="", description="계좌번호")

class DailyBalanceReturnRateRequest(BaseModel):
    """[ka01690] 일별잔고수익률 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_dt: SafeStr = Field(default="", description="조회일자")

class DailyBalanceReturnRate_DayBalRt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    rmnd_qty: SafeStr = Field(default="", description="보유 수량")
    buy_uv: SafeStr = Field(default="", description="매입 단가")
    buy_wght: SafeStr = Field(default="", description="매수비중")
    evltv_prft: SafeStr = Field(default="", description="평가손익")
    prft_rt: SafeStr = Field(default="", description="수익률")
    evlt_amt: SafeStr = Field(default="", description="평가금액")
    evlt_wght: SafeStr = Field(default="", description="평가비중")

class DailyBalanceReturnRate(BaseModel):
    """[ka01690] 일별잔고수익률 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dt: SafeStr = Field(default="", description="일자")
    tot_buy_amt: SafeStr = Field(default="", description="총 매입가")
    tot_evlt_amt: SafeStr = Field(default="", description="총 평가금액")
    tot_evltv_prft: SafeStr = Field(default="", description="총 평가손익")
    tot_prft_rt: SafeStr = Field(default="", description="수익률")
    dbst_bal: SafeStr = Field(default="", description="예수금")
    day_stk_asst: SafeStr = Field(default="", description="추정자산")
    buy_wght: SafeStr = Field(default="", description="현금비중")
    day_bal_rt: Annotated[List[DailyBalanceReturnRate_DayBalRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별잔고수익률")

class RealizedProfitLossByDateItemDateRequest(BaseModel):
    """[ka10072] 일자별종목별실현손익요청_일자 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")

class RealizedProfitLossByDateItemDate_DtStkDivRlztPl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    buy_uv: SafeStr = Field(default="", description="매입단가")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    tdy_sel_pl: SafeStr = Field(default="", description="당일매도손익")
    pl_rt: SafeStr = Field(default="", description="손익율")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")
    wthd_alowa: SafeStr = Field(default="", description="인출가능금액")
    loan_dt: SafeStr = Field(default="", description="대출일")
    crd_tp: SafeStr = Field(default="", description="신용구분")
    stk_cd_1: SafeStr = Field(default="", description="종목코드1")
    tdy_sel_pl_1: SafeStr = Field(default="", description="당일매도손익1")

class RealizedProfitLossByDateItemDate(BaseModel):
    """[ka10072] 일자별종목별실현손익요청_일자 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dt_stk_div_rlzt_pl: Annotated[List[RealizedProfitLossByDateItemDate_DtStkDivRlztPl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일자별종목별실현손익")

class RealizedProfitLossByDateItemPeriodRequest(BaseModel):
    """[ka10073] 일자별종목별실현손익요청_기간 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")

class RealizedProfitLossByDateItemPeriod_DtStkRlztPl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    tdy_htssel_cmsn: SafeStr = Field(default="", description="당일hts매도수수료")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    buy_uv: SafeStr = Field(default="", description="매입단가")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    tdy_sel_pl: SafeStr = Field(default="", description="당일매도손익")
    pl_rt: SafeStr = Field(default="", description="손익율")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")
    wthd_alowa: SafeStr = Field(default="", description="인출가능금액")
    loan_dt: SafeStr = Field(default="", description="대출일")
    crd_tp: SafeStr = Field(default="", description="신용구분")

class RealizedProfitLossByDateItemPeriod(BaseModel):
    """[ka10073] 일자별종목별실현손익요청_기간 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dt_stk_rlzt_pl: Annotated[List[RealizedProfitLossByDateItemPeriod_DtStkRlztPl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일자별종목별실현손익")

class RealizedProfitLossByDateRequest(BaseModel):
    """[ka10074] 일자별실현손익요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자")
    end_dt: SafeStr = Field(default="", description="종료일자")

class RealizedProfitLossByDate_DtRlztPl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    buy_amt: SafeStr = Field(default="", description="매수금액")
    sell_amt: SafeStr = Field(default="", description="매도금액")
    tdy_sel_pl: SafeStr = Field(default="", description="당일매도손익")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")

class RealizedProfitLossByDate(BaseModel):
    """[ka10074] 일자별실현손익요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_buy_amt: SafeStr = Field(default="", description="총매수금액")
    tot_sell_amt: SafeStr = Field(default="", description="총매도금액")
    rlzt_pl: SafeStr = Field(default="", description="실현손익")
    trde_cmsn: SafeStr = Field(default="", description="매매수수료")
    trde_tax: SafeStr = Field(default="", description="매매세금")
    dt_rlzt_pl: Annotated[List[RealizedProfitLossByDate_DtRlztPl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일자별실현손익")

class NonConfirmationRequest(BaseModel):
    """[ka10075] 미체결요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    all_stk_tp: SafeStr = Field(default="", description="전체종목구분 0:전체, 1:종목")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:전체, 1:매도, 2:매수")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")

class NonConfirmation_Oso(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    acnt_no: SafeStr = Field(default="", description="계좌번호")
    ord_no: SafeStr = Field(default="", description="주문번호")
    mang_empno: SafeStr = Field(default="", description="관리사번")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    tsk_tp: SafeStr = Field(default="", description="업무구분")
    ord_stt: SafeStr = Field(default="", description="주문상태")
    stk_nm: SafeStr = Field(default="", description="종목명")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_pric: SafeStr = Field(default="", description="주문가격")
    oso_qty: SafeStr = Field(default="", description="미체결수량")
    cntr_tot_amt: SafeStr = Field(default="", description="체결누계금액")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    io_tp_nm: SafeStr = Field(default="", description="주문구분")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    tm: SafeStr = Field(default="", description="시간")
    cntr_no: SafeStr = Field(default="", description="체결번호")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    cur_prc: SafeStr = Field(default="", description="현재가")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    unit_cntr_pric: SafeStr = Field(default="", description="단위체결가")
    unit_cntr_qty: SafeStr = Field(default="", description="단위체결량")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")
    ind_invsr: SafeStr = Field(default="", description="개인투자자")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")
    stex_tp_txt: SafeStr = Field(default="", description="거래소구분텍스트 통합,KRX,NXT")
    sor_yn: SafeStr = Field(default="", description="SOR 여부값 Y,N")
    stop_pric: SafeStr = Field(default="", description="스톱가 스톱지정가주문 스톱가")

class NonConfirmation(BaseModel):
    """[ka10075] 미체결요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    oso: Annotated[List[NonConfirmation_Oso], BeforeValidator(_force_list)] = Field(default_factory=list, description="미체결")

class ConclusionRequest(BaseModel):
    """[ka10076] 체결요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    qry_tp: SafeStr = Field(default="", description="조회구분 0:전체, 1:종목")
    sell_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    ord_no: SafeStr = Field(default="", description="주문번호 검색 기준 값으로 입력한 주문번호 보다 과거에 체결된 내역이 조회됩니다.")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")

class Conclusion_Cntr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ord_no: SafeStr = Field(default="", description="주문번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    io_tp_nm: SafeStr = Field(default="", description="주문구분")
    ord_pric: SafeStr = Field(default="", description="주문가격")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    oso_qty: SafeStr = Field(default="", description="미체결수량")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")
    ord_stt: SafeStr = Field(default="", description="주문상태")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    ord_tm: SafeStr = Field(default="", description="주문시간")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")
    stex_tp_txt: SafeStr = Field(default="", description="거래소구분텍스트 통합,KRX,NXT")
    sor_yn: SafeStr = Field(default="", description="SOR 여부값 Y,N")
    stop_pric: SafeStr = Field(default="", description="스톱가 스톱지정가주문 스톱가")

class Conclusion(BaseModel):
    """[ka10076] 체결요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr: Annotated[List[Conclusion_Cntr], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결")

class SameDayRealizedProfitLossRequest(BaseModel):
    """[ka10077] 당일실현손익상세요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SameDayRealizedProfitLoss_TdyRlztPlDtl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    buy_uv: SafeStr = Field(default="", description="매입단가")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    tdy_sel_pl: SafeStr = Field(default="", description="당일매도손익")
    pl_rt: SafeStr = Field(default="", description="손익율")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SameDayRealizedProfitLoss(BaseModel):
    """[ka10077] 당일실현손익상세요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_rlzt_pl: SafeStr = Field(default="", description="당일실현손익")
    tdy_rlzt_pl_dtl: Annotated[List[SameDayRealizedProfitLoss_TdyRlztPlDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일실현손익상세")

class AccountYieldRequest(BaseModel):
    """[ka10085] 계좌수익률요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")

class AccountYield_AcntPrftRt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pur_pric: SafeStr = Field(default="", description="매입가")
    pur_amt: SafeStr = Field(default="", description="매입금액")
    rmnd_qty: SafeStr = Field(default="", description="보유수량")
    tdy_sel_pl: SafeStr = Field(default="", description="당일매도손익")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")
    crd_tp: SafeStr = Field(default="", description="신용구분")
    loan_dt: SafeStr = Field(default="", description="대출일")
    setl_remn: SafeStr = Field(default="", description="결제잔고")
    clrn_alow_qty: SafeStr = Field(default="", description="청산가능수량")
    crd_amt: SafeStr = Field(default="", description="신용금액")
    crd_int: SafeStr = Field(default="", description="신용이자")
    expr_dt: SafeStr = Field(default="", description="만기일")

class AccountYield(BaseModel):
    """[ka10085] 계좌수익률요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_prft_rt: Annotated[List[AccountYield_AcntPrftRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌수익률")

class UnfilledSplitOrderDetailsRequest(BaseModel):
    """[ka10088] 미체결 분할주문 상세 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_no: SafeStr = Field(default="", description="주문번호")

class UnfilledSplitOrderDetails_Osop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    ord_no: SafeStr = Field(default="", description="주문번호")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_pric: SafeStr = Field(default="", description="주문가격")
    osop_qty: SafeStr = Field(default="", description="미체결수량")
    io_tp_nm: SafeStr = Field(default="", description="주문구분")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    sell_tp: SafeStr = Field(default="", description="매도/수 구분")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    ord_stt: SafeStr = Field(default="", description="주문상태")
    cur_prc: SafeStr = Field(default="", description="현재가")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")
    stex_tp_txt: SafeStr = Field(default="", description="거래소구분텍스트 통합,KRX,NXT")

class UnfilledSplitOrderDetails(BaseModel):
    """[ka10088] 미체결 분할주문 상세 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    osop: Annotated[List[UnfilledSplitOrderDetails_Osop], BeforeValidator(_force_list)] = Field(default_factory=list, description="미체결분할주문리스트")

class SameDaySalesLogRequest(BaseModel):
    """[ka10170] 당일매매일지요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD(공백입력시 금일데이터,최근 2개월까지 제공)")
    ottks_tp: SafeStr = Field(default="", description="단주구분 1:당일매수에 대한 당일매도,2:당일매도 전체")
    ch_crd_tp: SafeStr = Field(default="", description="현금신용구분 0:전체, 1:현금매매만, 2:신용매매만")

class SameDaySalesLog_TdyTrdeDiary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    buy_avg_pric: SafeStr = Field(default="", description="매수평균가")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    sel_avg_pric: SafeStr = Field(default="", description="매도평균가")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    cmsn_alm_tax: SafeStr = Field(default="", description="수수료_제세금")
    pl_amt: SafeStr = Field(default="", description="손익금액")
    sell_amt: SafeStr = Field(default="", description="매도금액")
    buy_amt: SafeStr = Field(default="", description="매수금액")
    prft_rt: SafeStr = Field(default="", description="수익률")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SameDaySalesLog(BaseModel):
    """[ka10170] 당일매매일지요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_sell_amt: SafeStr = Field(default="", description="총매도금액")
    tot_buy_amt: SafeStr = Field(default="", description="총매수금액")
    tot_cmsn_tax: SafeStr = Field(default="", description="총수수료_세금")
    tot_exct_amt: SafeStr = Field(default="", description="총정산금액")
    tot_pl_amt: SafeStr = Field(default="", description="총손익금액")
    tot_prft_rt: SafeStr = Field(default="", description="총수익률")
    tdy_trde_diary: Annotated[List[SameDaySalesLog_TdyTrdeDiary], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일매매일지")

class DetailedDepositRequest(BaseModel):
    """[kt00001] 예수금상세현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="조회구분 3:추정조회, 2:일반조회")

class DetailedDeposit_StkEntrPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    crnc_cd: SafeStr = Field(default="", description="통화코드")
    fx_entr: SafeStr = Field(default="", description="외화예수금")
    fc_krw_repl_evlta: SafeStr = Field(default="", description="원화대용평가금")
    fc_trst_profa: SafeStr = Field(default="", description="해외주식증거금")
    pymn_alow_amt: SafeStr = Field(default="", description="출금가능금액")
    pymn_alow_amt_entr: SafeStr = Field(default="", description="출금가능금액(예수금)")
    ord_alow_amt_entr: SafeStr = Field(default="", description="주문가능금액(예수금)")
    fc_uncla: SafeStr = Field(default="", description="외화미수(합계)")
    fc_ch_uncla: SafeStr = Field(default="", description="외화현금미수금")
    dly_amt: SafeStr = Field(default="", description="연체료")
    d1_fx_entr: SafeStr = Field(default="", description="d+1외화예수금")
    d2_fx_entr: SafeStr = Field(default="", description="d+2외화예수금")
    d3_fx_entr: SafeStr = Field(default="", description="d+3외화예수금")
    d4_fx_entr: SafeStr = Field(default="", description="d+4외화예수금")

class DetailedDeposit(BaseModel):
    """[kt00001] 예수금상세현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    entr: SafeStr = Field(default="", description="예수금")
    profa_ch: SafeStr = Field(default="", description="주식증거금현금")
    bncr_profa_ch: SafeStr = Field(default="", description="수익증권증거금현금")
    nxdy_bncr_sell_exct: SafeStr = Field(default="", description="익일수익증권매도정산대금")
    fc_stk_krw_repl_set_amt: SafeStr = Field(default="", description="해외주식원화대용설정금")
    crd_grnta_ch: SafeStr = Field(default="", description="신용보증금현금")
    crd_grnt_ch: SafeStr = Field(default="", description="신용담보금현금")
    add_grnt_ch: SafeStr = Field(default="", description="추가담보금현금")
    etc_profa: SafeStr = Field(default="", description="기타증거금")
    uncl_stk_amt: SafeStr = Field(default="", description="미수확보금")
    shrts_prica: SafeStr = Field(default="", description="공매도대금")
    crd_set_grnta: SafeStr = Field(default="", description="신용설정평가금")
    chck_ina_amt: SafeStr = Field(default="", description="수표입금액")
    etc_chck_ina_amt: SafeStr = Field(default="", description="기타수표입금액")
    crd_grnt_ruse: SafeStr = Field(default="", description="신용담보재사용")
    knx_asset_evltv: SafeStr = Field(default="", description="코넥스기본예탁금")
    elwdpst_evlta: SafeStr = Field(default="", description="ELW예탁평가금")
    crd_ls_rght_frcs_amt: SafeStr = Field(default="", description="신용대주권리예정금액")
    lvlh_join_amt: SafeStr = Field(default="", description="생계형가입금액")
    lvlh_trns_alowa: SafeStr = Field(default="", description="생계형입금가능금액")
    repl_amt: SafeStr = Field(default="", description="대용금평가금액(합계)")
    remn_repl_evlta: SafeStr = Field(default="", description="잔고대용평가금액")
    trst_remn_repl_evlta: SafeStr = Field(default="", description="위탁대용잔고평가금액")
    bncr_remn_repl_evlta: SafeStr = Field(default="", description="수익증권대용평가금액")
    profa_repl: SafeStr = Field(default="", description="위탁증거금대용")
    crd_grnta_repl: SafeStr = Field(default="", description="신용보증금대용")
    crd_grnt_repl: SafeStr = Field(default="", description="신용담보금대용")
    add_grnt_repl: SafeStr = Field(default="", description="추가담보금대용")
    rght_repl_amt: SafeStr = Field(default="", description="권리대용금")
    pymn_alow_amt: SafeStr = Field(default="", description="출금가능금액")
    wrap_pymn_alow_amt: SafeStr = Field(default="", description="랩출금가능금액")
    ord_alow_amt: SafeStr = Field(default="", description="주문가능금액")
    bncr_buy_alowa: SafeStr = Field(default="", description="수익증권매수가능금액")
    n_20stk_ord_alow_amt: SafeStr = Field(default="", alias="20stk_ord_alow_amt", description="20%종목주문가능금액")
    n_30stk_ord_alow_amt: SafeStr = Field(default="", alias="30stk_ord_alow_amt", description="30%종목주문가능금액")
    n_40stk_ord_alow_amt: SafeStr = Field(default="", alias="40stk_ord_alow_amt", description="40%종목주문가능금액")
    n_100stk_ord_alow_amt: SafeStr = Field(default="", alias="100stk_ord_alow_amt", description="100%종목주문가능금액")
    ch_uncla: SafeStr = Field(default="", description="현금미수금")
    ch_uncla_dlfe: SafeStr = Field(default="", description="현금미수연체료")
    ch_uncla_tot: SafeStr = Field(default="", description="현금미수금합계")
    crd_int_npay: SafeStr = Field(default="", description="신용이자미납")
    int_npay_amt_dlfe: SafeStr = Field(default="", description="신용이자미납연체료")
    int_npay_amt_tot: SafeStr = Field(default="", description="신용이자미납합계")
    etc_loana: SafeStr = Field(default="", description="기타대여금")
    etc_loana_dlfe: SafeStr = Field(default="", description="기타대여금연체료")
    etc_loan_tot: SafeStr = Field(default="", description="기타대여금합계")
    nrpy_loan: SafeStr = Field(default="", description="미상환융자금")
    loan_sum: SafeStr = Field(default="", description="융자금합계")
    ls_sum: SafeStr = Field(default="", description="대주금합계")
    crd_grnt_rt: SafeStr = Field(default="", description="신용담보비율")
    mdstrm_usfe: SafeStr = Field(default="", description="중도이용료")
    min_ord_alow_yn: SafeStr = Field(default="", description="최소주문가능금액")
    loan_remn_evlt_amt: SafeStr = Field(default="", description="대출총평가금액")
    dpst_grntl_remn: SafeStr = Field(default="", description="예탁담보대출잔고")
    sell_grntl_remn: SafeStr = Field(default="", description="매도담보대출잔고")
    d1_entra: SafeStr = Field(default="", description="d+1추정예수금")
    d1_slby_exct_amt: SafeStr = Field(default="", description="d+1매도매수정산금")
    d1_buy_exct_amt: SafeStr = Field(default="", description="d+1매수정산금")
    d1_out_rep_mor: SafeStr = Field(default="", description="d+1미수변제소요금")
    d1_sel_exct_amt: SafeStr = Field(default="", description="d+1매도정산금")
    d1_pymn_alow_amt: SafeStr = Field(default="", description="d+1출금가능금액")
    d2_entra: SafeStr = Field(default="", description="d+2추정예수금")
    d2_slby_exct_amt: SafeStr = Field(default="", description="d+2매도매수정산금")
    d2_buy_exct_amt: SafeStr = Field(default="", description="d+2매수정산금")
    d2_out_rep_mor: SafeStr = Field(default="", description="d+2미수변제소요금")
    d2_sel_exct_amt: SafeStr = Field(default="", description="d+2매도정산금")
    d2_pymn_alow_amt: SafeStr = Field(default="", description="d+2출금가능금액")
    n_50stk_ord_alow_amt: SafeStr = Field(default="", alias="50stk_ord_alow_amt", description="50%종목주문가능금액")
    n_60stk_ord_alow_amt: SafeStr = Field(default="", alias="60stk_ord_alow_amt", description="60%종목주문가능금액")
    stk_entr_prst: Annotated[List[DetailedDeposit_StkEntrPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별예수금")

class DailyEstimatedDepositedAssetRequest(BaseModel):
    """[kt00002] 일별추정예탁자산현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    start_dt: SafeStr = Field(default="", description="시작조회기간 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료조회기간 YYYYMMDD")

class DailyEstimatedDepositedAsset_DalyPrsmDpstAsetAmtPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    entr: SafeStr = Field(default="", description="예수금")
    grnt_use_amt: SafeStr = Field(default="", description="담보대출금")
    crd_loan: SafeStr = Field(default="", description="신용융자금")
    ls_grnt: SafeStr = Field(default="", description="대주담보금")
    repl_amt: SafeStr = Field(default="", description="대용금")
    prsm_dpst_aset_amt: SafeStr = Field(default="", description="추정예탁자산")
    prsm_dpst_aset_amt_bncr_skip: SafeStr = Field(default="", description="추정예탁자산수익증권제외")

class DailyEstimatedDepositedAsset(BaseModel):
    """[kt00002] 일별추정예탁자산현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_prsm_dpst_aset_amt_prst: Annotated[List[DailyEstimatedDepositedAsset_DalyPrsmDpstAsetAmtPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별추정예탁자산현황")

class EstimatedAssetRequest(BaseModel):
    """[kt00003] 추정자산조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="상장폐지조회구분 0:전체, 1:상장폐지종목제외")

class EstimatedAsset(BaseModel):
    """[kt00003] 추정자산조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prsm_dpst_aset_amt: SafeStr = Field(default="", description="추정예탁자산")

class AccountEvaluationRequest(BaseModel):
    """[kt00004] 계좌평가현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="상장폐지조회구분 0:전체, 1:상장폐지종목제외")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드")

class AccountEvaluation_StkAcntEvltPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    rmnd_qty: SafeStr = Field(default="", description="보유수량")
    avg_prc: SafeStr = Field(default="", description="평균단가")
    cur_prc: SafeStr = Field(default="", description="현재가")
    evlt_amt: SafeStr = Field(default="", description="평가금액")
    pl_amt: SafeStr = Field(default="", description="손익금액")
    pl_rt: SafeStr = Field(default="", description="손익율")
    loan_dt: SafeStr = Field(default="", description="대출일")
    pur_amt: SafeStr = Field(default="", description="매입금액")
    setl_remn: SafeStr = Field(default="", description="결제잔고")
    pred_buyq: SafeStr = Field(default="", description="전일매수수량")
    pred_sellq: SafeStr = Field(default="", description="전일매도수량")
    tdy_buyq: SafeStr = Field(default="", description="금일매수수량")
    tdy_sellq: SafeStr = Field(default="", description="금일매도수량")

class AccountEvaluation(BaseModel):
    """[kt00004] 계좌평가현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_nm: SafeStr = Field(default="", description="계좌명")
    brch_nm: SafeStr = Field(default="", description="지점명")
    entr: SafeStr = Field(default="", description="예수금")
    d2_entra: SafeStr = Field(default="", description="D+2추정예수금")
    tot_est_amt: SafeStr = Field(default="", description="유가잔고평가액")
    aset_evlt_amt: SafeStr = Field(default="", description="예탁자산평가액")
    tot_pur_amt: SafeStr = Field(default="", description="총매입금액")
    prsm_dpst_aset_amt: SafeStr = Field(default="", description="추정예탁자산")
    tot_grnt_sella: SafeStr = Field(default="", description="매도담보대출금")
    tdy_lspft_amt: SafeStr = Field(default="", description="당일투자원금")
    invt_bsamt: SafeStr = Field(default="", description="당월투자원금")
    lspft_amt: SafeStr = Field(default="", description="누적투자원금")
    tdy_lspft: SafeStr = Field(default="", description="당일투자손익")
    lspft2: SafeStr = Field(default="", description="당월투자손익")
    lspft: SafeStr = Field(default="", description="누적투자손익")
    tdy_lspft_rt: SafeStr = Field(default="", description="당일손익율")
    lspft_ratio: SafeStr = Field(default="", description="당월손익율")
    lspft_rt: SafeStr = Field(default="", description="누적손익율")
    stk_acnt_evlt_prst: Annotated[List[AccountEvaluation_StkAcntEvltPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별계좌평가현황")

class TransactionBalanceRequest(BaseModel):
    """[kt00005] 체결잔고요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드")

class TransactionBalance_StkCntrRemn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    crd_tp: SafeStr = Field(default="", description="신용구분")
    loan_dt: SafeStr = Field(default="", description="대출일")
    expr_dt: SafeStr = Field(default="", description="만기일")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    setl_remn: SafeStr = Field(default="", description="결제잔고")
    cur_qty: SafeStr = Field(default="", description="현재잔고")
    cur_prc: SafeStr = Field(default="", description="현재가")
    buy_uv: SafeStr = Field(default="", description="매입단가")
    pur_amt: SafeStr = Field(default="", description="매입금액")
    evlt_amt: SafeStr = Field(default="", description="평가금액")
    evltv_prft: SafeStr = Field(default="", description="평가손익")
    pl_rt: SafeStr = Field(default="", description="손익률")

class TransactionBalance(BaseModel):
    """[kt00005] 체결잔고요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    entr: SafeStr = Field(default="", description="예수금")
    entr_d1: SafeStr = Field(default="", description="예수금D+1")
    entr_d2: SafeStr = Field(default="", description="예수금D+2")
    pymn_alow_amt: SafeStr = Field(default="", description="출금가능금액")
    uncl_stk_amt: SafeStr = Field(default="", description="미수확보금")
    repl_amt: SafeStr = Field(default="", description="대용금")
    rght_repl_amt: SafeStr = Field(default="", description="권리대용금")
    ord_alowa: SafeStr = Field(default="", description="주문가능현금")
    ch_uncla: SafeStr = Field(default="", description="현금미수금")
    crd_int_npay_gold: SafeStr = Field(default="", description="신용이자미납금")
    etc_loana: SafeStr = Field(default="", description="기타대여금")
    nrpy_loan: SafeStr = Field(default="", description="미상환융자금")
    profa_ch: SafeStr = Field(default="", description="증거금현금")
    repl_profa: SafeStr = Field(default="", description="증거금대용")
    stk_buy_tot_amt: SafeStr = Field(default="", description="주식매수총액")
    evlt_amt_tot: SafeStr = Field(default="", description="평가금액합계")
    tot_pl_tot: SafeStr = Field(default="", description="총손익합계")
    tot_pl_rt: SafeStr = Field(default="", description="총손익률")
    tot_re_buy_alowa: SafeStr = Field(default="", description="총재매수가능금액")
    n_20ord_alow_amt: SafeStr = Field(default="", alias="20ord_alow_amt", description="20%주문가능금액")
    n_30ord_alow_amt: SafeStr = Field(default="", alias="30ord_alow_amt", description="30%주문가능금액")
    n_40ord_alow_amt: SafeStr = Field(default="", alias="40ord_alow_amt", description="40%주문가능금액")
    n_50ord_alow_amt: SafeStr = Field(default="", alias="50ord_alow_amt", description="50%주문가능금액")
    n_60ord_alow_amt: SafeStr = Field(default="", alias="60ord_alow_amt", description="60%주문가능금액")
    n_100ord_alow_amt: SafeStr = Field(default="", alias="100ord_alow_amt", description="100%주문가능금액")
    crd_loan_tot: SafeStr = Field(default="", description="신용융자합계")
    crd_loan_ls_tot: SafeStr = Field(default="", description="신용융자대주합계")
    crd_grnt_rt: SafeStr = Field(default="", description="신용담보비율")
    dpst_grnt_use_amt_amt: SafeStr = Field(default="", description="예탁담보대출금액")
    grnt_loan_amt: SafeStr = Field(default="", description="매도담보대출금액")
    stk_cntr_remn: Annotated[List[TransactionBalance_StkCntrRemn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별체결잔고")

class OrderDetailsByAccountRequest(BaseModel):
    """[kt00007] 계좌별주문체결내역상세요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_dt: SafeStr = Field(default="", description="주문일자 YYYYMMDD")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:주문순, 2:역순, 3:미체결, 4:체결내역만")
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분 0:전체, 1:주식, 2:채권")
    sell_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    stk_cd: SafeStr = Field(default="", description="종목코드 공백허용 (공백일때 전체종목)")
    fr_ord_no: SafeStr = Field(default="", description="시작주문번호 공백허용 (공백일때 전체주문)")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행")

class OrderDetailsByAccount_AcntOrdCntrPrpsDtl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ord_no: SafeStr = Field(default="", description="주문번호")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    crd_tp: SafeStr = Field(default="", description="신용구분")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    cnfm_qty: SafeStr = Field(default="", description="확인수량")
    acpt_tp: SafeStr = Field(default="", description="접수구분")
    rsrv_tp: SafeStr = Field(default="", description="반대여부")
    ord_tm: SafeStr = Field(default="", description="주문시간")
    ori_ord: SafeStr = Field(default="", description="원주문")
    stk_nm: SafeStr = Field(default="", description="종목명")
    io_tp_nm: SafeStr = Field(default="", description="주문구분")
    loan_dt: SafeStr = Field(default="", description="대출일")
    cntr_qty: SafeStr = Field(default="", description="체결수량")
    cntr_uv: SafeStr = Field(default="", description="체결단가")
    ord_remnq: SafeStr = Field(default="", description="주문잔량")
    comm_ord_tp: SafeStr = Field(default="", description="통신구분")
    mdfy_cncl: SafeStr = Field(default="", description="정정취소")
    cnfm_tm: SafeStr = Field(default="", description="확인시간")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")
    cond_uv: SafeStr = Field(default="", description="스톱가")

class OrderDetailsByAccount(BaseModel):
    """[kt00007] 계좌별주문체결내역상세요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_cntr_prps_dtl: Annotated[List[OrderDetailsByAccount_AcntOrdCntrPrpsDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결내역상세")

class NextDayPaymentScheduleDetailsByAccountRequest(BaseModel):
    """[kt00008] 계좌별익일결제예정내역요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dcd_seq: SafeStr = Field(default="", description="시작결제번호")

class NextDayPaymentScheduleDetailsByAccount_AcntNxdySetlFrcsPrpsArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    seq: SafeStr = Field(default="", description="일련번호")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    loan_dt: SafeStr = Field(default="", description="대출일")
    qty: SafeStr = Field(default="", description="수량")
    engg_amt: SafeStr = Field(default="", description="약정금액")
    cmsn: SafeStr = Field(default="", description="수수료")
    incm_tax: SafeStr = Field(default="", description="소득세")
    rstx: SafeStr = Field(default="", description="농특세")
    stk_nm: SafeStr = Field(default="", description="종목명")
    sell_tp: SafeStr = Field(default="", description="매도수구분")
    unp: SafeStr = Field(default="", description="단가")
    exct_amt: SafeStr = Field(default="", description="정산금액")
    trde_tax: SafeStr = Field(default="", description="거래세")
    resi_tax: SafeStr = Field(default="", description="주민세")
    crd_tp: SafeStr = Field(default="", description="신용구분")

class NextDayPaymentScheduleDetailsByAccount(BaseModel):
    """[kt00008] 계좌별익일결제예정내역요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_dt: SafeStr = Field(default="", description="매매일자")
    setl_dt: SafeStr = Field(default="", description="결제일자")
    sell_amt_sum: SafeStr = Field(default="", description="매도정산합")
    buy_amt_sum: SafeStr = Field(default="", description="매수정산합")
    acnt_nxdy_setl_frcs_prps_array: Annotated[List[NextDayPaymentScheduleDetailsByAccount_AcntNxdySetlFrcsPrpsArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별익일결제예정내역배열")

class OrderExecutionByAccountRequest(BaseModel):
    """[kt00009] 계좌별주문체결현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_dt: SafeStr = Field(default="", description="주문일자 YYYYMMDD")
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분 0:전체, 1:주식, 2:채권")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN")
    sell_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    qry_tp: SafeStr = Field(default="", description="조회구분 0:전체, 1:체결")
    stk_cd: SafeStr = Field(default="", description="종목코드 전문 조회할 종목코드")
    fr_ord_no: SafeStr = Field(default="", description="시작주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행")

class OrderExecutionByAccount_AcntOrdCntrPrstArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분")
    ord_no: SafeStr = Field(default="", description="주문번호")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    io_tp_nm: SafeStr = Field(default="", description="주문유형구분")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    cnfm_qty: SafeStr = Field(default="", description="확인수량")
    rsrv_oppo: SafeStr = Field(default="", description="예약/반대")
    cntr_no: SafeStr = Field(default="", description="체결번호")
    acpt_tp: SafeStr = Field(default="", description="접수구분")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    setl_tp: SafeStr = Field(default="", description="결제구분")
    crd_deal_tp: SafeStr = Field(default="", description="신용거래구분")
    cntr_qty: SafeStr = Field(default="", description="체결수량")
    cntr_uv: SafeStr = Field(default="", description="체결단가")
    comm_ord_tp: SafeStr = Field(default="", description="통신구분")
    mdfy_cncl_tp: SafeStr = Field(default="", description="정정/취소구분")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")
    cond_uv: SafeStr = Field(default="", description="스톱가")

class OrderExecutionByAccount(BaseModel):
    """[kt00009] 계좌별주문체결현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sell_grntl_engg_amt: SafeStr = Field(default="", description="매도약정금액")
    buy_engg_amt: SafeStr = Field(default="", description="매수약정금액")
    engg_amt: SafeStr = Field(default="", description="약정금액")
    acnt_ord_cntr_prst_array: Annotated[List[OrderExecutionByAccount_AcntOrdCntrPrstArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결현황배열")

class OrderWithdrawalAmountRequest(BaseModel):
    """[kt00010] 주문인출가능금액요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    io_amt: SafeStr = Field(default="", description="입출금액")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:매도, 2:매수")
    trde_qty: SafeStr = Field(default="", description="매매수량")
    uv: SafeStr = Field(default="", description="매수가격")
    exp_buy_unp: SafeStr = Field(default="", description="예상매수단가")

class OrderWithdrawalAmount(BaseModel):
    """[kt00010] 주문인출가능금액요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    profa_20ord_alow_amt: SafeStr = Field(default="", description="증거금20%주문가능금액")
    profa_20ord_alowq: SafeStr = Field(default="", description="증거금20%주문가능수량")
    profa_30ord_alow_amt: SafeStr = Field(default="", description="증거금30%주문가능금액")
    profa_30ord_alowq: SafeStr = Field(default="", description="증거금30%주문가능수량")
    profa_40ord_alow_amt: SafeStr = Field(default="", description="증거금40%주문가능금액")
    profa_40ord_alowq: SafeStr = Field(default="", description="증거금40%주문가능수량")
    profa_50ord_alow_amt: SafeStr = Field(default="", description="증거금50%주문가능금액")
    profa_50ord_alowq: SafeStr = Field(default="", description="증거금50%주문가능수량")
    profa_60ord_alow_amt: SafeStr = Field(default="", description="증거금60%주문가능금액")
    profa_60ord_alowq: SafeStr = Field(default="", description="증거금60%주문가능수량")
    profa_rdex_60ord_alow_amt: SafeStr = Field(default="", description="증거금감면60%주문가능금")
    profa_rdex_60ord_alowq: SafeStr = Field(default="", description="증거금감면60%주문가능수")
    profa_100ord_alow_amt: SafeStr = Field(default="", description="증거금100%주문가능금액")
    profa_100ord_alowq: SafeStr = Field(default="", description="증거금100%주문가능수량")
    pred_reu_alowa: SafeStr = Field(default="", description="전일재사용가능금액")
    tdy_reu_alowa: SafeStr = Field(default="", description="금일재사용가능금액")
    entr: SafeStr = Field(default="", description="예수금")
    repl_amt: SafeStr = Field(default="", description="대용금")
    uncla: SafeStr = Field(default="", description="미수금")
    ord_pos_repl: SafeStr = Field(default="", description="주문가능대용")
    ord_alowa: SafeStr = Field(default="", description="주문가능현금")
    wthd_alowa: SafeStr = Field(default="", description="인출가능금액")
    nxdy_wthd_alowa: SafeStr = Field(default="", description="익일인출가능금액")
    pur_amt: SafeStr = Field(default="", description="매입금액")
    cmsn: SafeStr = Field(default="", description="수수료")
    pur_exct_amt: SafeStr = Field(default="", description="매입정산금")
    d2entra: SafeStr = Field(default="", description="D2추정예수금")
    profa_rdex_aplc_tp: SafeStr = Field(default="", description="증거금감면적용구분 0:일반,1:60%감면")

class QuantityAvailableOrderByMarginRateRequest(BaseModel):
    """[kt00011] 증거금율별주문가능수량조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    uv: SafeStr = Field(default="", description="매수가격")

class QuantityAvailableOrderByMarginRate(BaseModel):
    """[kt00011] 증거금율별주문가능수량조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_profa_rt: SafeStr = Field(default="", description="종목증거금율")
    profa_rt: SafeStr = Field(default="", description="계좌증거금율")
    aplc_rt: SafeStr = Field(default="", description="적용증거금율")
    profa_20ord_alow_amt: SafeStr = Field(default="", description="증거금20%주문가능금액")
    profa_20ord_alowq: SafeStr = Field(default="", description="증거금20%주문가능수량")
    profa_20pred_reu_amt: SafeStr = Field(default="", description="증거금20%전일재사용금액")
    profa_20tdy_reu_amt: SafeStr = Field(default="", description="증거금20%금일재사용금액")
    profa_30ord_alow_amt: SafeStr = Field(default="", description="증거금30%주문가능금액")
    profa_30ord_alowq: SafeStr = Field(default="", description="증거금30%주문가능수량")
    profa_30pred_reu_amt: SafeStr = Field(default="", description="증거금30%전일재사용금액")
    profa_30tdy_reu_amt: SafeStr = Field(default="", description="증거금30%금일재사용금액")
    profa_40ord_alow_amt: SafeStr = Field(default="", description="증거금40%주문가능금액")
    profa_40ord_alowq: SafeStr = Field(default="", description="증거금40%주문가능수량")
    profa_40pred_reu_amt: SafeStr = Field(default="", description="증거금40전일재사용금액")
    profa_40tdy_reu_amt: SafeStr = Field(default="", description="증거금40%금일재사용금액")
    profa_50ord_alow_amt: SafeStr = Field(default="", description="증거금50%주문가능금액")
    profa_50ord_alowq: SafeStr = Field(default="", description="증거금50%주문가능수량")
    profa_50pred_reu_amt: SafeStr = Field(default="", description="증거금50%전일재사용금액")
    profa_50tdy_reu_amt: SafeStr = Field(default="", description="증거금50%금일재사용금액")
    profa_60ord_alow_amt: SafeStr = Field(default="", description="증거금60%주문가능금액")
    profa_60ord_alowq: SafeStr = Field(default="", description="증거금60%주문가능수량")
    profa_60pred_reu_amt: SafeStr = Field(default="", description="증거금60%전일재사용금액")
    profa_60tdy_reu_amt: SafeStr = Field(default="", description="증거금60%금일재사용금액")
    profa_100ord_alow_amt: SafeStr = Field(default="", description="증거금100%주문가능금액")
    profa_100ord_alowq: SafeStr = Field(default="", description="증거금100%주문가능수량")
    profa_100pred_reu_amt: SafeStr = Field(default="", description="증거금100%전일재사용금액")
    profa_100tdy_reu_amt: SafeStr = Field(default="", description="증거금100%금일재사용금액")
    min_ord_alow_amt: SafeStr = Field(default="", description="미수불가주문가능금액")
    min_ord_alowq: SafeStr = Field(default="", description="미수불가주문가능수량")
    min_pred_reu_amt: SafeStr = Field(default="", description="미수불가전일재사용금액")
    min_tdy_reu_amt: SafeStr = Field(default="", description="미수불가금일재사용금액")
    entr: SafeStr = Field(default="", description="예수금")
    repl_amt: SafeStr = Field(default="", description="대용금")
    uncla: SafeStr = Field(default="", description="미수금")
    ord_pos_repl: SafeStr = Field(default="", description="주문가능대용")
    ord_alowa: SafeStr = Field(default="", description="주문가능현금")

class QuantityAvailableOrderByCreditDepositRateRequest(BaseModel):
    """[kt00012] 신용보증금율별주문가능수량조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    uv: SafeStr = Field(default="", description="매수가격")

class QuantityAvailableOrderByCreditDepositRate(BaseModel):
    """[kt00012] 신용보증금율별주문가능수량조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_assr_rt: SafeStr = Field(default="", description="종목보증금율")
    stk_assr_rt_nm: SafeStr = Field(default="", description="종목보증금율명")
    assr_30ord_alow_amt: SafeStr = Field(default="", description="보증금30%주문가능금액")
    assr_30ord_alowq: SafeStr = Field(default="", description="보증금30%주문가능수량")
    assr_30pred_reu_amt: SafeStr = Field(default="", description="보증금30%전일재사용금액")
    assr_30tdy_reu_amt: SafeStr = Field(default="", description="보증금30%금일재사용금액")
    assr_40ord_alow_amt: SafeStr = Field(default="", description="보증금40%주문가능금액")
    assr_40ord_alowq: SafeStr = Field(default="", description="보증금40%주문가능수량")
    assr_40pred_reu_amt: SafeStr = Field(default="", description="보증금40%전일재사용금액")
    assr_40tdy_reu_amt: SafeStr = Field(default="", description="보증금40%금일재사용금액")
    assr_50ord_alow_amt: SafeStr = Field(default="", description="보증금50%주문가능금액")
    assr_50ord_alowq: SafeStr = Field(default="", description="보증금50%주문가능수량")
    assr_50pred_reu_amt: SafeStr = Field(default="", description="보증금50%전일재사용금액")
    assr_50tdy_reu_amt: SafeStr = Field(default="", description="보증금50%금일재사용금액")
    assr_60ord_alow_amt: SafeStr = Field(default="", description="보증금60%주문가능금액")
    assr_60ord_alowq: SafeStr = Field(default="", description="보증금60%주문가능수량")
    assr_60pred_reu_amt: SafeStr = Field(default="", description="보증금60%전일재사용금액")
    assr_60tdy_reu_amt: SafeStr = Field(default="", description="보증금60%금일재사용금액")
    entr: SafeStr = Field(default="", description="예수금")
    repl_amt: SafeStr = Field(default="", description="대용금")
    uncla: SafeStr = Field(default="", description="미수금")
    ord_pos_repl: SafeStr = Field(default="", description="주문가능대용")
    ord_alowa: SafeStr = Field(default="", description="주문가능현금")
    out_alowa: SafeStr = Field(default="", description="미수가능금액")
    out_pos_qty: SafeStr = Field(default="", description="미수가능수량")
    min_amt: SafeStr = Field(default="", description="미수불가금액")
    min_qty: SafeStr = Field(default="", description="미수불가수량")

class MarginDetailsRequest(BaseModel):
    """[kt00013] 증거금세부내역조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class MarginDetails(BaseModel):
    """[kt00013] 증거금세부내역조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_reu_objt_amt: SafeStr = Field(default="", description="금일재사용대상금액")
    tdy_reu_use_amt: SafeStr = Field(default="", description="금일재사용사용금액")
    tdy_reu_alowa: SafeStr = Field(default="", description="금일재사용가능금액")
    tdy_reu_lmtt_amt: SafeStr = Field(default="", description="금일재사용제한금액")
    tdy_reu_alowa_fin: SafeStr = Field(default="", description="금일재사용가능금액최종")
    pred_reu_objt_amt: SafeStr = Field(default="", description="전일재사용대상금액")
    pred_reu_use_amt: SafeStr = Field(default="", description="전일재사용사용금액")
    pred_reu_alowa: SafeStr = Field(default="", description="전일재사용가능금액")
    pred_reu_lmtt_amt: SafeStr = Field(default="", description="전일재사용제한금액")
    pred_reu_alowa_fin: SafeStr = Field(default="", description="전일재사용가능금액최종")
    ch_amt: SafeStr = Field(default="", description="현금금액")
    ch_profa: SafeStr = Field(default="", description="현금증거금")
    use_pos_ch: SafeStr = Field(default="", description="사용가능현금")
    ch_use_lmtt_amt: SafeStr = Field(default="", description="현금사용제한금액")
    use_pos_ch_fin: SafeStr = Field(default="", description="사용가능현금최종")
    repl_amt_amt: SafeStr = Field(default="", description="대용금액")
    repl_profa: SafeStr = Field(default="", description="대용증거금")
    use_pos_repl: SafeStr = Field(default="", description="사용가능대용")
    repl_use_lmtt_amt: SafeStr = Field(default="", description="대용사용제한금액")
    use_pos_repl_fin: SafeStr = Field(default="", description="사용가능대용최종")
    crd_grnta_ch: SafeStr = Field(default="", description="신용보증금현금")
    crd_grnta_repl: SafeStr = Field(default="", description="신용보증금대용")
    crd_grnt_ch: SafeStr = Field(default="", description="신용담보금현금")
    crd_grnt_repl: SafeStr = Field(default="", description="신용담보금대용")
    uncla: SafeStr = Field(default="", description="미수금")
    ls_grnt_reu_gold: SafeStr = Field(default="", description="대주담보금재사용금")
    n_20ord_alow_amt: SafeStr = Field(default="", alias="20ord_alow_amt", description="20%주문가능금액")
    n_30ord_alow_amt: SafeStr = Field(default="", alias="30ord_alow_amt", description="30%주문가능금액")
    n_40ord_alow_amt: SafeStr = Field(default="", alias="40ord_alow_amt", description="40%주문가능금액")
    n_50ord_alow_amt: SafeStr = Field(default="", alias="50ord_alow_amt", description="50%주문가능금액")
    n_60ord_alow_amt: SafeStr = Field(default="", alias="60ord_alow_amt", description="60%주문가능금액")
    n_100ord_alow_amt: SafeStr = Field(default="", alias="100ord_alow_amt", description="100%주문가능금액")
    tdy_crd_rpya_loss_amt: SafeStr = Field(default="", description="금일신용상환손실금액")
    pred_crd_rpya_loss_amt: SafeStr = Field(default="", description="전일신용상환손실금액")
    tdy_ls_rpya_loss_repl_profa: SafeStr = Field(default="", description="금일대주상환손실대용증거금")
    pred_ls_rpya_loss_repl_profa: SafeStr = Field(default="", description="전일대주상환손실대용증거금")
    evlt_repl_amt_spg_use_skip: SafeStr = Field(default="", description="평가대용금(현물사용제외)")
    evlt_repl_rt: SafeStr = Field(default="", description="평가대용비율")
    crd_repl_profa: SafeStr = Field(default="", description="신용대용증거금")
    ch_ord_repl_profa: SafeStr = Field(default="", description="현금주문대용증거금")
    crd_ord_repl_profa: SafeStr = Field(default="", description="신용주문대용증거금")
    crd_repl_conv_gold: SafeStr = Field(default="", description="신용대용환산금")
    repl_alowa: SafeStr = Field(default="", description="대용가능금액(현금제한)")
    repl_alowa_2: SafeStr = Field(default="", description="대용가능금액2(신용제한)")
    ch_repl_lck_gold: SafeStr = Field(default="", description="현금대용부족금")
    crd_repl_lck_gold: SafeStr = Field(default="", description="신용대용부족금")
    ch_ord_alow_repla: SafeStr = Field(default="", description="현금주문가능대용금")
    crd_ord_alow_repla: SafeStr = Field(default="", description="신용주문가능대용금")
    d2vexct_entr: SafeStr = Field(default="", description="D2가정산예수금")
    d2ch_ord_alow_amt: SafeStr = Field(default="", description="D2현금주문가능금액")

class ComprehensiveConsignmentTransactionDetailsRequest(BaseModel):
    """[kt00015] 위탁종합거래내역요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자")
    end_dt: SafeStr = Field(default="", description="종료일자")
    tp: SafeStr = Field(default="", description="구분 0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,6:입금,7:출금,A:예탁담보대출입금,B:매도담보대출입금,C:현금상환(융자,담보상환),F:환전,M:입출금+환전,G:외화매수,H:외화매도,I:환전정산입금,J:환전정산출금")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    crnc_cd: SafeStr = Field(default="", description="통화코드")
    gds_tp: SafeStr = Field(default="", description="상품구분 0:전체, 1:국내주식, 2:수익증권, 3:해외주식, 4:금융상품")
    frgn_stex_code: SafeStr = Field(default="", description="해외거래소코드")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드")

class ComprehensiveConsignmentTransactionDetails_TrstOvrlTrdePrpsArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    trde_dt: SafeStr = Field(default="", description="거래일자")
    trde_no: SafeStr = Field(default="", description="거래번호")
    rmrk_nm: SafeStr = Field(default="", description="적요명")
    crd_deal_tp_nm: SafeStr = Field(default="", description="신용거래구분명")
    exct_amt: SafeStr = Field(default="", description="정산금액")
    loan_amt_rpya: SafeStr = Field(default="", description="대출금상환")
    fc_trde_amt: SafeStr = Field(default="", description="거래금액(외)")
    fc_exct_amt: SafeStr = Field(default="", description="정산금액(외)")
    entra_remn: SafeStr = Field(default="", description="예수금잔고")
    crnc_cd: SafeStr = Field(default="", description="통화코드")
    trde_ocr_tp: SafeStr = Field(default="", description="거래종류구분 1:입출금, 2:펀드, 3:ELS, 4:채권, 5:해외채권, 6:외화RP, 7:외화발행어음")
    trde_kind_nm: SafeStr = Field(default="", description="거래종류명")
    stk_nm: SafeStr = Field(default="", description="종목명")
    trde_amt: SafeStr = Field(default="", description="거래금액")
    trde_agri_tax: SafeStr = Field(default="", description="거래및농특세")
    rpy_diffa: SafeStr = Field(default="", description="상환차금")
    fc_trde_tax: SafeStr = Field(default="", description="거래세(외)")
    dly_sum: SafeStr = Field(default="", description="연체합")
    fc_entra: SafeStr = Field(default="", description="외화예수금잔고")
    mdia_tp_nm: SafeStr = Field(default="", description="매체구분명")
    io_tp: SafeStr = Field(default="", description="입출구분")
    io_tp_nm: SafeStr = Field(default="", description="입출구분명")
    orig_deal_no: SafeStr = Field(default="", description="원거래번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    trde_qty_jwa_cnt: SafeStr = Field(default="", description="거래수량/좌수")
    cmsn: SafeStr = Field(default="", description="수수료")
    int_ls_usfe: SafeStr = Field(default="", description="이자/대주이용")
    fc_cmsn: SafeStr = Field(default="", description="수수료(외)")
    fc_dly_sum: SafeStr = Field(default="", description="연체합(외)")
    vlbl_nowrm: SafeStr = Field(default="", description="유가금잔")
    proc_tm: SafeStr = Field(default="", description="처리시간")
    isin_cd: SafeStr = Field(default="", description="ISIN코드")
    stex_cd: SafeStr = Field(default="", description="거래소코드")
    stex_nm: SafeStr = Field(default="", description="거래소명")
    trde_unit: SafeStr = Field(default="", description="거래단가/환율")
    incm_resi_tax: SafeStr = Field(default="", description="소득/주민세")
    loan_dt: SafeStr = Field(default="", description="대출일")
    uncl_ocr: SafeStr = Field(default="", description="미수(원/주)")
    rpym_sum: SafeStr = Field(default="", description="변제합")
    cntr_dt: SafeStr = Field(default="", description="체결일")
    rcpy_no: SafeStr = Field(default="", description="출납번호")
    prcsr: SafeStr = Field(default="", description="처리자")
    proc_brch: SafeStr = Field(default="", description="처리점")
    trde_stle: SafeStr = Field(default="", description="매매형태")
    txon_base_pric: SafeStr = Field(default="", description="과세기준가")
    tax_sum_cmsn: SafeStr = Field(default="", description="세금수수료합")
    frgn_pay_txam: SafeStr = Field(default="", description="외국납부세액(외)")
    fc_uncl_ocr: SafeStr = Field(default="", description="미수(외)")
    rpym_sum_fr: SafeStr = Field(default="", description="변제합(외)")
    rcpmnyer: SafeStr = Field(default="", description="입금자")
    trde_prtc_tp: SafeStr = Field(default="", description="거래내역구분")

class ComprehensiveConsignmentTransactionDetails(BaseModel):
    """[kt00015] 위탁종합거래내역요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trst_ovrl_trde_prps_array: Annotated[List[ComprehensiveConsignmentTransactionDetails_TrstOvrlTrdePrpsArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="위탁종합거래내역배열")

class DetailedDailyAccountReturnsRequest(BaseModel):
    """[kt00016] 일별계좌수익률상세현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    fr_dt: SafeStr = Field(default="", description="평가시작일")
    to_dt: SafeStr = Field(default="", description="평가종료일")

class DetailedDailyAccountReturns(BaseModel):
    """[kt00016] 일별계좌수익률상세현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    mang_empno: SafeStr = Field(default="", description="관리사원번호")
    mngr_nm: SafeStr = Field(default="", description="관리자명")
    dept_nm: SafeStr = Field(default="", description="관리자지점")
    entr_fr: SafeStr = Field(default="", description="예수금_초")
    entr_to: SafeStr = Field(default="", description="예수금_말")
    scrt_evlt_amt_fr: SafeStr = Field(default="", description="유가증권평가금액_초")
    scrt_evlt_amt_to: SafeStr = Field(default="", description="유가증권평가금액_말")
    ls_grnt_fr: SafeStr = Field(default="", description="대주담보금_초")
    ls_grnt_to: SafeStr = Field(default="", description="대주담보금_말")
    crd_loan_fr: SafeStr = Field(default="", description="신용융자금_초")
    crd_loan_to: SafeStr = Field(default="", description="신용융자금_말")
    ch_uncla_fr: SafeStr = Field(default="", description="현금미수금_초")
    ch_uncla_to: SafeStr = Field(default="", description="현금미수금_말")
    krw_asgna_fr: SafeStr = Field(default="", description="원화대용금_초")
    krw_asgna_to: SafeStr = Field(default="", description="원화대용금_말")
    ls_evlta_fr: SafeStr = Field(default="", description="대주평가금_초")
    ls_evlta_to: SafeStr = Field(default="", description="대주평가금_말")
    rght_evlta_fr: SafeStr = Field(default="", description="권리평가금_초")
    rght_evlta_to: SafeStr = Field(default="", description="권리평가금_말")
    loan_amt_fr: SafeStr = Field(default="", description="대출금_초")
    loan_amt_to: SafeStr = Field(default="", description="대출금_말")
    etc_loana_fr: SafeStr = Field(default="", description="기타대여금_초")
    etc_loana_to: SafeStr = Field(default="", description="기타대여금_말")
    crd_int_npay_gold_fr: SafeStr = Field(default="", description="신용이자미납금_초")
    crd_int_npay_gold_to: SafeStr = Field(default="", description="신용이자미납금_말")
    crd_int_fr: SafeStr = Field(default="", description="신용이자_초")
    crd_int_to: SafeStr = Field(default="", description="신용이자_말")
    tot_amt_fr: SafeStr = Field(default="", description="순자산액계_초")
    tot_amt_to: SafeStr = Field(default="", description="순자산액계_말")
    invt_bsamt: SafeStr = Field(default="", description="투자원금평잔")
    evltv_prft: SafeStr = Field(default="", description="평가손익")
    prft_rt: SafeStr = Field(default="", description="수익률")
    tern_rt: SafeStr = Field(default="", description="회전율")
    termin_tot_trns: SafeStr = Field(default="", description="기간내총입금")
    termin_tot_pymn: SafeStr = Field(default="", description="기간내총출금")
    termin_tot_inq: SafeStr = Field(default="", description="기간내총입고")
    termin_tot_outq: SafeStr = Field(default="", description="기간내총출고")
    futr_repl_sella: SafeStr = Field(default="", description="선물대용매도금액")
    trst_repl_sella: SafeStr = Field(default="", description="위탁대용매도금액")

class DailyByAccountRequest(BaseModel):
    """[kt00017] 계좌별당일현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class DailyByAccount(BaseModel):
    """[kt00017] 계좌별당일현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    d2_entra: SafeStr = Field(default="", description="D+2추정예수금")
    crd_int_npay_gold: SafeStr = Field(default="", description="신용이자미납금")
    etc_loana: SafeStr = Field(default="", description="기타대여금")
    gnrl_stk_evlt_amt_d2: SafeStr = Field(default="", description="일반주식평가금액D+2")
    dpst_grnt_use_amt_d2: SafeStr = Field(default="", description="예탁담보대출금D+2")
    crd_stk_evlt_amt_d2: SafeStr = Field(default="", description="예탁담보주식평가금액D+2")
    crd_loan_d2: SafeStr = Field(default="", description="신용융자금D+2")
    crd_loan_evlta_d2: SafeStr = Field(default="", description="신용융자평가금D+2")
    crd_ls_grnt_d2: SafeStr = Field(default="", description="신용대주담보금D+2")
    crd_ls_evlta_d2: SafeStr = Field(default="", description="신용대주평가금D+2")
    ina_amt: SafeStr = Field(default="", description="입금금액")
    outa: SafeStr = Field(default="", description="출금금액")
    inq_amt: SafeStr = Field(default="", description="입고금액")
    outq_amt: SafeStr = Field(default="", description="출고금액")
    sell_amt: SafeStr = Field(default="", description="매도금액")
    buy_amt: SafeStr = Field(default="", description="매수금액")
    cmsn: SafeStr = Field(default="", description="수수료")
    tax: SafeStr = Field(default="", description="세금")
    stk_pur_cptal_loan_amt: SafeStr = Field(default="", description="주식매입자금대출금")
    rp_evlt_amt: SafeStr = Field(default="", description="RP평가금액")
    bd_evlt_amt: SafeStr = Field(default="", description="채권평가금액")
    elsevlt_amt: SafeStr = Field(default="", description="ELS평가금액")
    crd_int_amt: SafeStr = Field(default="", description="신용이자금액")
    sel_prica_grnt_loan_int_amt_amt: SafeStr = Field(default="", description="매도대금담보대출이자금액")
    dvida_amt: SafeStr = Field(default="", description="배당금액")

class AccountEvaluationBalanceDetailsRequest(BaseModel):
    """[kt00018] 계좌평가잔고내역요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:합산, 2:개별")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드")

class AccountEvaluationBalanceDetails_AcntEvltRemnIndvTot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    evltv_prft: SafeStr = Field(default="", description="평가손익")
    prft_rt: SafeStr = Field(default="", description="수익률(%)")
    pur_pric: SafeStr = Field(default="", description="매입가")
    pred_close_pric: SafeStr = Field(default="", description="전일종가")
    rmnd_qty: SafeStr = Field(default="", description="보유수량")
    trde_able_qty: SafeStr = Field(default="", description="매매가능수량")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_buyq: SafeStr = Field(default="", description="전일매수수량")
    pred_sellq: SafeStr = Field(default="", description="전일매도수량")
    tdy_buyq: SafeStr = Field(default="", description="금일매수수량")
    tdy_sellq: SafeStr = Field(default="", description="금일매도수량")
    pur_amt: SafeStr = Field(default="", description="매입금액")
    pur_cmsn: SafeStr = Field(default="", description="매입수수료")
    evlt_amt: SafeStr = Field(default="", description="평가금액")
    sell_cmsn: SafeStr = Field(default="", description="평가수수료")
    tax: SafeStr = Field(default="", description="세금")
    sum_cmsn: SafeStr = Field(default="", description="수수료합 매입수수료 + 평가수수료")
    poss_rt: SafeStr = Field(default="", description="보유비중(%)")
    crd_tp: SafeStr = Field(default="", description="신용구분")
    crd_tp_nm: SafeStr = Field(default="", description="신용구분명")
    crd_loan_dt: SafeStr = Field(default="", description="대출일")

class AccountEvaluationBalanceDetails(BaseModel):
    """[kt00018] 계좌평가잔고내역요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_pur_amt: SafeStr = Field(default="", description="총매입금액")
    tot_evlt_amt: SafeStr = Field(default="", description="총평가금액")
    tot_evlt_pl: SafeStr = Field(default="", description="총평가손익금액")
    tot_prft_rt: SafeStr = Field(default="", description="총수익률(%)")
    prsm_dpst_aset_amt: SafeStr = Field(default="", description="추정예탁자산")
    tot_loan_amt: SafeStr = Field(default="", description="총대출금")
    tot_crd_loan_amt: SafeStr = Field(default="", description="총융자금액")
    tot_crd_ls_amt: SafeStr = Field(default="", description="총대주금액")
    acnt_evlt_remn_indv_tot: Annotated[List[AccountEvaluationBalanceDetails_AcntEvltRemnIndvTot], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌평가잔고개별합산")

class CheckGoldSpotBalanceRequest(BaseModel):
    """[kt50020] 금현물 잔고확인 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class CheckGoldSpotBalance_GoldAcntEvltPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    real_qty: SafeStr = Field(default="", description="보유수량")
    avg_prc: SafeStr = Field(default="", description="평균단가")
    cur_prc: SafeStr = Field(default="", description="현재가")
    est_amt: SafeStr = Field(default="", description="평가금액")
    est_lspft: SafeStr = Field(default="", description="손익금액")
    est_ratio: SafeStr = Field(default="", description="손익율")
    cmsn: SafeStr = Field(default="", description="수수료")
    vlad_tax: SafeStr = Field(default="", description="부가가치세")
    book_amt2: SafeStr = Field(default="", description="매입금액")
    pl_prch_prc: SafeStr = Field(default="", description="손익분기매입가")
    qty: SafeStr = Field(default="", description="결제잔고")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    able_qty: SafeStr = Field(default="", description="가능수량")

class CheckGoldSpotBalance(BaseModel):
    """[kt50020] 금현물 잔고확인 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_entr: SafeStr = Field(default="", description="예수금")
    net_entr: SafeStr = Field(default="", description="추정예수금")
    tot_est_amt: SafeStr = Field(default="", description="잔고평가액")
    net_amt: SafeStr = Field(default="", description="예탁자산평가액")
    tot_book_amt2: SafeStr = Field(default="", description="총매입금액")
    tot_dep_amt: SafeStr = Field(default="", description="추정예탁자산")
    paym_alowa: SafeStr = Field(default="", description="출금가능금액")
    pl_amt: SafeStr = Field(default="", description="실현손익")
    gold_acnt_evlt_prst: Annotated[List[CheckGoldSpotBalance_GoldAcntEvltPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물계좌평가현황")

class GoldSpotDepositRequest(BaseModel):
    """[kt50021] 금현물 예수금 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class GoldSpotDeposit(BaseModel):
    """[kt50021] 금현물 예수금 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    entra: SafeStr = Field(default="", description="예수금")
    profa_ch: SafeStr = Field(default="", description="증거금현금")
    chck_ina_amt: SafeStr = Field(default="", description="수표입금액")
    etc_loan: SafeStr = Field(default="", description="기타대여금")
    etc_loan_dlfe: SafeStr = Field(default="", description="기타대여금연체료")
    etc_loan_tot: SafeStr = Field(default="", description="기타대여금합계")
    prsm_entra: SafeStr = Field(default="", description="추정예수금")
    buy_exct_amt: SafeStr = Field(default="", description="매수정산금")
    sell_exct_amt: SafeStr = Field(default="", description="매도정산금")
    sell_buy_exct_amt: SafeStr = Field(default="", description="매도매수정산금")
    dly_amt: SafeStr = Field(default="", description="미수변제소요금")
    prsm_pymn_alow_amt: SafeStr = Field(default="", description="추정출금가능금액")
    pymn_alow_amt: SafeStr = Field(default="", description="출금가능금액")
    ord_alow_amt: SafeStr = Field(default="", description="주문가능금액")

class AllGoldSpotOrdersRequest(BaseModel):
    """[kt50030] 금현물 주문체결전체조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_dt: SafeStr = Field(default="", description="주문일자")
    qry_tp: SafeStr = Field(default="", description="조회구분 1: 주문순, 2: 역순")
    mrkt_deal_tp: SafeStr = Field(default="", description="시장구분")
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분 0:전체, 1:주식, 2:채권")
    slby_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    fr_ord_no: SafeStr = Field(default="", description="시작주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 %:(전체), KRX, NXT, SOR")

class AllGoldSpotOrders_AcntOrdCntrPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분")
    ord_no: SafeStr = Field(default="", description="주문번호")
    stk_cd: SafeStr = Field(default="", description="상품코드")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    io_tp_nm: SafeStr = Field(default="", description="주문유형구분")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    cnfm_qty: SafeStr = Field(default="", description="확인수량")
    data_send_end_tp: SafeStr = Field(default="", description="접수구분")
    mrkt_deal_tp: SafeStr = Field(default="", description="시장구분")
    rsrv_tp: SafeStr = Field(default="", description="예약/반대여부")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    dcd_tp_nm: SafeStr = Field(default="", description="결제구분")
    crd_deal_tp: SafeStr = Field(default="", description="신용거래구분")
    cntr_qty: SafeStr = Field(default="", description="체결수량")
    cntr_uv: SafeStr = Field(default="", description="체결단가")
    ord_remnq: SafeStr = Field(default="", description="미체결수량")
    comm_ord_tp: SafeStr = Field(default="", description="통신구분")
    mdfy_cncl_tp: SafeStr = Field(default="", description="정정취소구분")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")
    cond_uv: SafeStr = Field(default="", description="스톱가")

class AllGoldSpotOrders(BaseModel):
    """[kt50030] 금현물 주문체결전체조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_cntr_prst: Annotated[List[AllGoldSpotOrders_AcntOrdCntrPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결현황")

class GoldSpotOrderExecutionRequest(BaseModel):
    """[kt50031] 금현물 주문체결조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_dt: SafeStr = Field(default="", description="주문일자 YYYYMMDD")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:주문순, 2:역순, 3:미체결, 4:체결내역만")
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분 0:전체, 1:주식, 2:채권")
    sell_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    stk_cd: SafeStr = Field(default="", description="종목코드 공백허용 (공백일때 전체종목)")
    fr_ord_no: SafeStr = Field(default="", description="시작주문번호 공백허용 (공백일때 전체주문)")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행")

class GoldSpotOrderExecution_AcntOrdCntrPrpsDtl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ord_no: SafeStr = Field(default="", description="주문번호")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    crd_tp: SafeStr = Field(default="", description="신용구분")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    cnfm_qty: SafeStr = Field(default="", description="확인수량")
    acpt_tp: SafeStr = Field(default="", description="접수구분")
    rsrv_tp: SafeStr = Field(default="", description="반대여부")
    ord_tm: SafeStr = Field(default="", description="주문시간")
    ori_ord: SafeStr = Field(default="", description="원주문")
    stk_nm: SafeStr = Field(default="", description="종목명")
    io_tp_nm: SafeStr = Field(default="", description="주문구분")
    loan_dt: SafeStr = Field(default="", description="대출일")
    cntr_qty: SafeStr = Field(default="", description="체결수량")
    cntr_uv: SafeStr = Field(default="", description="체결단가")
    ord_remnq: SafeStr = Field(default="", description="주문잔량")
    comm_ord_tp: SafeStr = Field(default="", description="통신구분")
    mdfy_cncl: SafeStr = Field(default="", description="정정취소")
    cnfm_tm: SafeStr = Field(default="", description="확인시간")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")
    cond_uv: SafeStr = Field(default="", description="스톱가")

class GoldSpotOrderExecution(BaseModel):
    """[kt50031] 금현물 주문체결조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_cntr_prps_dtl: Annotated[List[GoldSpotOrderExecution_AcntOrdCntrPrpsDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결내역상세")

class GoldSpotTransactionHistoryRequest(BaseModel):
    """[kt50032] 금현물 거래내역조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자")
    end_dt: SafeStr = Field(default="", description="종료일자")
    tp: SafeStr = Field(default="", description="구분 0:전체, 1:입출금, 2:출고, 3:매매, 4:매수, 5:매도, 6:입금, 7:출금")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class GoldSpotTransactionHistory_GoldTrdeHist(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    deal_dt: SafeStr = Field(default="", description="거래일자")
    deal_no: SafeStr = Field(default="", description="거래번호")
    rmrk_nm: SafeStr = Field(default="", description="적요명")
    deal_qty: SafeStr = Field(default="", description="거래수량")
    gold_spot_vat: SafeStr = Field(default="", description="금현물부가가치세")
    exct_amt: SafeStr = Field(default="", description="정산금액")
    dly_sum: SafeStr = Field(default="", description="연체합")
    entra_remn: SafeStr = Field(default="", description="예수금잔고")
    mdia_nm: SafeStr = Field(default="", description="메체구분명")
    orig_deal_no: SafeStr = Field(default="", description="원거래번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    uv_exrt: SafeStr = Field(default="", description="거래단가")
    cmsn: SafeStr = Field(default="", description="수수료")
    uncl_ocr: SafeStr = Field(default="", description="미수(원/g)")
    rpym_sum: SafeStr = Field(default="", description="변제합")
    spot_remn: SafeStr = Field(default="", description="현물잔고")
    proc_time: SafeStr = Field(default="", description="처리시간")
    rcpy_no: SafeStr = Field(default="", description="출납번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    deal_amt: SafeStr = Field(default="", description="거래금액")
    tax_tot_amt: SafeStr = Field(default="", description="소득/주민세")
    cntr_dt: SafeStr = Field(default="", description="체결일")
    proc_brch_nm: SafeStr = Field(default="", description="처리점")
    prcsr: SafeStr = Field(default="", description="처리자")

class GoldSpotTransactionHistory(BaseModel):
    """[kt50032] 금현물 거래내역조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_print: SafeStr = Field(default="", description="계좌번호 계좌번호 출력용")
    gold_trde_hist: Annotated[List[GoldSpotTransactionHistory_GoldTrdeHist], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물거래내역")

class GoldSpotNonTradingRequest(BaseModel):
    """[kt50075] 금현물 미체결조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_dt: SafeStr = Field(default="", description="주문일자")
    qry_tp: SafeStr = Field(default="", description="조회구분 1: 주문순, 2: 역순")
    mrkt_deal_tp: SafeStr = Field(default="", description="시장구분")
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분 0:전체, 1:주식, 2:채권")
    sell_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    fr_ord_no: SafeStr = Field(default="", description="시작주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 %:(전체), KRX, NXT, SOR")

class GoldSpotNonTrading_AcntOrdOsoPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_bond_tp: SafeStr = Field(default="", description="주식채권구분")
    ord_no: SafeStr = Field(default="", description="주문번호")
    stk_cd: SafeStr = Field(default="", description="상품코드")
    trde_tp: SafeStr = Field(default="", description="매매구분")
    io_tp_nm: SafeStr = Field(default="", description="주문유형구분")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    cnfm_qty: SafeStr = Field(default="", description="확인수량")
    data_send_end_tp: SafeStr = Field(default="", description="접수구분")
    mrkt_deal_tp: SafeStr = Field(default="", description="시장구분")
    rsrv_tp: SafeStr = Field(default="", description="예약/반대여부")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_nm: SafeStr = Field(default="", description="종목명")
    dcd_tp_nm: SafeStr = Field(default="", description="결제구분")
    crd_deal_tp: SafeStr = Field(default="", description="신용거래구분")
    cntr_qty: SafeStr = Field(default="", description="체결수량")
    cntr_uv: SafeStr = Field(default="", description="체결단가")
    ord_remnq: SafeStr = Field(default="", description="미체결수량")
    comm_ord_tp: SafeStr = Field(default="", description="통신구분")
    mdfy_cncl_tp: SafeStr = Field(default="", description="정정취소구분")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")
    cond_uv: SafeStr = Field(default="", description="스톱가")

class GoldSpotNonTrading(BaseModel):
    """[kt50075] 금현물 미체결조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_oso_prst: Annotated[List[GoldSpotNonTrading_AcntOrdOsoPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문미체결현황")

class ShortSellingTrendRequest(BaseModel):
    """[ka10014] 공매도추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tm_tp: SafeStr = Field(default="", description="시간구분 0:시작일, 1:기간")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")

class ShortSellingTrend_ShrtsTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    close_pric: SafeStr = Field(default="", description="종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    shrts_qty: SafeStr = Field(default="", description="공매도량")
    ovr_shrts_qty: SafeStr = Field(default="", description="누적공매도량 설정 기간의 공매도량 합산데이터")
    trde_wght: SafeStr = Field(default="", description="매매비중")
    shrts_trde_prica: SafeStr = Field(default="", description="공매도거래대금")
    shrts_avg_pric: SafeStr = Field(default="", description="공매도평균가")

class ShortSellingTrend(BaseModel):
    """[ka10014] 공매도추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    shrts_trnsn: Annotated[List[ShortSellingTrend_ShrtsTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="공매도추이")

class ForeignStockTradingTrendsByItemRequest(BaseModel):
    """[ka10008] 주식외국인종목별매매동향 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class ForeignStockTradingTrendsByItem_StkFrgnr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    close_pric: SafeStr = Field(default="", description="종가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    chg_qty: SafeStr = Field(default="", description="변동수량")
    poss_stkcnt: SafeStr = Field(default="", description="보유주식수")
    wght: SafeStr = Field(default="", description="비중")
    gain_pos_stkcnt: SafeStr = Field(default="", description="취득가능주식수")
    frgnr_limit: SafeStr = Field(default="", description="외국인한도")
    frgnr_limit_irds: SafeStr = Field(default="", description="외국인한도증감")
    limit_exh_rt: SafeStr = Field(default="", description="한도소진률")

class ForeignStockTradingTrendsByItem(BaseModel):
    """[ka10008] 주식외국인종목별매매동향 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_frgnr: Annotated[List[ForeignStockTradingTrendsByItem_StkFrgnr], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식외국인")

class StockInstitutionRequest(BaseModel):
    """[ka10009] 주식기관요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockInstitution(BaseModel):
    """[ka10009] 주식기관요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    date: SafeStr = Field(default="", description="날짜")
    close_pric: SafeStr = Field(default="", description="종가")
    pre: SafeStr = Field(default="", description="대비")
    orgn_dt_acc: SafeStr = Field(default="", description="기관기간누적")
    orgn_daly_nettrde: SafeStr = Field(default="", description="기관일별순매매")
    frgnr_daly_nettrde: SafeStr = Field(default="", description="외국인일별순매매")
    frgnr_qota_rt: SafeStr = Field(default="", description="외국인지분율")

class ContinuousTradingByInstitutionalForeignersRequest(BaseModel):
    """[ka10131] 기관외국인연속매매현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="기간 1:최근일, 3:3일, 5:5일, 10:10일, 20:20일, 120:120일, 0:시작일자/종료일자로 조회")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    mrkt_tp: SafeStr = Field(default="", description="장구분 001:코스피, 101:코스닥")
    netslmt_tp: SafeStr = Field(default="", description="순매도수구분 2:순매수(고정값)")
    stk_inds_tp: SafeStr = Field(default="", description="종목업종구분 0:종목(주식),1:업종")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 0:금액, 1:수량")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ContinuousTradingByInstitutionalForeigners_OrgnFrgnrContTrdePrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    prid_stkpc_flu_rt: SafeStr = Field(default="", description="기간중주가등락률")
    orgn_nettrde_amt: SafeStr = Field(default="", description="기관순매매금액")
    orgn_nettrde_qty: SafeStr = Field(default="", description="기관순매매량")
    orgn_cont_netprps_dys: SafeStr = Field(default="", description="기관계연속순매수일수")
    orgn_cont_netprps_qty: SafeStr = Field(default="", description="기관계연속순매수량")
    orgn_cont_netprps_amt: SafeStr = Field(default="", description="기관계연속순매수금액")
    frgnr_nettrde_qty: SafeStr = Field(default="", description="외국인순매매량")
    frgnr_nettrde_amt: SafeStr = Field(default="", description="외국인순매매액")
    frgnr_cont_netprps_dys: SafeStr = Field(default="", description="외국인연속순매수일수")
    frgnr_cont_netprps_qty: SafeStr = Field(default="", description="외국인연속순매수량")
    frgnr_cont_netprps_amt: SafeStr = Field(default="", description="외국인연속순매수금액")
    nettrde_qty: SafeStr = Field(default="", description="순매매량")
    nettrde_amt: SafeStr = Field(default="", description="순매매액")
    tot_cont_netprps_dys: SafeStr = Field(default="", description="합계연속순매수일수")
    tot_cont_nettrde_qty: SafeStr = Field(default="", description="합계연속순매매수량")
    tot_cont_netprps_amt: SafeStr = Field(default="", description="합계연속순매수금액")

class ContinuousTradingByInstitutionalForeigners(BaseModel):
    """[ka10131] 기관외국인연속매매현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    orgn_frgnr_cont_trde_prst: Annotated[List[ContinuousTradingByInstitutionalForeigners_OrgnFrgnrContTrdePrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="기관외국인연속매매현황")

class CurrentGoldSpotInvestorsRequest(BaseModel):
    """[ka52301] 금현물투자자현황 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class CurrentGoldSpotInvestors_InveTradStat(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    all_dfrt_trst_sell_qty: SafeStr = Field(default="", description="투자자별 매도 수량(천)")
    sell_qty_irds: SafeStr = Field(default="", description="투자자별 매도 수량 증감(천)")
    all_dfrt_trst_sell_amt: SafeStr = Field(default="", description="투자자별 매도 금액(억)")
    sell_amt_irds: SafeStr = Field(default="", description="투자자별 매도 금액 증감(억)")
    all_dfrt_trst_buy_qty: SafeStr = Field(default="", description="투자자별 매수 수량(천)")
    buy_qty_irds: SafeStr = Field(default="", description="투자자별 매수 수량 증감(천)")
    all_dfrt_trst_buy_amt: SafeStr = Field(default="", description="투자자별 매수 금액(억)")
    buy_amt_irds: SafeStr = Field(default="", description="투자자별 매수 금액 증감(억)")
    all_dfrt_trst_netprps_qty: SafeStr = Field(default="", description="투자자별 순매수 수량(천)")
    netprps_qty_irds: SafeStr = Field(default="", description="투자자별 순매수 수량 증감(천)")
    all_dfrt_trst_netprps_amt: SafeStr = Field(default="", description="투자자별 순매수 금액(억)")
    netprps_amt_irds: SafeStr = Field(default="", description="투자자별 순매수 금액 증감(억)")
    sell_uv: SafeStr = Field(default="", description="투자자별 매도 단가")
    buy_uv: SafeStr = Field(default="", description="투자자별 매수 단가")
    stk_nm: SafeStr = Field(default="", description="투자자 구분명")
    acc_netprps_amt: SafeStr = Field(default="", description="누적 순매수 금액(억)")
    acc_netprps_qty: SafeStr = Field(default="", description="누적 순매수 수량(천)")
    stk_cd: SafeStr = Field(default="", description="투자자 코드")

class CurrentGoldSpotInvestors(BaseModel):
    """[ka52301] 금현물투자자현황 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inve_trad_stat: Annotated[List[CurrentGoldSpotInvestors_InveTradStat], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물투자자현황")

class LoanLendingTransactionTrendRequest(BaseModel):
    """[ka10068] 대차거래추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    all_tp: SafeStr = Field(default="", description="전체구분 1: 전체표시")

class LoanLendingTransactionTrend_DbrtTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    dbrt_trde_irds: SafeStr = Field(default="", description="대차거래증감")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class LoanLendingTransactionTrend(BaseModel):
    """[ka10068] 대차거래추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_trnsn: Annotated[List[LoanLendingTransactionTrend_DbrtTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래추이")

class Top10BorrowingStocksRequest(BaseModel):
    """[ka10069] 대차거래상위10종목요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")

class Top10BorrowingStocks_DbrtTrdeUpper10Stk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class Top10BorrowingStocks(BaseModel):
    """[ka10069] 대차거래상위10종목요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_cntrcnt_sum: SafeStr = Field(default="", description="대차거래체결주수합")
    dbrt_trde_rpy_sum: SafeStr = Field(default="", description="대차거래상환주수합")
    rmnd_sum: SafeStr = Field(default="", description="잔고주수합")
    remn_amt_sum: SafeStr = Field(default="", description="잔고금액합")
    dbrt_trde_cntrcnt_rt: SafeStr = Field(default="", description="대차거래체결주수비율")
    dbrt_trde_rpy_rt: SafeStr = Field(default="", description="대차거래상환주수비율")
    rmnd_rt: SafeStr = Field(default="", description="잔고주수비율")
    remn_amt_rt: SafeStr = Field(default="", description="잔고금액비율")
    dbrt_trde_upper_10stk: Annotated[List[Top10BorrowingStocks_DbrtTrdeUpper10Stk], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래상위10종목")

class LoanLendingTransactionTrendByItemRequest(BaseModel):
    """[ka20068] 대차거래추이요청(종목별) 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    all_tp: SafeStr = Field(default="", description="전체구분 0:종목코드 입력종목만 표시")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class LoanLendingTransactionTrendByItem_DbrtTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    dbrt_trde_irds: SafeStr = Field(default="", description="대차거래증감")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class LoanLendingTransactionTrendByItem(BaseModel):
    """[ka20068] 대차거래추이요청(종목별) 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_trnsn: Annotated[List[LoanLendingTransactionTrendByItem_DbrtTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래추이")

class LoanTransactionDetailsRequest(BaseModel):
    """[ka90012] 대차거래내역요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")

class LoanTransactionDetails_DbrtTrdePrps(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class LoanTransactionDetails(BaseModel):
    """[ka90012] 대차거래내역요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_prps: Annotated[List[LoanTransactionDetails_DbrtTrdePrps], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래내역")

class HigherQuotaBalanceRequest(BaseModel):
    """[ka10020] 호가잔량상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:순매수잔량순, 2:순매도잔량순, 3:매수비율순, 4:매도비율순")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0000:장시작전(0주이상), 0010:만주이상, 0050:5만주이상, 00100:10만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HigherQuotaBalance_BidReqUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    tot_sel_req: SafeStr = Field(default="", description="총매도잔량")
    tot_buy_req: SafeStr = Field(default="", description="총매수잔량")
    netprps_req: SafeStr = Field(default="", description="순매수잔량")
    buy_rt: SafeStr = Field(default="", description="매수비율")

class HigherQuotaBalance(BaseModel):
    """[ka10020] 호가잔량상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    bid_req_upper: Annotated[List[HigherQuotaBalance_BidReqUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="호가잔량상위")

class SuddenIncreaseQuotationBalanceRequest(BaseModel):
    """[ka10021] 호가잔량급증요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:매수잔량, 2:매도잔량")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:급증량, 2:급증률")
    tm_tp: SafeStr = Field(default="", description="시간구분 분 입력")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 1:천주이상, 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class SuddenIncreaseQuotationBalance_BidReqSdnin(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    int: SafeStr = Field(default="", description="기준률")
    now: SafeStr = Field(default="", description="현재")
    sdnin_qty: SafeStr = Field(default="", description="급증수량")
    sdnin_rt: SafeStr = Field(default="", description="급증률")
    tot_buy_qty: SafeStr = Field(default="", description="총매수량")

class SuddenIncreaseQuotationBalance(BaseModel):
    """[ka10021] 호가잔량급증요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    bid_req_sdnin: Annotated[List[SuddenIncreaseQuotationBalance_BidReqSdnin], BeforeValidator(_force_list)] = Field(default_factory=list, description="호가잔량급증")

class SuddenIncreaseRemainingCapacityRequest(BaseModel):
    """[ka10022] 잔량율급증요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    rt_tp: SafeStr = Field(default="", description="비율구분 1:매수/매도비율, 2:매도/매수비율")
    tm_tp: SafeStr = Field(default="", description="시간구분 분 입력")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class SuddenIncreaseRemainingCapacity_ReqRtSdnin(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    int: SafeStr = Field(default="", description="기준률")
    now_rt: SafeStr = Field(default="", description="현재비율")
    sdnin_rt: SafeStr = Field(default="", description="급증률")
    tot_sel_req: SafeStr = Field(default="", description="총매도잔량")
    tot_buy_req: SafeStr = Field(default="", description="총매수잔량")

class SuddenIncreaseRemainingCapacity(BaseModel):
    """[ka10022] 잔량율급증요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    req_rt_sdnin: Annotated[List[SuddenIncreaseRemainingCapacity_ReqRtSdnin], BeforeValidator(_force_list)] = Field(default_factory=list, description="잔량율급증")

class SuddenIncreaseTradingVolumeRequest(BaseModel):
    """[ka10023] 거래량급증요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:급증량, 2:급증률, 3:급감량, 4:급감률")
    tm_tp: SafeStr = Field(default="", description="시간구분 1:분, 2:전일")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상")
    tm: SafeStr = Field(default="", description="시간 분 입력")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 3:우선주제외, 11:정리매매종목제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 17:ETN제외, 14:ETF제외, 18:ETF+ETN제외, 15:스팩제외, 20:ETF+ETN+스팩제외")
    pric_tp: SafeStr = Field(default="", description="가격구분 0:전체조회, 2:5만원이상, 5:1만원이상, 6:5천원이상, 8:1천원이상, 9:10만원이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class SuddenIncreaseTradingVolume_TrdeQtySdnin(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    prev_trde_qty: SafeStr = Field(default="", description="이전거래량")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    sdnin_qty: SafeStr = Field(default="", description="급증량")
    sdnin_rt: SafeStr = Field(default="", description="급증률")

class SuddenIncreaseTradingVolume(BaseModel):
    """[ka10023] 거래량급증요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_qty_sdnin: Annotated[List[SuddenIncreaseTradingVolume_TrdeQtySdnin], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래량급증")

class HigherFluctuationRateComparedPreviousDayRequest(BaseModel):
    """[ka10027] 전일대비등락률상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합")
    trde_qty_cnd: SafeStr = Field(default="", description="거래량조건 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0150:15만주이상, 0200:20만주이상, 0300:30만주이상, 0500:50만주이상, 1000:백만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외, 15:스펙제외, 16:ETF+ETN제외")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    updown_incls: SafeStr = Field(default="", description="상하한포함 0:불 포함, 1:포함")
    pric_cnd: SafeStr = Field(default="", description="가격조건 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10: 1만원미만")
    trde_prica_cnd: SafeStr = Field(default="", description="거래대금조건 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HigherFluctuationRateComparedPreviousDay_PredPreFluRtUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cls: SafeStr = Field(default="", description="종목분류")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    buy_req: SafeStr = Field(default="", description="매수잔량")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    cnt: SafeStr = Field(default="", description="횟수")

class HigherFluctuationRateComparedPreviousDay(BaseModel):
    """[ka10027] 전일대비등락률상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pred_pre_flu_rt_upper: Annotated[List[HigherFluctuationRateComparedPreviousDay_PredPreFluRtUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="전일대비등락률상위")

class HigherExpectedTransactionRateRequest(BaseModel):
    """[ka10029] 예상체결등락률상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:상승률, 2:상승폭, 3:보합, 4:하락률, 5:하락폭, 6:체결량, 7:상한, 8:하한")
    trde_qty_cnd: SafeStr = Field(default="", description="거래량조건 0:전체조회, 1;천주이상, 3:3천주, 5:5천주, 10:만주이상, 50:5만주이상, 100:10만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 3:우선주제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 5:신용한도초과제외, 7:신용융자E군, 8:신용대주, 9:신용융자전체")
    pric_cnd: SafeStr = Field(default="", description="가격조건 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10:1만원미만")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HigherExpectedTransactionRate_ExpCntrFluRtUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    exp_cntr_pric: SafeStr = Field(default="", description="예상체결가")
    base_pric: SafeStr = Field(default="", description="기준가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    exp_cntr_qty: SafeStr = Field(default="", description="예상체결량")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    buy_req: SafeStr = Field(default="", description="매수잔량")

class HigherExpectedTransactionRate(BaseModel):
    """[ka10029] 예상체결등락률상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    exp_cntr_flu_rt_upper: Annotated[List[HigherExpectedTransactionRate_ExpCntrFluRtUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="예상체결등락률상위")

class HighTransactionVolumeDayRequest(BaseModel):
    """[ka10030] 당일거래량상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:거래량, 2:거래회전율, 3:거래대금")
    mang_stk_incls: SafeStr = Field(default="", description="관리종목포함 0:관리종목 포함, 1:관리종목 미포함, 3:우선주제외, 11:정리매매종목제외, 4:관리종목, 우선주제외, 5:증100제외, 6:증100마나보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외")
    crd_tp: SafeStr = Field(default="", description="신용구분 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 8:신용대주")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체조회, 5:5천주이상, 10:1만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:500만주이상, 1000:백만주이상")
    pric_tp: SafeStr = Field(default="", description="가격구분 0:전체조회, 1:1천원미만, 2:1천원이상, 3:1천원~2천원, 4:2천원~5천원, 5:5천원이상, 6:5천원~1만원, 10:1만원미만, 7:1만원이상, 8:5만원이상, 9:10만원이상")
    trde_prica_tp: SafeStr = Field(default="", description="거래대금구분 0:전체조회, 1:1천만원이상, 3:3천만원이상, 4:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상")
    mrkt_open_tp: SafeStr = Field(default="", description="장운영구분 0:전체조회, 1:장중, 2:장전시간외, 3:장후시간외")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HighTransactionVolumeDay_TdyTrdeQtyUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    pred_rt: SafeStr = Field(default="", description="전일비")
    trde_tern_rt: SafeStr = Field(default="", description="거래회전율")
    trde_amt: SafeStr = Field(default="", description="거래금액")
    opmr_trde_qty: SafeStr = Field(default="", description="장중거래량")
    opmr_pred_rt: SafeStr = Field(default="", description="장중전일비")
    opmr_trde_rt: SafeStr = Field(default="", description="장중거래회전율")
    opmr_trde_amt: SafeStr = Field(default="", description="장중거래금액")
    af_mkrt_trde_qty: SafeStr = Field(default="", description="장후거래량")
    af_mkrt_pred_rt: SafeStr = Field(default="", description="장후전일비")
    af_mkrt_trde_rt: SafeStr = Field(default="", description="장후거래회전율")
    af_mkrt_trde_amt: SafeStr = Field(default="", description="장후거래금액")
    bf_mkrt_trde_qty: SafeStr = Field(default="", description="장전거래량")
    bf_mkrt_pred_rt: SafeStr = Field(default="", description="장전전일비")
    bf_mkrt_trde_rt: SafeStr = Field(default="", description="장전거래회전율")
    bf_mkrt_trde_amt: SafeStr = Field(default="", description="장전거래금액")

class HighTransactionVolumeDay(BaseModel):
    """[ka10030] 당일거래량상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_trde_qty_upper: Annotated[List[HighTransactionVolumeDay_TdyTrdeQtyUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일거래량상위")

class PreviousDayHighestTradingVolumeRequest(BaseModel):
    """[ka10031] 전일거래량상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:전일거래량 상위100종목, 2:전일거래대금 상위100종목")
    rank_strt: SafeStr = Field(default="", description="순위시작 0 ~ 100 값 중에  조회를 원하는 순위 시작값")
    rank_end: SafeStr = Field(default="", description="순위끝 0 ~ 100 값 중에  조회를 원하는 순위 끝값")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class PreviousDayHighestTradingVolume_PredTrdeQtyUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")

class PreviousDayHighestTradingVolume(BaseModel):
    """[ka10031] 전일거래량상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pred_trde_qty_upper: Annotated[List[PreviousDayHighestTradingVolume_PredTrdeQtyUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="전일거래량상위")

class HigherTransactionAmountRequest(BaseModel):
    """[ka10032] 거래대금상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    mang_stk_incls: SafeStr = Field(default="", description="관리종목포함 0:관리종목 미포함, 1:관리종목 포함")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HigherTransactionAmount_TrdePricaUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    now_rank: SafeStr = Field(default="", description="현재순위")
    pred_rank: SafeStr = Field(default="", description="전일순위")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    pred_trde_qty: SafeStr = Field(default="", description="전일거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class HigherTransactionAmount(BaseModel):
    """[ka10032] 거래대금상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_prica_upper: Annotated[List[HigherTransactionAmount_TrdePricaUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래대금상위")

class HigherCreditRatioRequest(BaseModel):
    """[ka10033] 신용비율상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체조회, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    updown_incls: SafeStr = Field(default="", description="상하한포함 0:상하한 미포함, 1:상하한포함")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HigherCreditRatio_CrdRtUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_infr: SafeStr = Field(default="", description="종목정보")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    crd_rt: SafeStr = Field(default="", description="신용비율")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    buy_req: SafeStr = Field(default="", description="매수잔량")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")

class HigherCreditRatio(BaseModel):
    """[ka10033] 신용비율상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_rt_upper: Annotated[List[HigherCreditRatio_CrdRtUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="신용비율상위")

class ExternalTransactionTopSalesByPeriodRequest(BaseModel):
    """[ka10034] 외인기간별매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매도, 2:순매수, 3:순매매")
    dt: SafeStr = Field(default="", description="기간 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ExternalTransactionTopSalesByPeriod_ForDtTrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    netprps_qty: SafeStr = Field(default="", description="순매수량")
    gain_pos_stkcnt: SafeStr = Field(default="", description="취득가능주식수")

class ExternalTransactionTopSalesByPeriod(BaseModel):
    """[ka10034] 외인기간별매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    for_dt_trde_upper: Annotated[List[ExternalTransactionTopSalesByPeriod_ForDtTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외인기간별매매상위")

class ForeignContinuousNetSalesTopRequest(BaseModel):
    """[ka10035] 외인연속순매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:연속순매도, 2:연속순매수")
    base_dt_tp: SafeStr = Field(default="", description="기준일구분 0:당일기준, 1:전일기준")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ForeignContinuousNetSalesTop_ForContNettrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    dm1: SafeStr = Field(default="", description="D-1")
    dm2: SafeStr = Field(default="", description="D-2")
    dm3: SafeStr = Field(default="", description="D-3")
    tot: SafeStr = Field(default="", description="합계")
    limit_exh_rt: SafeStr = Field(default="", description="한도소진율")
    pred_pre_1: SafeStr = Field(default="", description="전일대비1")
    pred_pre_2: SafeStr = Field(default="", description="전일대비2")
    pred_pre_3: SafeStr = Field(default="", description="전일대비3")

class ForeignContinuousNetSalesTop(BaseModel):
    """[ka10035] 외인연속순매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    for_cont_nettrde_upper: Annotated[List[ForeignContinuousNetSalesTop_ForContNettrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외인연속순매매상위")

class TopForeignLimitBurnoutRateIncreaseRequest(BaseModel):
    """[ka10036] 외인한도소진율증가상위 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    dt: SafeStr = Field(default="", description="기간 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class TopForeignLimitBurnoutRateIncrease_ForLimitExhRtIncrsUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    poss_stkcnt: SafeStr = Field(default="", description="보유주식수")
    gain_pos_stkcnt: SafeStr = Field(default="", description="취득가능주식수")
    base_limit_exh_rt: SafeStr = Field(default="", description="기준한도소진율")
    limit_exh_rt: SafeStr = Field(default="", description="한도소진율")
    exh_rt_incrs: SafeStr = Field(default="", description="소진율증가")

class TopForeignLimitBurnoutRateIncrease(BaseModel):
    """[ka10036] 외인한도소진율증가상위 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    for_limit_exh_rt_incrs_upper: Annotated[List[TopForeignLimitBurnoutRateIncrease_ForLimitExhRtIncrsUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외인한도소진율증가상위")

class ForeignOverCounterSalesRequest(BaseModel):
    """[ka10037] 외국계창구매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    dt: SafeStr = Field(default="", description="기간 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도, 3:매수, 4:매도")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:금액, 2:수량")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ForeignOverCounterSales_FrgnWicketTrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    sel_trde_qty: SafeStr = Field(default="", description="매도거래량")
    buy_trde_qty: SafeStr = Field(default="", description="매수거래량")
    netprps_trde_qty: SafeStr = Field(default="", description="순매수거래량")
    netprps_prica: SafeStr = Field(default="", description="순매수대금")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class ForeignOverCounterSales(BaseModel):
    """[ka10037] 외국계창구매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    frgn_wicket_trde_upper: Annotated[List[ForeignOverCounterSales_FrgnWicketTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외국계창구매매상위")

class RankingSecuritiesCompaniesByStockRequest(BaseModel):
    """[ka10038] 종목별증권사순위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:순매도순위정렬, 2:순매수순위정렬")
    dt: SafeStr = Field(default="", description="기간 1:전일, 4:5일, 9:10일, 19:20일, 39:40일, 59:60일, 119:120일")

class RankingSecuritiesCompaniesByStock_StkSecRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    mmcm_nm: SafeStr = Field(default="", description="회원사명")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    acc_netprps_qty: SafeStr = Field(default="", description="누적순매수수량")

class RankingSecuritiesCompaniesByStock(BaseModel):
    """[ka10038] 종목별증권사순위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    rank_1: SafeStr = Field(default="", description="순위1")
    rank_2: SafeStr = Field(default="", description="순위2")
    rank_3: SafeStr = Field(default="", description="순위3")
    prid_trde_qty: SafeStr = Field(default="", description="기간중거래량")
    stk_sec_rank: Annotated[List[RankingSecuritiesCompaniesByStock_StkSecRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별증권사순위")

class TopTradingBySecuritiesCompanyRequest(BaseModel):
    """[ka10039] 증권사별매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체, 5:5000주, 10:1만주, 50:5만주, 100:10만주, 500:50만주, 1000: 100만주")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    dt: SafeStr = Field(default="", description="기간 1:전일, 5:5일, 10:10일, 60:60일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TopTradingBySecuritiesCompany_SecTrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    prid_stkpc_flu: SafeStr = Field(default="", description="기간중주가등락")
    flu_rt: SafeStr = Field(default="", description="등락율")
    prid_trde_qty: SafeStr = Field(default="", description="기간중거래량")
    netprps: SafeStr = Field(default="", description="순매수")
    buy_trde_qty: SafeStr = Field(default="", description="매수거래량")
    sel_trde_qty: SafeStr = Field(default="", description="매도거래량")
    netprps_amt: SafeStr = Field(default="", description="순매수금액")
    buy_amt: SafeStr = Field(default="", description="매수금액")
    sell_amt: SafeStr = Field(default="", description="매도금액")

class TopTradingBySecuritiesCompany(BaseModel):
    """[ka10039] 증권사별매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sec_trde_upper: Annotated[List[TopTradingBySecuritiesCompany_SecTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="증권사별매매상위")

class SameDayMajorTransactionRequest(BaseModel):
    """[ka10040] 당일주요거래원요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SameDayMajorTransaction_TdyMainTrdeOri(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sel_scesn_tm: SafeStr = Field(default="", description="매도이탈시간")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    sel_upper_scesn_ori: SafeStr = Field(default="", description="매도상위이탈원")
    buy_scesn_tm: SafeStr = Field(default="", description="매수이탈시간")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    buy_upper_scesn_ori: SafeStr = Field(default="", description="매수상위이탈원")
    qry_dt: SafeStr = Field(default="", description="조회일자")
    qry_tm: SafeStr = Field(default="", description="조회시간")

class SameDayMajorTransaction(BaseModel):
    """[ka10040] 당일주요거래원요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sel_trde_ori_irds_1: SafeStr = Field(default="", description="매도거래원별증감1")
    sel_trde_ori_qty_1: SafeStr = Field(default="", description="매도거래원수량1")
    sel_trde_ori_1: SafeStr = Field(default="", description="매도거래원1")
    sel_trde_ori_cd_1: SafeStr = Field(default="", description="매도거래원코드1")
    buy_trde_ori_1: SafeStr = Field(default="", description="매수거래원1")
    buy_trde_ori_cd_1: SafeStr = Field(default="", description="매수거래원코드1")
    buy_trde_ori_qty_1: SafeStr = Field(default="", description="매수거래원수량1")
    buy_trde_ori_irds_1: SafeStr = Field(default="", description="매수거래원별증감1")
    sel_trde_ori_irds_2: SafeStr = Field(default="", description="매도거래원별증감2")
    sel_trde_ori_qty_2: SafeStr = Field(default="", description="매도거래원수량2")
    sel_trde_ori_2: SafeStr = Field(default="", description="매도거래원2")
    sel_trde_ori_cd_2: SafeStr = Field(default="", description="매도거래원코드2")
    buy_trde_ori_2: SafeStr = Field(default="", description="매수거래원2")
    buy_trde_ori_cd_2: SafeStr = Field(default="", description="매수거래원코드2")
    buy_trde_ori_qty_2: SafeStr = Field(default="", description="매수거래원수량2")
    buy_trde_ori_irds_2: SafeStr = Field(default="", description="매수거래원별증감2")
    sel_trde_ori_irds_3: SafeStr = Field(default="", description="매도거래원별증감3")
    sel_trde_ori_qty_3: SafeStr = Field(default="", description="매도거래원수량3")
    sel_trde_ori_3: SafeStr = Field(default="", description="매도거래원3")
    sel_trde_ori_cd_3: SafeStr = Field(default="", description="매도거래원코드3")
    buy_trde_ori_3: SafeStr = Field(default="", description="매수거래원3")
    buy_trde_ori_cd_3: SafeStr = Field(default="", description="매수거래원코드3")
    buy_trde_ori_qty_3: SafeStr = Field(default="", description="매수거래원수량3")
    buy_trde_ori_irds_3: SafeStr = Field(default="", description="매수거래원별증감3")
    sel_trde_ori_irds_4: SafeStr = Field(default="", description="매도거래원별증감4")
    sel_trde_ori_qty_4: SafeStr = Field(default="", description="매도거래원수량4")
    sel_trde_ori_4: SafeStr = Field(default="", description="매도거래원4")
    sel_trde_ori_cd_4: SafeStr = Field(default="", description="매도거래원코드4")
    buy_trde_ori_4: SafeStr = Field(default="", description="매수거래원4")
    buy_trde_ori_cd_4: SafeStr = Field(default="", description="매수거래원코드4")
    buy_trde_ori_qty_4: SafeStr = Field(default="", description="매수거래원수량4")
    buy_trde_ori_irds_4: SafeStr = Field(default="", description="매수거래원별증감4")
    sel_trde_ori_irds_5: SafeStr = Field(default="", description="매도거래원별증감5")
    sel_trde_ori_qty_5: SafeStr = Field(default="", description="매도거래원수량5")
    sel_trde_ori_5: SafeStr = Field(default="", description="매도거래원5")
    sel_trde_ori_cd_5: SafeStr = Field(default="", description="매도거래원코드5")
    buy_trde_ori_5: SafeStr = Field(default="", description="매수거래원5")
    buy_trde_ori_cd_5: SafeStr = Field(default="", description="매수거래원코드5")
    buy_trde_ori_qty_5: SafeStr = Field(default="", description="매수거래원수량5")
    buy_trde_ori_irds_5: SafeStr = Field(default="", description="매수거래원별증감5")
    frgn_sel_prsm_sum_chang: SafeStr = Field(default="", description="외국계매도추정합변동")
    frgn_sel_prsm_sum: SafeStr = Field(default="", description="외국계매도추정합")
    frgn_buy_prsm_sum: SafeStr = Field(default="", description="외국계매수추정합")
    frgn_buy_prsm_sum_chang: SafeStr = Field(default="", description="외국계매수추정합변동")
    tdy_main_trde_ori: Annotated[List[SameDayMajorTransaction_TdyMainTrdeOri], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일주요거래원")

class NetBuyingTraderRankingRequest(BaseModel):
    """[ka10042] 순매수거래원순위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    qry_dt_tp: SafeStr = Field(default="", description="조회기간구분 0:기간으로 조회, 1:시작일자, 종료일자로 조회")
    pot_tp: SafeStr = Field(default="", description="시점구분 0:당일, 1:전일")
    dt: SafeStr = Field(default="", description="기간 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일")
    sort_base: SafeStr = Field(default="", description="정렬기준 1:종가순, 2:날짜순")

class NetBuyingTraderRanking_NetprpsTrdeOriRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드")
    mmcm_nm: SafeStr = Field(default="", description="회원사명")

class NetBuyingTraderRanking(BaseModel):
    """[ka10042] 순매수거래원순위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    netprps_trde_ori_rank: Annotated[List[NetBuyingTraderRanking_NetprpsTrdeOriRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="순매수거래원순위")

class SameDayHighWithdrawalRequest(BaseModel):
    """[ka10053] 당일상위이탈원요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class SameDayHighWithdrawal_TdyUpperScesnOri(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sel_scesn_tm: SafeStr = Field(default="", description="매도이탈시간")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    sel_upper_scesn_ori: SafeStr = Field(default="", description="매도상위이탈원")
    buy_scesn_tm: SafeStr = Field(default="", description="매수이탈시간")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    buy_upper_scesn_ori: SafeStr = Field(default="", description="매수상위이탈원")
    qry_dt: SafeStr = Field(default="", description="조회일자")
    qry_tm: SafeStr = Field(default="", description="조회시간")

class SameDayHighWithdrawal(BaseModel):
    """[ka10053] 당일상위이탈원요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_upper_scesn_ori: Annotated[List[SameDayHighWithdrawal_TdyUpperScesnOri], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일상위이탈원")

class SameNetSalesRankingRequest(BaseModel):
    """[ka10062] 동일순매매순위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001: 코스피, 101:코스닥")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    sort_cnd: SafeStr = Field(default="", description="정렬조건 1:수량, 2:금액")
    unit_tp: SafeStr = Field(default="", description="단위구분 1:단주, 1000:천주")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class SameNetSalesRanking_EqlNettrdeRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    rank: SafeStr = Field(default="", description="순위")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    orgn_nettrde_qty: SafeStr = Field(default="", description="기관순매매수량")
    orgn_nettrde_amt: SafeStr = Field(default="", description="기관순매매금액")
    orgn_nettrde_avg_pric: SafeStr = Field(default="", description="기관순매매평균가")
    for_nettrde_qty: SafeStr = Field(default="", description="외인순매매수량")
    for_nettrde_amt: SafeStr = Field(default="", description="외인순매매금액")
    for_nettrde_avg_pric: SafeStr = Field(default="", description="외인순매매평균가")
    nettrde_qty: SafeStr = Field(default="", description="순매매수량")
    nettrde_amt: SafeStr = Field(default="", description="순매매금액")

class SameNetSalesRanking(BaseModel):
    """[ka10062] 동일순매매순위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    eql_nettrde_rank: Annotated[List[SameNetSalesRanking_EqlNettrdeRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="동일순매매순위")

class IntradayTradingByInvestorRequest(BaseModel):
    """[ka10065] 장중투자자별매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    orgn_tp: SafeStr = Field(default="", description="기관구분 9000:외국인, 9100:외국계, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")

class IntradayTradingByInvestor_OpmrInvsrTrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    sel_qty: SafeStr = Field(default="", description="매도량 매도금액/매도량")
    buy_qty: SafeStr = Field(default="", description="매수량 매수금액/매수량")
    netslmt: SafeStr = Field(default="", description="순매도 순매수/순매도(금액/수량)")

class IntradayTradingByInvestor(BaseModel):
    """[ka10065] 장중투자자별매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opmr_invsr_trde_upper: Annotated[List[IntradayTradingByInvestor_OpmrInvsrTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매상위")

class RankingOutHoursSinglePriceFluctuationRateRequest(BaseModel):
    """[ka10098] 시간외단일가등락율순위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체,001:코스피,101:코스닥")
    sort_base: SafeStr = Field(default="", description="정렬기준 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회,1:관리종목제외,2:정리매매종목제외,3:우선주제외,4:관리종목우선주제외,5:증100제외,6:증100만보기,7:증40만보기,8:증30만보기,9:증20만보기,12:증50만보기,13:증60만보기,14:ETF제외,15:스팩제외,16:ETF+ETN제외,17:ETN제외")
    trde_qty_cnd: SafeStr = Field(default="", description="거래량조건 0:전체조회, 10:백주이상,50:5백주이상,100;천주이상, 500:5천주이상, 1000:만주이상, 5000:5만주이상, 10000:10만주이상")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 8:신용대주, 5:신용한도초과제외")
    trde_prica: SafeStr = Field(default="", description="거래대금 0:전체조회, 5:5백만원이상,10:1천만원이상, 30:3천만원이상, 50:5천만원이상, 100:1억원이상, 300:3억원이상, 500:5억원이상, 1000:10억원이상, 3000:30억원이상, 5000:50억원이상, 10000:100억원이상")

class RankingOutHoursSinglePriceFluctuationRate_OvtSigpricFluRtRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    sel_tot_req: SafeStr = Field(default="", description="매도총잔량")
    buy_tot_req: SafeStr = Field(default="", description="매수총잔량")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    tdy_close_pric: SafeStr = Field(default="", description="당일종가")
    tdy_close_pric_flu_rt: SafeStr = Field(default="", description="당일종가등락률")

class RankingOutHoursSinglePriceFluctuationRate(BaseModel):
    """[ka10098] 시간외단일가등락율순위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ovt_sigpric_flu_rt_rank: Annotated[List[RankingOutHoursSinglePriceFluctuationRate_OvtSigpricFluRtRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="시간외단일가등락율순위")

class ForeignInstitutionalTradingTopRequest(BaseModel):
    """[ka90009] 외국인기관매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액(천만), 2:수량(천)")
    qry_dt_tp: SafeStr = Field(default="", description="조회일자구분 0:조회일자 미포함, 1:조회일자 포함")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ForeignInstitutionalTradingTop_FrgnrOrgnTrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    for_netslmt_stk_cd: SafeStr = Field(default="", description="외인순매도종목코드")
    for_netslmt_stk_nm: SafeStr = Field(default="", description="외인순매도종목명")
    for_netslmt_amt: SafeStr = Field(default="", description="외인순매도금액")
    for_netslmt_qty: SafeStr = Field(default="", description="외인순매도수량")
    for_netprps_stk_cd: SafeStr = Field(default="", description="외인순매수종목코드")
    for_netprps_stk_nm: SafeStr = Field(default="", description="외인순매수종목명")
    for_netprps_amt: SafeStr = Field(default="", description="외인순매수금액")
    for_netprps_qty: SafeStr = Field(default="", description="외인순매수수량")
    orgn_netslmt_stk_cd: SafeStr = Field(default="", description="기관순매도종목코드")
    orgn_netslmt_stk_nm: SafeStr = Field(default="", description="기관순매도종목명")
    orgn_netslmt_amt: SafeStr = Field(default="", description="기관순매도금액")
    orgn_netslmt_qty: SafeStr = Field(default="", description="기관순매도수량")
    orgn_netprps_stk_cd: SafeStr = Field(default="", description="기관순매수종목코드")
    orgn_netprps_stk_nm: SafeStr = Field(default="", description="기관순매수종목명")
    orgn_netprps_amt: SafeStr = Field(default="", description="기관순매수금액")
    orgn_netprps_qty: SafeStr = Field(default="", description="기관순매수수량")

class ForeignInstitutionalTradingTop(BaseModel):
    """[ka90009] 외국인기관매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    frgnr_orgn_trde_upper: Annotated[List[ForeignInstitutionalTradingTop_FrgnrOrgnTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외국인기관매매상위")

class StockQuoteRequest(BaseModel):
    """[ka10004] 주식호가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockQuote(BaseModel):
    """[ka10004] 주식호가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    bid_req_base_tm: SafeStr = Field(default="", description="호가잔량기준시간 호가시간")
    sel_10th_pre_req_pre: SafeStr = Field(default="", description="매도10차선잔량대비 매도호가직전대비10")
    sel_10th_pre_req: SafeStr = Field(default="", description="매도10차선잔량 매도호가수량10")
    sel_10th_pre_bid: SafeStr = Field(default="", description="매도10차선호가 매도호가10")
    sel_9th_pre_req_pre: SafeStr = Field(default="", description="매도9차선잔량대비 매도호가직전대비9")
    sel_9th_pre_req: SafeStr = Field(default="", description="매도9차선잔량 매도호가수량9")
    sel_9th_pre_bid: SafeStr = Field(default="", description="매도9차선호가 매도호가9")
    sel_8th_pre_req_pre: SafeStr = Field(default="", description="매도8차선잔량대비 매도호가직전대비8")
    sel_8th_pre_req: SafeStr = Field(default="", description="매도8차선잔량 매도호가수량8")
    sel_8th_pre_bid: SafeStr = Field(default="", description="매도8차선호가 매도호가8")
    sel_7th_pre_req_pre: SafeStr = Field(default="", description="매도7차선잔량대비 매도호가직전대비7")
    sel_7th_pre_req: SafeStr = Field(default="", description="매도7차선잔량 매도호가수량7")
    sel_7th_pre_bid: SafeStr = Field(default="", description="매도7차선호가 매도호가7")
    sel_6th_pre_req_pre: SafeStr = Field(default="", description="매도6차선잔량대비 매도호가직전대비6")
    sel_6th_pre_req: SafeStr = Field(default="", description="매도6차선잔량 매도호가수량6")
    sel_6th_pre_bid: SafeStr = Field(default="", description="매도6차선호가 매도호가6")
    sel_5th_pre_req_pre: SafeStr = Field(default="", description="매도5차선잔량대비 매도호가직전대비5")
    sel_5th_pre_req: SafeStr = Field(default="", description="매도5차선잔량 매도호가수량5")
    sel_5th_pre_bid: SafeStr = Field(default="", description="매도5차선호가 매도호가5")
    sel_4th_pre_req_pre: SafeStr = Field(default="", description="매도4차선잔량대비 매도호가직전대비4")
    sel_4th_pre_req: SafeStr = Field(default="", description="매도4차선잔량 매도호가수량4")
    sel_4th_pre_bid: SafeStr = Field(default="", description="매도4차선호가 매도호가4")
    sel_3th_pre_req_pre: SafeStr = Field(default="", description="매도3차선잔량대비 매도호가직전대비3")
    sel_3th_pre_req: SafeStr = Field(default="", description="매도3차선잔량 매도호가수량3")
    sel_3th_pre_bid: SafeStr = Field(default="", description="매도3차선호가 매도호가3")
    sel_2th_pre_req_pre: SafeStr = Field(default="", description="매도2차선잔량대비 매도호가직전대비2")
    sel_2th_pre_req: SafeStr = Field(default="", description="매도2차선잔량 매도호가수량2")
    sel_2th_pre_bid: SafeStr = Field(default="", description="매도2차선호가 매도호가2")
    sel_1th_pre_req_pre: SafeStr = Field(default="", description="매도1차선잔량대비 매도호가직전대비1")
    sel_fpr_req: SafeStr = Field(default="", description="매도최우선잔량 매도호가수량1")
    sel_fpr_bid: SafeStr = Field(default="", description="매도최우선호가 매도호가1")
    buy_fpr_bid: SafeStr = Field(default="", description="매수최우선호가 매수호가1")
    buy_fpr_req: SafeStr = Field(default="", description="매수최우선잔량 매수호가수량1")
    buy_1th_pre_req_pre: SafeStr = Field(default="", description="매수1차선잔량대비 매수호가직전대비1")
    buy_2th_pre_bid: SafeStr = Field(default="", description="매수2차선호가 매수호가2")
    buy_2th_pre_req: SafeStr = Field(default="", description="매수2차선잔량 매수호가수량2")
    buy_2th_pre_req_pre: SafeStr = Field(default="", description="매수2차선잔량대비 매수호가직전대비2")
    buy_3th_pre_bid: SafeStr = Field(default="", description="매수3차선호가 매수호가3")
    buy_3th_pre_req: SafeStr = Field(default="", description="매수3차선잔량 매수호가수량3")
    buy_3th_pre_req_pre: SafeStr = Field(default="", description="매수3차선잔량대비 매수호가직전대비3")
    buy_4th_pre_bid: SafeStr = Field(default="", description="매수4차선호가 매수호가4")
    buy_4th_pre_req: SafeStr = Field(default="", description="매수4차선잔량 매수호가수량4")
    buy_4th_pre_req_pre: SafeStr = Field(default="", description="매수4차선잔량대비 매수호가직전대비4")
    buy_5th_pre_bid: SafeStr = Field(default="", description="매수5차선호가 매수호가5")
    buy_5th_pre_req: SafeStr = Field(default="", description="매수5차선잔량 매수호가수량5")
    buy_5th_pre_req_pre: SafeStr = Field(default="", description="매수5차선잔량대비 매수호가직전대비5")
    buy_6th_pre_bid: SafeStr = Field(default="", description="매수6차선호가 매수호가6")
    buy_6th_pre_req: SafeStr = Field(default="", description="매수6차선잔량 매수호가수량6")
    buy_6th_pre_req_pre: SafeStr = Field(default="", description="매수6차선잔량대비 매수호가직전대비6")
    buy_7th_pre_bid: SafeStr = Field(default="", description="매수7차선호가 매수호가7")
    buy_7th_pre_req: SafeStr = Field(default="", description="매수7차선잔량 매수호가수량7")
    buy_7th_pre_req_pre: SafeStr = Field(default="", description="매수7차선잔량대비 매수호가직전대비7")
    buy_8th_pre_bid: SafeStr = Field(default="", description="매수8차선호가 매수호가8")
    buy_8th_pre_req: SafeStr = Field(default="", description="매수8차선잔량 매수호가수량8")
    buy_8th_pre_req_pre: SafeStr = Field(default="", description="매수8차선잔량대비 매수호가직전대비8")
    buy_9th_pre_bid: SafeStr = Field(default="", description="매수9차선호가 매수호가9")
    buy_9th_pre_req: SafeStr = Field(default="", description="매수9차선잔량 매수호가수량9")
    buy_9th_pre_req_pre: SafeStr = Field(default="", description="매수9차선잔량대비 매수호가직전대비9")
    buy_10th_pre_bid: SafeStr = Field(default="", description="매수10차선호가 매수호가10")
    buy_10th_pre_req: SafeStr = Field(default="", description="매수10차선잔량 매수호가수량10")
    buy_10th_pre_req_pre: SafeStr = Field(default="", description="매수10차선잔량대비 매수호가직전대비10")
    tot_sel_req_jub_pre: SafeStr = Field(default="", description="총매도잔량직전대비 매도호가총잔량직전대비")
    tot_sel_req: SafeStr = Field(default="", description="총매도잔량 매도호가총잔량")
    tot_buy_req: SafeStr = Field(default="", description="총매수잔량 매수호가총잔량")
    tot_buy_req_jub_pre: SafeStr = Field(default="", description="총매수잔량직전대비 매수호가총잔량직전대비")
    ovt_sel_req_pre: SafeStr = Field(default="", description="시간외매도잔량대비 시간외 매도호가 총잔량 직전대비")
    ovt_sel_req: SafeStr = Field(default="", description="시간외매도잔량 시간외 매도호가 총잔량")
    ovt_buy_req: SafeStr = Field(default="", description="시간외매수잔량 시간외 매수호가 총잔량")
    ovt_buy_req_pre: SafeStr = Field(default="", description="시간외매수잔량대비 시간외 매수호가 총잔량 직전대비")

class StockWeeklyMonthlyHourlyMinutesRequest(BaseModel):
    """[ka10005] 주식일주월시분요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockWeeklyMonthlyHourlyMinutes_StkDdwkmm(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    date: SafeStr = Field(default="", description="날짜")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    close_pric: SafeStr = Field(default="", description="종가")
    pre: SafeStr = Field(default="", description="대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    for_poss: SafeStr = Field(default="", description="외인보유")
    for_wght: SafeStr = Field(default="", description="외인비중")
    for_netprps: SafeStr = Field(default="", description="외인순매수")
    orgn_netprps: SafeStr = Field(default="", description="기관순매수")
    ind_netprps: SafeStr = Field(default="", description="개인순매수")
    crd_remn_rt: SafeStr = Field(default="", description="신용잔고율")
    frgn: SafeStr = Field(default="", description="외국계")
    prm: SafeStr = Field(default="", description="프로그램")

class StockWeeklyMonthlyHourlyMinutes(BaseModel):
    """[ka10005] 주식일주월시분요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_ddwkmm: Annotated[List[StockWeeklyMonthlyHourlyMinutes_StkDdwkmm], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식일주월시분")

class StockTimeRequest(BaseModel):
    """[ka10006] 주식시분요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockTime(BaseModel):
    """[ka10006] 주식시분요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    date: SafeStr = Field(default="", description="날짜")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    close_pric: SafeStr = Field(default="", description="종가")
    pre: SafeStr = Field(default="", description="대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    cntr_str: SafeStr = Field(default="", description="체결강도")

class PriceInformationRequest(BaseModel):
    """[ka10007] 시세표성정보요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class PriceInformation(BaseModel):
    """[ka10007] 시세표성정보요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_nm: SafeStr = Field(default="", description="종목명")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    date: SafeStr = Field(default="", description="날짜")
    tm: SafeStr = Field(default="", description="시간")
    pred_close_pric: SafeStr = Field(default="", description="전일종가")
    pred_trde_qty: SafeStr = Field(default="", description="전일거래량")
    upl_pric: SafeStr = Field(default="", description="상한가")
    lst_pric: SafeStr = Field(default="", description="하한가")
    pred_trde_prica: SafeStr = Field(default="", description="전일거래대금")
    flo_stkcnt: SafeStr = Field(default="", description="상장주식수")
    cur_prc: SafeStr = Field(default="", description="현재가")
    smbol: SafeStr = Field(default="", description="부호")
    flu_rt: SafeStr = Field(default="", description="등락률")
    pred_rt: SafeStr = Field(default="", description="전일비")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    exp_cntr_pric: SafeStr = Field(default="", description="예상체결가")
    exp_cntr_qty: SafeStr = Field(default="", description="예상체결량")
    exp_sel_pri_bid: SafeStr = Field(default="", description="예상매도우선호가")
    exp_buy_pri_bid: SafeStr = Field(default="", description="예상매수우선호가")
    trde_strt_dt: SafeStr = Field(default="", description="거래시작일")
    exec_pric: SafeStr = Field(default="", description="행사가격")
    hgst_pric: SafeStr = Field(default="", description="최고가")
    lwst_pric: SafeStr = Field(default="", description="최저가")
    hgst_pric_dt: SafeStr = Field(default="", description="최고가일")
    lwst_pric_dt: SafeStr = Field(default="", description="최저가일")
    sel_1bid: SafeStr = Field(default="", description="매도1호가")
    sel_2bid: SafeStr = Field(default="", description="매도2호가")
    sel_3bid: SafeStr = Field(default="", description="매도3호가")
    sel_4bid: SafeStr = Field(default="", description="매도4호가")
    sel_5bid: SafeStr = Field(default="", description="매도5호가")
    sel_6bid: SafeStr = Field(default="", description="매도6호가")
    sel_7bid: SafeStr = Field(default="", description="매도7호가")
    sel_8bid: SafeStr = Field(default="", description="매도8호가")
    sel_9bid: SafeStr = Field(default="", description="매도9호가")
    sel_10bid: SafeStr = Field(default="", description="매도10호가")
    buy_1bid: SafeStr = Field(default="", description="매수1호가")
    buy_2bid: SafeStr = Field(default="", description="매수2호가")
    buy_3bid: SafeStr = Field(default="", description="매수3호가")
    buy_4bid: SafeStr = Field(default="", description="매수4호가")
    buy_5bid: SafeStr = Field(default="", description="매수5호가")
    buy_6bid: SafeStr = Field(default="", description="매수6호가")
    buy_7bid: SafeStr = Field(default="", description="매수7호가")
    buy_8bid: SafeStr = Field(default="", description="매수8호가")
    buy_9bid: SafeStr = Field(default="", description="매수9호가")
    buy_10bid: SafeStr = Field(default="", description="매수10호가")
    sel_1bid_req: SafeStr = Field(default="", description="매도1호가잔량")
    sel_2bid_req: SafeStr = Field(default="", description="매도2호가잔량")
    sel_3bid_req: SafeStr = Field(default="", description="매도3호가잔량")
    sel_4bid_req: SafeStr = Field(default="", description="매도4호가잔량")
    sel_5bid_req: SafeStr = Field(default="", description="매도5호가잔량")
    sel_6bid_req: SafeStr = Field(default="", description="매도6호가잔량")
    sel_7bid_req: SafeStr = Field(default="", description="매도7호가잔량")
    sel_8bid_req: SafeStr = Field(default="", description="매도8호가잔량")
    sel_9bid_req: SafeStr = Field(default="", description="매도9호가잔량")
    sel_10bid_req: SafeStr = Field(default="", description="매도10호가잔량")
    buy_1bid_req: SafeStr = Field(default="", description="매수1호가잔량")
    buy_2bid_req: SafeStr = Field(default="", description="매수2호가잔량")
    buy_3bid_req: SafeStr = Field(default="", description="매수3호가잔량")
    buy_4bid_req: SafeStr = Field(default="", description="매수4호가잔량")
    buy_5bid_req: SafeStr = Field(default="", description="매수5호가잔량")
    buy_6bid_req: SafeStr = Field(default="", description="매수6호가잔량")
    buy_7bid_req: SafeStr = Field(default="", description="매수7호가잔량")
    buy_8bid_req: SafeStr = Field(default="", description="매수8호가잔량")
    buy_9bid_req: SafeStr = Field(default="", description="매수9호가잔량")
    buy_10bid_req: SafeStr = Field(default="", description="매수10호가잔량")
    sel_1bid_jub_pre: SafeStr = Field(default="", description="매도1호가직전대비")
    sel_2bid_jub_pre: SafeStr = Field(default="", description="매도2호가직전대비")
    sel_3bid_jub_pre: SafeStr = Field(default="", description="매도3호가직전대비")
    sel_4bid_jub_pre: SafeStr = Field(default="", description="매도4호가직전대비")
    sel_5bid_jub_pre: SafeStr = Field(default="", description="매도5호가직전대비")
    sel_6bid_jub_pre: SafeStr = Field(default="", description="매도6호가직전대비")
    sel_7bid_jub_pre: SafeStr = Field(default="", description="매도7호가직전대비")
    sel_8bid_jub_pre: SafeStr = Field(default="", description="매도8호가직전대비")
    sel_9bid_jub_pre: SafeStr = Field(default="", description="매도9호가직전대비")
    sel_10bid_jub_pre: SafeStr = Field(default="", description="매도10호가직전대비")
    buy_1bid_jub_pre: SafeStr = Field(default="", description="매수1호가직전대비")
    buy_2bid_jub_pre: SafeStr = Field(default="", description="매수2호가직전대비")
    buy_3bid_jub_pre: SafeStr = Field(default="", description="매수3호가직전대비")
    buy_4bid_jub_pre: SafeStr = Field(default="", description="매수4호가직전대비")
    buy_5bid_jub_pre: SafeStr = Field(default="", description="매수5호가직전대비")
    buy_6bid_jub_pre: SafeStr = Field(default="", description="매수6호가직전대비")
    buy_7bid_jub_pre: SafeStr = Field(default="", description="매수7호가직전대비")
    buy_8bid_jub_pre: SafeStr = Field(default="", description="매수8호가직전대비")
    buy_9bid_jub_pre: SafeStr = Field(default="", description="매수9호가직전대비")
    buy_10bid_jub_pre: SafeStr = Field(default="", description="매수10호가직전대비")
    sel_1bid_cnt: SafeStr = Field(default="", description="매도1호가건수")
    sel_2bid_cnt: SafeStr = Field(default="", description="매도2호가건수")
    sel_3bid_cnt: SafeStr = Field(default="", description="매도3호가건수")
    sel_4bid_cnt: SafeStr = Field(default="", description="매도4호가건수")
    sel_5bid_cnt: SafeStr = Field(default="", description="매도5호가건수")
    buy_1bid_cnt: SafeStr = Field(default="", description="매수1호가건수")
    buy_2bid_cnt: SafeStr = Field(default="", description="매수2호가건수")
    buy_3bid_cnt: SafeStr = Field(default="", description="매수3호가건수")
    buy_4bid_cnt: SafeStr = Field(default="", description="매수4호가건수")
    buy_5bid_cnt: SafeStr = Field(default="", description="매수5호가건수")
    lpsel_1bid_req: SafeStr = Field(default="", description="LP매도1호가잔량")
    lpsel_2bid_req: SafeStr = Field(default="", description="LP매도2호가잔량")
    lpsel_3bid_req: SafeStr = Field(default="", description="LP매도3호가잔량")
    lpsel_4bid_req: SafeStr = Field(default="", description="LP매도4호가잔량")
    lpsel_5bid_req: SafeStr = Field(default="", description="LP매도5호가잔량")
    lpsel_6bid_req: SafeStr = Field(default="", description="LP매도6호가잔량")
    lpsel_7bid_req: SafeStr = Field(default="", description="LP매도7호가잔량")
    lpsel_8bid_req: SafeStr = Field(default="", description="LP매도8호가잔량")
    lpsel_9bid_req: SafeStr = Field(default="", description="LP매도9호가잔량")
    lpsel_10bid_req: SafeStr = Field(default="", description="LP매도10호가잔량")
    lpbuy_1bid_req: SafeStr = Field(default="", description="LP매수1호가잔량")
    lpbuy_2bid_req: SafeStr = Field(default="", description="LP매수2호가잔량")
    lpbuy_3bid_req: SafeStr = Field(default="", description="LP매수3호가잔량")
    lpbuy_4bid_req: SafeStr = Field(default="", description="LP매수4호가잔량")
    lpbuy_5bid_req: SafeStr = Field(default="", description="LP매수5호가잔량")
    lpbuy_6bid_req: SafeStr = Field(default="", description="LP매수6호가잔량")
    lpbuy_7bid_req: SafeStr = Field(default="", description="LP매수7호가잔량")
    lpbuy_8bid_req: SafeStr = Field(default="", description="LP매수8호가잔량")
    lpbuy_9bid_req: SafeStr = Field(default="", description="LP매수9호가잔량")
    lpbuy_10bid_req: SafeStr = Field(default="", description="LP매수10호가잔량")
    tot_buy_req: SafeStr = Field(default="", description="총매수잔량")
    tot_sel_req: SafeStr = Field(default="", description="총매도잔량")
    tot_buy_cnt: SafeStr = Field(default="", description="총매수건수")
    tot_sel_cnt: SafeStr = Field(default="", description="총매도건수")

class AllNewStockWarrantsRequest(BaseModel):
    """[ka10011] 신주인수권전체시세요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    newstk_recvrht_tp: SafeStr = Field(default="", description="신주인수권구분 00:전체, 05:신주인수권증권, 07:신주인수권증서")

class AllNewStockWarrants_NewstkRecvrhtMrpr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    fpr_sel_bid: SafeStr = Field(default="", description="최우선매도호가")
    fpr_buy_bid: SafeStr = Field(default="", description="최우선매수호가")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")

class AllNewStockWarrants(BaseModel):
    """[ka10011] 신주인수권전체시세요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    newstk_recvrht_mrpr: Annotated[List[AllNewStockWarrants_NewstkRecvrhtMrpr], BeforeValidator(_force_list)] = Field(default_factory=list, description="신주인수권시세")

class DailyInstitutionalTradingItemsRequest(BaseModel):
    """[ka10044] 일별기관매매종목요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매도, 2:순매수")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class DailyInstitutionalTradingItems_DalyOrgnTrdeStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    netprps_qty: SafeStr = Field(default="", description="순매수수량")
    netprps_amt: SafeStr = Field(default="", description="순매수금액")

class DailyInstitutionalTradingItems(BaseModel):
    """[ka10044] 일별기관매매종목요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_orgn_trde_stk: Annotated[List[DailyInstitutionalTradingItems_DalyOrgnTrdeStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별기관매매종목")

class InstitutionalTradingTrendByItemRequest(BaseModel):
    """[ka10045] 종목별기관매매추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    orgn_prsm_unp_tp: SafeStr = Field(default="", description="기관추정단가구분 1:매수단가, 2:매도단가")
    for_prsm_unp_tp: SafeStr = Field(default="", description="외인추정단가구분 1:매수단가, 2:매도단가")

class InstitutionalTradingTrendByItem_StkOrgnTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    close_pric: SafeStr = Field(default="", description="종가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    orgn_dt_acc: SafeStr = Field(default="", description="기관기간누적")
    orgn_daly_nettrde_qty: SafeStr = Field(default="", description="기관일별순매매수량")
    for_dt_acc: SafeStr = Field(default="", description="외인기간누적")
    for_daly_nettrde_qty: SafeStr = Field(default="", description="외인일별순매매수량")
    limit_exh_rt: SafeStr = Field(default="", description="한도소진율")

class InstitutionalTradingTrendByItem(BaseModel):
    """[ka10045] 종목별기관매매추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    orgn_prsm_avg_pric: SafeStr = Field(default="", description="기관추정평균가")
    for_prsm_avg_pric: SafeStr = Field(default="", description="외인추정평균가")
    stk_orgn_trde_trnsn: Annotated[List[InstitutionalTradingTrendByItem_StkOrgnTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별기관매매추이")

class FasteningStrengthTrendByTimeRequest(BaseModel):
    """[ka10046] 체결강도추이시간별요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class FasteningStrengthTrendByTime_CntrStrTm(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    cntr_str_5min: SafeStr = Field(default="", description="체결강도5분")
    cntr_str_20min: SafeStr = Field(default="", description="체결강도20분")
    cntr_str_60min: SafeStr = Field(default="", description="체결강도60분")
    stex_tp: SafeStr = Field(default="", description="거래소구분")

class FasteningStrengthTrendByTime(BaseModel):
    """[ka10046] 체결강도추이시간별요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_str_tm: Annotated[List[FasteningStrengthTrendByTime_CntrStrTm], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결강도시간별")

class DailyTighteningStrengthTrendRequest(BaseModel):
    """[ka10047] 체결강도추이일별요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class DailyTighteningStrengthTrend_CntrStrDaly(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    cntr_str_5min: SafeStr = Field(default="", description="체결강도5일")
    cntr_str_20min: SafeStr = Field(default="", description="체결강도20일")
    cntr_str_60min: SafeStr = Field(default="", description="체결강도60일")

class DailyTighteningStrengthTrend(BaseModel):
    """[ka10047] 체결강도추이일별요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_str_daly: Annotated[List[DailyTighteningStrengthTrend_CntrStrDaly], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결강도일별")

class IntradayInvestorSpecificTradingRequest(BaseModel):
    """[ka10063] 장중투자자별매매요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1: 금액&수량")
    invsr: SafeStr = Field(default="", description="투자자별 6:외국인, 7:기관계, 1:투신, 0:보험, 2:은행, 3:연기금, 4:국가, 5:기타법인")
    frgn_all: SafeStr = Field(default="", description="외국계전체 1:체크, 0:미체크")
    smtm_netprps_tp: SafeStr = Field(default="", description="동시순매수구분 1:체크, 0:미체크")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class IntradayInvestorSpecificTrading_OpmrInvsrTrde(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    netprps_amt: SafeStr = Field(default="", description="순매수금액")
    prev_netprps_amt: SafeStr = Field(default="", description="이전순매수금액")
    buy_amt: SafeStr = Field(default="", description="매수금액")
    netprps_amt_irds: SafeStr = Field(default="", description="순매수금액증감")
    buy_amt_irds: SafeStr = Field(default="", description="매수금액증감")
    sell_amt: SafeStr = Field(default="", description="매도금액")
    sell_amt_irds: SafeStr = Field(default="", description="매도금액증감")
    netprps_qty: SafeStr = Field(default="", description="순매수수량")
    prev_pot_netprps_qty: SafeStr = Field(default="", description="이전시점순매수수량")
    netprps_irds: SafeStr = Field(default="", description="순매수증감")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    buy_qty_irds: SafeStr = Field(default="", description="매수수량증감")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    sell_qty_irds: SafeStr = Field(default="", description="매도수량증감")

class IntradayInvestorSpecificTrading(BaseModel):
    """[ka10063] 장중투자자별매매요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opmr_invsr_trde: Annotated[List[IntradayInvestorSpecificTrading_OpmrInvsrTrde], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매")

class TradingByInvestorAfterMarketCloseRequest(BaseModel):
    """[ka10066] 장마감후투자자별매매요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TradingByInvestorAfterMarketClose_OpafInvsrTrde(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    ind_invsr: SafeStr = Field(default="", description="개인투자자")
    frgnr_invsr: SafeStr = Field(default="", description="외국인투자자")
    orgn: SafeStr = Field(default="", description="기관계")
    fnnc_invt: SafeStr = Field(default="", description="금융투자")
    insrnc: SafeStr = Field(default="", description="보험")
    invtrt: SafeStr = Field(default="", description="투신")
    etc_fnnc: SafeStr = Field(default="", description="기타금융")
    bank: SafeStr = Field(default="", description="은행")
    penfnd_etc: SafeStr = Field(default="", description="연기금등")
    samo_fund: SafeStr = Field(default="", description="사모펀드")
    natn: SafeStr = Field(default="", description="국가")
    etc_corp: SafeStr = Field(default="", description="기타법인")

class TradingByInvestorAfterMarketClose(BaseModel):
    """[ka10066] 장마감후투자자별매매요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opaf_invsr_trde: Annotated[List[TradingByInvestorAfterMarketClose_OpafInvsrTrde], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매차트")

class StockTradingTrendsBySecuritiesCompanyRequest(BaseModel):
    """[ka10078] 증권사별종목매매동향요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")

class StockTradingTrendsBySecuritiesCompany_SecStkTrdeTrend(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    netprps_qty: SafeStr = Field(default="", description="순매수수량")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    sell_qty: SafeStr = Field(default="", description="매도수량")

class StockTradingTrendsBySecuritiesCompany(BaseModel):
    """[ka10078] 증권사별종목매매동향요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sec_stk_trde_trend: Annotated[List[StockTradingTrendsBySecuritiesCompany_SecStkTrdeTrend], BeforeValidator(_force_list)] = Field(default_factory=list, description="증권사별종목매매동향")

class DailyStockRequest(BaseModel):
    """[ka10086] 일별주가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    qry_dt: SafeStr = Field(default="", description="조회일자 YYYYMMDD")
    indc_tp: SafeStr = Field(default="", description="표시구분 0:수량, 1:금액(백만원)")

class DailyStock_DalyStkpc(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    date: SafeStr = Field(default="", description="날짜")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    close_pric: SafeStr = Field(default="", description="종가")
    pred_rt: SafeStr = Field(default="", description="전일비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    amt_mn: SafeStr = Field(default="", description="금액(백만)")
    crd_rt: SafeStr = Field(default="", description="신용비")
    ind: SafeStr = Field(default="", description="개인")
    orgn: SafeStr = Field(default="", description="기관")
    for_qty: SafeStr = Field(default="", description="외인수량")
    frgn: SafeStr = Field(default="", description="외국계")
    prm: SafeStr = Field(default="", description="프로그램")
    for_rt: SafeStr = Field(default="", description="외인비")
    for_poss: SafeStr = Field(default="", description="외인보유")
    for_wght: SafeStr = Field(default="", description="외인비중")
    for_netprps: SafeStr = Field(default="", description="외인순매수")
    orgn_netprps: SafeStr = Field(default="", description="기관순매수")
    ind_netprps: SafeStr = Field(default="", description="개인순매수")
    crd_remn_rt: SafeStr = Field(default="", description="신용잔고율")

class DailyStock(BaseModel):
    """[ka10086] 일별주가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_stkpc: Annotated[List[DailyStock_DalyStkpc], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별주가")

class SingleAfterHoursRequest(BaseModel):
    """[ka10087] 시간외단일가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SingleAfterHours(BaseModel):
    """[ka10087] 시간외단일가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    bid_req_base_tm: SafeStr = Field(default="", description="호가잔량기준시간")
    ovt_sigpric_sel_bid_jub_pre_5: SafeStr = Field(default="", description="시간외단일가_매도호가직전대비5")
    ovt_sigpric_sel_bid_jub_pre_4: SafeStr = Field(default="", description="시간외단일가_매도호가직전대비4")
    ovt_sigpric_sel_bid_jub_pre_3: SafeStr = Field(default="", description="시간외단일가_매도호가직전대비3")
    ovt_sigpric_sel_bid_jub_pre_2: SafeStr = Field(default="", description="시간외단일가_매도호가직전대비2")
    ovt_sigpric_sel_bid_jub_pre_1: SafeStr = Field(default="", description="시간외단일가_매도호가직전대비1")
    ovt_sigpric_sel_bid_qty_5: SafeStr = Field(default="", description="시간외단일가_매도호가수량5")
    ovt_sigpric_sel_bid_qty_4: SafeStr = Field(default="", description="시간외단일가_매도호가수량4")
    ovt_sigpric_sel_bid_qty_3: SafeStr = Field(default="", description="시간외단일가_매도호가수량3")
    ovt_sigpric_sel_bid_qty_2: SafeStr = Field(default="", description="시간외단일가_매도호가수량2")
    ovt_sigpric_sel_bid_qty_1: SafeStr = Field(default="", description="시간외단일가_매도호가수량1")
    ovt_sigpric_sel_bid_5: SafeStr = Field(default="", description="시간외단일가_매도호가5")
    ovt_sigpric_sel_bid_4: SafeStr = Field(default="", description="시간외단일가_매도호가4")
    ovt_sigpric_sel_bid_3: SafeStr = Field(default="", description="시간외단일가_매도호가3")
    ovt_sigpric_sel_bid_2: SafeStr = Field(default="", description="시간외단일가_매도호가2")
    ovt_sigpric_sel_bid_1: SafeStr = Field(default="", description="시간외단일가_매도호가1")
    ovt_sigpric_buy_bid_1: SafeStr = Field(default="", description="시간외단일가_매수호가1")
    ovt_sigpric_buy_bid_2: SafeStr = Field(default="", description="시간외단일가_매수호가2")
    ovt_sigpric_buy_bid_3: SafeStr = Field(default="", description="시간외단일가_매수호가3")
    ovt_sigpric_buy_bid_4: SafeStr = Field(default="", description="시간외단일가_매수호가4")
    ovt_sigpric_buy_bid_5: SafeStr = Field(default="", description="시간외단일가_매수호가5")
    ovt_sigpric_buy_bid_qty_1: SafeStr = Field(default="", description="시간외단일가_매수호가수량1")
    ovt_sigpric_buy_bid_qty_2: SafeStr = Field(default="", description="시간외단일가_매수호가수량2")
    ovt_sigpric_buy_bid_qty_3: SafeStr = Field(default="", description="시간외단일가_매수호가수량3")
    ovt_sigpric_buy_bid_qty_4: SafeStr = Field(default="", description="시간외단일가_매수호가수량4")
    ovt_sigpric_buy_bid_qty_5: SafeStr = Field(default="", description="시간외단일가_매수호가수량5")
    ovt_sigpric_buy_bid_jub_pre_1: SafeStr = Field(default="", description="시간외단일가_매수호가직전대비1")
    ovt_sigpric_buy_bid_jub_pre_2: SafeStr = Field(default="", description="시간외단일가_매수호가직전대비2")
    ovt_sigpric_buy_bid_jub_pre_3: SafeStr = Field(default="", description="시간외단일가_매수호가직전대비3")
    ovt_sigpric_buy_bid_jub_pre_4: SafeStr = Field(default="", description="시간외단일가_매수호가직전대비4")
    ovt_sigpric_buy_bid_jub_pre_5: SafeStr = Field(default="", description="시간외단일가_매수호가직전대비5")
    ovt_sigpric_sel_bid_tot_req: SafeStr = Field(default="", description="시간외단일가_매도호가총잔량")
    ovt_sigpric_buy_bid_tot_req: SafeStr = Field(default="", description="시간외단일가_매수호가총잔량")
    sel_bid_tot_req_jub_pre: SafeStr = Field(default="", description="매도호가총잔량직전대비")
    sel_bid_tot_req: SafeStr = Field(default="", description="매도호가총잔량")
    buy_bid_tot_req: SafeStr = Field(default="", description="매수호가총잔량")
    buy_bid_tot_req_jub_pre: SafeStr = Field(default="", description="매수호가총잔량직전대비")
    ovt_sel_bid_tot_req_jub_pre: SafeStr = Field(default="", description="시간외매도호가총잔량직전대비")
    ovt_sel_bid_tot_req: SafeStr = Field(default="", description="시간외매도호가총잔량")
    ovt_buy_bid_tot_req: SafeStr = Field(default="", description="시간외매수호가총잔량")
    ovt_buy_bid_tot_req_jub_pre: SafeStr = Field(default="", description="시간외매수호가총잔량직전대비")
    ovt_sigpric_cur_prc: SafeStr = Field(default="", description="시간외단일가_현재가")
    ovt_sigpric_pred_pre_sig: SafeStr = Field(default="", description="시간외단일가_전일대비기호")
    ovt_sigpric_pred_pre: SafeStr = Field(default="", description="시간외단일가_전일대비")
    ovt_sigpric_flu_rt: SafeStr = Field(default="", description="시간외단일가_등락률")
    ovt_sigpric_acc_trde_qty: SafeStr = Field(default="", description="시간외단일가_누적거래량")

class GoldSpotTradingTrendRequest(BaseModel):
    """[ka50010] 금현물체결추이 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")

class GoldSpotTradingTrend_GoldCntr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_pric: SafeStr = Field(default="", description="체결가")
    pred_pre: SafeStr = Field(default="", description="전일 대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    cntr_trde_qty: SafeStr = Field(default="", description="거래량(체결량)")
    tm: SafeStr = Field(default="", description="체결시간")
    pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pri_sel_bid_unit: SafeStr = Field(default="", description="매도호가")
    pri_buy_bid_unit: SafeStr = Field(default="", description="매수호가")
    trde_pre: SafeStr = Field(default="", description="전일 거래량 대비 비율")
    trde_tern_rt: SafeStr = Field(default="", description="전일 거래량 대비 순간 거래량 비율")
    cntr_str: SafeStr = Field(default="", description="체결강도")

class GoldSpotTradingTrend(BaseModel):
    """[ka50010] 금현물체결추이 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_cntr: Annotated[List[GoldSpotTradingTrend_GoldCntr], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물체결추이")

class SpotGoldDailyTrendRequest(BaseModel):
    """[ka50012] 금현물일별추이 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class SpotGoldDailyTrend_GoldDalyTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="종가")
    pred_pre: SafeStr = Field(default="", description="전일 대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금(백만)")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")
    pre_sig: SafeStr = Field(default="", description="전일대비기호")
    orgn_netprps: SafeStr = Field(default="", description="기관 순매수 수량")
    for_netprps: SafeStr = Field(default="", description="외국인 순매수 수량")
    ind_netprps: SafeStr = Field(default="", description="순매매량(개인)")

class SpotGoldDailyTrend(BaseModel):
    """[ka50012] 금현물일별추이 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_daly_trnsn: Annotated[List[SpotGoldDailyTrend_GoldDalyTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일별추이")

class GoldSpotExpectedTransactionRequest(BaseModel):
    """[ka50087] 금현물예상체결 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")

class GoldSpotExpectedTransaction_GoldExptExec(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    exp_cntr_pric: SafeStr = Field(default="", description="예상 체결가")
    exp_pred_pre: SafeStr = Field(default="", description="예상 체결가 전일대비")
    exp_flu_rt: SafeStr = Field(default="", description="예상 체결가 등락율")
    exp_acc_trde_qty: SafeStr = Field(default="", description="예상 체결 수량(누적)")
    exp_cntr_trde_qty: SafeStr = Field(default="", description="예상 체결 수량")
    exp_tm: SafeStr = Field(default="", description="예상 체결 시간")
    exp_pre_sig: SafeStr = Field(default="", description="예상 체결가 전일대비기호")
    stex_tp: SafeStr = Field(default="", description="거래소 구분")

class GoldSpotExpectedTransaction(BaseModel):
    """[ka50087] 금현물예상체결 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_expt_exec: Annotated[List[GoldSpotExpectedTransaction_GoldExptExec], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물예상체결")

class GoldSpotPriceInformationRequest(BaseModel):
    """[ka50100] 금현물 시세정보 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class GoldSpotPriceInformation(BaseModel):
    """[ka50100] 금현물 시세정보 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_rt: SafeStr = Field(default="", description="전일비")
    upl_pric: SafeStr = Field(default="", description="상한가")
    lst_pric: SafeStr = Field(default="", description="하한가")
    pred_close_pric: SafeStr = Field(default="", description="전일종가")

class GoldSpotQuoteRequest(BaseModel):
    """[ka50101] 금현물 호가 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class GoldSpotQuote_GoldBid(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_pric: SafeStr = Field(default="", description="체결가")
    pred_pre: SafeStr = Field(default="", description="전일 대비(원)")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    cntr_trde_qty: SafeStr = Field(default="", description="거래량(체결량)")
    tm: SafeStr = Field(default="", description="체결시간")
    pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pri_sel_bid_unit: SafeStr = Field(default="", description="매도호가")
    pri_buy_bid_unit: SafeStr = Field(default="", description="매수호가")
    trde_pre: SafeStr = Field(default="", description="전일 거래량 대비 비율")
    trde_tern_rt: SafeStr = Field(default="", description="전일 거래량 대비 순간 거래량 비율")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    lpmmcm_nm_1: SafeStr = Field(default="", description="K.O 접근도")
    stex_tp: SafeStr = Field(default="", description="거래소구분")

class GoldSpotQuote(BaseModel):
    """[ka50101] 금현물 호가 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_bid: Annotated[List[GoldSpotQuote_GoldBid], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물호가")

class ProgramTradingTrendByTimeZoneRequest(BaseModel):
    """[ka90005] 프로그램매매추이요청 시간대별 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액(백만원), 2:수량(천주)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01, 3일경우:P001_AL01  코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02, 3일경우:P101_AL02")
    min_tic_tp: SafeStr = Field(default="", description="분틱구분 0:틱, 1:분")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingTrendByTimeZone_PrmTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dfrt_trde_sel: SafeStr = Field(default="", description="차익거래매도")
    dfrt_trde_buy: SafeStr = Field(default="", description="차익거래매수")
    dfrt_trde_netprps: SafeStr = Field(default="", description="차익거래순매수")
    ndiffpro_trde_sel: SafeStr = Field(default="", description="비차익거래매도")
    ndiffpro_trde_buy: SafeStr = Field(default="", description="비차익거래매수")
    ndiffpro_trde_netprps: SafeStr = Field(default="", description="비차익거래순매수")
    dfrt_trde_sell_qty: SafeStr = Field(default="", description="차익거래매도수량")
    dfrt_trde_buy_qty: SafeStr = Field(default="", description="차익거래매수수량")
    dfrt_trde_netprps_qty: SafeStr = Field(default="", description="차익거래순매수수량")
    ndiffpro_trde_sell_qty: SafeStr = Field(default="", description="비차익거래매도수량")
    ndiffpro_trde_buy_qty: SafeStr = Field(default="", description="비차익거래매수수량")
    ndiffpro_trde_netprps_qty: SafeStr = Field(default="", description="비차익거래순매수수량")
    all_sel: SafeStr = Field(default="", description="전체매도")
    all_buy: SafeStr = Field(default="", description="전체매수")
    all_netprps: SafeStr = Field(default="", description="전체순매수")
    kospi200: SafeStr = Field(default="", description="KOSPI200")
    basis: SafeStr = Field(default="", description="BASIS")

class ProgramTradingTrendByTimeZone(BaseModel):
    """[ka90005] 프로그램매매추이요청 시간대별 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_trnsn: Annotated[List[ProgramTradingTrendByTimeZone_PrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매추이")

class ProgramTradingProfitBalanceTrendRequest(BaseModel):
    """[ka90006] 프로그램매매차익잔고추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingProfitBalanceTrend_PrmTrdeDfrtRemnTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    buy_dfrt_trde_qty: SafeStr = Field(default="", description="매수차익거래수량")
    buy_dfrt_trde_amt: SafeStr = Field(default="", description="매수차익거래금액")
    buy_dfrt_trde_irds_amt: SafeStr = Field(default="", description="매수차익거래증감액")
    sel_dfrt_trde_qty: SafeStr = Field(default="", description="매도차익거래수량")
    sel_dfrt_trde_amt: SafeStr = Field(default="", description="매도차익거래금액")
    sel_dfrt_trde_irds_amt: SafeStr = Field(default="", description="매도차익거래증감액")

class ProgramTradingProfitBalanceTrend(BaseModel):
    """[ka90006] 프로그램매매차익잔고추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_dfrt_remn_trnsn: Annotated[List[ProgramTradingProfitBalanceTrend_PrmTrdeDfrtRemnTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매차익잔고추이")

class CumulativeProgramTradingTrendRequest(BaseModel):
    """[ka90007] 프로그램매매누적추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD (종료일기준 1년간 데이터만 조회가능)")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피 , 1:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class CumulativeProgramTradingTrend_PrmTrdeAccTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    kospi200: SafeStr = Field(default="", description="KOSPI200")
    basis: SafeStr = Field(default="", description="BASIS")
    dfrt_trde_tdy: SafeStr = Field(default="", description="차익거래당일")
    dfrt_trde_acc: SafeStr = Field(default="", description="차익거래누적")
    ndiffpro_trde_tdy: SafeStr = Field(default="", description="비차익거래당일")
    ndiffpro_trde_acc: SafeStr = Field(default="", description="비차익거래누적")
    all_tdy: SafeStr = Field(default="", description="전체당일")
    all_acc: SafeStr = Field(default="", description="전체누적")

class CumulativeProgramTradingTrend(BaseModel):
    """[ka90007] 프로그램매매누적추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_acc_trnsn: Annotated[List[CumulativeProgramTradingTrend_PrmTrdeAccTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매누적추이")

class ProgramTradingTrendByItemTimeRequest(BaseModel):
    """[ka90008] 종목시간별프로그램매매추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")

class ProgramTradingTrendByItemTime_StkTmPrmTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm: SafeStr = Field(default="", description="시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    prm_sell_amt: SafeStr = Field(default="", description="프로그램매도금액")
    prm_buy_amt: SafeStr = Field(default="", description="프로그램매수금액")
    prm_netprps_amt: SafeStr = Field(default="", description="프로그램순매수금액")
    prm_netprps_amt_irds: SafeStr = Field(default="", description="프로그램순매수금액증감")
    prm_sell_qty: SafeStr = Field(default="", description="프로그램매도수량")
    prm_buy_qty: SafeStr = Field(default="", description="프로그램매수수량")
    prm_netprps_qty: SafeStr = Field(default="", description="프로그램순매수수량")
    prm_netprps_qty_irds: SafeStr = Field(default="", description="프로그램순매수수량증감")
    base_pric_tm: SafeStr = Field(default="", description="기준가시간")
    dbrt_trde_rpy_sum: SafeStr = Field(default="", description="대차거래상환주수합")
    remn_rcvord_sum: SafeStr = Field(default="", description="잔고수주합")
    stex_tp: SafeStr = Field(default="", description="거래소구분 KRX , NXT , 통합")

class ProgramTradingTrendByItemTime(BaseModel):
    """[ka90008] 종목시간별프로그램매매추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_tm_prm_trde_trnsn: Annotated[List[ProgramTradingTrendByItemTime_StkTmPrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목시간별프로그램매매추이")

class ProgramTradingTrendDateRequest(BaseModel):
    """[ka90010] 프로그램매매추이요청 일자별 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액(백만원), 2:수량(천주)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01, 3일경우:P001_AL01  코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02, 3일경우:P001_AL02")
    min_tic_tp: SafeStr = Field(default="", description="분틱구분 0:틱, 1:분")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingTrendDate_PrmTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dfrt_trde_sel: SafeStr = Field(default="", description="차익거래매도")
    dfrt_trde_buy: SafeStr = Field(default="", description="차익거래매수")
    dfrt_trde_netprps: SafeStr = Field(default="", description="차익거래순매수")
    ndiffpro_trde_sel: SafeStr = Field(default="", description="비차익거래매도")
    ndiffpro_trde_buy: SafeStr = Field(default="", description="비차익거래매수")
    ndiffpro_trde_netprps: SafeStr = Field(default="", description="비차익거래순매수")
    dfrt_trde_sell_qty: SafeStr = Field(default="", description="차익거래매도수량")
    dfrt_trde_buy_qty: SafeStr = Field(default="", description="차익거래매수수량")
    dfrt_trde_netprps_qty: SafeStr = Field(default="", description="차익거래순매수수량")
    ndiffpro_trde_sell_qty: SafeStr = Field(default="", description="비차익거래매도수량")
    ndiffpro_trde_buy_qty: SafeStr = Field(default="", description="비차익거래매수수량")
    ndiffpro_trde_netprps_qty: SafeStr = Field(default="", description="비차익거래순매수수량")
    all_sel: SafeStr = Field(default="", description="전체매도")
    all_buy: SafeStr = Field(default="", description="전체매수")
    all_netprps: SafeStr = Field(default="", description="전체순매수")
    kospi200: SafeStr = Field(default="", description="KOSPI200")
    basis: SafeStr = Field(default="", description="BASIS")

class ProgramTradingTrendDate(BaseModel):
    """[ka90010] 프로그램매매추이요청 일자별 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_trnsn: Annotated[List[ProgramTradingTrendDate_PrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매추이")

class DailyProgramTradingTrendItemsRequest(BaseModel):
    """[ka90013] 종목일별프로그램매매추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")

class DailyProgramTradingTrendItems_StkDalyPrmTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    prm_sell_amt: SafeStr = Field(default="", description="프로그램매도금액")
    prm_buy_amt: SafeStr = Field(default="", description="프로그램매수금액")
    prm_netprps_amt: SafeStr = Field(default="", description="프로그램순매수금액")
    prm_netprps_amt_irds: SafeStr = Field(default="", description="프로그램순매수금액증감")
    prm_sell_qty: SafeStr = Field(default="", description="프로그램매도수량")
    prm_buy_qty: SafeStr = Field(default="", description="프로그램매수수량")
    prm_netprps_qty: SafeStr = Field(default="", description="프로그램순매수수량")
    prm_netprps_qty_irds: SafeStr = Field(default="", description="프로그램순매수수량증감")
    base_pric_tm: SafeStr = Field(default="", description="기준가시간")
    dbrt_trde_rpy_sum: SafeStr = Field(default="", description="대차거래상환주수합")
    remn_rcvord_sum: SafeStr = Field(default="", description="잔고수주합")
    stex_tp: SafeStr = Field(default="", description="거래소구분 KRX , NXT , 통합")

class DailyProgramTradingTrendItems(BaseModel):
    """[ka90013] 종목일별프로그램매매추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_daly_prm_trde_trnsn: Annotated[List[DailyProgramTradingTrendItems_StkDalyPrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목일별프로그램매매추이")

class CreditBuyOrderRequest(BaseModel):
    """[kt10006] 신용 매수주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class CreditBuyOrder(BaseModel):
    """[kt10006] 신용 매수주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class CreditSellOrderRequest(BaseModel):
    """[kt10007] 신용 매도주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    crd_deal_tp: SafeStr = Field(default="", description="신용거래구분 33:융자 , 99:융자합")
    crd_loan_dt: SafeStr = Field(default="", description="대출일 YYYYMMDD(융자일경우필수)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class CreditSellOrder(BaseModel):
    """[kt10007] 신용 매도주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class CreditCorrectionOrderRequest(BaseModel):
    """[kt10008] 신용 정정주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    mdfy_uv: SafeStr = Field(default="", description="정정단가")
    mdfy_cond_uv: SafeStr = Field(default="", description="정정조건단가")

class CreditCorrectionOrder(BaseModel):
    """[kt10008] 신용 정정주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class CreditCancellationOrderRequest(BaseModel):
    """[kt10009] 신용 취소주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    cncl_qty: SafeStr = Field(default="", description="취소수량 '0' 입력시 잔량 전부 취소")

class CreditCancellationOrder(BaseModel):
    """[kt10009] 신용 취소주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    cncl_qty: SafeStr = Field(default="", description="취소수량")

class OrderExecutionRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class OrderExecutionRequest(BaseModel):
    """[00] 주문체결 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시  0:기존유지안함 1:기존유지(Default)  0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지  해지(REMOVE)시 값 불필요")
    data: Annotated[List[OrderExecutionRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class OrderExecution_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_9201: SafeStr = Field(default="", alias="9201", description="계좌번호")
    n_9203: SafeStr = Field(default="", alias="9203", description="주문번호")
    n_9205: SafeStr = Field(default="", alias="9205", description="관리자사번")
    n_9001: SafeStr = Field(default="", alias="9001", description="종목코드,업종코드")
    n_912: SafeStr = Field(default="", alias="912", description="주문업무분류")
    n_913: SafeStr = Field(default="", alias="913", description="주문상태 접수, 체결, 확인, 취소, 거부")
    n_302: SafeStr = Field(default="", alias="302", description="종목명")
    n_900: SafeStr = Field(default="", alias="900", description="주문수량")
    n_901: SafeStr = Field(default="", alias="901", description="주문가격")
    n_902: SafeStr = Field(default="", alias="902", description="미체결수량")
    n_903: SafeStr = Field(default="", alias="903", description="체결누계금액")
    n_904: SafeStr = Field(default="", alias="904", description="원주문번호")
    n_905: SafeStr = Field(default="", alias="905", description="주문구분 '+/-', 매도, 매수, 매도정정, 매수정정, 매수취소, 매도취소  ※ 영웅문4에서 적색으로 표기되어있으면 +가, 청색으로 표기되어있으면 -가 앞에 기재됩니다")
    n_906: SafeStr = Field(default="", alias="906", description="매매구분 보통, 시장가, 조건부지정가, 최유리지정가, 최우선지정가, 보통(IOC), 시장가(IOC), 최유리(IOC), 보통(FOK), 시장가(FOK), 최유리(FOK), 스톰지정가, 중간가, 중간가(IOC), 중간가(FOK), 장전시간외, 장후시간외, 시간외대량, 시간외바스켓, 시간외자사주, 시간외단일가")
    n_907: SafeStr = Field(default="", alias="907", description="매도수구분 1:매도, 2:매수")
    n_908: SafeStr = Field(default="", alias="908", description="주문/체결시간")
    n_909: SafeStr = Field(default="", alias="909", description="체결번호")
    n_910: SafeStr = Field(default="", alias="910", description="체결가")
    n_911: SafeStr = Field(default="", alias="911", description="체결량")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_27: SafeStr = Field(default="", alias="27", description="(최우선)매도호가")
    n_28: SafeStr = Field(default="", alias="28", description="(최우선)매수호가")
    n_914: SafeStr = Field(default="", alias="914", description="단위체결가")
    n_915: SafeStr = Field(default="", alias="915", description="단위체결량")
    n_938: SafeStr = Field(default="", alias="938", description="당일매매수수료")
    n_939: SafeStr = Field(default="", alias="939", description="당일매매세금")
    n_919: SafeStr = Field(default="", alias="919", description="거부사유")
    n_920: SafeStr = Field(default="", alias="920", description="화면번호")
    n_921: SafeStr = Field(default="", alias="921", description="터미널번호")
    n_922: SafeStr = Field(default="", alias="922", description="신용구분 실시간 체결용")
    n_923: SafeStr = Field(default="", alias="923", description="대출일 실시간 체결용")
    n_10010: SafeStr = Field(default="", alias="10010", description="시간외단일가_현재가")
    n_2134: SafeStr = Field(default="", alias="2134", description="거래소구분 0:통합,1:KRX,2:NXT")
    n_2135: SafeStr = Field(default="", alias="2135", description="거래소구분명 통합,KRX,NXT")
    n_2136: SafeStr = Field(default="", alias="2136", description="SOR여부 Y,N")

class OrderExecution_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[OrderExecution_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class OrderExecution(BaseModel):
    """[00] 주문체결 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[OrderExecution_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class BalanceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class BalanceRequest(BaseModel):
    """[04] 잔고 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시   0:기존유지안함 1:기존유지(Default)  0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지  해지(REMOVE)시 값 불필요")
    data: Annotated[List[BalanceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class Balance_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_9201: SafeStr = Field(default="", alias="9201", description="계좌번호")
    n_9001: SafeStr = Field(default="", alias="9001", description="종목코드,업종코드")
    n_917: SafeStr = Field(default="", alias="917", description="신용구분")
    n_916: SafeStr = Field(default="", alias="916", description="대출일")
    n_302: SafeStr = Field(default="", alias="302", description="종목명")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_930: SafeStr = Field(default="", alias="930", description="보유수량")
    n_931: SafeStr = Field(default="", alias="931", description="매입단가")
    n_932: SafeStr = Field(default="", alias="932", description="총매입가(당일누적)")
    n_933: SafeStr = Field(default="", alias="933", description="주문가능수량")
    n_945: SafeStr = Field(default="", alias="945", description="당일순매수량")
    n_946: SafeStr = Field(default="", alias="946", description="매도/매수구분 계약,주")
    n_950: SafeStr = Field(default="", alias="950", description="당일총매도손익")
    n_951: SafeStr = Field(default="", alias="951", description="Extra Item")
    n_27: SafeStr = Field(default="", alias="27", description="(최우선)매도호가")
    n_28: SafeStr = Field(default="", alias="28", description="(최우선)매수호가")
    n_307: SafeStr = Field(default="", alias="307", description="기준가")
    n_8019: SafeStr = Field(default="", alias="8019", description="손익률(실현손익)")
    n_957: SafeStr = Field(default="", alias="957", description="신용금액")
    n_958: SafeStr = Field(default="", alias="958", description="신용이자")
    n_918: SafeStr = Field(default="", alias="918", description="만기일")
    n_990: SafeStr = Field(default="", alias="990", description="당일실현손익(유가)")
    n_991: SafeStr = Field(default="", alias="991", description="당일실현손익율(유가)")
    n_992: SafeStr = Field(default="", alias="992", description="당일실현손익(신용)")
    n_993: SafeStr = Field(default="", alias="993", description="당일실현손익율(신용)")
    n_959: SafeStr = Field(default="", alias="959", description="담보대출수량")
    n_924: SafeStr = Field(default="", alias="924", description="Extra Item")

class Balance_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[Balance_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class Balance(BaseModel):
    """[04] 잔고 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[Balance_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockMomentumRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockMomentumRequest(BaseModel):
    """[0A] 주식기세 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시  0:기존유지안함 1:기존유지(Default)  0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지  해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockMomentumRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockMomentum_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_27: SafeStr = Field(default="", alias="27", description="(최우선)매도호가")
    n_28: SafeStr = Field(default="", alias="28", description="(최우선)매수호가")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_14: SafeStr = Field(default="", alias="14", description="누적거래대금")
    n_16: SafeStr = Field(default="", alias="16", description="시가")
    n_17: SafeStr = Field(default="", alias="17", description="고가")
    n_18: SafeStr = Field(default="", alias="18", description="저가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")
    n_26: SafeStr = Field(default="", alias="26", description="전일거래량대비(계약,주)")
    n_29: SafeStr = Field(default="", alias="29", description="거래대금증감")
    n_30: SafeStr = Field(default="", alias="30", description="전일거래량대비(비율)")
    n_31: SafeStr = Field(default="", alias="31", description="거래회전율")
    n_32: SafeStr = Field(default="", alias="32", description="거래비용")
    n_311: SafeStr = Field(default="", alias="311", description="시가총액(억)")
    n_567: SafeStr = Field(default="", alias="567", description="상한가발생시간")
    n_568: SafeStr = Field(default="", alias="568", description="하한가발생시간")

class StockMomentum_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockMomentum_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockMomentum(BaseModel):
    """[0A] 주식기세 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지(등록,해지시에만 값 전송,데이터 실시간 수신시 미전송)")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockMomentum_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockSigningRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockSigningRequest(BaseModel):
    """[0B] 주식체결 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockSigningRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockSigning_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_27: SafeStr = Field(default="", alias="27", description="(최우선)매도호가")
    n_28: SafeStr = Field(default="", alias="28", description="(최우선)매수호가")
    n_15: SafeStr = Field(default="", alias="15", description="거래량 +는 매수체결,-는 매도체결")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_14: SafeStr = Field(default="", alias="14", description="누적거래대금")
    n_16: SafeStr = Field(default="", alias="16", description="시가")
    n_17: SafeStr = Field(default="", alias="17", description="고가")
    n_18: SafeStr = Field(default="", alias="18", description="저가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")
    n_26: SafeStr = Field(default="", alias="26", description="전일거래량대비(계약,주)")
    n_29: SafeStr = Field(default="", alias="29", description="거래대금증감")
    n_30: SafeStr = Field(default="", alias="30", description="전일거래량대비(비율)")
    n_31: SafeStr = Field(default="", alias="31", description="거래회전율")
    n_32: SafeStr = Field(default="", alias="32", description="거래비용")
    n_228: SafeStr = Field(default="", alias="228", description="체결강도")
    n_311: SafeStr = Field(default="", alias="311", description="시가총액(억)")
    n_290: SafeStr = Field(default="", alias="290", description="장구분 1: 장전 시간외 , 2: 장중 , 3: 장후 시간외")
    n_691: SafeStr = Field(default="", alias="691", description="K.O 접근도")
    n_567: SafeStr = Field(default="", alias="567", description="상한가발생시간")
    n_568: SafeStr = Field(default="", alias="568", description="하한가발생시간")
    n_851: SafeStr = Field(default="", alias="851", description="전일 동시간 거래량 비율")
    n_1890: SafeStr = Field(default="", alias="1890", description="시가시간")
    n_1891: SafeStr = Field(default="", alias="1891", description="고가시간")
    n_1892: SafeStr = Field(default="", alias="1892", description="저가시간")
    n_1030: SafeStr = Field(default="", alias="1030", description="매도체결량")
    n_1031: SafeStr = Field(default="", alias="1031", description="매수체결량")
    n_1032: SafeStr = Field(default="", alias="1032", description="매수비율")
    n_1071: SafeStr = Field(default="", alias="1071", description="매도체결건수")
    n_1072: SafeStr = Field(default="", alias="1072", description="매수체결건수")
    n_1313: SafeStr = Field(default="", alias="1313", description="순간거래대금")
    n_1315: SafeStr = Field(default="", alias="1315", description="매도체결량_단건")
    n_1316: SafeStr = Field(default="", alias="1316", description="매수체결량_단건")
    n_1314: SafeStr = Field(default="", alias="1314", description="순매수체결량")
    n_1497: SafeStr = Field(default="", alias="1497", description="CFD증거금")
    n_1498: SafeStr = Field(default="", alias="1498", description="유지증거금")
    n_620: SafeStr = Field(default="", alias="620", description="당일거래평균가")
    n_732: SafeStr = Field(default="", alias="732", description="CFD거래비용")
    n_852: SafeStr = Field(default="", alias="852", description="대주거래비용")
    n_9081: SafeStr = Field(default="", alias="9081", description="거래소구분")

class StockSigning_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0B,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockSigning_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockSigning(BaseModel):
    """[0B] 주식체결 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockSigning_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockPreferredPriceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockPreferredPriceRequest(BaseModel):
    """[0C] 주식우선호가 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockPreferredPriceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockPreferredPrice_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_27: SafeStr = Field(default="", alias="27", description="(최우선)매도호가")
    n_28: SafeStr = Field(default="", alias="28", description="(최우선)매수호가")

class StockPreferredPrice_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockPreferredPrice_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockPreferredPrice(BaseModel):
    """[0C] 주식우선호가 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockPreferredPrice_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockQuoteBalanceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockQuoteBalanceRequest(BaseModel):
    """[0D] 주식호가잔량 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockQuoteBalanceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockQuoteBalance_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_21: SafeStr = Field(default="", alias="21", description="호가시간")
    n_41: SafeStr = Field(default="", alias="41", description="매도호가1")
    n_61: SafeStr = Field(default="", alias="61", description="매도호가수량1")
    n_81: SafeStr = Field(default="", alias="81", description="매도호가직전대비1")
    n_51: SafeStr = Field(default="", alias="51", description="매수호가1")
    n_71: SafeStr = Field(default="", alias="71", description="매수호가수량1")
    n_91: SafeStr = Field(default="", alias="91", description="매수호가직전대비1")
    n_42: SafeStr = Field(default="", alias="42", description="매도호가2")
    n_62: SafeStr = Field(default="", alias="62", description="매도호가수량2")
    n_82: SafeStr = Field(default="", alias="82", description="매도호가직전대비2")
    n_52: SafeStr = Field(default="", alias="52", description="매수호가2")
    n_72: SafeStr = Field(default="", alias="72", description="매수호가수량2")
    n_92: SafeStr = Field(default="", alias="92", description="매수호가직전대비2")
    n_43: SafeStr = Field(default="", alias="43", description="매도호가3")
    n_63: SafeStr = Field(default="", alias="63", description="매도호가수량3")
    n_83: SafeStr = Field(default="", alias="83", description="매도호가직전대비3")
    n_53: SafeStr = Field(default="", alias="53", description="매수호가3")
    n_73: SafeStr = Field(default="", alias="73", description="매수호가수량3")
    n_93: SafeStr = Field(default="", alias="93", description="매수호가직전대비3")
    n_44: SafeStr = Field(default="", alias="44", description="매도호가4")
    n_64: SafeStr = Field(default="", alias="64", description="매도호가수량4")
    n_84: SafeStr = Field(default="", alias="84", description="매도호가직전대비4")
    n_54: SafeStr = Field(default="", alias="54", description="매수호가4")
    n_74: SafeStr = Field(default="", alias="74", description="매수호가수량4")
    n_94: SafeStr = Field(default="", alias="94", description="매수호가직전대비4")
    n_45: SafeStr = Field(default="", alias="45", description="매도호가5")
    n_65: SafeStr = Field(default="", alias="65", description="매도호가수량5")
    n_85: SafeStr = Field(default="", alias="85", description="매도호가직전대비5")
    n_55: SafeStr = Field(default="", alias="55", description="매수호가5")
    n_75: SafeStr = Field(default="", alias="75", description="매수호가수량5")
    n_95: SafeStr = Field(default="", alias="95", description="매수호가직전대비5")
    n_46: SafeStr = Field(default="", alias="46", description="매도호가6")
    n_66: SafeStr = Field(default="", alias="66", description="매도호가수량6")
    n_86: SafeStr = Field(default="", alias="86", description="매도호가직전대비6")
    n_56: SafeStr = Field(default="", alias="56", description="매수호가6")
    n_76: SafeStr = Field(default="", alias="76", description="매수호가수량6")
    n_96: SafeStr = Field(default="", alias="96", description="매수호가직전대비6")
    n_47: SafeStr = Field(default="", alias="47", description="매도호가7")
    n_67: SafeStr = Field(default="", alias="67", description="매도호가수량7")
    n_87: SafeStr = Field(default="", alias="87", description="매도호가직전대비7")
    n_57: SafeStr = Field(default="", alias="57", description="매수호가7")
    n_77: SafeStr = Field(default="", alias="77", description="매수호가수량7")
    n_97: SafeStr = Field(default="", alias="97", description="매수호가직전대비7")
    n_48: SafeStr = Field(default="", alias="48", description="매도호가8")
    n_68: SafeStr = Field(default="", alias="68", description="매도호가수량8")
    n_88: SafeStr = Field(default="", alias="88", description="매도호가직전대비8")
    n_58: SafeStr = Field(default="", alias="58", description="매수호가8")
    n_78: SafeStr = Field(default="", alias="78", description="매수호가수량8")
    n_98: SafeStr = Field(default="", alias="98", description="매수호가직전대비8")
    n_49: SafeStr = Field(default="", alias="49", description="매도호가9")
    n_69: SafeStr = Field(default="", alias="69", description="매도호가수량9")
    n_89: SafeStr = Field(default="", alias="89", description="매도호가직전대비9")
    n_59: SafeStr = Field(default="", alias="59", description="매수호가9")
    n_79: SafeStr = Field(default="", alias="79", description="매수호가수량9")
    n_99: SafeStr = Field(default="", alias="99", description="매수호가직전대비9")
    n_50: SafeStr = Field(default="", alias="50", description="매도호가10")
    n_70: SafeStr = Field(default="", alias="70", description="매도호가수량10")
    n_60: SafeStr = Field(default="", alias="60", description="매수호가10")
    n_90: SafeStr = Field(default="", alias="90", description="매도호가직전대비10")
    n_80: SafeStr = Field(default="", alias="80", description="매수호가수량10")
    n_100: SafeStr = Field(default="", alias="100", description="매수호가직전대비10")
    n_121: SafeStr = Field(default="", alias="121", description="매도호가총잔량")
    n_122: SafeStr = Field(default="", alias="122", description="매도호가총잔량직전대비")
    n_125: SafeStr = Field(default="", alias="125", description="매수호가총잔량")
    n_126: SafeStr = Field(default="", alias="126", description="매수호가총잔량직전대비")
    n_23: SafeStr = Field(default="", alias="23", description="예상체결가")
    n_24: SafeStr = Field(default="", alias="24", description="예상체결수량")
    n_128: SafeStr = Field(default="", alias="128", description="순매수잔량")
    n_129: SafeStr = Field(default="", alias="129", description="매수비율")
    n_138: SafeStr = Field(default="", alias="138", description="순매도잔량")
    n_139: SafeStr = Field(default="", alias="139", description="매도비율")
    n_200: SafeStr = Field(default="", alias="200", description="예상체결가전일종가대비")
    n_201: SafeStr = Field(default="", alias="201", description="예상체결가전일종가대비등락율")
    n_238: SafeStr = Field(default="", alias="238", description="예상체결가전일종가대비기호")
    n_291: SafeStr = Field(default="", alias="291", description="예상체결가 예상체결 시간동안에만 유효한 값")
    n_292: SafeStr = Field(default="", alias="292", description="예상체결량")
    n_293: SafeStr = Field(default="", alias="293", description="예상체결가전일대비기호")
    n_294: SafeStr = Field(default="", alias="294", description="예상체결가전일대비")
    n_295: SafeStr = Field(default="", alias="295", description="예상체결가전일대비등락율")
    n_621: SafeStr = Field(default="", alias="621", description="LP매도호가수량1")
    n_631: SafeStr = Field(default="", alias="631", description="LP매수호가수량1")
    n_622: SafeStr = Field(default="", alias="622", description="LP매도호가수량2")
    n_632: SafeStr = Field(default="", alias="632", description="LP매수호가수량2")
    n_623: SafeStr = Field(default="", alias="623", description="LP매도호가수량3")
    n_633: SafeStr = Field(default="", alias="633", description="LP매수호가수량3")
    n_624: SafeStr = Field(default="", alias="624", description="LP매도호가수량4")
    n_634: SafeStr = Field(default="", alias="634", description="LP매수호가수량4")
    n_625: SafeStr = Field(default="", alias="625", description="LP매도호가수량5")
    n_635: SafeStr = Field(default="", alias="635", description="LP매수호가수량5")
    n_626: SafeStr = Field(default="", alias="626", description="LP매도호가수량6")
    n_636: SafeStr = Field(default="", alias="636", description="LP매수호가수량6")
    n_627: SafeStr = Field(default="", alias="627", description="LP매도호가수량7")
    n_637: SafeStr = Field(default="", alias="637", description="LP매수호가수량7")
    n_628: SafeStr = Field(default="", alias="628", description="LP매도호가수량8")
    n_638: SafeStr = Field(default="", alias="638", description="LP매수호가수량8")
    n_629: SafeStr = Field(default="", alias="629", description="LP매도호가수량9")
    n_639: SafeStr = Field(default="", alias="639", description="LP매수호가수량9")
    n_630: SafeStr = Field(default="", alias="630", description="LP매도호가수량10")
    n_640: SafeStr = Field(default="", alias="640", description="LP매수호가수량10")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_299: SafeStr = Field(default="", alias="299", description="전일거래량대비예상체결율")
    n_215: SafeStr = Field(default="", alias="215", description="장운영구분")
    n_216: SafeStr = Field(default="", alias="216", description="투자자별ticker")
    n_6044: SafeStr = Field(default="", alias="6044", description="KRX 매도호가잔량1")
    n_6045: SafeStr = Field(default="", alias="6045", description="KRX 매도호가잔량2")
    n_6046: SafeStr = Field(default="", alias="6046", description="KRX 매도호가잔량3")
    n_6047: SafeStr = Field(default="", alias="6047", description="KRX 매도호가잔량4")
    n_6048: SafeStr = Field(default="", alias="6048", description="KRX 매도호가잔량5")
    n_6049: SafeStr = Field(default="", alias="6049", description="KRX 매도호가잔량6")
    n_6050: SafeStr = Field(default="", alias="6050", description="KRX 매도호가잔량7")
    n_6051: SafeStr = Field(default="", alias="6051", description="KRX 매도호가잔량8")
    n_6052: SafeStr = Field(default="", alias="6052", description="KRX 매도호가잔량9")
    n_6053: SafeStr = Field(default="", alias="6053", description="KRX 매도호가잔량10")
    n_6054: SafeStr = Field(default="", alias="6054", description="KRX 매수호가잔량1")
    n_6055: SafeStr = Field(default="", alias="6055", description="KRX 매수호가잔량2")
    n_6056: SafeStr = Field(default="", alias="6056", description="KRX 매수호가잔량3")
    n_6057: SafeStr = Field(default="", alias="6057", description="KRX 매수호가잔량4")
    n_6058: SafeStr = Field(default="", alias="6058", description="KRX 매수호가잔량5")
    n_6059: SafeStr = Field(default="", alias="6059", description="KRX 매수호가잔량6")
    n_6060: SafeStr = Field(default="", alias="6060", description="KRX 매수호가잔량7")
    n_6061: SafeStr = Field(default="", alias="6061", description="KRX 매수호가잔량8")
    n_6062: SafeStr = Field(default="", alias="6062", description="KRX 매수호가잔량9")
    n_6063: SafeStr = Field(default="", alias="6063", description="KRX 매수호가잔량10")
    n_6064: SafeStr = Field(default="", alias="6064", description="KRX 매도호가총잔량")
    n_6065: SafeStr = Field(default="", alias="6065", description="KRX 매수호가총잔량")
    n_6066: SafeStr = Field(default="", alias="6066", description="NXT 매도호가잔량1")
    n_6067: SafeStr = Field(default="", alias="6067", description="NXT 매도호가잔량2")
    n_6068: SafeStr = Field(default="", alias="6068", description="NXT 매도호가잔량3")
    n_6069: SafeStr = Field(default="", alias="6069", description="NXT 매도호가잔량4")
    n_6070: SafeStr = Field(default="", alias="6070", description="NXT 매도호가잔량5")
    n_6071: SafeStr = Field(default="", alias="6071", description="NXT 매도호가잔량6")
    n_6072: SafeStr = Field(default="", alias="6072", description="NXT 매도호가잔량7")
    n_6073: SafeStr = Field(default="", alias="6073", description="NXT 매도호가잔량8")
    n_6074: SafeStr = Field(default="", alias="6074", description="NXT 매도호가잔량9")
    n_6075: SafeStr = Field(default="", alias="6075", description="NXT 매도호가잔량10")
    n_6076: SafeStr = Field(default="", alias="6076", description="NXT 매수호가잔량1")
    n_6077: SafeStr = Field(default="", alias="6077", description="NXT 매수호가잔량2")
    n_6078: SafeStr = Field(default="", alias="6078", description="NXT 매수호가잔량3")
    n_6079: SafeStr = Field(default="", alias="6079", description="NXT 매수호가잔량4")
    n_6080: SafeStr = Field(default="", alias="6080", description="NXT 매수호가잔량5")
    n_6081: SafeStr = Field(default="", alias="6081", description="NXT 매수호가잔량6")
    n_6082: SafeStr = Field(default="", alias="6082", description="NXT 매수호가잔량7")
    n_6083: SafeStr = Field(default="", alias="6083", description="NXT 매수호가잔량8")
    n_6084: SafeStr = Field(default="", alias="6084", description="NXT 매수호가잔량9")
    n_6085: SafeStr = Field(default="", alias="6085", description="NXT 매수호가잔량10")
    n_6086: SafeStr = Field(default="", alias="6086", description="NXT 매도호가총잔량")
    n_6087: SafeStr = Field(default="", alias="6087", description="NXT 매수호가총잔량")
    n_6100: SafeStr = Field(default="", alias="6100", description="KRX 중간가 매도 총잔량 증감")
    n_6101: SafeStr = Field(default="", alias="6101", description="KRX 중간가 매도 총잔량")
    n_6102: SafeStr = Field(default="", alias="6102", description="KRX 중간가")
    n_6103: SafeStr = Field(default="", alias="6103", description="KRX 중간가 매수 총잔량")
    n_6104: SafeStr = Field(default="", alias="6104", description="KRX 중간가 매수 총잔량 증감")
    n_6105: SafeStr = Field(default="", alias="6105", description="NXT중간가 매도 총잔량 증감")
    n_6106: SafeStr = Field(default="", alias="6106", description="NXT중간가 매도 총잔량")
    n_6107: SafeStr = Field(default="", alias="6107", description="NXT중간가")
    n_6108: SafeStr = Field(default="", alias="6108", description="NXT중간가 매수 총잔량")
    n_6109: SafeStr = Field(default="", alias="6109", description="NXT중간가 매수 총잔량 증감")
    n_6110: SafeStr = Field(default="", alias="6110", description="KRX중간가대비 기준가대비")
    n_6111: SafeStr = Field(default="", alias="6111", description="KRX중간가대비 기호 기준가대비")
    n_6112: SafeStr = Field(default="", alias="6112", description="KRX중간가대비등락율 기준가대비")
    n_6113: SafeStr = Field(default="", alias="6113", description="NXT중간가대비 기준가대비")
    n_6114: SafeStr = Field(default="", alias="6114", description="NXT중간가대비 기호 기준가대비")
    n_6115: SafeStr = Field(default="", alias="6115", description="NXT중간가대비등락율 기준가대비")

class StockQuoteBalance_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockQuoteBalance_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockQuoteBalance(BaseModel):
    """[0D] 주식호가잔량 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockQuoteBalance_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockAfterHoursQuoteRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockAfterHoursQuoteRequest(BaseModel):
    """[0E] 주식시간외호가 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockAfterHoursQuoteRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockAfterHoursQuote_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_21: SafeStr = Field(default="", alias="21", description="호가시간")
    n_131: SafeStr = Field(default="", alias="131", description="시간외매도호가총잔량")
    n_132: SafeStr = Field(default="", alias="132", description="시간외매도호가총잔량직전대비")
    n_135: SafeStr = Field(default="", alias="135", description="시간외매수호가총잔량")
    n_136: SafeStr = Field(default="", alias="136", description="시간외매수호가총잔량직전대비")

class StockAfterHoursQuote_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 거래소별 종목코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    values: Annotated[List[StockAfterHoursQuote_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockAfterHoursQuote(BaseModel):
    """[0E] 주식시간외호가 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockAfterHoursQuote_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockDayTraderRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockDayTraderRequest(BaseModel):
    """[0F] 주식당일거래원 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockDayTraderRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockDayTrader_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_141: SafeStr = Field(default="", alias="141", description="매도거래원1")
    n_161: SafeStr = Field(default="", alias="161", description="매도거래원수량1")
    n_166: SafeStr = Field(default="", alias="166", description="매도거래원별증감1")
    n_146: SafeStr = Field(default="", alias="146", description="매도거래원코드1")
    n_271: SafeStr = Field(default="", alias="271", description="매도거래원색깔1")
    n_151: SafeStr = Field(default="", alias="151", description="매수거래원1")
    n_171: SafeStr = Field(default="", alias="171", description="매수거래원수량1")
    n_176: SafeStr = Field(default="", alias="176", description="매수거래원별증감1")
    n_156: SafeStr = Field(default="", alias="156", description="매수거래원코드1")
    n_281: SafeStr = Field(default="", alias="281", description="매수거래원색깔1")
    n_142: SafeStr = Field(default="", alias="142", description="매도거래원2")
    n_162: SafeStr = Field(default="", alias="162", description="매도거래원수량2")
    n_167: SafeStr = Field(default="", alias="167", description="매도거래원별증감2")
    n_147: SafeStr = Field(default="", alias="147", description="매도거래원코드2")
    n_272: SafeStr = Field(default="", alias="272", description="매도거래원색깔2")
    n_152: SafeStr = Field(default="", alias="152", description="매수거래원2")
    n_172: SafeStr = Field(default="", alias="172", description="매수거래원수량2")
    n_177: SafeStr = Field(default="", alias="177", description="매수거래원별증감2")
    n_157: SafeStr = Field(default="", alias="157", description="매수거래원코드2")
    n_282: SafeStr = Field(default="", alias="282", description="매수거래원색깔2")
    n_143: SafeStr = Field(default="", alias="143", description="매도거래원3")
    n_163: SafeStr = Field(default="", alias="163", description="매도거래원수량3")
    n_168: SafeStr = Field(default="", alias="168", description="매도거래원별증감3")
    n_148: SafeStr = Field(default="", alias="148", description="매도거래원코드3")
    n_273: SafeStr = Field(default="", alias="273", description="매도거래원색깔3")
    n_153: SafeStr = Field(default="", alias="153", description="매수거래원3")
    n_173: SafeStr = Field(default="", alias="173", description="매수거래원수량3")
    n_178: SafeStr = Field(default="", alias="178", description="매수거래원별증감3")
    n_158: SafeStr = Field(default="", alias="158", description="매수거래원코드3")
    n_283: SafeStr = Field(default="", alias="283", description="매수거래원색깔3")
    n_144: SafeStr = Field(default="", alias="144", description="매도거래원4")
    n_164: SafeStr = Field(default="", alias="164", description="매도거래원수량4")
    n_169: SafeStr = Field(default="", alias="169", description="매도거래원별증감4")
    n_149: SafeStr = Field(default="", alias="149", description="매도거래원코드4")
    n_274: SafeStr = Field(default="", alias="274", description="매도거래원색깔4")
    n_154: SafeStr = Field(default="", alias="154", description="매수거래원4")
    n_174: SafeStr = Field(default="", alias="174", description="매수거래원수량4")
    n_179: SafeStr = Field(default="", alias="179", description="매수거래원별증감4")
    n_159: SafeStr = Field(default="", alias="159", description="매수거래원코드4")
    n_284: SafeStr = Field(default="", alias="284", description="매수거래원색깔4")
    n_145: SafeStr = Field(default="", alias="145", description="매도거래원5")
    n_165: SafeStr = Field(default="", alias="165", description="매도거래원수량5")
    n_170: SafeStr = Field(default="", alias="170", description="매도거래원별증감5")
    n_150: SafeStr = Field(default="", alias="150", description="매도거래원코드5")
    n_275: SafeStr = Field(default="", alias="275", description="매도거래원색깔5")
    n_155: SafeStr = Field(default="", alias="155", description="매수거래원5")
    n_175: SafeStr = Field(default="", alias="175", description="매수거래원수량5")
    n_180: SafeStr = Field(default="", alias="180", description="매수거래원별증감5")
    n_160: SafeStr = Field(default="", alias="160", description="매수거래원코드5")
    n_285: SafeStr = Field(default="", alias="285", description="매수거래원색깔5")
    n_261: SafeStr = Field(default="", alias="261", description="외국계매도추정합")
    n_262: SafeStr = Field(default="", alias="262", description="외국계매도추정합변동")
    n_263: SafeStr = Field(default="", alias="263", description="외국계매수추정합")
    n_264: SafeStr = Field(default="", alias="264", description="외국계매수추정합변동")
    n_267: SafeStr = Field(default="", alias="267", description="외국계순매수추정합")
    n_268: SafeStr = Field(default="", alias="268", description="외국계순매수변동")
    n_337: SafeStr = Field(default="", alias="337", description="거래소구분")

class StockDayTrader_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockDayTrader_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockDayTrader(BaseModel):
    """[0F] 주식당일거래원 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockDayTrader_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class EtfNavRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class EtfNavRequest(BaseModel):
    """[0G] ETF NAV 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[EtfNavRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class EtfNav_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_36: SafeStr = Field(default="", alias="36", description="NAV")
    n_37: SafeStr = Field(default="", alias="37", description="NAV전일대비")
    n_38: SafeStr = Field(default="", alias="38", description="NAV등락율")
    n_39: SafeStr = Field(default="", alias="39", description="추적오차율")
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")
    n_667: SafeStr = Field(default="", alias="667", description="ELW기어링비율")
    n_668: SafeStr = Field(default="", alias="668", description="ELW손익분기율")
    n_669: SafeStr = Field(default="", alias="669", description="ELW자본지지점")
    n_265: SafeStr = Field(default="", alias="265", description="NAV/지수괴리율")
    n_266: SafeStr = Field(default="", alias="266", description="NAV/ETF괴리율")

class EtfNav_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[EtfNav_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class EtfNav(BaseModel):
    """[0G] ETF NAV 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[EtfNav_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockExpectedExecutionRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockExpectedExecutionRequest(BaseModel):
    """[0H] 주식예상체결 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockExpectedExecutionRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockExpectedExecution_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_15: SafeStr = Field(default="", alias="15", description="거래량 +는 매수체결, -는 매도체결")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")

class StockExpectedExecution_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockExpectedExecution_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockExpectedExecution(BaseModel):
    """[0H] 주식예상체결 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockExpectedExecution_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class InternationalGoldConversionPriceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 MGD: 원/g, MGU: $/온스,소수점2자리")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class InternationalGoldConversionPriceRequest(BaseModel):
    """[0I] 국제금환산가격 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[InternationalGoldConversionPriceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class InternationalGoldConversionPrice_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호 1:상한, 2:상승, 3:없음, 4:하한, 5:하락")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")

class InternationalGoldConversionPrice_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0B,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[InternationalGoldConversionPrice_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class InternationalGoldConversionPrice(BaseModel):
    """[0I] 국제금환산가격 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[InternationalGoldConversionPrice_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class SectorIndexRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class SectorIndexRequest(BaseModel):
    """[0J] 업종지수 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[SectorIndexRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class SectorIndex_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_15: SafeStr = Field(default="", alias="15", description="거래량 +는 매수체결,-는 매도체결")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_14: SafeStr = Field(default="", alias="14", description="누적거래대금")
    n_16: SafeStr = Field(default="", alias="16", description="시가")
    n_17: SafeStr = Field(default="", alias="17", description="고가")
    n_18: SafeStr = Field(default="", alias="18", description="저가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")
    n_26: SafeStr = Field(default="", alias="26", description="전일거래량대비 계약,주")

class SectorIndex_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[SectorIndex_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class SectorIndex(BaseModel):
    """[0J] 업종지수 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[SectorIndex_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class IndustryFluctuationsRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class IndustryFluctuationsRequest(BaseModel):
    """[0U] 업종등락 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[IndustryFluctuationsRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class IndustryFluctuations_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_252: SafeStr = Field(default="", alias="252", description="상승종목수")
    n_251: SafeStr = Field(default="", alias="251", description="상한종목수")
    n_253: SafeStr = Field(default="", alias="253", description="보합종목수")
    n_255: SafeStr = Field(default="", alias="255", description="하락종목수")
    n_254: SafeStr = Field(default="", alias="254", description="하한종목수")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_14: SafeStr = Field(default="", alias="14", description="누적거래대금")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_256: SafeStr = Field(default="", alias="256", description="거래형성종목수 계약,주")
    n_257: SafeStr = Field(default="", alias="257", description="거래형성비율")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")

class IndustryFluctuations_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[IndustryFluctuations_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class IndustryFluctuations(BaseModel):
    """[0U] 업종등락 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[IndustryFluctuations_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockItemInformationRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockItemInformationRequest(BaseModel):
    """[0g] 주식종목정보 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockItemInformationRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockItemInformation_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_297: SafeStr = Field(default="", alias="297", description="임의연장")
    n_592: SafeStr = Field(default="", alias="592", description="장전임의연장")
    n_593: SafeStr = Field(default="", alias="593", description="장후임의연장")
    n_305: SafeStr = Field(default="", alias="305", description="상한가")
    n_306: SafeStr = Field(default="", alias="306", description="하한가")
    n_307: SafeStr = Field(default="", alias="307", description="기준가")
    n_689: SafeStr = Field(default="", alias="689", description="조기종료ELW발생")
    n_594: SafeStr = Field(default="", alias="594", description="통화단위")
    n_382: SafeStr = Field(default="", alias="382", description="증거금율표시")
    n_370: SafeStr = Field(default="", alias="370", description="종목정보")

class StockItemInformation_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockItemInformation_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockItemInformation(BaseModel):
    """[0g] 주식종목정보 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockItemInformation_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class ElwTheoristRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class ElwTheoristRequest(BaseModel):
    """[0m] ELW 이론가 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[ElwTheoristRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class ElwTheorist_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_670: SafeStr = Field(default="", alias="670", description="ELW이론가")
    n_671: SafeStr = Field(default="", alias="671", description="ELW내재변동성")
    n_672: SafeStr = Field(default="", alias="672", description="ELW델타")
    n_673: SafeStr = Field(default="", alias="673", description="ELW감마")
    n_674: SafeStr = Field(default="", alias="674", description="ELW쎄타")
    n_675: SafeStr = Field(default="", alias="675", description="ELW베가")
    n_676: SafeStr = Field(default="", alias="676", description="ELW로")
    n_706: SafeStr = Field(default="", alias="706", description="LP호가내재변동성")

class ElwTheorist_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[ElwTheorist_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class ElwTheorist(BaseModel):
    """[0m] ELW 이론가 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[ElwTheorist_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class LongStartTimeRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class LongStartTimeRequest(BaseModel):
    """[0s] 장시작시간 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[LongStartTimeRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class LongStartTime_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_215: SafeStr = Field(default="", alias="215", description="장운영구분 0 : 장시작전 알림(8:40~),  3 : 장시작(09:00),  2 : 장마감 알림(15:20~),  4 : 장마감(15:30),  8 : 정규장마감(거래소 수신시 15:30 이후),  9 : 전체장마감(거래소 수신시 18:00 이후),  a : 시간외 종가매매 시작(15:40),  b : 시간외 종가매매 종료(16:00),  c : 시간외 단일가 시작(16:00),  d : 시간외 단일가 종료(18:00),  e : 선옵 장마감전 동시호가 종료,  f : 선물옵션 장운영시간 알림(조기개장 상품),  o : 선옵 장시작,  s : 선옵 장마감전 동시호가 시작,  P : NXT 프리마켓 시작 알림,  Q : NXT 프리마켓 종료 알림,  R : NXT 메인마켓 시작 알림,  S : NXT 메인마켓 종료 알림,  T : NXT 에프터마켓 단일가 시작 알림,  U : NXT 에프터마켓 시작 알림,  V : NXT 에프터마켓 종료 알림")
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_214: SafeStr = Field(default="", alias="214", description="장시작예상잔여시간")

class LongStartTime_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[LongStartTime_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class LongStartTime(BaseModel):
    """[0s] 장시작시간 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[LongStartTime_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class ElwIndicatorRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class ElwIndicatorRequest(BaseModel):
    """[0u] ELW 지표 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[ElwIndicatorRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class ElwIndicator_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_666: SafeStr = Field(default="", alias="666", description="ELW패리티")
    n_1211: SafeStr = Field(default="", alias="1211", description="ELW프리미엄")
    n_667: SafeStr = Field(default="", alias="667", description="ELW기어링비율")
    n_668: SafeStr = Field(default="", alias="668", description="ELW손익분기율")
    n_669: SafeStr = Field(default="", alias="669", description="ELW자본지지점")

class ElwIndicator_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[ElwIndicator_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class ElwIndicator(BaseModel):
    """[0u] ELW 지표 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[ElwIndicator_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockProgramTradingRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockProgramTradingRequest(BaseModel):
    """[0w] 종목프로그램매매 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockProgramTradingRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockProgramTrading_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_202: SafeStr = Field(default="", alias="202", description="매도수량")
    n_204: SafeStr = Field(default="", alias="204", description="매도금액")
    n_206: SafeStr = Field(default="", alias="206", description="매수수량")
    n_208: SafeStr = Field(default="", alias="208", description="매수금액")
    n_210: SafeStr = Field(default="", alias="210", description="순매수수량")
    n_211: SafeStr = Field(default="", alias="211", description="순매수수량증감 계약,주")
    n_212: SafeStr = Field(default="", alias="212", description="순매수금액")
    n_213: SafeStr = Field(default="", alias="213", description="순매수금액증감")
    n_214: SafeStr = Field(default="", alias="214", description="장시작예상잔여시간")
    n_215: SafeStr = Field(default="", alias="215", description="장운영구분")
    n_216: SafeStr = Field(default="", alias="216", description="투자자별ticker")

class StockProgramTrading_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockProgramTrading_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockProgramTrading(BaseModel):
    """[0w] 종목프로그램매매 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockProgramTrading_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class ActivateDisableViRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class ActivateDisableViRequest(BaseModel):
    """[1h] VI발동/해제 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[ActivateDisableViRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class ActivateDisableVi_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_9001: SafeStr = Field(default="", alias="9001", description="종목코드")
    n_302: SafeStr = Field(default="", alias="302", description="종목명")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_14: SafeStr = Field(default="", alias="14", description="누적거래대금")
    n_9068: SafeStr = Field(default="", alias="9068", description="VI발동구분")
    n_9008: SafeStr = Field(default="", alias="9008", description="KOSPI,KOSDAQ,전체구분")
    n_9075: SafeStr = Field(default="", alias="9075", description="장전구분")
    n_1221: SafeStr = Field(default="", alias="1221", description="VI발동가격")
    n_1223: SafeStr = Field(default="", alias="1223", description="매매체결처리시각")
    n_1224: SafeStr = Field(default="", alias="1224", description="VI해제시각")
    n_1225: SafeStr = Field(default="", alias="1225", description="VI적용구분 정적/동적/동적+정적")
    n_1236: SafeStr = Field(default="", alias="1236", description="기준가격 정적 계약,주")
    n_1237: SafeStr = Field(default="", alias="1237", description="기준가격 동적")
    n_1238: SafeStr = Field(default="", alias="1238", description="괴리율 정적")
    n_1239: SafeStr = Field(default="", alias="1239", description="괴리율 동적")
    n_1489: SafeStr = Field(default="", alias="1489", description="VI발동가 등락율")
    n_1490: SafeStr = Field(default="", alias="1490", description="VI발동횟수")
    n_9069: SafeStr = Field(default="", alias="9069", description="발동방향구분")
    n_1279: SafeStr = Field(default="", alias="1279", description="Extra Item")

class ActivateDisableVi_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[ActivateDisableVi_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class ActivateDisableVi(BaseModel):
    """[1h] VI발동/해제 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[ActivateDisableVi_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class IndustryProgramRequest(BaseModel):
    """[ka10010] 업종프로그램요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class IndustryProgram(BaseModel):
    """[ka10010] 업종프로그램요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dfrt_trst_sell_qty: SafeStr = Field(default="", description="차익위탁매도수량")
    dfrt_trst_sell_amt: SafeStr = Field(default="", description="차익위탁매도금액")
    dfrt_trst_buy_qty: SafeStr = Field(default="", description="차익위탁매수수량")
    dfrt_trst_buy_amt: SafeStr = Field(default="", description="차익위탁매수금액")
    dfrt_trst_netprps_qty: SafeStr = Field(default="", description="차익위탁순매수수량")
    dfrt_trst_netprps_amt: SafeStr = Field(default="", description="차익위탁순매수금액")
    ndiffpro_trst_sell_qty: SafeStr = Field(default="", description="비차익위탁매도수량")
    ndiffpro_trst_sell_amt: SafeStr = Field(default="", description="비차익위탁매도금액")
    ndiffpro_trst_buy_qty: SafeStr = Field(default="", description="비차익위탁매수수량")
    ndiffpro_trst_buy_amt: SafeStr = Field(default="", description="비차익위탁매수금액")
    ndiffpro_trst_netprps_qty: SafeStr = Field(default="", description="비차익위탁순매수수량")
    ndiffpro_trst_netprps_amt: SafeStr = Field(default="", description="비차익위탁순매수금액")
    all_dfrt_trst_sell_qty: SafeStr = Field(default="", description="전체차익위탁매도수량")
    all_dfrt_trst_sell_amt: SafeStr = Field(default="", description="전체차익위탁매도금액")
    all_dfrt_trst_buy_qty: SafeStr = Field(default="", description="전체차익위탁매수수량")
    all_dfrt_trst_buy_amt: SafeStr = Field(default="", description="전체차익위탁매수금액")
    all_dfrt_trst_netprps_qty: SafeStr = Field(default="", description="전체차익위탁순매수수량")
    all_dfrt_trst_netprps_amt: SafeStr = Field(default="", description="전체차익위탁순매수금액")

class InvestorNetPurchaseByIndustryRequest(BaseModel):
    """[ka10051] 업종별투자자순매수요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 코스피:0, 코스닥:1")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 금액:0, 수량:1")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class InvestorNetPurchaseByIndustry_IndsNetprps(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_nm: SafeStr = Field(default="", description="업종명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_smbol: SafeStr = Field(default="", description="대비부호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    sc_netprps: SafeStr = Field(default="", description="증권순매수")
    insrnc_netprps: SafeStr = Field(default="", description="보험순매수")
    invtrt_netprps: SafeStr = Field(default="", description="투신순매수")
    bank_netprps: SafeStr = Field(default="", description="은행순매수")
    jnsinkm_netprps: SafeStr = Field(default="", description="종신금순매수")
    endw_netprps: SafeStr = Field(default="", description="기금순매수")
    etc_corp_netprps: SafeStr = Field(default="", description="기타법인순매수")
    ind_netprps: SafeStr = Field(default="", description="개인순매수")
    frgnr_netprps: SafeStr = Field(default="", description="외국인순매수")
    native_trmt_frgnr_netprps: SafeStr = Field(default="", description="내국인대우외국인순매수")
    natn_netprps: SafeStr = Field(default="", description="국가순매수")
    samo_fund_netprps: SafeStr = Field(default="", description="사모펀드순매수")
    orgn_netprps: SafeStr = Field(default="", description="기관계순매수")

class InvestorNetPurchaseByIndustry(BaseModel):
    """[ka10051] 업종별투자자순매수요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_netprps: Annotated[List[InvestorNetPurchaseByIndustry_IndsNetprps], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종별순매수")

class CurrentIndustryRequest(BaseModel):
    """[ka20001] 업종현재가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피, 1:코스닥, 2:코스피200")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")

class CurrentIndustry_IndsCurPrcTm(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm_n: SafeStr = Field(default="", description="시간n")
    cur_prc_n: SafeStr = Field(default="", description="현재가n")
    pred_pre_sig_n: SafeStr = Field(default="", description="전일대비기호n")
    pred_pre_n: SafeStr = Field(default="", description="전일대비n")
    flu_rt_n: SafeStr = Field(default="", description="등락률n")
    trde_qty_n: SafeStr = Field(default="", description="거래량n")
    acc_trde_qty_n: SafeStr = Field(default="", description="누적거래량n")

class CurrentIndustry(BaseModel):
    """[ka20001] 업종현재가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    trde_frmatn_stk_num: SafeStr = Field(default="", description="거래형성종목수")
    trde_frmatn_rt: SafeStr = Field(default="", description="거래형성비율")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    upl: SafeStr = Field(default="", description="상한")
    rising: SafeStr = Field(default="", description="상승")
    stdns: SafeStr = Field(default="", description="보합")
    fall: SafeStr = Field(default="", description="하락")
    lst: SafeStr = Field(default="", description="하한")
    n_52wk_hgst_pric: SafeStr = Field(default="", alias="52wk_hgst_pric", description="52주최고가")
    n_52wk_hgst_pric_dt: SafeStr = Field(default="", alias="52wk_hgst_pric_dt", description="52주최고가일")
    n_52wk_hgst_pric_pre_rt: SafeStr = Field(default="", alias="52wk_hgst_pric_pre_rt", description="52주최고가대비율")
    n_52wk_lwst_pric: SafeStr = Field(default="", alias="52wk_lwst_pric", description="52주최저가")
    n_52wk_lwst_pric_dt: SafeStr = Field(default="", alias="52wk_lwst_pric_dt", description="52주최저가일")
    n_52wk_lwst_pric_pre_rt: SafeStr = Field(default="", alias="52wk_lwst_pric_pre_rt", description="52주최저가대비율")
    inds_cur_prc_tm: Annotated[List[CurrentIndustry_IndsCurPrcTm], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종현재가_시간별")

class StocksByIndustryRequest(BaseModel):
    """[ka20002] 업종별주가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피, 1:코스닥, 2:코스피200")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class StocksByIndustry_IndsStkpc(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")

class StocksByIndustry(BaseModel):
    """[ka20002] 업종별주가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_stkpc: Annotated[List[StocksByIndustry_IndsStkpc], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종별주가")

class AllIndustryIndicesRequest(BaseModel):
    """[ka20003] 전업종지수요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 101:종합(KOSDAQ)")

class AllIndustryIndices_AllIndsIdex(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    wght: SafeStr = Field(default="", description="비중")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    upl: SafeStr = Field(default="", description="상한")
    rising: SafeStr = Field(default="", description="상승")
    stdns: SafeStr = Field(default="", description="보합")
    fall: SafeStr = Field(default="", description="하락")
    lst: SafeStr = Field(default="", description="하한")
    flo_stk_num: SafeStr = Field(default="", description="상장종목수")

class AllIndustryIndices(BaseModel):
    """[ka20003] 전업종지수요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    all_inds_idex: Annotated[List[AllIndustryIndices_AllIndsIdex], BeforeValidator(_force_list)] = Field(default_factory=list, description="전업종지수")

class IndustryCurrentPriceDailyRequest(BaseModel):
    """[ka20009] 업종현재가일별요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피, 1:코스닥, 2:코스피200")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")

class IndustryCurrentPriceDaily_IndsCurPrcDalyRept(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt_n: SafeStr = Field(default="", description="일자n")
    cur_prc_n: SafeStr = Field(default="", description="현재가n")
    pred_pre_sig_n: SafeStr = Field(default="", description="전일대비기호n")
    pred_pre_n: SafeStr = Field(default="", description="전일대비n")
    flu_rt_n: SafeStr = Field(default="", description="등락률n")
    acc_trde_qty_n: SafeStr = Field(default="", description="누적거래량n")

class IndustryCurrentPriceDaily(BaseModel):
    """[ka20009] 업종현재가일별요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    trde_frmatn_stk_num: SafeStr = Field(default="", description="거래형성종목수")
    trde_frmatn_rt: SafeStr = Field(default="", description="거래형성비율")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    upl: SafeStr = Field(default="", description="상한")
    rising: SafeStr = Field(default="", description="상승")
    stdns: SafeStr = Field(default="", description="보합")
    fall: SafeStr = Field(default="", description="하락")
    lst: SafeStr = Field(default="", description="하한")
    n_52wk_hgst_pric: SafeStr = Field(default="", alias="52wk_hgst_pric", description="52주최고가")
    n_52wk_hgst_pric_dt: SafeStr = Field(default="", alias="52wk_hgst_pric_dt", description="52주최고가일")
    n_52wk_hgst_pric_pre_rt: SafeStr = Field(default="", alias="52wk_hgst_pric_pre_rt", description="52주최고가대비율")
    n_52wk_lwst_pric: SafeStr = Field(default="", alias="52wk_lwst_pric", description="52주최저가")
    n_52wk_lwst_pric_dt: SafeStr = Field(default="", alias="52wk_lwst_pric_dt", description="52주최저가일")
    n_52wk_lwst_pric_pre_rt: SafeStr = Field(default="", alias="52wk_lwst_pric_pre_rt", description="52주최저가대비율")
    inds_cur_prc_daly_rept: Annotated[List[IndustryCurrentPriceDaily_IndsCurPrcDalyRept], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종현재가_일별반복")

class ConditionSearchListRequest(BaseModel):
    """[ka10171] 조건검색 목록조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="TR명 CNSRLST고정값")

class ConditionSearchList_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    name: SafeStr = Field(default="", description="조건검색식 명")

class ConditionSearchList(BaseModel):
    """[ka10171] 조건검색 목록조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상 : 0")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRLST 고정값")
    data: Annotated[List[ConditionSearchList_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="조건검색식 목록")

class ConditionalSearchGeneralRequest(BaseModel):
    """[ka10172] 조건검색 요청 일반 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    search_type: SafeStr = Field(default="", description="조회타입 0:조건검색")
    stex_tp: SafeStr = Field(default="", description="거래소구분 K:KRX")
    cont_yn: SafeStr = Field(default="", description="연속조회여부 Y:연속조회요청,N:연속조회미요청")
    next_key: SafeStr = Field(default="", description="연속조회키")

class ConditionalSearchGeneral_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_9001: SafeStr = Field(default="", alias="9001", description="종목코드")
    n_302: SafeStr = Field(default="", alias="302", description="종목명")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_16: SafeStr = Field(default="", alias="16", description="시가")
    n_17: SafeStr = Field(default="", alias="17", description="고가")
    n_18: SafeStr = Field(default="", alias="18", description="저가")

class ConditionalSearchGeneral(BaseModel):
    """[ka10172] 조건검색 요청 일반 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상:0 나머지:에러")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    cont_yn: SafeStr = Field(default="", description="연속조회여부 연속 데이터가 존재하는경우 Y, 없으면 N")
    next_key: SafeStr = Field(default="", description="연속조회키 연속조회여부가Y일경우 다음 조회시 필요한 조회값")
    data: Annotated[List[ConditionalSearchGeneral_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="검색결과데이터")

class RealTimeConditionalSearchRequest(BaseModel):
    """[ka10173] 조건검색 요청 실시간 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    search_type: SafeStr = Field(default="", description="조회타입 1: 조건검색+실시간조건검색")
    stex_tp: SafeStr = Field(default="", description="거래소구분 K:KRX")

class RealTimeConditionalSearch_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    jmcode: SafeStr = Field(default="", description="종목코드")

class RealTimeConditionalSearch(BaseModel):
    """[ka10173] 조건검색 요청 실시간 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상:0 나머지:에러")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    data: Annotated[List[RealTimeConditionalSearch_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="검색결과데이터")

class ConditionalSearchRealTimeCancellationRequest(BaseModel):
    """[ka10174] 조건검색 실시간 해제 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 CNSRCLR 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")

class ConditionalSearchRealTimeCancellation(BaseModel):
    """[ka10174] 조건검색 실시간 해제 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상:0 나머지:에러")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRCLR 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")

class RealTimeItemRankingRequest(BaseModel):
    """[ka00198] 실시간종목조회순위 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="구분 1:1분, 2:10분, 3:1시간, 4:당일 누적, 5:30초")

class RealTimeItemRanking_ItemInqRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    bigd_rank: SafeStr = Field(default="", description="빅데이터 순위")
    rank_chg: SafeStr = Field(default="", description="순위 등락")
    rank_chg_sign: SafeStr = Field(default="", description="순위 등락 부호")
    past_curr_prc: SafeStr = Field(default="", description="과거 현재가")
    base_comp_sign: SafeStr = Field(default="", description="기준가 대비 부호")
    base_comp_chgr: SafeStr = Field(default="", description="기준가 대비 등락율")
    prev_base_sign: SafeStr = Field(default="", description="직전 기준 대비 부호")
    prev_base_chgr: SafeStr = Field(default="", description="직전 기준 대비 등락율")
    dt: SafeStr = Field(default="", description="일자")
    tm: SafeStr = Field(default="", description="시간")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class RealTimeItemRanking(BaseModel):
    """[ka00198] 실시간종목조회순위 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    item_inq_rank: Annotated[List[RealTimeItemRanking_ItemInqRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간종목조회순위")

class BasicStockInformationRequest(BaseModel):
    """[ka10001] 주식기본정보요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class BasicStockInformation(BaseModel):
    """[ka10001] 주식기본정보요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    setl_mm: SafeStr = Field(default="", description="결산월")
    fav: SafeStr = Field(default="", description="액면가")
    cap: SafeStr = Field(default="", description="자본금")
    flo_stk: SafeStr = Field(default="", description="상장주식")
    crd_rt: SafeStr = Field(default="", description="신용비율")
    oyr_hgst: SafeStr = Field(default="", description="연중최고")
    oyr_lwst: SafeStr = Field(default="", description="연중최저")
    mac: SafeStr = Field(default="", description="시가총액")
    mac_wght: SafeStr = Field(default="", description="시가총액비중")
    for_exh_rt: SafeStr = Field(default="", description="외인소진률")
    repl_pric: SafeStr = Field(default="", description="대용가")
    per: SafeStr = Field(default="", description="PER [ 주의 ] PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨")
    eps: SafeStr = Field(default="", description="EPS")
    roe: SafeStr = Field(default="", description="ROE [ 주의 ]  PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨")
    pbr: SafeStr = Field(default="", description="PBR")
    ev: SafeStr = Field(default="", description="EV")
    bps: SafeStr = Field(default="", description="BPS")
    sale_amt: SafeStr = Field(default="", description="매출액")
    bus_pro: SafeStr = Field(default="", description="영업이익")
    cup_nga: SafeStr = Field(default="", description="당기순이익")
    n_250hgst: SafeStr = Field(default="", alias="250hgst", description="250최고")
    n_250lwst: SafeStr = Field(default="", alias="250lwst", description="250최저")
    high_pric: SafeStr = Field(default="", description="고가")
    open_pric: SafeStr = Field(default="", description="시가")
    low_pric: SafeStr = Field(default="", description="저가")
    upl_pric: SafeStr = Field(default="", description="상한가")
    lst_pric: SafeStr = Field(default="", description="하한가")
    base_pric: SafeStr = Field(default="", description="기준가")
    exp_cntr_pric: SafeStr = Field(default="", description="예상체결가")
    exp_cntr_qty: SafeStr = Field(default="", description="예상체결수량")
    n_250hgst_pric_dt: SafeStr = Field(default="", alias="250hgst_pric_dt", description="250최고가일")
    n_250hgst_pric_pre_rt: SafeStr = Field(default="", alias="250hgst_pric_pre_rt", description="250최고가대비율")
    n_250lwst_pric_dt: SafeStr = Field(default="", alias="250lwst_pric_dt", description="250최저가일")
    n_250lwst_pric_pre_rt: SafeStr = Field(default="", alias="250lwst_pric_pre_rt", description="250최저가대비율")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_pre: SafeStr = Field(default="", description="거래대비")
    fav_unit: SafeStr = Field(default="", description="액면가단위")
    dstr_stk: SafeStr = Field(default="", description="유통주식")
    dstr_rt: SafeStr = Field(default="", description="유통비율")

class StockExchangeRequest(BaseModel):
    """[ka10002] 주식거래원요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockExchange(BaseModel):
    """[ka10002] 주식거래원요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    flu_smbol: SafeStr = Field(default="", description="등락부호")
    base_pric: SafeStr = Field(default="", description="기준가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    sel_trde_ori_nm_1: SafeStr = Field(default="", description="매도거래원명1")
    sel_trde_ori_1: SafeStr = Field(default="", description="매도거래원1")
    sel_trde_qty_1: SafeStr = Field(default="", description="매도거래량1")
    buy_trde_ori_nm_1: SafeStr = Field(default="", description="매수거래원명1")
    buy_trde_ori_1: SafeStr = Field(default="", description="매수거래원1")
    buy_trde_qty_1: SafeStr = Field(default="", description="매수거래량1")
    sel_trde_ori_nm_2: SafeStr = Field(default="", description="매도거래원명2")
    sel_trde_ori_2: SafeStr = Field(default="", description="매도거래원2")
    sel_trde_qty_2: SafeStr = Field(default="", description="매도거래량2")
    buy_trde_ori_nm_2: SafeStr = Field(default="", description="매수거래원명2")
    buy_trde_ori_2: SafeStr = Field(default="", description="매수거래원2")
    buy_trde_qty_2: SafeStr = Field(default="", description="매수거래량2")
    sel_trde_ori_nm_3: SafeStr = Field(default="", description="매도거래원명3")
    sel_trde_ori_3: SafeStr = Field(default="", description="매도거래원3")
    sel_trde_qty_3: SafeStr = Field(default="", description="매도거래량3")
    buy_trde_ori_nm_3: SafeStr = Field(default="", description="매수거래원명3")
    buy_trde_ori_3: SafeStr = Field(default="", description="매수거래원3")
    buy_trde_qty_3: SafeStr = Field(default="", description="매수거래량3")
    sel_trde_ori_nm_4: SafeStr = Field(default="", description="매도거래원명4")
    sel_trde_ori_4: SafeStr = Field(default="", description="매도거래원4")
    sel_trde_qty_4: SafeStr = Field(default="", description="매도거래량4")
    buy_trde_ori_nm_4: SafeStr = Field(default="", description="매수거래원명4")
    buy_trde_ori_4: SafeStr = Field(default="", description="매수거래원4")
    buy_trde_qty_4: SafeStr = Field(default="", description="매수거래량4")
    sel_trde_ori_nm_5: SafeStr = Field(default="", description="매도거래원명5")
    sel_trde_ori_5: SafeStr = Field(default="", description="매도거래원5")
    sel_trde_qty_5: SafeStr = Field(default="", description="매도거래량5")
    buy_trde_ori_nm_5: SafeStr = Field(default="", description="매수거래원명5")
    buy_trde_ori_5: SafeStr = Field(default="", description="매수거래원5")
    buy_trde_qty_5: SafeStr = Field(default="", description="매수거래량5")

class ConclusionInformationRequest(BaseModel):
    """[ka10003] 체결정보요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class ConclusionInformation_CntrInfr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm: SafeStr = Field(default="", description="시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pre_rt: SafeStr = Field(default="", description="대비율")
    pri_sel_bid_unit: SafeStr = Field(default="", description="우선매도호가단위")
    pri_buy_bid_unit: SafeStr = Field(default="", description="우선매수호가단위")
    cntr_trde_qty: SafeStr = Field(default="", description="체결거래량")
    sign: SafeStr = Field(default="", description="sign")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    stex_tp: SafeStr = Field(default="", description="거래소구분 KRX , NXT , 통합")

class ConclusionInformation(BaseModel):
    """[ka10003] 체결정보요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_infr: Annotated[List[ConclusionInformation_CntrInfr], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결정보")

class CreditTradingTrendRequest(BaseModel):
    """[ka10013] 신용매매동향요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:융자, 2:대주")

class CreditTradingTrend_CrdTrdeTrend(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    new: SafeStr = Field(default="", description="신규")
    rpya: SafeStr = Field(default="", description="상환")
    remn: SafeStr = Field(default="", description="잔고")
    amt: SafeStr = Field(default="", description="금액")
    pre: SafeStr = Field(default="", description="대비")
    shr_rt: SafeStr = Field(default="", description="공여율")
    remn_rt: SafeStr = Field(default="", description="잔고율")

class CreditTradingTrend(BaseModel):
    """[ka10013] 신용매매동향요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_trde_trend: Annotated[List[CreditTradingTrend_CrdTrdeTrend], BeforeValidator(_force_list)] = Field(default_factory=list, description="신용매매동향")

class DailyTransactionRequest(BaseModel):
    """[ka10015] 일별거래상세요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")

class DailyTransaction_DalyTrdeDtl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    close_pric: SafeStr = Field(default="", description="종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    bf_mkrt_trde_qty: SafeStr = Field(default="", description="장전거래량")
    bf_mkrt_trde_wght: SafeStr = Field(default="", description="장전거래비중")
    opmr_trde_qty: SafeStr = Field(default="", description="장중거래량")
    opmr_trde_wght: SafeStr = Field(default="", description="장중거래비중")
    af_mkrt_trde_qty: SafeStr = Field(default="", description="장후거래량")
    af_mkrt_trde_wght: SafeStr = Field(default="", description="장후거래비중")
    tot_3: SafeStr = Field(default="", description="합계3")
    prid_trde_qty: SafeStr = Field(default="", description="기간중거래량")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    for_poss: SafeStr = Field(default="", description="외인보유")
    for_wght: SafeStr = Field(default="", description="외인비중")
    for_netprps: SafeStr = Field(default="", description="외인순매수")
    orgn_netprps: SafeStr = Field(default="", description="기관순매수")
    ind_netprps: SafeStr = Field(default="", description="개인순매수")
    frgn: SafeStr = Field(default="", description="외국계")
    crd_remn_rt: SafeStr = Field(default="", description="신용잔고율")
    prm: SafeStr = Field(default="", description="프로그램")
    bf_mkrt_trde_prica: SafeStr = Field(default="", description="장전거래대금")
    bf_mkrt_trde_prica_wght: SafeStr = Field(default="", description="장전거래대금비중")
    opmr_trde_prica: SafeStr = Field(default="", description="장중거래대금")
    opmr_trde_prica_wght: SafeStr = Field(default="", description="장중거래대금비중")
    af_mkrt_trde_prica: SafeStr = Field(default="", description="장후거래대금")
    af_mkrt_trde_prica_wght: SafeStr = Field(default="", description="장후거래대금비중")

class DailyTransaction(BaseModel):
    """[ka10015] 일별거래상세요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_trde_dtl: Annotated[List[DailyTransaction_DalyTrdeDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별거래상세")

class LowReportRequest(BaseModel):
    """[ka10016] 신고저가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    ntl_tp: SafeStr = Field(default="", description="신고저구분 1:신고가,2:신저가")
    high_low_close_tp: SafeStr = Field(default="", description="고저종구분 1:고저기준, 2:종가기준")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    updown_incls: SafeStr = Field(default="", description="상하한포함 0:미포함, 1:포함")
    dt: SafeStr = Field(default="", description="기간 5:5일, 10:10일, 20:20일, 60:60일, 250:250일, 250일까지 입력가능")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class LowReport_NtlPric(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    pred_trde_qty_pre_rt: SafeStr = Field(default="", description="전일거래량대비율")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")

class LowReport(BaseModel):
    """[ka10016] 신고저가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ntl_pric: Annotated[List[LowReport_NtlPric], BeforeValidator(_force_list)] = Field(default_factory=list, description="신고저가")

class UpperLowerLimitsRequest(BaseModel):
    """[ka10017] 상하한가요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    updown_tp: SafeStr = Field(default="", description="상하한구분 1:상한, 2:상승, 3:보합, 4: 하한, 5:하락, 6:전일상한, 7:전일하한")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:종목코드순, 2:연속횟수순(상위100개), 3:등락률순")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회,1:관리종목제외, 3:우선주제외, 4:우선주+관리종목제외, 5:증100제외, 6:증100만 보기, 7:증40만 보기, 8:증30만 보기, 9:증20만 보기, 10:우선주+관리종목+환기종목제외")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    trde_gold_tp: SafeStr = Field(default="", description="매매금구분 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class UpperLowerLimits_UpdownPric(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_infr: SafeStr = Field(default="", description="종목정보")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    pred_trde_qty: SafeStr = Field(default="", description="전일거래량")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    buy_req: SafeStr = Field(default="", description="매수잔량")
    cnt: SafeStr = Field(default="", description="횟수")

class UpperLowerLimits(BaseModel):
    """[ka10017] 상하한가요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    updown_pric: Annotated[List[UpperLowerLimits_UpdownPric], BeforeValidator(_force_list)] = Field(default_factory=list, description="상하한가")

class HighLowPriceProximityRequest(BaseModel):
    """[ka10018] 고저가근접요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    high_low_tp: SafeStr = Field(default="", description="고저구분 1:고가, 2:저가")
    alacc_rt: SafeStr = Field(default="", description="근접율 05:0.5 10:1.0, 15:1.5, 20:2.0. 25:2.5, 30:3.0")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HighLowPriceProximity_HighLowPricAlacc(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    tdy_high_pric: SafeStr = Field(default="", description="당일고가")
    tdy_low_pric: SafeStr = Field(default="", description="당일저가")

class HighLowPriceProximity(BaseModel):
    """[ka10018] 고저가근접요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    high_low_pric_alacc: Annotated[List[HighLowPriceProximity_HighLowPricAlacc], BeforeValidator(_force_list)] = Field(default_factory=list, description="고저가근접")

class SuddenPriceFluctuationRequest(BaseModel):
    """[ka10019] 가격급등락요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥, 201:코스피200")
    flu_tp: SafeStr = Field(default="", description="등락구분 1:급등, 2:급락")
    tm_tp: SafeStr = Field(default="", description="시간구분 1:분전, 2:일전")
    tm: SafeStr = Field(default="", description="시간 분 혹은 일입력")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    pric_cnd: SafeStr = Field(default="", description="가격조건 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상")
    updown_incls: SafeStr = Field(default="", description="상하한포함 0:미포함, 1:포함")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class SuddenPriceFluctuation_PricJmpflu(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_cls: SafeStr = Field(default="", description="종목분류")
    stk_nm: SafeStr = Field(default="", description="종목명")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    base_pric: SafeStr = Field(default="", description="기준가")
    cur_prc: SafeStr = Field(default="", description="현재가")
    base_pre: SafeStr = Field(default="", description="기준대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    jmp_rt: SafeStr = Field(default="", description="급등률")

class SuddenPriceFluctuation(BaseModel):
    """[ka10019] 가격급등락요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pric_jmpflu: Annotated[List[SuddenPriceFluctuation_PricJmpflu], BeforeValidator(_force_list)] = Field(default_factory=list, description="가격급등락")

class TransactionVolumeUpdateRequest(BaseModel):
    """[ka10024] 거래량갱신요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    cycle_tp: SafeStr = Field(default="", description="주기구분 5:5일, 10:10일, 20:20일, 60:60일, 250:250일")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TransactionVolumeUpdate_TrdeQtyUpdt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    prev_trde_qty: SafeStr = Field(default="", description="이전거래량")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")

class TransactionVolumeUpdate(BaseModel):
    """[ka10024] 거래량갱신요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_qty_updt: Annotated[List[TransactionVolumeUpdate_TrdeQtyUpdt], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래량갱신")

class ConcentrationPropertiesSaleRequest(BaseModel):
    """[ka10025] 매물대집중요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    prps_cnctr_rt: SafeStr = Field(default="", description="매물집중비율 0~100 입력")
    cur_prc_entry: SafeStr = Field(default="", description="현재가진입 0:현재가 매물대 진입 포함안함, 1:현재가 매물대 진입포함")
    prpscnt: SafeStr = Field(default="", description="매물대수 숫자입력")
    cycle_tp: SafeStr = Field(default="", description="주기구분 50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ConcentrationPropertiesSale_PrpsCnctr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    pric_strt: SafeStr = Field(default="", description="가격대시작")
    pric_end: SafeStr = Field(default="", description="가격대끝")
    prps_qty: SafeStr = Field(default="", description="매물량")
    prps_rt: SafeStr = Field(default="", description="매물비")

class ConcentrationPropertiesSale(BaseModel):
    """[ka10025] 매물대집중요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prps_cnctr: Annotated[List[ConcentrationPropertiesSale_PrpsCnctr], BeforeValidator(_force_list)] = Field(default_factory=list, description="매물대집중")

class HighLowPerRequest(BaseModel):
    """[ka10026] 고저PER요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    pertp: SafeStr = Field(default="", description="PER구분 1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class HighLowPer_HighLowPer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    per: SafeStr = Field(default="", description="PER")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    sel_bid: SafeStr = Field(default="", description="매도호가")

class HighLowPer(BaseModel):
    """[ka10026] 고저PER요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    high_low_per: Annotated[List[HighLowPer_HighLowPer], BeforeValidator(_force_list)] = Field(default_factory=list, description="고저PER")

class FluctuationRateComparedMarketPriceRequest(BaseModel):
    """[ka10028] 시가대비등락률요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:시가, 2:고가, 3:저가, 4:기준가")
    trde_qty_cnd: SafeStr = Field(default="", description="거래량조건 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0500:50만주이상, 1000:백만주이상")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    updown_incls: SafeStr = Field(default="", description="상하한포함 0:불 포함, 1:포함")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    trde_prica_cnd: SafeStr = Field(default="", description="거래대금조건 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상")
    flu_cnd: SafeStr = Field(default="", description="등락조건 1:상위, 2:하위")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class FluctuationRateComparedMarketPrice_OpenPricPreFluRt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    open_pric_pre: SafeStr = Field(default="", description="시가대비")
    now_trde_qty: SafeStr = Field(default="", description="현재거래량")
    cntr_str: SafeStr = Field(default="", description="체결강도")

class FluctuationRateComparedMarketPrice(BaseModel):
    """[ka10028] 시가대비등락률요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    open_pric_pre_flu_rt: Annotated[List[FluctuationRateComparedMarketPrice_OpenPricPreFluRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="시가대비등락률")

class TransactionPriceAnalysisRequest(BaseModel):
    """[ka10043] 거래원매물대분석요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    qry_dt_tp: SafeStr = Field(default="", description="조회기간구분 0:기간으로 조회, 1:시작일자, 종료일자로 조회")
    pot_tp: SafeStr = Field(default="", description="시점구분 0:당일, 1:전일")
    dt: SafeStr = Field(default="", description="기간 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일")
    sort_base: SafeStr = Field(default="", description="정렬기준 1:종가순, 2:날짜순")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TransactionPriceAnalysis_TrdeOriPrpsAnly(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    close_pric: SafeStr = Field(default="", description="종가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    sel_qty: SafeStr = Field(default="", description="매도량")
    buy_qty: SafeStr = Field(default="", description="매수량")
    netprps_qty: SafeStr = Field(default="", description="순매수수량")
    trde_qty_sum: SafeStr = Field(default="", description="거래량합")
    trde_wght: SafeStr = Field(default="", description="거래비중")

class TransactionPriceAnalysis(BaseModel):
    """[ka10043] 거래원매물대분석요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_ori_prps_anly: Annotated[List[TransactionPriceAnalysis_TrdeOriPrpsAnly], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래원매물대분석")

class TraderInstantaneousTradingVolumeRequest(BaseModel):
    """[ka10052] 거래원순간거래량요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:전체, 1:코스피, 2:코스닥, 3:종목")
    qty_tp: SafeStr = Field(default="", description="수량구분 0:전체, 1:1000주, 2:2000주, 3:, 5:, 10:10000주, 30: 30000주, 50: 50000주, 100: 100000주")
    pric_tp: SafeStr = Field(default="", description="가격구분 0:전체, 1:1천원 미만, 8:1천원 이상, 2:1천원 ~ 2천원, 3:2천원 ~ 5천원, 4:5천원 ~ 1만원, 5:1만원 이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TraderInstantaneousTradingVolume_TrdeOriMontTrdeQty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm: SafeStr = Field(default="", description="시간")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    trde_ori_nm: SafeStr = Field(default="", description="거래원명")
    tp: SafeStr = Field(default="", description="구분")
    mont_trde_qty: SafeStr = Field(default="", description="순간거래량")
    acc_netprps: SafeStr = Field(default="", description="누적순매수")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")

class TraderInstantaneousTradingVolume(BaseModel):
    """[ka10052] 거래원순간거래량요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_ori_mont_trde_qty: Annotated[List[TraderInstantaneousTradingVolume_TrdeOriMontTrdeQty], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래원순간거래량")

class ItemsActivateVolatilityMitigationDeviceRequest(BaseModel):
    """[ka10054] 변동성완화장치발동종목요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001: 코스피, 101:코스닥")
    bf_mkrt_tp: SafeStr = Field(default="", description="장전구분 0:전체, 1:정규시장,2:시간외단일가")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL) 공백입력시 시장구분으로 설정한 전체종목조회")
    motn_tp: SafeStr = Field(default="", description="발동구분 0:전체, 1:정적VI, 2:동적VI, 3:동적VI + 정적VI")
    skip_stk: SafeStr = Field(default="", description="제외종목 전종목포함 조회시 9개 0으로 설정(000000000),전종목제외 조회시 9개 1으로 설정(111111111),9개 종목조회여부를 조회포함(0), 조회제외(1)로 설정하며 종목순서는 우선주,관리종목,투자경고/위험,투자주의,환기종목,단기과열종목,증거금100%,ETF,ETN가 됨.우선주만 조회시'011111111'', 관리종목만 조회시 ''101111111'' 설정'")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:사용안함, 1:사용")
    min_trde_qty: SafeStr = Field(default="", description="최소거래량 0 주 이상, 거래량구분이 1일때만 입력(공백허용)")
    max_trde_qty: SafeStr = Field(default="", description="최대거래량 100000000 주 이하, 거래량구분이 1일때만 입력(공백허용)")
    trde_prica_tp: SafeStr = Field(default="", description="거래대금구분 0:사용안함, 1:사용")
    min_trde_prica: SafeStr = Field(default="", description="최소거래대금 0 백만원 이상, 거래대금구분 1일때만 입력(공백허용)")
    max_trde_prica: SafeStr = Field(default="", description="최대거래대금 100000000 백만원 이하, 거래대금구분 1일때만 입력(공백허용)")
    motn_drc: SafeStr = Field(default="", description="발동방향 0:전체, 1:상승, 2:하락")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ItemsActivateVolatilityMitigationDevice_MotnStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    motn_pric: SafeStr = Field(default="", description="발동가격")
    dynm_dispty_rt: SafeStr = Field(default="", description="동적괴리율")
    trde_cntr_proc_time: SafeStr = Field(default="", description="매매체결처리시각")
    virelis_time: SafeStr = Field(default="", description="VI해제시각")
    viaplc_tp: SafeStr = Field(default="", description="VI적용구분")
    dynm_stdpc: SafeStr = Field(default="", description="동적기준가격")
    static_stdpc: SafeStr = Field(default="", description="정적기준가격")
    static_dispty_rt: SafeStr = Field(default="", description="정적괴리율")
    open_pric_pre_flu_rt: SafeStr = Field(default="", description="시가대비등락률")
    vimotn_cnt: SafeStr = Field(default="", description="VI발동횟수")
    stex_tp: SafeStr = Field(default="", description="거래소구분")

class ItemsActivateVolatilityMitigationDevice(BaseModel):
    """[ka10054] 변동성완화장치발동종목요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    motn_stk: Annotated[List[ItemsActivateVolatilityMitigationDevice_MotnStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="발동종목")

class SettlementDayBeforeDayRequest(BaseModel):
    """[ka10055] 당일전일체결량요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tdy_pred: SafeStr = Field(default="", description="당일전일 1:당일, 2:전일")

class SettlementDayBeforeDay_TdyPredCntrQty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")

class SettlementDayBeforeDay(BaseModel):
    """[ka10055] 당일전일체결량요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_pred_cntr_qty: Annotated[List[SettlementDayBeforeDay_TdyPredCntrQty], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일전일체결량")

class DailyTradingItemsByInvestorRequest(BaseModel):
    """[ka10058] 투자자별일별매매종목요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    trde_tp: SafeStr = Field(default="", description="매매구분 순매도:1, 순매수:2")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    invsr_tp: SafeStr = Field(default="", description="투자자구분 8000:개인, 9000:외국인, 1000:금융투자, 3000:투신, 3100:사모펀드, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class DailyTradingItemsByInvestor_InvsrDalyTrdeStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    netslmt_qty: SafeStr = Field(default="", description="순매도수량")
    netslmt_amt: SafeStr = Field(default="", description="순매도금액")
    prsm_avg_pric: SafeStr = Field(default="", description="추정평균가")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    avg_pric_pre: SafeStr = Field(default="", description="평균가대비")
    pre_rt: SafeStr = Field(default="", description="대비율")
    dt_trde_qty: SafeStr = Field(default="", description="기간거래량")

class DailyTradingItemsByInvestor(BaseModel):
    """[ka10058] 투자자별일별매매종목요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    invsr_daly_trde_stk: Annotated[List[DailyTradingItemsByInvestor_InvsrDalyTrdeStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="투자자별일별매매종목")

class RequestsByItemInvestorInstitutionRequest(BaseModel):
    """[ka10059] 종목별투자자기관별요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    unit_tp: SafeStr = Field(default="", description="단위구분 1000:천주, 1:단주")

class RequestsByItemInvestorInstitution_StkInvsrOrgn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율 우측 2자리 소수점자리수")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    ind_invsr: SafeStr = Field(default="", description="개인투자자")
    frgnr_invsr: SafeStr = Field(default="", description="외국인투자자")
    orgn: SafeStr = Field(default="", description="기관계")
    fnnc_invt: SafeStr = Field(default="", description="금융투자")
    insrnc: SafeStr = Field(default="", description="보험")
    invtrt: SafeStr = Field(default="", description="투신")
    etc_fnnc: SafeStr = Field(default="", description="기타금융")
    bank: SafeStr = Field(default="", description="은행")
    penfnd_etc: SafeStr = Field(default="", description="연기금등")
    samo_fund: SafeStr = Field(default="", description="사모펀드")
    natn: SafeStr = Field(default="", description="국가")
    etc_corp: SafeStr = Field(default="", description="기타법인")
    natfor: SafeStr = Field(default="", description="내외국인")

class RequestsByItemInvestorInstitution(BaseModel):
    """[ka10059] 종목별투자자기관별요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_invsr_orgn: Annotated[List[RequestsByItemInvestorInstitution_StkInvsrOrgn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별투자자기관별")

class TotalByItemInvestorInstitutionRequest(BaseModel):
    """[ka10061] 종목별투자자기관별합계요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수")
    unit_tp: SafeStr = Field(default="", description="단위구분 1000:천주, 1:단주")

class TotalByItemInvestorInstitution_StkInvsrOrgnTot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ind_invsr: SafeStr = Field(default="", description="개인투자자")
    frgnr_invsr: SafeStr = Field(default="", description="외국인투자자")
    orgn: SafeStr = Field(default="", description="기관계")
    fnnc_invt: SafeStr = Field(default="", description="금융투자")
    insrnc: SafeStr = Field(default="", description="보험")
    invtrt: SafeStr = Field(default="", description="투신")
    etc_fnnc: SafeStr = Field(default="", description="기타금융")
    bank: SafeStr = Field(default="", description="은행")
    penfnd_etc: SafeStr = Field(default="", description="연기금등")
    samo_fund: SafeStr = Field(default="", description="사모펀드")
    natn: SafeStr = Field(default="", description="국가")
    etc_corp: SafeStr = Field(default="", description="기타법인")
    natfor: SafeStr = Field(default="", description="내외국인")

class TotalByItemInvestorInstitution(BaseModel):
    """[ka10061] 종목별투자자기관별합계요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_invsr_orgn_tot: Annotated[List[TotalByItemInvestorInstitution_StkInvsrOrgnTot], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별투자자기관별합계")

class SettlementDayBeforeSameDayRequest(BaseModel):
    """[ka10084] 당일전일체결요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tdy_pred: SafeStr = Field(default="", description="당일전일 당일 : 1, 전일 : 2")
    tic_min: SafeStr = Field(default="", description="틱분 0:틱, 1:분")
    tm: SafeStr = Field(default="", description="시간 조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430")

class SettlementDayBeforeSameDay_TdyPredCntr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm: SafeStr = Field(default="", description="시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pre_rt: SafeStr = Field(default="", description="대비율")
    pri_sel_bid_unit: SafeStr = Field(default="", description="우선매도호가단위")
    pri_buy_bid_unit: SafeStr = Field(default="", description="우선매수호가단위")
    cntr_trde_qty: SafeStr = Field(default="", description="체결거래량")
    sign: SafeStr = Field(default="", description="전일대비기호")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    stex_tp: SafeStr = Field(default="", description="거래소구분 KRX , NXT , 통합")

class SettlementDayBeforeSameDay(BaseModel):
    """[ka10084] 당일전일체결요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_pred_cntr: Annotated[List[SettlementDayBeforeSameDay_TdyPredCntr], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일전일체결")

class InformationItemsInterestRequest(BaseModel):
    """[ka10095] 관심종목정보요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)여러개의 종목코드 입력시 | 로 구분")

class InformationItemsInterest_AtnStkInfr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    base_pric: SafeStr = Field(default="", description="기준가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    cntr_str: SafeStr = Field(default="", description="체결강도")
    pred_trde_qty_pre: SafeStr = Field(default="", description="전일거래량대비")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    sel_1th_bid: SafeStr = Field(default="", description="매도1차호가")
    sel_2th_bid: SafeStr = Field(default="", description="매도2차호가")
    sel_3th_bid: SafeStr = Field(default="", description="매도3차호가")
    sel_4th_bid: SafeStr = Field(default="", description="매도4차호가")
    sel_5th_bid: SafeStr = Field(default="", description="매도5차호가")
    buy_1th_bid: SafeStr = Field(default="", description="매수1차호가")
    buy_2th_bid: SafeStr = Field(default="", description="매수2차호가")
    buy_3th_bid: SafeStr = Field(default="", description="매수3차호가")
    buy_4th_bid: SafeStr = Field(default="", description="매수4차호가")
    buy_5th_bid: SafeStr = Field(default="", description="매수5차호가")
    upl_pric: SafeStr = Field(default="", description="상한가")
    lst_pric: SafeStr = Field(default="", description="하한가")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    close_pric: SafeStr = Field(default="", description="종가")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    exp_cntr_pric: SafeStr = Field(default="", description="예상체결가")
    exp_cntr_qty: SafeStr = Field(default="", description="예상체결량")
    cap: SafeStr = Field(default="", description="자본금")
    fav: SafeStr = Field(default="", description="액면가")
    mac: SafeStr = Field(default="", description="시가총액")
    stkcnt: SafeStr = Field(default="", description="주식수")
    bid_tm: SafeStr = Field(default="", description="호가시간")
    dt: SafeStr = Field(default="", description="일자")
    pri_sel_req: SafeStr = Field(default="", description="우선매도잔량")
    pri_buy_req: SafeStr = Field(default="", description="우선매수잔량")
    pri_sel_cnt: SafeStr = Field(default="", description="우선매도건수")
    pri_buy_cnt: SafeStr = Field(default="", description="우선매수건수")
    tot_sel_req: SafeStr = Field(default="", description="총매도잔량")
    tot_buy_req: SafeStr = Field(default="", description="총매수잔량")
    tot_sel_cnt: SafeStr = Field(default="", description="총매도건수")
    tot_buy_cnt: SafeStr = Field(default="", description="총매수건수")
    prty: SafeStr = Field(default="", description="패리티")
    gear: SafeStr = Field(default="", description="기어링")
    pl_qutr: SafeStr = Field(default="", description="손익분기")
    cap_support: SafeStr = Field(default="", description="자본지지")
    elwexec_pric: SafeStr = Field(default="", description="ELW행사가")
    cnvt_rt: SafeStr = Field(default="", description="전환비율")
    elwexpr_dt: SafeStr = Field(default="", description="ELW만기일")
    cntr_engg: SafeStr = Field(default="", description="미결제약정")
    cntr_pred_pre: SafeStr = Field(default="", description="미결제전일대비")
    theory_pric: SafeStr = Field(default="", description="이론가")
    innr_vltl: SafeStr = Field(default="", description="내재변동성")
    delta: SafeStr = Field(default="", description="델타")
    gam: SafeStr = Field(default="", description="감마")
    theta: SafeStr = Field(default="", description="쎄타")
    vega: SafeStr = Field(default="", description="베가")
    law: SafeStr = Field(default="", description="로")

class InformationItemsInterest(BaseModel):
    """[ka10095] 관심종목정보요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    atn_stk_infr: Annotated[List[InformationItemsInterest_AtnStkInfr], BeforeValidator(_force_list)] = Field(default_factory=list, description="관심종목정보")

class StockInformationListRequest(BaseModel):
    """[ka10099] 종목정보 리스트 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0 : 코스피,  10 : 코스닥,  30 : K-OTC,  50 : 코넥스,  60 : ETN,  70 : 손실제한 ETN,  80 : 금현물,  90 : 변동성 ETN,  2 : 인프라투융자,  3 : ELW,  4 : 뮤추얼펀드,  5 : 신주인수권,  6 : 리츠종목,  7 : 신주인수권증서,  8 : ETF,  9 : 하이일드펀드")

class StockInformationList_List(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    code: SafeStr = Field(default="", description="종목코드 단축코드")
    name: SafeStr = Field(default="", description="종목명")
    listCount: SafeStr = Field(default="", description="상장주식수")
    auditInfo: SafeStr = Field(default="", description="감리구분")
    regDay: SafeStr = Field(default="", description="상장일")
    lastPrice: SafeStr = Field(default="", description="전일종가")
    state: SafeStr = Field(default="", description="종목상태")
    marketCode: SafeStr = Field(default="", description="시장구분코드")
    marketName: SafeStr = Field(default="", description="시장명")
    upName: SafeStr = Field(default="", description="업종명")
    upSizeName: SafeStr = Field(default="", description="회사크기분류")
    companyClassName: SafeStr = Field(default="", description="회사분류 코스닥만 존재함")
    orderWarning: SafeStr = Field(default="", description="투자유의종목여부 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달")
    nxtEnable: SafeStr = Field(default="", description="NXT가능여부 Y: 가능")

class StockInformationList(BaseModel):
    """[ka10099] 종목정보 리스트 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    list: Annotated[List[StockInformationList_List], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목리스트")

class CheckStockInformationRequest(BaseModel):
    """[ka10100] 종목정보 조회 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class CheckStockInformation(BaseModel):
    """[ka10100] 종목정보 조회 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    code: SafeStr = Field(default="", description="종목코드 단축코드")
    name: SafeStr = Field(default="", description="종목명")
    listCount: SafeStr = Field(default="", description="상장주식수")
    auditInfo: SafeStr = Field(default="", description="감리구분")
    regDay: SafeStr = Field(default="", description="상장일")
    lastPrice: SafeStr = Field(default="", description="전일종가")
    state: SafeStr = Field(default="", description="종목상태")
    marketCode: SafeStr = Field(default="", description="시장구분코드")
    marketName: SafeStr = Field(default="", description="시장명")
    upName: SafeStr = Field(default="", description="업종명")
    upSizeName: SafeStr = Field(default="", description="회사크기분류")
    companyClassName: SafeStr = Field(default="", description="회사분류 코스닥만 존재함")
    orderWarning: SafeStr = Field(default="", description="투자유의종목여부 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달")
    nxtEnable: SafeStr = Field(default="", description="NXT가능여부 Y: 가능")

class IndustryCodeListRequest(BaseModel):
    """[ka10101] 업종코드 리스트 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피(거래소),1:코스닥,2:KOSPI200,4:KOSPI100,7:KRX100(통합지수)")

class IndustryCodeList_List(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    marketCode: SafeStr = Field(default="", description="시장구분코드")
    code: SafeStr = Field(default="", description="코드")
    name: SafeStr = Field(default="", description="업종명")
    group: SafeStr = Field(default="", description="그룹")

class IndustryCodeList(BaseModel):
    """[ka10101] 업종코드 리스트 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    list: Annotated[List[IndustryCodeList_List], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종코드리스트")

class MemberCompanyListRequest(BaseModel):
    """[ka10102] 회원사 리스트 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class MemberCompanyList_List(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    code: SafeStr = Field(default="", description="코드")
    name: SafeStr = Field(default="", description="업종명")
    gb: SafeStr = Field(default="", description="구분")

class MemberCompanyList(BaseModel):
    """[ka10102] 회원사 리스트 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    list: Annotated[List[MemberCompanyList_List], BeforeValidator(_force_list)] = Field(default_factory=list, description="회원사코드리스트")

class Top50ProgramNetPurchasesRequest(BaseModel):
    """[ka90003] 프로그램순매수상위50요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    trde_upper_tp: SafeStr = Field(default="", description="매매상위구분 1:순매도상위, 2:순매수상위")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 P00101:코스피, P10102:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class Top50ProgramNetPurchases_PrmNetprpsUpper50(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    flu_sig: SafeStr = Field(default="", description="등락기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    prm_sell_amt: SafeStr = Field(default="", description="프로그램매도금액")
    prm_buy_amt: SafeStr = Field(default="", description="프로그램매수금액")
    prm_netprps_amt: SafeStr = Field(default="", description="프로그램순매수금액")

class Top50ProgramNetPurchases(BaseModel):
    """[ka90003] 프로그램순매수상위50요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_netprps_upper_50: Annotated[List[Top50ProgramNetPurchases_PrmNetprpsUpper50], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램순매수상위50")

class ProgramTradingByItemRequest(BaseModel):
    """[ka90004] 종목별프로그램매매현황요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 P00101:코스피, P10102:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingByItem_StkPrmTrdePrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    flu_sig: SafeStr = Field(default="", description="등락기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    buy_cntr_qty: SafeStr = Field(default="", description="매수체결수량")
    buy_cntr_amt: SafeStr = Field(default="", description="매수체결금액")
    sel_cntr_qty: SafeStr = Field(default="", description="매도체결수량")
    sel_cntr_amt: SafeStr = Field(default="", description="매도체결금액")
    netprps_prica: SafeStr = Field(default="", description="순매수대금")
    all_trde_rt: SafeStr = Field(default="", description="전체거래비율")

class ProgramTradingByItem(BaseModel):
    """[ka90004] 종목별프로그램매매현황요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_1: SafeStr = Field(default="", description="매수체결수량합계")
    tot_2: SafeStr = Field(default="", description="매수체결금액합계")
    tot_3: SafeStr = Field(default="", description="매도체결수량합계")
    tot_4: SafeStr = Field(default="", description="매도체결금액합계")
    tot_5: SafeStr = Field(default="", description="순매수대금합계")
    tot_6: SafeStr = Field(default="", description="합계6")
    stk_prm_trde_prst: Annotated[List[ProgramTradingByItem_StkPrmTrdePrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별프로그램매매현황")

class CreditLoanAvailableItemsRequest(BaseModel):
    """[kt20016] 신용융자 가능종목요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    crd_stk_grde_tp: SafeStr = Field(default="", description="신용종목등급구분 %:전체, A:A군, B:B군, C:C군, D:D군, E:E군")
    mrkt_deal_tp: SafeStr = Field(default="", description="시장거래구분 %:전체, 1:코스피, 0:코스닥")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class CreditLoanAvailableItems_CrdLoanPosStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    crd_assr_rt: SafeStr = Field(default="", description="신용보증금율")
    repl_pric: SafeStr = Field(default="", description="대용가")
    pred_close_pric: SafeStr = Field(default="", description="전일종가")
    crd_limit_over_yn: SafeStr = Field(default="", description="신용한도초과여부")
    crd_limit_over_txt: SafeStr = Field(default="", description="신용한도초과 N:공란,Y:회사한도 초과")

class CreditLoanAvailableItems(BaseModel):
    """[kt20016] 신용융자 가능종목요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_loan_able: SafeStr = Field(default="", description="신용융자가능여부")
    crd_loan_pos_stk: Annotated[List[CreditLoanAvailableItems_CrdLoanPosStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="신용융자가능종목")

class CreditLoanAvailabilityRequest(BaseModel):
    """[kt20017] 신용융자 가능문의 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class CreditLoanAvailability(BaseModel):
    """[kt20017] 신용융자 가능문의 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_alow_yn: SafeStr = Field(default="", description="신용가능여부")

class StockPurchaseOrderRequest(BaseModel):
    """[kt10000] 주식 매수주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class StockPurchaseOrder(BaseModel):
    """[kt10000] 주식 매수주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class StockSellOrderRequest(BaseModel):
    """[kt10001] 주식 매도주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class StockSellOrder(BaseModel):
    """[kt10001] 주식 매도주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class StockCorrectionOrderRequest(BaseModel):
    """[kt10002] 주식 정정주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    mdfy_uv: SafeStr = Field(default="", description="정정단가")
    mdfy_cond_uv: SafeStr = Field(default="", description="정정조건단가")

class StockCorrectionOrder(BaseModel):
    """[kt10002] 주식 정정주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class StockCancellationOrderRequest(BaseModel):
    """[kt10003] 주식 취소주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    cncl_qty: SafeStr = Field(default="", description="취소수량 '0' 입력시 잔량 전부 취소")

class StockCancellationOrder(BaseModel):
    """[kt10003] 주식 취소주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    cncl_qty: SafeStr = Field(default="", description="취소수량")

class GoldSpotPurchaseOrderRequest(BaseModel):
    """[kt50000] 금현물 매수주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 00:보통, 10:보통(IOC), 20:보통(FOK)")

class GoldSpotPurchaseOrder(BaseModel):
    """[kt50000] 금현물 매수주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")

class GoldSpotSellOrderRequest(BaseModel):
    """[kt50001] 금현물 매도주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 00:보통, 10:보통(IOC), 20:보통(FOK)")

class GoldSpotSellOrder(BaseModel):
    """[kt50001] 금현물 매도주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")

class SpotGoldCorrectionOrderRequest(BaseModel):
    """[kt50002] 금현물 정정주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    mdfy_uv: SafeStr = Field(default="", description="정정단가")

class SpotGoldCorrectionOrder(BaseModel):
    """[kt50002] 금현물 정정주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")

class GoldSpotCancellationOrderRequest(BaseModel):
    """[kt50003] 금현물 취소주문 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    cncl_qty: SafeStr = Field(default="", description="취소수량 '0' 입력시 잔량 전부 취소")

class GoldSpotCancellationOrder(BaseModel):
    """[kt50003] 금현물 취소주문 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    cncl_qty: SafeStr = Field(default="", description="취소수량")

class ChartByItemInvestorInstitutionRequest(BaseModel):
    """[ka10060] 종목별투자자기관별차트요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    unit_tp: SafeStr = Field(default="", description="단위구분 1000:천주, 1:단주")

class ChartByItemInvestorInstitution_StkInvsrOrgnChart(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    ind_invsr: SafeStr = Field(default="", description="개인투자자")
    frgnr_invsr: SafeStr = Field(default="", description="외국인투자자")
    orgn: SafeStr = Field(default="", description="기관계")
    fnnc_invt: SafeStr = Field(default="", description="금융투자")
    insrnc: SafeStr = Field(default="", description="보험")
    invtrt: SafeStr = Field(default="", description="투신")
    etc_fnnc: SafeStr = Field(default="", description="기타금융")
    bank: SafeStr = Field(default="", description="은행")
    penfnd_etc: SafeStr = Field(default="", description="연기금등")
    samo_fund: SafeStr = Field(default="", description="사모펀드")
    natn: SafeStr = Field(default="", description="국가")
    etc_corp: SafeStr = Field(default="", description="기타법인")
    natfor: SafeStr = Field(default="", description="내외국인")

class ChartByItemInvestorInstitution(BaseModel):
    """[ka10060] 종목별투자자기관별차트요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_invsr_orgn_chart: Annotated[List[ChartByItemInvestorInstitution_StkInvsrOrgnChart], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별투자자기관별차트")

class IntradayInvestorSpecificTradingChartRequest(BaseModel):
    """[ka10064] 장중투자자별매매차트요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class IntradayInvestorSpecificTradingChart_OpmrInvsrTrdeChart(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm: SafeStr = Field(default="", description="시간")
    frgnr_invsr: SafeStr = Field(default="", description="외국인투자자")
    orgn: SafeStr = Field(default="", description="기관계")
    invtrt: SafeStr = Field(default="", description="투신")
    insrnc: SafeStr = Field(default="", description="보험")
    bank: SafeStr = Field(default="", description="은행")
    penfnd_etc: SafeStr = Field(default="", description="연기금등")
    etc_corp: SafeStr = Field(default="", description="기타법인")
    natn: SafeStr = Field(default="", description="국가")

class IntradayInvestorSpecificTradingChart(BaseModel):
    """[ka10064] 장중투자자별매매차트요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opmr_invsr_trde_chart: Annotated[List[IntradayInvestorSpecificTradingChart_OpmrInvsrTrdeChart], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매차트")

class StockTickChartRequest(BaseModel):
    """[ka10079] 주식틱차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockTickChart_StkTicChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")

class StockTickChart(BaseModel):
    """[ka10079] 주식틱차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    last_tic_cnt: SafeStr = Field(default="", description="마지막틱갯수")
    stk_tic_chart_qry: Annotated[List[StockTickChart_StkTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식틱차트조회")

class StockChartRequest(BaseModel):
    """[ka10080] 주식분봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class StockChart_StkMinPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 종가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량 (공식문서 누락 수동 패치)")

class StockChart(BaseModel):
    """[ka10080] 주식분봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_min_pole_chart_qry: Annotated[List[StockChart_StkMinPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식분봉차트조회")

class StockDailyChartRequest(BaseModel):
    """[ka10081] 주식일봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockDailyChart_StkDtPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    trde_tern_rt: SafeStr = Field(default="", description="거래회전율")

class StockDailyChart(BaseModel):
    """[ka10081] 주식일봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_dt_pole_chart_qry: Annotated[List[StockDailyChart_StkDtPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식일봉차트조회")

class StockWeeklyChartRequest(BaseModel):
    """[ka10082] 주식주봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockWeeklyChart_StkStkPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    trde_tern_rt: SafeStr = Field(default="", description="거래회전율")

class StockWeeklyChart(BaseModel):
    """[ka10082] 주식주봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_stk_pole_chart_qry: Annotated[List[StockWeeklyChart_StkStkPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식주봉차트조회")

class StockMonthlyChartRequest(BaseModel):
    """[ka10083] 주식월봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockMonthlyChart_StkMthPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    trde_tern_rt: SafeStr = Field(default="", description="거래회전율")

class StockMonthlyChart(BaseModel):
    """[ka10083] 주식월봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_mth_pole_chart_qry: Annotated[List[StockMonthlyChart_StkMthPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식월봉차트조회")

class StockAnnualChartRequest(BaseModel):
    """[ka10094] 주식년봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockAnnualChart_StkYrPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")

class StockAnnualChart(BaseModel):
    """[ka10094] 주식년봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_yr_pole_chart_qry: Annotated[List[StockAnnualChart_StkYrPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식년봉차트조회")

class IndustryTickChartRequest(BaseModel):
    """[ka20004] 업종틱차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class IndustryTickChart_IndsTicChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")

class IndustryTickChart(BaseModel):
    """[ka20004] 업종틱차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_tic_chart_qry: Annotated[List[IndustryTickChart_IndsTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종틱차트조회")

class IndustryDivisionRequest(BaseModel):
    """[ka20005] 업종분봉조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryDivision_IndsMinPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")

class IndustryDivision(BaseModel):
    """[ka20005] 업종분봉조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_min_pole_qry: Annotated[List[IndustryDivision_IndsMinPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종분봉조회")

class IndustryDailySalaryRequest(BaseModel):
    """[ka20006] 업종일봉조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryDailySalary_IndsDtPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustryDailySalary(BaseModel):
    """[ka20006] 업종일봉조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_dt_pole_qry: Annotated[List[IndustryDailySalary_IndsDtPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종일봉조회")

class IndustrySalaryRequest(BaseModel):
    """[ka20007] 업종주봉조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustrySalary_IndsStkPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustrySalary(BaseModel):
    """[ka20007] 업종주봉조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_stk_pole_qry: Annotated[List[IndustrySalary_IndsStkPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종주봉조회")

class IndustryMonthlySalaryRequest(BaseModel):
    """[ka20008] 업종월봉조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryMonthlySalary_IndsMthPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustryMonthlySalary(BaseModel):
    """[ka20008] 업종월봉조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_mth_pole_qry: Annotated[List[IndustryMonthlySalary_IndsMthPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종월봉조회")

class IndustryYearSalaryRequest(BaseModel):
    """[ka20019] 업종년봉조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryYearSalary_IndsYrPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustryYearSalary(BaseModel):
    """[ka20019] 업종년봉조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_yr_pole_qry: Annotated[List[IndustryYearSalary_IndsYrPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종년봉조회")

class GoldSpotTickChartRequest(BaseModel):
    """[ka50079] 금현물틱차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotTickChart_GdsTicChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dt: SafeStr = Field(default="", description="일자")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")

class GoldSpotTickChart(BaseModel):
    """[ka50079] 금현물틱차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_tic_chart_qry: Annotated[List[GoldSpotTickChart_GdsTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물틱차트조회")

class GoldSpotFractionalChartRequest(BaseModel):
    """[ka50080] 금현물분봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotFractionalChart_GdsMinChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    trde_qty: SafeStr = Field(default="", description="거래량")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dt: SafeStr = Field(default="", description="일자")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")

class GoldSpotFractionalChart(BaseModel):
    """[ka50080] 금현물분봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_min_chart_qry: Annotated[List[GoldSpotFractionalChart_GdsMinChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물분봉차트조회")

class GoldSpotDailyChartRequest(BaseModel):
    """[ka50081] 금현물일봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotDailyChart_GdsDayChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")

class GoldSpotDailyChart(BaseModel):
    """[ka50081] 금현물일봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_day_chart_qry: Annotated[List[GoldSpotDailyChart_GdsDayChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotWeeklyChartRequest(BaseModel):
    """[ka50082] 금현물주봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotWeeklyChart_GdsWeekChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")

class GoldSpotWeeklyChart(BaseModel):
    """[ka50082] 금현물주봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_week_chart_qry: Annotated[List[GoldSpotWeeklyChart_GdsWeekChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotMonthlyChartRequest(BaseModel):
    """[ka50083] 금현물월봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotMonthlyChart_GdsMonthChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")

class GoldSpotMonthlyChart(BaseModel):
    """[ka50083] 금현물월봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_month_chart_qry: Annotated[List[GoldSpotMonthlyChart_GdsMonthChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotDailyTickChartRequest(BaseModel):
    """[ka50091] 금현물당일틱차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class GoldSpotDailyTickChart_GdsTicChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_pric: SafeStr = Field(default="", description="체결가")
    pred_pre: SafeStr = Field(default="", description="전일 대비(원)")
    trde_qty: SafeStr = Field(default="", description="거래량(체결량)")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dt: SafeStr = Field(default="", description="일자")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")

class GoldSpotDailyTickChart(BaseModel):
    """[ka50091] 금현물당일틱차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_tic_chart_qry: Annotated[List[GoldSpotDailyTickChart_GdsTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotDailyChartRequest(BaseModel):
    """[ka50092] 금현물당일분봉차트조회요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class GoldSpotDailyChart_GdsMinChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_pric: SafeStr = Field(default="", description="체결가")
    pred_pre: SafeStr = Field(default="", description="전일 대비(원)")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    trde_qty: SafeStr = Field(default="", description="거래량(체결량)")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    dt: SafeStr = Field(default="", description="일자")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")

class GoldSpotDailyChart(BaseModel):
    """[ka50092] 금현물당일분봉차트조회요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_min_chart_qry: Annotated[List[GoldSpotDailyChart_GdsMinChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class RequestsByThemeGroupRequest(BaseModel):
    """[ka90001] 테마그룹별요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="검색구분 0:전체검색, 1:테마검색, 2:종목검색")
    stk_cd: SafeStr = Field(default="", description="종목코드 검색하려는 종목코드")
    date_tp: SafeStr = Field(default="", description="날짜구분 n일전 (1일 ~ 99일 날짜입력)")
    thema_nm: SafeStr = Field(default="", description="테마명 검색하려는 테마명")
    flu_pl_amt_tp: SafeStr = Field(default="", description="등락수익구분 1:상위기간수익률, 2:하위기간수익률, 3:상위등락률, 4:하위등락률")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestsByThemeGroup_ThemaGrp(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    thema_grp_cd: SafeStr = Field(default="", description="테마그룹코드")
    thema_nm: SafeStr = Field(default="", description="테마명")
    stk_num: SafeStr = Field(default="", description="종목수")
    flu_sig: SafeStr = Field(default="", description="등락기호")
    flu_rt: SafeStr = Field(default="", description="등락율")
    rising_stk_num: SafeStr = Field(default="", description="상승종목수")
    fall_stk_num: SafeStr = Field(default="", description="하락종목수")
    dt_prft_rt: SafeStr = Field(default="", description="기간수익률")
    main_stk: SafeStr = Field(default="", description="주요종목")

class RequestsByThemeGroup(BaseModel):
    """[ka90001] 테마그룹별요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    thema_grp: Annotated[List[RequestsByThemeGroup_ThemaGrp], BeforeValidator(_force_list)] = Field(default_factory=list, description="테마그룹별")

class ThemeItemsRequest(BaseModel):
    """[ka90002] 테마구성종목요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date_tp: SafeStr = Field(default="", description="날짜구분 1일 ~ 99일 날짜입력")
    thema_grp_cd: SafeStr = Field(default="", description="테마그룹코드 테마그룹코드 번호")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ThemeItems_ThemaCompStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    flu_sig: SafeStr = Field(default="", description="등락기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    buy_req: SafeStr = Field(default="", description="매수잔량")
    dt_prft_rt_n: SafeStr = Field(default="", description="기간수익률n")

class ThemeItems(BaseModel):
    """[ka90002] 테마구성종목요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    flu_rt: SafeStr = Field(default="", description="등락률")
    dt_prft_rt: SafeStr = Field(default="", description="기간수익률")
    thema_comp_stk: Annotated[List[ThemeItems_ThemaCompStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="테마구성종목")

class ElwDailySensitivityIndicatorRequest(BaseModel):
    """[ka10048] ELW일별민감도지표요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class ElwDailySensitivityIndicator_ElwdalySnstIx(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    iv: SafeStr = Field(default="", description="IV")
    delta: SafeStr = Field(default="", description="델타")
    gam: SafeStr = Field(default="", description="감마")
    theta: SafeStr = Field(default="", description="쎄타")
    vega: SafeStr = Field(default="", description="베가")
    law: SafeStr = Field(default="", description="로")
    lp: SafeStr = Field(default="", description="LP")

class ElwDailySensitivityIndicator(BaseModel):
    """[ka10048] ELW일별민감도지표요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwdaly_snst_ix: Annotated[List[ElwDailySensitivityIndicator_ElwdalySnstIx], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW일별민감도지표")

class ElwSensitivityIndicatorRequest(BaseModel):
    """[ka10050] ELW민감도지표요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class ElwSensitivityIndicator_ElwsnstIxArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    elwtheory_pric: SafeStr = Field(default="", description="ELW이론가")
    iv: SafeStr = Field(default="", description="IV")
    delta: SafeStr = Field(default="", description="델타")
    gam: SafeStr = Field(default="", description="감마")
    theta: SafeStr = Field(default="", description="쎄타")
    vega: SafeStr = Field(default="", description="베가")
    law: SafeStr = Field(default="", description="로")
    lp: SafeStr = Field(default="", description="LP")

class ElwSensitivityIndicator(BaseModel):
    """[ka10050] ELW민감도지표요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwsnst_ix_array: Annotated[List[ElwSensitivityIndicator_ElwsnstIxArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW민감도지표배열")

class SuddenFluctuationElwPriceRequest(BaseModel):
    """[ka30001] ELW가격급등락요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    flu_tp: SafeStr = Field(default="", description="등락구분 1:급등, 2:급락")
    tm_tp: SafeStr = Field(default="", description="시간구분 1:분전, 2:일전")
    tm: SafeStr = Field(default="", description="시간 분 혹은 일입력 (예 1, 3, 5)")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체, 10:만주이상, 50:5만주이상, 100:10만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200..")
    rght_tp: SafeStr = Field(default="", description="권리구분 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 005:EX, 006:조기종료콜, 007:조기종료풋")
    lpcd: SafeStr = Field(default="", description="LP코드 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17")
    trde_end_elwskip: SafeStr = Field(default="", description="거래종료ELW제외 0:포함, 1:제외")

class SuddenFluctuationElwPrice_ElwpricJmpflu(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    rank: SafeStr = Field(default="", description="순위")
    stk_nm: SafeStr = Field(default="", description="종목명")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_end_elwbase_pric: SafeStr = Field(default="", description="거래종료ELW기준가")
    cur_prc: SafeStr = Field(default="", description="현재가")
    base_pre: SafeStr = Field(default="", description="기준대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    jmp_rt: SafeStr = Field(default="", description="급등율")

class SuddenFluctuationElwPrice(BaseModel):
    """[ka30001] ELW가격급등락요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    base_pric_tm: SafeStr = Field(default="", description="기준가시간")
    elwpric_jmpflu: Annotated[List[SuddenFluctuationElwPrice_ElwpricJmpflu], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW가격급등락")

class ElwNetSalesTopByTraderRequest(BaseModel):
    """[ka30002] 거래원별ELW순매매상위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 3자리, 영웅문4 0273화면참조 (교보:001, 신한금융투자:002, 한국투자증권:003, 대신:004, 미래대우:005, ,,,)")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체, 5:5천주, 10:만주, 50:5만주, 100:10만주, 500:50만주, 1000:백만주")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    dt: SafeStr = Field(default="", description="기간 1:전일, 5:5일, 10:10일, 40:40일, 60:60일")
    trde_end_elwskip: SafeStr = Field(default="", description="거래종료ELW제외 0:포함, 1:제외")

class ElwNetSalesTopByTrader_TrdeOriElwnettrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    stkpc_flu: SafeStr = Field(default="", description="주가등락")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    netprps: SafeStr = Field(default="", description="순매수")
    buy_trde_qty: SafeStr = Field(default="", description="매수거래량")
    sel_trde_qty: SafeStr = Field(default="", description="매도거래량")

class ElwNetSalesTopByTrader(BaseModel):
    """[ka30002] 거래원별ELW순매매상위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_ori_elwnettrde_upper: Annotated[List[ElwNetSalesTopByTrader_TrdeOriElwnettrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래원별ELW순매매상위")

class DailyTrendElwlpHoldingsRequest(BaseModel):
    """[ka30003] ELWLP보유일별추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class DailyTrendElwlpHoldings_ElwlppossDalyTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_tp: SafeStr = Field(default="", description="대비구분")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    chg_qty: SafeStr = Field(default="", description="변동수량")
    lprmnd_qty: SafeStr = Field(default="", description="LP보유수량")
    wght: SafeStr = Field(default="", description="비중")

class DailyTrendElwlpHoldings(BaseModel):
    """[ka30003] ELWLP보유일별추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwlpposs_daly_trnsn: Annotated[List[DailyTrendElwlpHoldings_ElwlppossDalyTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELWLP보유일별추이")

class ElwDisparityRateRequest(BaseModel):
    """[ka30004] ELW괴리율요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200..")
    rght_tp: SafeStr = Field(default="", description="권리구분 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 005: EX, 006: 조기종료콜, 007: 조기종료풋")
    lpcd: SafeStr = Field(default="", description="LP코드 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17")
    trde_end_elwskip: SafeStr = Field(default="", description="거래종료ELW제외 1:거래종료ELW제외, 0:거래종료ELW포함")

class ElwDisparityRate_ElwdisptyRt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    isscomp_nm: SafeStr = Field(default="", description="발행사명")
    sqnc: SafeStr = Field(default="", description="회차")
    base_aset_nm: SafeStr = Field(default="", description="기초자산명")
    rght_tp: SafeStr = Field(default="", description="권리구분")
    dispty_rt: SafeStr = Field(default="", description="괴리율")
    basis: SafeStr = Field(default="", description="베이시스")
    srvive_dys: SafeStr = Field(default="", description="잔존일수")
    theory_pric: SafeStr = Field(default="", description="이론가")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_tp: SafeStr = Field(default="", description="대비구분")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    stk_nm: SafeStr = Field(default="", description="종목명")

class ElwDisparityRate(BaseModel):
    """[ka30004] ELW괴리율요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwdispty_rt: Annotated[List[ElwDisparityRate_ElwdisptyRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW괴리율")

class ElwConditionSearchRequest(BaseModel):
    """[ka30005] ELW조건검색요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 12자리입력(전체:000000000000, 한국투자증권:000,,,3, 미래대우:000,,,5, 신영:000,,,6, NK투자증권:000,,,12, KB증권:000,,,17)")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드 전체일때만 12자리입력(전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼정전자:005930, KT:030200,,)")
    rght_tp: SafeStr = Field(default="", description="권리구분 0:전체, 1:콜, 2:풋, 3:DC, 4:DP, 5:EX, 6:조기종료콜, 7:조기종료풋")
    lpcd: SafeStr = Field(default="", description="LP코드 전체일때만 12자리입력(전체:000000000000, 한국투자증권:003, 미래대우:005, 신영:006, NK투자증권:012, KB증권:017)")
    sort_tp: SafeStr = Field(default="", description="정렬구분 0:정렬없음, 1:상승율순, 2:상승폭순, 3:하락율순, 4:하락폭순, 5:거래량순, 6:거래대금순, 7:잔존일순")

class ElwConditionSearch_ElwcndQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    isscomp_nm: SafeStr = Field(default="", description="발행사명")
    sqnc: SafeStr = Field(default="", description="회차")
    base_aset_nm: SafeStr = Field(default="", description="기초자산명")
    rght_tp: SafeStr = Field(default="", description="권리구분")
    expr_dt: SafeStr = Field(default="", description="만기일")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_tp: SafeStr = Field(default="", description="대비구분")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_qty_pre: SafeStr = Field(default="", description="거래량대비")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    pred_trde_qty: SafeStr = Field(default="", description="전일거래량")
    sel_bid: SafeStr = Field(default="", description="매도호가")
    buy_bid: SafeStr = Field(default="", description="매수호가")
    prty: SafeStr = Field(default="", description="패리티")
    gear_rt: SafeStr = Field(default="", description="기어링비율")
    pl_qutr_rt: SafeStr = Field(default="", description="손익분기율")
    cfp: SafeStr = Field(default="", description="자본지지점")
    theory_pric: SafeStr = Field(default="", description="이론가")
    innr_vltl: SafeStr = Field(default="", description="내재변동성")
    delta: SafeStr = Field(default="", description="델타")
    lvrg: SafeStr = Field(default="", description="레버리지")
    exec_pric: SafeStr = Field(default="", description="행사가격")
    cnvt_rt: SafeStr = Field(default="", description="전환비율")
    lpposs_rt: SafeStr = Field(default="", description="LP보유비율")
    pl_qutr_pt: SafeStr = Field(default="", description="손익분기점")
    fin_trde_dt: SafeStr = Field(default="", description="최종거래일")
    flo_dt: SafeStr = Field(default="", description="상장일")
    lpinitlast_suply_dt: SafeStr = Field(default="", description="LP초종공급일")
    stk_nm: SafeStr = Field(default="", description="종목명")
    srvive_dys: SafeStr = Field(default="", description="잔존일수")
    dispty_rt: SafeStr = Field(default="", description="괴리율")
    lpmmcm_nm: SafeStr = Field(default="", description="LP회원사명")
    lpmmcm_nm_1: SafeStr = Field(default="", description="LP회원사명1")
    lpmmcm_nm_2: SafeStr = Field(default="", description="LP회원사명2")
    xraymont_cntr_qty_arng_trde_tp: SafeStr = Field(default="", description="Xray순간체결량정리매매구분")
    xraymont_cntr_qty_profa_100tp: SafeStr = Field(default="", description="Xray순간체결량증거금100구분")

class ElwConditionSearch(BaseModel):
    """[ka30005] ELW조건검색요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwcnd_qry: Annotated[List[ElwConditionSearch_ElwcndQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW조건검색")

class ElwFluctuationRateRankingRequest(BaseModel):
    """[ka30009] ELW등락율순위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:상승률, 2:상승폭, 3:하락률, 4:하락폭")
    rght_tp: SafeStr = Field(default="", description="권리구분 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 006:조기종료콜, 007:조기종료풋")
    trde_end_skip: SafeStr = Field(default="", description="거래종료제외 1:거래종료제외, 0:거래종료포함")

class ElwFluctuationRateRanking_ElwfluRtRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    buy_req: SafeStr = Field(default="", description="매수잔량")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class ElwFluctuationRateRanking(BaseModel):
    """[ka30009] ELW등락율순위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwflu_rt_rank: Annotated[List[ElwFluctuationRateRanking_ElwfluRtRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW등락율순위")

class ElwRemainingBalanceRankingRequest(BaseModel):
    """[ka30010] ELW잔량순위요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:순매수잔량상위, 2: 순매도 잔량상위")
    rght_tp: SafeStr = Field(default="", description="권리구분 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 006: 조기종료콜, 007: 조기종료풋")
    trde_end_skip: SafeStr = Field(default="", description="거래종료제외 1:거래종료제외, 0:거래종료포함")

class ElwRemainingBalanceRanking_ElwreqRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    rank: SafeStr = Field(default="", description="순위")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락률")
    trde_qty: SafeStr = Field(default="", description="거래량")
    sel_req: SafeStr = Field(default="", description="매도잔량")
    buy_req: SafeStr = Field(default="", description="매수잔량")
    netprps_req: SafeStr = Field(default="", description="순매수잔량")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class ElwRemainingBalanceRanking(BaseModel):
    """[ka30010] ELW잔량순위요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwreq_rank: Annotated[List[ElwRemainingBalanceRanking_ElwreqRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW잔량순위")

class ElwProximityRateRequest(BaseModel):
    """[ka30011] ELW근접율요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class ElwProximityRate_ElwalaccRt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    alacc_rt: SafeStr = Field(default="", description="근접율")

class ElwProximityRate(BaseModel):
    """[ka30011] ELW근접율요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwalacc_rt: Annotated[List[ElwProximityRate_ElwalaccRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW근접율")

class DetailedInformationElwItemsRequest(BaseModel):
    """[ka30012] ELW종목상세정보요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class DetailedInformationElwItems(BaseModel):
    """[ka30012] ELW종목상세정보요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    aset_cd: SafeStr = Field(default="", description="자산코드")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    lpmmcm_nm: SafeStr = Field(default="", description="LP회원사명")
    lpmmcm_nm_1: SafeStr = Field(default="", description="LP회원사명1")
    lpmmcm_nm_2: SafeStr = Field(default="", description="LP회원사명2")
    elwrght_cntn: SafeStr = Field(default="", description="ELW권리내용")
    elwexpr_evlt_pric: SafeStr = Field(default="", description="ELW만기평가가격")
    elwtheory_pric: SafeStr = Field(default="", description="ELW이론가")
    dispty_rt: SafeStr = Field(default="", description="괴리율")
    elwinnr_vltl: SafeStr = Field(default="", description="ELW내재변동성")
    exp_rght_pric: SafeStr = Field(default="", description="예상권리가")
    elwpl_qutr_rt: SafeStr = Field(default="", description="ELW손익분기율")
    elwexec_pric: SafeStr = Field(default="", description="ELW행사가")
    elwcnvt_rt: SafeStr = Field(default="", description="ELW전환비율")
    elwcmpn_rt: SafeStr = Field(default="", description="ELW보상율")
    elwpric_rising_part_rt: SafeStr = Field(default="", description="ELW가격상승참여율")
    elwrght_type: SafeStr = Field(default="", description="ELW권리유형")
    elwsrvive_dys: SafeStr = Field(default="", description="ELW잔존일수")
    stkcnt: SafeStr = Field(default="", description="주식수")
    elwlpord_pos: SafeStr = Field(default="", description="ELWLP주문가능")
    lpposs_rt: SafeStr = Field(default="", description="LP보유비율")
    lprmnd_qty: SafeStr = Field(default="", description="LP보유수량")
    elwspread: SafeStr = Field(default="", description="ELW스프레드")
    elwprty: SafeStr = Field(default="", description="ELW패리티")
    elwgear: SafeStr = Field(default="", description="ELW기어링")
    elwflo_dt: SafeStr = Field(default="", description="ELW상장일")
    elwfin_trde_dt: SafeStr = Field(default="", description="ELW최종거래일")
    expr_dt: SafeStr = Field(default="", description="만기일")
    exec_dt: SafeStr = Field(default="", description="행사일")
    lpsuply_end_dt: SafeStr = Field(default="", description="LP공급종료일")
    elwpay_dt: SafeStr = Field(default="", description="ELW지급일")
    elwinvt_ix_comput: SafeStr = Field(default="", description="ELW투자지표산출")
    elwpay_agnt: SafeStr = Field(default="", description="ELW지급대리인")
    elwappr_way: SafeStr = Field(default="", description="ELW결재방법")
    elwrght_exec_way: SafeStr = Field(default="", description="ELW권리행사방식")
    elwpblicte_orgn: SafeStr = Field(default="", description="ELW발행기관")
    dcsn_pay_amt: SafeStr = Field(default="", description="확정지급액")
    kobarr: SafeStr = Field(default="", description="KO베리어")
    iv: SafeStr = Field(default="", description="IV")
    clsprd_end_elwocr: SafeStr = Field(default="", description="종기종료ELW발생")
    bsis_aset_1: SafeStr = Field(default="", description="기초자산1")
    bsis_aset_comp_rt_1: SafeStr = Field(default="", description="기초자산구성비율1")
    bsis_aset_2: SafeStr = Field(default="", description="기초자산2")
    bsis_aset_comp_rt_2: SafeStr = Field(default="", description="기초자산구성비율2")
    bsis_aset_3: SafeStr = Field(default="", description="기초자산3")
    bsis_aset_comp_rt_3: SafeStr = Field(default="", description="기초자산구성비율3")
    bsis_aset_4: SafeStr = Field(default="", description="기초자산4")
    bsis_aset_comp_rt_4: SafeStr = Field(default="", description="기초자산구성비율4")
    bsis_aset_5: SafeStr = Field(default="", description="기초자산5")
    bsis_aset_comp_rt_5: SafeStr = Field(default="", description="기초자산구성비율5")
    fr_dt: SafeStr = Field(default="", description="평가시작일자")
    to_dt: SafeStr = Field(default="", description="평가종료일자")
    fr_tm: SafeStr = Field(default="", description="평가시작시간")
    evlt_end_tm: SafeStr = Field(default="", description="평가종료시간")
    evlt_pric: SafeStr = Field(default="", description="평가가격")
    evlt_fnsh_yn: SafeStr = Field(default="", description="평가완료여부")
    all_hgst_pric: SafeStr = Field(default="", description="전체최고가")
    all_lwst_pric: SafeStr = Field(default="", description="전체최저가")
    imaf_hgst_pric: SafeStr = Field(default="", description="직후최고가")
    imaf_lwst_pric: SafeStr = Field(default="", description="직후최저가")
    sndhalf_mrkt_hgst_pric: SafeStr = Field(default="", description="후반장최고가")
    sndhalf_mrkt_lwst_pric: SafeStr = Field(default="", description="후반장최저가")

class EtfReturnRateRequest(BaseModel):
    """[ka40001] ETF수익율요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    etfobjt_idex_cd: SafeStr = Field(default="", description="ETF대상지수코드")
    dt: SafeStr = Field(default="", description="기간 0:1주, 1:1달, 2:6개월, 3:1년")

class EtfReturnRate_EtfprftRtLst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    etfprft_rt: SafeStr = Field(default="", description="ETF수익률")
    cntr_prft_rt: SafeStr = Field(default="", description="체결수익률")
    for_netprps_qty: SafeStr = Field(default="", description="외인순매수수량")
    orgn_netprps_qty: SafeStr = Field(default="", description="기관순매수수량")

class EtfReturnRate(BaseModel):
    """[ka40001] ETF수익율요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfprft_rt_lst: Annotated[List[EtfReturnRate_EtfprftRtLst], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF수익율")

class EtfItemInformationRequest(BaseModel):
    """[ka40002] ETF종목정보요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfItemInformation(BaseModel):
    """[ka40002] ETF종목정보요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_nm: SafeStr = Field(default="", description="종목명")
    etfobjt_idex_nm: SafeStr = Field(default="", description="ETF대상지수명")
    wonju_pric: SafeStr = Field(default="", description="원주가격")
    etftxon_type: SafeStr = Field(default="", description="ETF과세유형")
    etntxon_type: SafeStr = Field(default="", description="ETN과세유형")

class EtfDailyTrendRequest(BaseModel):
    """[ka40003] ETF일별추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfDailyTrend_EtfdalyTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_dt: SafeStr = Field(default="", description="체결일자")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pre_rt: SafeStr = Field(default="", description="대비율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    nav: SafeStr = Field(default="", description="NAV")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")
    navidex_dispty_rt: SafeStr = Field(default="", description="NAV/지수괴리율")
    navetfdispty_rt: SafeStr = Field(default="", description="NAV/ETF괴리율")
    trace_eor_rt: SafeStr = Field(default="", description="추적오차율")
    trace_cur_prc: SafeStr = Field(default="", description="추적현재가")
    trace_pred_pre: SafeStr = Field(default="", description="추적전일대비")
    trace_pre_sig: SafeStr = Field(default="", description="추적대비기호")

class EtfDailyTrend(BaseModel):
    """[ka40003] ETF일별추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfdaly_trnsn: Annotated[List[EtfDailyTrend_EtfdalyTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF일별추이")

class FullEtfRequest(BaseModel):
    """[ka40004] ETF전체시세요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    txon_type: SafeStr = Field(default="", description="과세유형 0:전체, 1:비과세, 2:보유기간과세, 3:회사형, 4:외국, 5:비과세해외(보유기간관세)")
    navpre: SafeStr = Field(default="", description="NAV대비 0:전체, 1:NAV > 전일종가, 2:NAV < 전일종가")
    mngmcomp: SafeStr = Field(default="", description="운용사 0000:전체, 3020:KODEX(삼성), 3027:KOSEF(키움), 3191:TIGER(미래에셋), 3228:KINDEX(한국투자), 3023:KStar(KB), 3022:아리랑(한화), 9999:기타운용사")
    txon_yn: SafeStr = Field(default="", description="과세여부 0:전체, 1:과세, 2:비과세")
    trace_idex: SafeStr = Field(default="", description="추적지수 0:전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class FullEtf_EtfallMrpr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_cls: SafeStr = Field(default="", description="종목분류")
    stk_nm: SafeStr = Field(default="", description="종목명")
    close_pric: SafeStr = Field(default="", description="종가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    pre_rt: SafeStr = Field(default="", description="대비율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    nav: SafeStr = Field(default="", description="NAV")
    trace_eor_rt: SafeStr = Field(default="", description="추적오차율")
    txbs: SafeStr = Field(default="", description="과표기준")
    dvid_bf_base: SafeStr = Field(default="", description="배당전기준")
    pred_dvida: SafeStr = Field(default="", description="전일배당금")
    trace_idex_nm: SafeStr = Field(default="", description="추적지수명")
    drng: SafeStr = Field(default="", description="배수")
    trace_idex_cd: SafeStr = Field(default="", description="추적지수코드")
    trace_idex: SafeStr = Field(default="", description="추적지수")
    trace_flu_rt: SafeStr = Field(default="", description="추적등락율")

class FullEtf(BaseModel):
    """[ka40004] ETF전체시세요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfall_mrpr: Annotated[List[FullEtf_EtfallMrpr], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF전체시세")

class EtfTimeZoneTrendRequest(BaseModel):
    """[ka40006] ETF시간대별추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTimeZoneTrend_EtftislTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm: SafeStr = Field(default="", description="시간")
    close_pric: SafeStr = Field(default="", description="종가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    nav: SafeStr = Field(default="", description="NAV")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    navidex: SafeStr = Field(default="", description="NAV지수")
    navetf: SafeStr = Field(default="", description="NAVETF")
    trace: SafeStr = Field(default="", description="추적")
    trace_idex: SafeStr = Field(default="", description="추적지수")
    trace_idex_pred_pre: SafeStr = Field(default="", description="추적지수전일대비")
    trace_idex_pred_pre_sig: SafeStr = Field(default="", description="추적지수전일대비기호")

class EtfTimeZoneTrend(BaseModel):
    """[ka40006] ETF시간대별추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_nm: SafeStr = Field(default="", description="종목명")
    etfobjt_idex_nm: SafeStr = Field(default="", description="ETF대상지수명")
    wonju_pric: SafeStr = Field(default="", description="원주가격")
    etftxon_type: SafeStr = Field(default="", description="ETF과세유형")
    etntxon_type: SafeStr = Field(default="", description="ETN과세유형")
    etftisl_trnsn: Annotated[List[EtfTimeZoneTrend_EtftislTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF시간대별추이")

class EtfTradingByTimeSlotRequest(BaseModel):
    """[ka40007] ETF시간대별체결요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTradingByTimeSlot_EtftislCntrArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    stex_tp: SafeStr = Field(default="", description="거래소구분 KRX , NXT , 통합")

class EtfTradingByTimeSlot(BaseModel):
    """[ka40007] ETF시간대별체결요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cls: SafeStr = Field(default="", description="종목분류")
    stk_nm: SafeStr = Field(default="", description="종목명")
    etfobjt_idex_nm: SafeStr = Field(default="", description="ETF대상지수명")
    etfobjt_idex_cd: SafeStr = Field(default="", description="ETF대상지수코드")
    objt_idex_pre_rt: SafeStr = Field(default="", description="대상지수대비율")
    wonju_pric: SafeStr = Field(default="", description="원주가격")
    etftisl_cntr_array: Annotated[List[EtfTradingByTimeSlot_EtftislCntrArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF시간대별체결배열")

class EtfTransactionByDateRequest(BaseModel):
    """[ka40008] ETF일자별체결요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTransactionByDate_EtfnetprpsQtyArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc_n: SafeStr = Field(default="", description="현재가n")
    pre_sig_n: SafeStr = Field(default="", description="대비기호n")
    pred_pre_n: SafeStr = Field(default="", description="전일대비n")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    for_netprps_qty: SafeStr = Field(default="", description="외인순매수수량")
    orgn_netprps_qty: SafeStr = Field(default="", description="기관순매수수량")

class EtfTransactionByDate(BaseModel):
    """[ka40008] ETF일자별체결요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    etfnetprps_qty_array: Annotated[List[EtfTransactionByDate_EtfnetprpsQtyArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF순매수수량배열")

class EtfTradingByTimeSlot1Request(BaseModel):
    """[ka40009] ETF시간대별체결요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTradingByTimeSlot1_Etfnavarray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    nav: SafeStr = Field(default="", description="NAV")
    navpred_pre: SafeStr = Field(default="", description="NAV전일대비")
    navflu_rt: SafeStr = Field(default="", description="NAV등락율")
    trace_eor_rt: SafeStr = Field(default="", description="추적오차율")
    dispty_rt: SafeStr = Field(default="", description="괴리율")
    stkcnt: SafeStr = Field(default="", description="주식수")
    base_pric: SafeStr = Field(default="", description="기준가")
    for_rmnd_qty: SafeStr = Field(default="", description="외인보유수량")
    repl_pric: SafeStr = Field(default="", description="대용가")
    conv_pric: SafeStr = Field(default="", description="환산가격")
    drstk: SafeStr = Field(default="", description="DR/주")
    wonju_pric: SafeStr = Field(default="", description="원주가격")

class EtfTradingByTimeSlot1(BaseModel):
    """[ka40009] ETF시간대별체결요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfnavarray: Annotated[List[EtfTradingByTimeSlot1_Etfnavarray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETFNAV배열")

class EtfTimeZoneTrendRequest1Request(BaseModel):
    """[ka40010] ETF시간대별추이요청 요청 모델 (내부 검증 및 Playground UI 용)"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTimeZoneTrendRequest1_EtftislTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    for_netprps: SafeStr = Field(default="", description="외인순매수")

class EtfTimeZoneTrendRequest1(BaseModel):
    """[ka40010] ETF시간대별추이요청 응답 데이터 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etftisl_trnsn: Annotated[List[EtfTimeZoneTrendRequest1_EtftislTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF시간대별추이")

# ====================================================================
# 2. Generated API Client (자동 생성된 중수준 레이어)
# ====================================================================

class KiwoomGeneratedClient:
    """
    명시적 파라미터(Named Arguments)를 통해 IDE 자동완성을 완벽하게 지원하는 중수준 클라이언트입니다.
    입력값은 자동으로 Pydantic 내부 검증을 거치며, 응답은 타입이 보장된 객체(BaseModel)로 반환됩니다.
    """
    def __init__(self, core: KiwoomCore):
        self.core = core

    async def connect_ws(self, on_message: Callable[[Dict[str, Any]], Any]):
        await self.core.connect_ws(on_message)

    async def disconnect_ws(self):
        await self.core.disconnect_ws()

    def issue_access_token(self, grant_type: str = "", appkey: str = "", secretkey: str = "") -> IssueAccessToken:
        """
        [au10001] 접근토큰 발급
        분류: OAuth 인증 - 접근토큰발급
        """
        req = IssueAccessTokenRequest(grant_type=grant_type, appkey=appkey, secretkey=secretkey)
        raw_response = self.core.call("au10001", **req.model_dump(by_alias=True, exclude_none=True))
        return IssueAccessToken(**raw_response)

    def revoke_access_token(self, appkey: str = "", secretkey: str = "", token: str = "") -> RevokeAccessToken:
        """
        [au10002] 접근토큰폐기
        분류: OAuth 인증 - 접근토큰폐기
        """
        req = RevokeAccessTokenRequest(appkey=appkey, secretkey=secretkey, token=token)
        raw_response = self.core.call("au10002", **req.model_dump(by_alias=True, exclude_none=True))
        return RevokeAccessToken(**raw_response)

    def account_number(self, cont_yn: str = "", next_key: str = "") -> AccountNumber:
        """
        [ka00001] 계좌번호조회
        분류: 국내주식 - 계좌
        """
        req = AccountNumberRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("ka00001", **req.model_dump(by_alias=True, exclude_none=True))
        return AccountNumber(**raw_response)

    def daily_balance_return_rate(self, cont_yn: str = "", next_key: str = "", qry_dt: str = "") -> DailyBalanceReturnRate:
        """
        [ka01690] 일별잔고수익률
        분류: 국내주식 - 계좌
        """
        req = DailyBalanceReturnRateRequest(cont_yn=cont_yn, next_key=next_key, qry_dt=qry_dt)
        raw_response = self.core.call("ka01690", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyBalanceReturnRate(**raw_response)

    def realized_profit_loss_by_date_item_date(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "") -> RealizedProfitLossByDateItemDate:
        """
        [ka10072] 일자별종목별실현손익요청_일자
        분류: 국내주식 - 계좌
        """
        req = RealizedProfitLossByDateItemDateRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt)
        raw_response = self.core.call("ka10072", **req.model_dump(by_alias=True, exclude_none=True))
        return RealizedProfitLossByDateItemDate(**raw_response)

    def realized_profit_loss_by_date_item_period(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "") -> RealizedProfitLossByDateItemPeriod:
        """
        [ka10073] 일자별종목별실현손익요청_기간
        분류: 국내주식 - 계좌
        """
        req = RealizedProfitLossByDateItemPeriodRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt)
        raw_response = self.core.call("ka10073", **req.model_dump(by_alias=True, exclude_none=True))
        return RealizedProfitLossByDateItemPeriod(**raw_response)

    def realized_profit_loss_by_date(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "") -> RealizedProfitLossByDate:
        """
        [ka10074] 일자별실현손익요청
        분류: 국내주식 - 계좌
        """
        req = RealizedProfitLossByDateRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt)
        raw_response = self.core.call("ka10074", **req.model_dump(by_alias=True, exclude_none=True))
        return RealizedProfitLossByDate(**raw_response)

    def non_confirmation(self, cont_yn: str = "", next_key: str = "", all_stk_tp: str = "", trde_tp: str = "", stk_cd: str = "", stex_tp: str = "") -> NonConfirmation:
        """
        [ka10075] 미체결요청
        분류: 국내주식 - 계좌
        """
        req = NonConfirmationRequest(cont_yn=cont_yn, next_key=next_key, all_stk_tp=all_stk_tp, trde_tp=trde_tp, stk_cd=stk_cd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10075", **req.model_dump(by_alias=True, exclude_none=True))
        return NonConfirmation(**raw_response)

    def conclusion(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", qry_tp: str = "", sell_tp: str = "", ord_no: str = "", stex_tp: str = "") -> Conclusion:
        """
        [ka10076] 체결요청
        분류: 국내주식 - 계좌
        """
        req = ConclusionRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, qry_tp=qry_tp, sell_tp=sell_tp, ord_no=ord_no, stex_tp=stex_tp)
        raw_response = self.core.call("ka10076", **req.model_dump(by_alias=True, exclude_none=True))
        return Conclusion(**raw_response)

    def same_day_realized_profit_loss(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> SameDayRealizedProfitLoss:
        """
        [ka10077] 당일실현손익상세요청
        분류: 국내주식 - 계좌
        """
        req = SameDayRealizedProfitLossRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10077", **req.model_dump(by_alias=True, exclude_none=True))
        return SameDayRealizedProfitLoss(**raw_response)

    def account_yield(self, cont_yn: str = "", next_key: str = "", stex_tp: str = "") -> AccountYield:
        """
        [ka10085] 계좌수익률요청
        분류: 국내주식 - 계좌
        """
        req = AccountYieldRequest(cont_yn=cont_yn, next_key=next_key, stex_tp=stex_tp)
        raw_response = self.core.call("ka10085", **req.model_dump(by_alias=True, exclude_none=True))
        return AccountYield(**raw_response)

    def unfilled_split_order_details(self, cont_yn: str = "", next_key: str = "", ord_no: str = "") -> UnfilledSplitOrderDetails:
        """
        [ka10088] 미체결 분할주문 상세
        분류: 국내주식 - 계좌
        """
        req = UnfilledSplitOrderDetailsRequest(cont_yn=cont_yn, next_key=next_key, ord_no=ord_no)
        raw_response = self.core.call("ka10088", **req.model_dump(by_alias=True, exclude_none=True))
        return UnfilledSplitOrderDetails(**raw_response)

    def same_day_sales_log(self, cont_yn: str = "", next_key: str = "", base_dt: str = "", ottks_tp: str = "", ch_crd_tp: str = "") -> SameDaySalesLog:
        """
        [ka10170] 당일매매일지요청
        분류: 국내주식 - 계좌
        """
        req = SameDaySalesLogRequest(cont_yn=cont_yn, next_key=next_key, base_dt=base_dt, ottks_tp=ottks_tp, ch_crd_tp=ch_crd_tp)
        raw_response = self.core.call("ka10170", **req.model_dump(by_alias=True, exclude_none=True))
        return SameDaySalesLog(**raw_response)

    def detailed_deposit(self, cont_yn: str = "", next_key: str = "", qry_tp: str = "") -> DetailedDeposit:
        """
        [kt00001] 예수금상세현황요청
        분류: 국내주식 - 계좌
        """
        req = DetailedDepositRequest(cont_yn=cont_yn, next_key=next_key, qry_tp=qry_tp)
        raw_response = self.core.call("kt00001", **req.model_dump(by_alias=True, exclude_none=True))
        return DetailedDeposit(**raw_response)

    def daily_estimated_deposited_asset(self, cont_yn: str = "", next_key: str = "", start_dt: str = "", end_dt: str = "") -> DailyEstimatedDepositedAsset:
        """
        [kt00002] 일별추정예탁자산현황요청
        분류: 국내주식 - 계좌
        """
        req = DailyEstimatedDepositedAssetRequest(cont_yn=cont_yn, next_key=next_key, start_dt=start_dt, end_dt=end_dt)
        raw_response = self.core.call("kt00002", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyEstimatedDepositedAsset(**raw_response)

    def estimated_asset(self, cont_yn: str = "", next_key: str = "", qry_tp: str = "") -> EstimatedAsset:
        """
        [kt00003] 추정자산조회요청
        분류: 국내주식 - 계좌
        """
        req = EstimatedAssetRequest(cont_yn=cont_yn, next_key=next_key, qry_tp=qry_tp)
        raw_response = self.core.call("kt00003", **req.model_dump(by_alias=True, exclude_none=True))
        return EstimatedAsset(**raw_response)

    def account_evaluation(self, cont_yn: str = "", next_key: str = "", qry_tp: str = "", dmst_stex_tp: str = "") -> AccountEvaluation:
        """
        [kt00004] 계좌평가현황요청
        분류: 국내주식 - 계좌
        """
        req = AccountEvaluationRequest(cont_yn=cont_yn, next_key=next_key, qry_tp=qry_tp, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt00004", **req.model_dump(by_alias=True, exclude_none=True))
        return AccountEvaluation(**raw_response)

    def transaction_balance(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "") -> TransactionBalance:
        """
        [kt00005] 체결잔고요청
        분류: 국내주식 - 계좌
        """
        req = TransactionBalanceRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt00005", **req.model_dump(by_alias=True, exclude_none=True))
        return TransactionBalance(**raw_response)

    def order_details_by_account(self, cont_yn: str = "", next_key: str = "", ord_dt: str = "", qry_tp: str = "", stk_bond_tp: str = "", sell_tp: str = "", stk_cd: str = "", fr_ord_no: str = "", dmst_stex_tp: str = "") -> OrderDetailsByAccount:
        """
        [kt00007] 계좌별주문체결내역상세요청
        분류: 국내주식 - 계좌
        """
        req = OrderDetailsByAccountRequest(cont_yn=cont_yn, next_key=next_key, ord_dt=ord_dt, qry_tp=qry_tp, stk_bond_tp=stk_bond_tp, sell_tp=sell_tp, stk_cd=stk_cd, fr_ord_no=fr_ord_no, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt00007", **req.model_dump(by_alias=True, exclude_none=True))
        return OrderDetailsByAccount(**raw_response)

    def next_day_payment_schedule_details_by_account(self, cont_yn: str = "", next_key: str = "", strt_dcd_seq: str = "") -> NextDayPaymentScheduleDetailsByAccount:
        """
        [kt00008] 계좌별익일결제예정내역요청
        분류: 국내주식 - 계좌
        """
        req = NextDayPaymentScheduleDetailsByAccountRequest(cont_yn=cont_yn, next_key=next_key, strt_dcd_seq=strt_dcd_seq)
        raw_response = self.core.call("kt00008", **req.model_dump(by_alias=True, exclude_none=True))
        return NextDayPaymentScheduleDetailsByAccount(**raw_response)

    def order_execution_by_account(self, cont_yn: str = "", next_key: str = "", ord_dt: str = "", stk_bond_tp: str = "", mrkt_tp: str = "", sell_tp: str = "", qry_tp: str = "", stk_cd: str = "", fr_ord_no: str = "", dmst_stex_tp: str = "") -> OrderExecutionByAccount:
        """
        [kt00009] 계좌별주문체결현황요청
        분류: 국내주식 - 계좌
        """
        req = OrderExecutionByAccountRequest(cont_yn=cont_yn, next_key=next_key, ord_dt=ord_dt, stk_bond_tp=stk_bond_tp, mrkt_tp=mrkt_tp, sell_tp=sell_tp, qry_tp=qry_tp, stk_cd=stk_cd, fr_ord_no=fr_ord_no, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt00009", **req.model_dump(by_alias=True, exclude_none=True))
        return OrderExecutionByAccount(**raw_response)

    def order_withdrawal_amount(self, cont_yn: str = "", next_key: str = "", io_amt: str = "", stk_cd: str = "", trde_tp: str = "", trde_qty: str = "", uv: str = "", exp_buy_unp: str = "") -> OrderWithdrawalAmount:
        """
        [kt00010] 주문인출가능금액요청
        분류: 국내주식 - 계좌
        """
        req = OrderWithdrawalAmountRequest(cont_yn=cont_yn, next_key=next_key, io_amt=io_amt, stk_cd=stk_cd, trde_tp=trde_tp, trde_qty=trde_qty, uv=uv, exp_buy_unp=exp_buy_unp)
        raw_response = self.core.call("kt00010", **req.model_dump(by_alias=True, exclude_none=True))
        return OrderWithdrawalAmount(**raw_response)

    def quantity_available_order_by_margin_rate(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", uv: str = "") -> QuantityAvailableOrderByMarginRate:
        """
        [kt00011] 증거금율별주문가능수량조회요청
        분류: 국내주식 - 계좌
        """
        req = QuantityAvailableOrderByMarginRateRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, uv=uv)
        raw_response = self.core.call("kt00011", **req.model_dump(by_alias=True, exclude_none=True))
        return QuantityAvailableOrderByMarginRate(**raw_response)

    def quantity_available_order_by_credit_deposit_rate(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", uv: str = "") -> QuantityAvailableOrderByCreditDepositRate:
        """
        [kt00012] 신용보증금율별주문가능수량조회요청
        분류: 국내주식 - 계좌
        """
        req = QuantityAvailableOrderByCreditDepositRateRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, uv=uv)
        raw_response = self.core.call("kt00012", **req.model_dump(by_alias=True, exclude_none=True))
        return QuantityAvailableOrderByCreditDepositRate(**raw_response)

    def margin_details(self, cont_yn: str = "", next_key: str = "") -> MarginDetails:
        """
        [kt00013] 증거금세부내역조회요청
        분류: 국내주식 - 계좌
        """
        req = MarginDetailsRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("kt00013", **req.model_dump(by_alias=True, exclude_none=True))
        return MarginDetails(**raw_response)

    def comprehensive_consignment_transaction_details(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", tp: str = "", stk_cd: str = "", crnc_cd: str = "", gds_tp: str = "", frgn_stex_code: str = "", dmst_stex_tp: str = "") -> ComprehensiveConsignmentTransactionDetails:
        """
        [kt00015] 위탁종합거래내역요청
        분류: 국내주식 - 계좌
        """
        req = ComprehensiveConsignmentTransactionDetailsRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, tp=tp, stk_cd=stk_cd, crnc_cd=crnc_cd, gds_tp=gds_tp, frgn_stex_code=frgn_stex_code, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt00015", **req.model_dump(by_alias=True, exclude_none=True))
        return ComprehensiveConsignmentTransactionDetails(**raw_response)

    def detailed_daily_account_returns(self, cont_yn: str = "", next_key: str = "", fr_dt: str = "", to_dt: str = "") -> DetailedDailyAccountReturns:
        """
        [kt00016] 일별계좌수익률상세현황요청
        분류: 국내주식 - 계좌
        """
        req = DetailedDailyAccountReturnsRequest(cont_yn=cont_yn, next_key=next_key, fr_dt=fr_dt, to_dt=to_dt)
        raw_response = self.core.call("kt00016", **req.model_dump(by_alias=True, exclude_none=True))
        return DetailedDailyAccountReturns(**raw_response)

    def daily_by_account(self, cont_yn: str = "", next_key: str = "") -> DailyByAccount:
        """
        [kt00017] 계좌별당일현황요청
        분류: 국내주식 - 계좌
        """
        req = DailyByAccountRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("kt00017", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyByAccount(**raw_response)

    def account_evaluation_balance_details(self, cont_yn: str = "", next_key: str = "", qry_tp: str = "", dmst_stex_tp: str = "") -> AccountEvaluationBalanceDetails:
        """
        [kt00018] 계좌평가잔고내역요청
        분류: 국내주식 - 계좌
        """
        req = AccountEvaluationBalanceDetailsRequest(cont_yn=cont_yn, next_key=next_key, qry_tp=qry_tp, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt00018", **req.model_dump(by_alias=True, exclude_none=True))
        return AccountEvaluationBalanceDetails(**raw_response)

    def check_gold_spot_balance(self, cont_yn: str = "", next_key: str = "") -> CheckGoldSpotBalance:
        """
        [kt50020] 금현물 잔고확인
        분류: 국내주식 - 계좌
        """
        req = CheckGoldSpotBalanceRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("kt50020", **req.model_dump(by_alias=True, exclude_none=True))
        return CheckGoldSpotBalance(**raw_response)

    def gold_spot_deposit(self, cont_yn: str = "", next_key: str = "") -> GoldSpotDeposit:
        """
        [kt50021] 금현물 예수금
        분류: 국내주식 - 계좌
        """
        req = GoldSpotDepositRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("kt50021", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDeposit(**raw_response)

    def all_gold_spot_orders(self, cont_yn: str = "", next_key: str = "", ord_dt: str = "", qry_tp: str = "", mrkt_deal_tp: str = "", stk_bond_tp: str = "", slby_tp: str = "", stk_cd: str = "", fr_ord_no: str = "", dmst_stex_tp: str = "") -> AllGoldSpotOrders:
        """
        [kt50030] 금현물 주문체결전체조회
        분류: 국내주식 - 계좌
        """
        req = AllGoldSpotOrdersRequest(cont_yn=cont_yn, next_key=next_key, ord_dt=ord_dt, qry_tp=qry_tp, mrkt_deal_tp=mrkt_deal_tp, stk_bond_tp=stk_bond_tp, slby_tp=slby_tp, stk_cd=stk_cd, fr_ord_no=fr_ord_no, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt50030", **req.model_dump(by_alias=True, exclude_none=True))
        return AllGoldSpotOrders(**raw_response)

    def gold_spot_order_execution(self, cont_yn: str = "", next_key: str = "", ord_dt: str = "", qry_tp: str = "", stk_bond_tp: str = "", sell_tp: str = "", stk_cd: str = "", fr_ord_no: str = "", dmst_stex_tp: str = "") -> GoldSpotOrderExecution:
        """
        [kt50031] 금현물 주문체결조회
        분류: 국내주식 - 계좌
        """
        req = GoldSpotOrderExecutionRequest(cont_yn=cont_yn, next_key=next_key, ord_dt=ord_dt, qry_tp=qry_tp, stk_bond_tp=stk_bond_tp, sell_tp=sell_tp, stk_cd=stk_cd, fr_ord_no=fr_ord_no, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt50031", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotOrderExecution(**raw_response)

    def gold_spot_transaction_history(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", tp: str = "", stk_cd: str = "") -> GoldSpotTransactionHistory:
        """
        [kt50032] 금현물 거래내역조회
        분류: 국내주식 - 계좌
        """
        req = GoldSpotTransactionHistoryRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, tp=tp, stk_cd=stk_cd)
        raw_response = self.core.call("kt50032", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotTransactionHistory(**raw_response)

    def gold_spot_non_trading(self, cont_yn: str = "", next_key: str = "", ord_dt: str = "", qry_tp: str = "", mrkt_deal_tp: str = "", stk_bond_tp: str = "", sell_tp: str = "", stk_cd: str = "", fr_ord_no: str = "", dmst_stex_tp: str = "") -> GoldSpotNonTrading:
        """
        [kt50075] 금현물 미체결조회
        분류: 국내주식 - 계좌
        """
        req = GoldSpotNonTradingRequest(cont_yn=cont_yn, next_key=next_key, ord_dt=ord_dt, qry_tp=qry_tp, mrkt_deal_tp=mrkt_deal_tp, stk_bond_tp=stk_bond_tp, sell_tp=sell_tp, stk_cd=stk_cd, fr_ord_no=fr_ord_no, dmst_stex_tp=dmst_stex_tp)
        raw_response = self.core.call("kt50075", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotNonTrading(**raw_response)

    def short_selling_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tm_tp: str = "", strt_dt: str = "", end_dt: str = "") -> ShortSellingTrend:
        """
        [ka10014] 공매도추이요청
        분류: 국내주식 - 공매도
        """
        req = ShortSellingTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tm_tp=tm_tp, strt_dt=strt_dt, end_dt=end_dt)
        raw_response = self.core.call("ka10014", **req.model_dump(by_alias=True, exclude_none=True))
        return ShortSellingTrend(**raw_response)

    def foreign_stock_trading_trends_by_item(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> ForeignStockTradingTrendsByItem:
        """
        [ka10008] 주식외국인종목별매매동향
        분류: 국내주식 - 기관/외국인
        """
        req = ForeignStockTradingTrendsByItemRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10008", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignStockTradingTrendsByItem(**raw_response)

    def stock_institution(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> StockInstitution:
        """
        [ka10009] 주식기관요청
        분류: 국내주식 - 기관/외국인
        """
        req = StockInstitutionRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10009", **req.model_dump(by_alias=True, exclude_none=True))
        return StockInstitution(**raw_response)

    def continuous_trading_by_institutional_foreigners(self, cont_yn: str = "", next_key: str = "", dt: str = "", strt_dt: str = "", end_dt: str = "", mrkt_tp: str = "", netslmt_tp: str = "", stk_inds_tp: str = "", amt_qty_tp: str = "", stex_tp: str = "") -> ContinuousTradingByInstitutionalForeigners:
        """
        [ka10131] 기관외국인연속매매현황요청
        분류: 국내주식 - 기관/외국인
        """
        req = ContinuousTradingByInstitutionalForeignersRequest(cont_yn=cont_yn, next_key=next_key, dt=dt, strt_dt=strt_dt, end_dt=end_dt, mrkt_tp=mrkt_tp, netslmt_tp=netslmt_tp, stk_inds_tp=stk_inds_tp, amt_qty_tp=amt_qty_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10131", **req.model_dump(by_alias=True, exclude_none=True))
        return ContinuousTradingByInstitutionalForeigners(**raw_response)

    def current_gold_spot_investors(self, cont_yn: str = "", next_key: str = "") -> CurrentGoldSpotInvestors:
        """
        [ka52301] 금현물투자자현황
        분류: 국내주식 - 기관/외국인
        """
        req = CurrentGoldSpotInvestorsRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("ka52301", **req.model_dump(by_alias=True, exclude_none=True))
        return CurrentGoldSpotInvestors(**raw_response)

    def loan_lending_transaction_trend(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", all_tp: str = "") -> LoanLendingTransactionTrend:
        """
        [ka10068] 대차거래추이요청
        분류: 국내주식 - 대차거래
        """
        req = LoanLendingTransactionTrendRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, all_tp=all_tp)
        raw_response = self.core.call("ka10068", **req.model_dump(by_alias=True, exclude_none=True))
        return LoanLendingTransactionTrend(**raw_response)

    def top10_borrowing_stocks(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", mrkt_tp: str = "") -> Top10BorrowingStocks:
        """
        [ka10069] 대차거래상위10종목요청
        분류: 국내주식 - 대차거래
        """
        req = Top10BorrowingStocksRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, mrkt_tp=mrkt_tp)
        raw_response = self.core.call("ka10069", **req.model_dump(by_alias=True, exclude_none=True))
        return Top10BorrowingStocks(**raw_response)

    def loan_lending_transaction_trend_by_item(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", all_tp: str = "", stk_cd: str = "") -> LoanLendingTransactionTrendByItem:
        """
        [ka20068] 대차거래추이요청(종목별)
        분류: 국내주식 - 대차거래
        """
        req = LoanLendingTransactionTrendByItemRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, all_tp=all_tp, stk_cd=stk_cd)
        raw_response = self.core.call("ka20068", **req.model_dump(by_alias=True, exclude_none=True))
        return LoanLendingTransactionTrendByItem(**raw_response)

    def loan_transaction_details(self, cont_yn: str = "", next_key: str = "", dt: str = "", mrkt_tp: str = "") -> LoanTransactionDetails:
        """
        [ka90012] 대차거래내역요청
        분류: 국내주식 - 대차거래
        """
        req = LoanTransactionDetailsRequest(cont_yn=cont_yn, next_key=next_key, dt=dt, mrkt_tp=mrkt_tp)
        raw_response = self.core.call("ka90012", **req.model_dump(by_alias=True, exclude_none=True))
        return LoanTransactionDetails(**raw_response)

    def higher_quota_balance(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", sort_tp: str = "", trde_qty_tp: str = "", stk_cnd: str = "", crd_cnd: str = "", stex_tp: str = "") -> HigherQuotaBalance:
        """
        [ka10020] 호가잔량상위요청
        분류: 국내주식 - 순위정보
        """
        req = HigherQuotaBalanceRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, crd_cnd=crd_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10020", **req.model_dump(by_alias=True, exclude_none=True))
        return HigherQuotaBalance(**raw_response)

    def sudden_increase_quotation_balance(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", trde_tp: str = "", sort_tp: str = "", tm_tp: str = "", trde_qty_tp: str = "", stk_cnd: str = "", stex_tp: str = "") -> SuddenIncreaseQuotationBalance:
        """
        [ka10021] 호가잔량급증요청
        분류: 국내주식 - 순위정보
        """
        req = SuddenIncreaseQuotationBalanceRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, trde_tp=trde_tp, sort_tp=sort_tp, tm_tp=tm_tp, trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10021", **req.model_dump(by_alias=True, exclude_none=True))
        return SuddenIncreaseQuotationBalance(**raw_response)

    def sudden_increase_remaining_capacity(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", rt_tp: str = "", tm_tp: str = "", trde_qty_tp: str = "", stk_cnd: str = "", stex_tp: str = "") -> SuddenIncreaseRemainingCapacity:
        """
        [ka10022] 잔량율급증요청
        분류: 국내주식 - 순위정보
        """
        req = SuddenIncreaseRemainingCapacityRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, rt_tp=rt_tp, tm_tp=tm_tp, trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10022", **req.model_dump(by_alias=True, exclude_none=True))
        return SuddenIncreaseRemainingCapacity(**raw_response)

    def sudden_increase_trading_volume(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", sort_tp: str = "", tm_tp: str = "", trde_qty_tp: str = "", tm: str = "", stk_cnd: str = "", pric_tp: str = "", stex_tp: str = "") -> SuddenIncreaseTradingVolume:
        """
        [ka10023] 거래량급증요청
        분류: 국내주식 - 순위정보
        """
        req = SuddenIncreaseTradingVolumeRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, sort_tp=sort_tp, tm_tp=tm_tp, trde_qty_tp=trde_qty_tp, tm=tm, stk_cnd=stk_cnd, pric_tp=pric_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10023", **req.model_dump(by_alias=True, exclude_none=True))
        return SuddenIncreaseTradingVolume(**raw_response)

    def higher_fluctuation_rate_compared_previous_day(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", sort_tp: str = "", trde_qty_cnd: str = "", stk_cnd: str = "", crd_cnd: str = "", updown_incls: str = "", pric_cnd: str = "", trde_prica_cnd: str = "", stex_tp: str = "") -> HigherFluctuationRateComparedPreviousDay:
        """
        [ka10027] 전일대비등락률상위요청
        분류: 국내주식 - 순위정보
        """
        req = HigherFluctuationRateComparedPreviousDayRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd, stk_cnd=stk_cnd, crd_cnd=crd_cnd, updown_incls=updown_incls, pric_cnd=pric_cnd, trde_prica_cnd=trde_prica_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10027", **req.model_dump(by_alias=True, exclude_none=True))
        return HigherFluctuationRateComparedPreviousDay(**raw_response)

    def higher_expected_transaction_rate(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", sort_tp: str = "", trde_qty_cnd: str = "", stk_cnd: str = "", crd_cnd: str = "", pric_cnd: str = "", stex_tp: str = "") -> HigherExpectedTransactionRate:
        """
        [ka10029] 예상체결등락률상위요청
        분류: 국내주식 - 순위정보
        """
        req = HigherExpectedTransactionRateRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd, stk_cnd=stk_cnd, crd_cnd=crd_cnd, pric_cnd=pric_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10029", **req.model_dump(by_alias=True, exclude_none=True))
        return HigherExpectedTransactionRate(**raw_response)

    def high_transaction_volume_day(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", sort_tp: str = "", mang_stk_incls: str = "", crd_tp: str = "", trde_qty_tp: str = "", pric_tp: str = "", trde_prica_tp: str = "", mrkt_open_tp: str = "", stex_tp: str = "") -> HighTransactionVolumeDay:
        """
        [ka10030] 당일거래량상위요청
        분류: 국내주식 - 순위정보
        """
        req = HighTransactionVolumeDayRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, sort_tp=sort_tp, mang_stk_incls=mang_stk_incls, crd_tp=crd_tp, trde_qty_tp=trde_qty_tp, pric_tp=pric_tp, trde_prica_tp=trde_prica_tp, mrkt_open_tp=mrkt_open_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10030", **req.model_dump(by_alias=True, exclude_none=True))
        return HighTransactionVolumeDay(**raw_response)

    def previous_day_highest_trading_volume(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", qry_tp: str = "", rank_strt: str = "", rank_end: str = "", stex_tp: str = "") -> PreviousDayHighestTradingVolume:
        """
        [ka10031] 전일거래량상위요청
        분류: 국내주식 - 순위정보
        """
        req = PreviousDayHighestTradingVolumeRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, qry_tp=qry_tp, rank_strt=rank_strt, rank_end=rank_end, stex_tp=stex_tp)
        raw_response = self.core.call("ka10031", **req.model_dump(by_alias=True, exclude_none=True))
        return PreviousDayHighestTradingVolume(**raw_response)

    def higher_transaction_amount(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", mang_stk_incls: str = "", stex_tp: str = "") -> HigherTransactionAmount:
        """
        [ka10032] 거래대금상위요청
        분류: 국내주식 - 순위정보
        """
        req = HigherTransactionAmountRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, mang_stk_incls=mang_stk_incls, stex_tp=stex_tp)
        raw_response = self.core.call("ka10032", **req.model_dump(by_alias=True, exclude_none=True))
        return HigherTransactionAmount(**raw_response)

    def higher_credit_ratio(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", trde_qty_tp: str = "", stk_cnd: str = "", updown_incls: str = "", crd_cnd: str = "", stex_tp: str = "") -> HigherCreditRatio:
        """
        [ka10033] 신용비율상위요청
        분류: 국내주식 - 순위정보
        """
        req = HigherCreditRatioRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, updown_incls=updown_incls, crd_cnd=crd_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10033", **req.model_dump(by_alias=True, exclude_none=True))
        return HigherCreditRatio(**raw_response)

    def external_transaction_top_sales_by_period(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", trde_tp: str = "", dt: str = "", stex_tp: str = "") -> ExternalTransactionTopSalesByPeriod:
        """
        [ka10034] 외인기간별매매상위요청
        분류: 국내주식 - 순위정보
        """
        req = ExternalTransactionTopSalesByPeriodRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, trde_tp=trde_tp, dt=dt, stex_tp=stex_tp)
        raw_response = self.core.call("ka10034", **req.model_dump(by_alias=True, exclude_none=True))
        return ExternalTransactionTopSalesByPeriod(**raw_response)

    def foreign_continuous_net_sales_top(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", trde_tp: str = "", base_dt_tp: str = "", stex_tp: str = "") -> ForeignContinuousNetSalesTop:
        """
        [ka10035] 외인연속순매매상위요청
        분류: 국내주식 - 순위정보
        """
        req = ForeignContinuousNetSalesTopRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, trde_tp=trde_tp, base_dt_tp=base_dt_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10035", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignContinuousNetSalesTop(**raw_response)

    def top_foreign_limit_burnout_rate_increase(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", dt: str = "", stex_tp: str = "") -> TopForeignLimitBurnoutRateIncrease:
        """
        [ka10036] 외인한도소진율증가상위
        분류: 국내주식 - 순위정보
        """
        req = TopForeignLimitBurnoutRateIncreaseRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, dt=dt, stex_tp=stex_tp)
        raw_response = self.core.call("ka10036", **req.model_dump(by_alias=True, exclude_none=True))
        return TopForeignLimitBurnoutRateIncrease(**raw_response)

    def foreign_over_counter_sales(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", dt: str = "", trde_tp: str = "", sort_tp: str = "", stex_tp: str = "") -> ForeignOverCounterSales:
        """
        [ka10037] 외국계창구매매상위요청
        분류: 국내주식 - 순위정보
        """
        req = ForeignOverCounterSalesRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, dt=dt, trde_tp=trde_tp, sort_tp=sort_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10037", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignOverCounterSales(**raw_response)

    def ranking_securities_companies_by_stock(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "", qry_tp: str = "", dt: str = "") -> RankingSecuritiesCompaniesByStock:
        """
        [ka10038] 종목별증권사순위요청
        분류: 국내주식 - 순위정보
        """
        req = RankingSecuritiesCompaniesByStockRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt, qry_tp=qry_tp, dt=dt)
        raw_response = self.core.call("ka10038", **req.model_dump(by_alias=True, exclude_none=True))
        return RankingSecuritiesCompaniesByStock(**raw_response)

    def top_trading_by_securities_company(self, cont_yn: str = "", next_key: str = "", mmcm_cd: str = "", trde_qty_tp: str = "", trde_tp: str = "", dt: str = "", stex_tp: str = "") -> TopTradingBySecuritiesCompany:
        """
        [ka10039] 증권사별매매상위요청
        분류: 국내주식 - 순위정보
        """
        req = TopTradingBySecuritiesCompanyRequest(cont_yn=cont_yn, next_key=next_key, mmcm_cd=mmcm_cd, trde_qty_tp=trde_qty_tp, trde_tp=trde_tp, dt=dt, stex_tp=stex_tp)
        raw_response = self.core.call("ka10039", **req.model_dump(by_alias=True, exclude_none=True))
        return TopTradingBySecuritiesCompany(**raw_response)

    def same_day_major_transaction(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> SameDayMajorTransaction:
        """
        [ka10040] 당일주요거래원요청
        분류: 국내주식 - 순위정보
        """
        req = SameDayMajorTransactionRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10040", **req.model_dump(by_alias=True, exclude_none=True))
        return SameDayMajorTransaction(**raw_response)

    def net_buying_trader_ranking(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "", qry_dt_tp: str = "", pot_tp: str = "", dt: str = "", sort_base: str = "") -> NetBuyingTraderRanking:
        """
        [ka10042] 순매수거래원순위요청
        분류: 국내주식 - 순위정보
        """
        req = NetBuyingTraderRankingRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt, qry_dt_tp=qry_dt_tp, pot_tp=pot_tp, dt=dt, sort_base=sort_base)
        raw_response = self.core.call("ka10042", **req.model_dump(by_alias=True, exclude_none=True))
        return NetBuyingTraderRanking(**raw_response)

    def same_day_high_withdrawal(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> SameDayHighWithdrawal:
        """
        [ka10053] 당일상위이탈원요청
        분류: 국내주식 - 순위정보
        """
        req = SameDayHighWithdrawalRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10053", **req.model_dump(by_alias=True, exclude_none=True))
        return SameDayHighWithdrawal(**raw_response)

    def same_net_sales_ranking(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", mrkt_tp: str = "", trde_tp: str = "", sort_cnd: str = "", unit_tp: str = "", stex_tp: str = "") -> SameNetSalesRanking:
        """
        [ka10062] 동일순매매순위요청
        분류: 국내주식 - 순위정보
        """
        req = SameNetSalesRankingRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, mrkt_tp=mrkt_tp, trde_tp=trde_tp, sort_cnd=sort_cnd, unit_tp=unit_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10062", **req.model_dump(by_alias=True, exclude_none=True))
        return SameNetSalesRanking(**raw_response)

    def intraday_trading_by_investor(self, cont_yn: str = "", next_key: str = "", trde_tp: str = "", mrkt_tp: str = "", orgn_tp: str = "", amt_qty_tp: str = "") -> IntradayTradingByInvestor:
        """
        [ka10065] 장중투자자별매매상위요청
        분류: 국내주식 - 순위정보
        """
        req = IntradayTradingByInvestorRequest(cont_yn=cont_yn, next_key=next_key, trde_tp=trde_tp, mrkt_tp=mrkt_tp, orgn_tp=orgn_tp, amt_qty_tp=amt_qty_tp)
        raw_response = self.core.call("ka10065", **req.model_dump(by_alias=True, exclude_none=True))
        return IntradayTradingByInvestor(**raw_response)

    def ranking_out_hours_single_price_fluctuation_rate(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", sort_base: str = "", stk_cnd: str = "", trde_qty_cnd: str = "", crd_cnd: str = "", trde_prica: str = "") -> RankingOutHoursSinglePriceFluctuationRate:
        """
        [ka10098] 시간외단일가등락율순위요청
        분류: 국내주식 - 순위정보
        """
        req = RankingOutHoursSinglePriceFluctuationRateRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, sort_base=sort_base, stk_cnd=stk_cnd, trde_qty_cnd=trde_qty_cnd, crd_cnd=crd_cnd, trde_prica=trde_prica)
        raw_response = self.core.call("ka10098", **req.model_dump(by_alias=True, exclude_none=True))
        return RankingOutHoursSinglePriceFluctuationRate(**raw_response)

    def foreign_institutional_trading_top(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", amt_qty_tp: str = "", qry_dt_tp: str = "", date: str = "", stex_tp: str = "") -> ForeignInstitutionalTradingTop:
        """
        [ka90009] 외국인기관매매상위요청
        분류: 국내주식 - 순위정보
        """
        req = ForeignInstitutionalTradingTopRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp, qry_dt_tp=qry_dt_tp, date=date, stex_tp=stex_tp)
        raw_response = self.core.call("ka90009", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignInstitutionalTradingTop(**raw_response)

    def stock_quote(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> StockQuote:
        """
        [ka10004] 주식호가요청
        분류: 국내주식 - 시세
        """
        req = StockQuoteRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10004", **req.model_dump(by_alias=True, exclude_none=True))
        return StockQuote(**raw_response)

    def stock_weekly_monthly_hourly_minutes(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> StockWeeklyMonthlyHourlyMinutes:
        """
        [ka10005] 주식일주월시분요청
        분류: 국내주식 - 시세
        """
        req = StockWeeklyMonthlyHourlyMinutesRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10005", **req.model_dump(by_alias=True, exclude_none=True))
        return StockWeeklyMonthlyHourlyMinutes(**raw_response)

    def stock_time(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> StockTime:
        """
        [ka10006] 주식시분요청
        분류: 국내주식 - 시세
        """
        req = StockTimeRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10006", **req.model_dump(by_alias=True, exclude_none=True))
        return StockTime(**raw_response)

    def price_information(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> PriceInformation:
        """
        [ka10007] 시세표성정보요청
        분류: 국내주식 - 시세
        """
        req = PriceInformationRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10007", **req.model_dump(by_alias=True, exclude_none=True))
        return PriceInformation(**raw_response)

    def all_new_stock_warrants(self, cont_yn: str = "", next_key: str = "", newstk_recvrht_tp: str = "") -> AllNewStockWarrants:
        """
        [ka10011] 신주인수권전체시세요청
        분류: 국내주식 - 시세
        """
        req = AllNewStockWarrantsRequest(cont_yn=cont_yn, next_key=next_key, newstk_recvrht_tp=newstk_recvrht_tp)
        raw_response = self.core.call("ka10011", **req.model_dump(by_alias=True, exclude_none=True))
        return AllNewStockWarrants(**raw_response)

    def daily_institutional_trading_items(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", trde_tp: str = "", mrkt_tp: str = "", stex_tp: str = "") -> DailyInstitutionalTradingItems:
        """
        [ka10044] 일별기관매매종목요청
        분류: 국내주식 - 시세
        """
        req = DailyInstitutionalTradingItemsRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, trde_tp=trde_tp, mrkt_tp=mrkt_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10044", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyInstitutionalTradingItems(**raw_response)

    def institutional_trading_trend_by_item(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "", orgn_prsm_unp_tp: str = "", for_prsm_unp_tp: str = "") -> InstitutionalTradingTrendByItem:
        """
        [ka10045] 종목별기관매매추이요청
        분류: 국내주식 - 시세
        """
        req = InstitutionalTradingTrendByItemRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt, orgn_prsm_unp_tp=orgn_prsm_unp_tp, for_prsm_unp_tp=for_prsm_unp_tp)
        raw_response = self.core.call("ka10045", **req.model_dump(by_alias=True, exclude_none=True))
        return InstitutionalTradingTrendByItem(**raw_response)

    def fastening_strength_trend_by_time(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> FasteningStrengthTrendByTime:
        """
        [ka10046] 체결강도추이시간별요청
        분류: 국내주식 - 시세
        """
        req = FasteningStrengthTrendByTimeRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10046", **req.model_dump(by_alias=True, exclude_none=True))
        return FasteningStrengthTrendByTime(**raw_response)

    def daily_tightening_strength_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> DailyTighteningStrengthTrend:
        """
        [ka10047] 체결강도추이일별요청
        분류: 국내주식 - 시세
        """
        req = DailyTighteningStrengthTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10047", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyTighteningStrengthTrend(**raw_response)

    def intraday_investor_specific_trading(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", amt_qty_tp: str = "", invsr: str = "", frgn_all: str = "", smtm_netprps_tp: str = "", stex_tp: str = "") -> IntradayInvestorSpecificTrading:
        """
        [ka10063] 장중투자자별매매요청
        분류: 국내주식 - 시세
        """
        req = IntradayInvestorSpecificTradingRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp, invsr=invsr, frgn_all=frgn_all, smtm_netprps_tp=smtm_netprps_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10063", **req.model_dump(by_alias=True, exclude_none=True))
        return IntradayInvestorSpecificTrading(**raw_response)

    def trading_by_investor_after_market_close(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", amt_qty_tp: str = "", trde_tp: str = "", stex_tp: str = "") -> TradingByInvestorAfterMarketClose:
        """
        [ka10066] 장마감후투자자별매매요청
        분류: 국내주식 - 시세
        """
        req = TradingByInvestorAfterMarketCloseRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp, trde_tp=trde_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10066", **req.model_dump(by_alias=True, exclude_none=True))
        return TradingByInvestorAfterMarketClose(**raw_response)

    def stock_trading_trends_by_securities_company(self, cont_yn: str = "", next_key: str = "", mmcm_cd: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "") -> StockTradingTrendsBySecuritiesCompany:
        """
        [ka10078] 증권사별종목매매동향요청
        분류: 국내주식 - 시세
        """
        req = StockTradingTrendsBySecuritiesCompanyRequest(cont_yn=cont_yn, next_key=next_key, mmcm_cd=mmcm_cd, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt)
        raw_response = self.core.call("ka10078", **req.model_dump(by_alias=True, exclude_none=True))
        return StockTradingTrendsBySecuritiesCompany(**raw_response)

    def daily_stock(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", qry_dt: str = "", indc_tp: str = "") -> DailyStock:
        """
        [ka10086] 일별주가요청
        분류: 국내주식 - 시세
        """
        req = DailyStockRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, qry_dt=qry_dt, indc_tp=indc_tp)
        raw_response = self.core.call("ka10086", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyStock(**raw_response)

    def single_after_hours(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> SingleAfterHours:
        """
        [ka10087] 시간외단일가요청
        분류: 국내주식 - 시세
        """
        req = SingleAfterHoursRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10087", **req.model_dump(by_alias=True, exclude_none=True))
        return SingleAfterHours(**raw_response)

    def gold_spot_trading_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> GoldSpotTradingTrend:
        """
        [ka50010] 금현물체결추이
        분류: 국내주식 - 시세
        """
        req = GoldSpotTradingTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka50010", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotTradingTrend(**raw_response)

    def spot_gold_daily_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "") -> SpotGoldDailyTrend:
        """
        [ka50012] 금현물일별추이
        분류: 국내주식 - 시세
        """
        req = SpotGoldDailyTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt)
        raw_response = self.core.call("ka50012", **req.model_dump(by_alias=True, exclude_none=True))
        return SpotGoldDailyTrend(**raw_response)

    def gold_spot_expected_transaction(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> GoldSpotExpectedTransaction:
        """
        [ka50087] 금현물예상체결
        분류: 국내주식 - 시세
        """
        req = GoldSpotExpectedTransactionRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka50087", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotExpectedTransaction(**raw_response)

    def gold_spot_price_information(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> GoldSpotPriceInformation:
        """
        [ka50100] 금현물 시세정보
        분류: 국내주식 - 시세
        """
        req = GoldSpotPriceInformationRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka50100", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotPriceInformation(**raw_response)

    def gold_spot_quote(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "") -> GoldSpotQuote:
        """
        [ka50101] 금현물 호가
        분류: 국내주식 - 시세
        """
        req = GoldSpotQuoteRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope)
        raw_response = self.core.call("ka50101", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotQuote(**raw_response)

    def program_trading_trend_by_time_zone(self, cont_yn: str = "", next_key: str = "", date: str = "", amt_qty_tp: str = "", mrkt_tp: str = "", min_tic_tp: str = "", stex_tp: str = "") -> ProgramTradingTrendByTimeZone:
        """
        [ka90005] 프로그램매매추이요청 시간대별
        분류: 국내주식 - 시세
        """
        req = ProgramTradingTrendByTimeZoneRequest(cont_yn=cont_yn, next_key=next_key, date=date, amt_qty_tp=amt_qty_tp, mrkt_tp=mrkt_tp, min_tic_tp=min_tic_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka90005", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingTrendByTimeZone(**raw_response)

    def program_trading_profit_balance_trend(self, cont_yn: str = "", next_key: str = "", date: str = "", stex_tp: str = "") -> ProgramTradingProfitBalanceTrend:
        """
        [ka90006] 프로그램매매차익잔고추이요청
        분류: 국내주식 - 시세
        """
        req = ProgramTradingProfitBalanceTrendRequest(cont_yn=cont_yn, next_key=next_key, date=date, stex_tp=stex_tp)
        raw_response = self.core.call("ka90006", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingProfitBalanceTrend(**raw_response)

    def cumulative_program_trading_trend(self, cont_yn: str = "", next_key: str = "", date: str = "", amt_qty_tp: str = "", mrkt_tp: str = "", stex_tp: str = "") -> CumulativeProgramTradingTrend:
        """
        [ka90007] 프로그램매매누적추이요청
        분류: 국내주식 - 시세
        """
        req = CumulativeProgramTradingTrendRequest(cont_yn=cont_yn, next_key=next_key, date=date, amt_qty_tp=amt_qty_tp, mrkt_tp=mrkt_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka90007", **req.model_dump(by_alias=True, exclude_none=True))
        return CumulativeProgramTradingTrend(**raw_response)

    def program_trading_trend_by_item_time(self, cont_yn: str = "", next_key: str = "", amt_qty_tp: str = "", stk_cd: str = "", date: str = "") -> ProgramTradingTrendByItemTime:
        """
        [ka90008] 종목시간별프로그램매매추이요청
        분류: 국내주식 - 시세
        """
        req = ProgramTradingTrendByItemTimeRequest(cont_yn=cont_yn, next_key=next_key, amt_qty_tp=amt_qty_tp, stk_cd=stk_cd, date=date)
        raw_response = self.core.call("ka90008", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingTrendByItemTime(**raw_response)

    def program_trading_trend_date(self, cont_yn: str = "", next_key: str = "", date: str = "", amt_qty_tp: str = "", mrkt_tp: str = "", min_tic_tp: str = "", stex_tp: str = "") -> ProgramTradingTrendDate:
        """
        [ka90010] 프로그램매매추이요청 일자별
        분류: 국내주식 - 시세
        """
        req = ProgramTradingTrendDateRequest(cont_yn=cont_yn, next_key=next_key, date=date, amt_qty_tp=amt_qty_tp, mrkt_tp=mrkt_tp, min_tic_tp=min_tic_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka90010", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingTrendDate(**raw_response)

    def daily_program_trading_trend_items(self, cont_yn: str = "", next_key: str = "", amt_qty_tp: str = "", stk_cd: str = "", date: str = "") -> DailyProgramTradingTrendItems:
        """
        [ka90013] 종목일별프로그램매매추이요청
        분류: 국내주식 - 시세
        """
        req = DailyProgramTradingTrendItemsRequest(cont_yn=cont_yn, next_key=next_key, amt_qty_tp=amt_qty_tp, stk_cd=stk_cd, date=date)
        raw_response = self.core.call("ka90013", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyProgramTradingTrendItems(**raw_response)

    def credit_buy_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", stk_cd: str = "", ord_qty: str = "", ord_uv: str = "", trde_tp: str = "", cond_uv: str = "") -> CreditBuyOrder:
        """
        [kt10006] 신용 매수주문
        분류: 국내주식 - 신용주문
        """
        req = CreditBuyOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, stk_cd=stk_cd, ord_qty=ord_qty, ord_uv=ord_uv, trde_tp=trde_tp, cond_uv=cond_uv)
        raw_response = self.core.call("kt10006", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditBuyOrder(**raw_response)

    def credit_sell_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", stk_cd: str = "", ord_qty: str = "", ord_uv: str = "", trde_tp: str = "", crd_deal_tp: str = "", crd_loan_dt: str = "", cond_uv: str = "") -> CreditSellOrder:
        """
        [kt10007] 신용 매도주문
        분류: 국내주식 - 신용주문
        """
        req = CreditSellOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, stk_cd=stk_cd, ord_qty=ord_qty, ord_uv=ord_uv, trde_tp=trde_tp, crd_deal_tp=crd_deal_tp, crd_loan_dt=crd_loan_dt, cond_uv=cond_uv)
        raw_response = self.core.call("kt10007", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditSellOrder(**raw_response)

    def credit_correction_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", orig_ord_no: str = "", stk_cd: str = "", mdfy_qty: str = "", mdfy_uv: str = "", mdfy_cond_uv: str = "") -> CreditCorrectionOrder:
        """
        [kt10008] 신용 정정주문
        분류: 국내주식 - 신용주문
        """
        req = CreditCorrectionOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, orig_ord_no=orig_ord_no, stk_cd=stk_cd, mdfy_qty=mdfy_qty, mdfy_uv=mdfy_uv, mdfy_cond_uv=mdfy_cond_uv)
        raw_response = self.core.call("kt10008", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditCorrectionOrder(**raw_response)

    def credit_cancellation_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", orig_ord_no: str = "", stk_cd: str = "", cncl_qty: str = "") -> CreditCancellationOrder:
        """
        [kt10009] 신용 취소주문
        분류: 국내주식 - 신용주문
        """
        req = CreditCancellationOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, orig_ord_no=orig_ord_no, stk_cd=stk_cd, cncl_qty=cncl_qty)
        raw_response = self.core.call("kt10009", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditCancellationOrder(**raw_response)

    async def order_execution(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [00] 주문체결
        분류: 국내주식 - 실시간시세
        """
        req = OrderExecutionRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def balance(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [04] 잔고
        분류: 국내주식 - 실시간시세
        """
        req = BalanceRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_momentum(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0A] 주식기세
        분류: 국내주식 - 실시간시세
        """
        req = StockMomentumRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_signing(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0B] 주식체결
        분류: 국내주식 - 실시간시세
        """
        req = StockSigningRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_preferred_price(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0C] 주식우선호가
        분류: 국내주식 - 실시간시세
        """
        req = StockPreferredPriceRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_quote_balance(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0D] 주식호가잔량
        분류: 국내주식 - 실시간시세
        """
        req = StockQuoteBalanceRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_after_hours_quote(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0E] 주식시간외호가
        분류: 국내주식 - 실시간시세
        """
        req = StockAfterHoursQuoteRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_day_trader(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0F] 주식당일거래원
        분류: 국내주식 - 실시간시세
        """
        req = StockDayTraderRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def etf_nav(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0G] ETF NAV
        분류: 국내주식 - 실시간시세
        """
        req = EtfNavRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_expected_execution(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0H] 주식예상체결
        분류: 국내주식 - 실시간시세
        """
        req = StockExpectedExecutionRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def international_gold_conversion_price(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0I] 국제금환산가격
        분류: 국내주식 - 실시간시세
        """
        req = InternationalGoldConversionPriceRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def sector_index(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0J] 업종지수
        분류: 국내주식 - 실시간시세
        """
        req = SectorIndexRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def industry_fluctuations(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0U] 업종등락
        분류: 국내주식 - 실시간시세
        """
        req = IndustryFluctuationsRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_item_information(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0g] 주식종목정보
        분류: 국내주식 - 실시간시세
        """
        req = StockItemInformationRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def elw_theorist(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0m] ELW 이론가
        분류: 국내주식 - 실시간시세
        """
        req = ElwTheoristRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def long_start_time(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0s] 장시작시간
        분류: 국내주식 - 실시간시세
        """
        req = LongStartTimeRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def elw_indicator(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0u] ELW 지표
        분류: 국내주식 - 실시간시세
        """
        req = ElwIndicatorRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_program_trading(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [0w] 종목프로그램매매
        분류: 국내주식 - 실시간시세
        """
        req = StockProgramTradingRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def activate_disable_vi(self, trnm: str = "", grp_no: str = "", refresh: str = "", data: str = ""):
        """
        [1h] VI발동/해제
        분류: 국내주식 - 실시간시세
        """
        req = ActivateDisableViRequest(trnm=trnm, grp_no=grp_no, refresh=refresh, data=data)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    def industry_program(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> IndustryProgram:
        """
        [ka10010] 업종프로그램요청
        분류: 국내주식 - 업종
        """
        req = IndustryProgramRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10010", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryProgram(**raw_response)

    def investor_net_purchase_by_industry(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", amt_qty_tp: str = "", base_dt: str = "", stex_tp: str = "") -> InvestorNetPurchaseByIndustry:
        """
        [ka10051] 업종별투자자순매수요청
        분류: 국내주식 - 업종
        """
        req = InvestorNetPurchaseByIndustryRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp, base_dt=base_dt, stex_tp=stex_tp)
        raw_response = self.core.call("ka10051", **req.model_dump(by_alias=True, exclude_none=True))
        return InvestorNetPurchaseByIndustry(**raw_response)

    def current_industry(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", inds_cd: str = "") -> CurrentIndustry:
        """
        [ka20001] 업종현재가요청
        분류: 국내주식 - 업종
        """
        req = CurrentIndustryRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, inds_cd=inds_cd)
        raw_response = self.core.call("ka20001", **req.model_dump(by_alias=True, exclude_none=True))
        return CurrentIndustry(**raw_response)

    def stocks_by_industry(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", inds_cd: str = "", stex_tp: str = "") -> StocksByIndustry:
        """
        [ka20002] 업종별주가요청
        분류: 국내주식 - 업종
        """
        req = StocksByIndustryRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, inds_cd=inds_cd, stex_tp=stex_tp)
        raw_response = self.core.call("ka20002", **req.model_dump(by_alias=True, exclude_none=True))
        return StocksByIndustry(**raw_response)

    def all_industry_indices(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "") -> AllIndustryIndices:
        """
        [ka20003] 전업종지수요청
        분류: 국내주식 - 업종
        """
        req = AllIndustryIndicesRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd)
        raw_response = self.core.call("ka20003", **req.model_dump(by_alias=True, exclude_none=True))
        return AllIndustryIndices(**raw_response)

    def industry_current_price_daily(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", inds_cd: str = "") -> IndustryCurrentPriceDaily:
        """
        [ka20009] 업종현재가일별요청
        분류: 국내주식 - 업종
        """
        req = IndustryCurrentPriceDailyRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, inds_cd=inds_cd)
        raw_response = self.core.call("ka20009", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryCurrentPriceDaily(**raw_response)

    async def condition_search_list(self, trnm: str = ""):
        """
        [ka10171] 조건검색 목록조회
        분류: 국내주식 - 조건검색
        """
        req = ConditionSearchListRequest(trnm=trnm)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def conditional_search_general(self, trnm: str = "", seq: str = "", search_type: str = "", stex_tp: str = "", cont_yn: str = "", next_key: str = ""):
        """
        [ka10172] 조건검색 요청 일반
        분류: 국내주식 - 조건검색
        """
        req = ConditionalSearchGeneralRequest(trnm=trnm, seq=seq, search_type=search_type, stex_tp=stex_tp, cont_yn=cont_yn, next_key=next_key)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def real_time_conditional_search(self, trnm: str = "", seq: str = "", search_type: str = "", stex_tp: str = ""):
        """
        [ka10173] 조건검색 요청 실시간
        분류: 국내주식 - 조건검색
        """
        req = RealTimeConditionalSearchRequest(trnm=trnm, seq=seq, search_type=search_type, stex_tp=stex_tp)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def conditional_search_real_time_cancellation(self, trnm: str = "", seq: str = ""):
        """
        [ka10174] 조건검색 실시간 해제
        분류: 국내주식 - 조건검색
        """
        req = ConditionalSearchRealTimeCancellationRequest(trnm=trnm, seq=seq)
        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    def real_time_item_ranking(self, cont_yn: str = "", next_key: str = "", qry_tp: str = "") -> RealTimeItemRanking:
        """
        [ka00198] 실시간종목조회순위
        분류: 국내주식 - 종목정보
        """
        req = RealTimeItemRankingRequest(cont_yn=cont_yn, next_key=next_key, qry_tp=qry_tp)
        raw_response = self.core.call("ka00198", **req.model_dump(by_alias=True, exclude_none=True))
        return RealTimeItemRanking(**raw_response)

    def basic_stock_information(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> BasicStockInformation:
        """
        [ka10001] 주식기본정보요청
        분류: 국내주식 - 종목정보
        """
        req = BasicStockInformationRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10001", **req.model_dump(by_alias=True, exclude_none=True))
        return BasicStockInformation(**raw_response)

    def stock_exchange(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> StockExchange:
        """
        [ka10002] 주식거래원요청
        분류: 국내주식 - 종목정보
        """
        req = StockExchangeRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10002", **req.model_dump(by_alias=True, exclude_none=True))
        return StockExchange(**raw_response)

    def conclusion_information(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> ConclusionInformation:
        """
        [ka10003] 체결정보요청
        분류: 국내주식 - 종목정보
        """
        req = ConclusionInformationRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10003", **req.model_dump(by_alias=True, exclude_none=True))
        return ConclusionInformation(**raw_response)

    def credit_trading_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", dt: str = "", qry_tp: str = "") -> CreditTradingTrend:
        """
        [ka10013] 신용매매동향요청
        분류: 국내주식 - 종목정보
        """
        req = CreditTradingTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, dt=dt, qry_tp=qry_tp)
        raw_response = self.core.call("ka10013", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditTradingTrend(**raw_response)

    def daily_transaction(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "") -> DailyTransaction:
        """
        [ka10015] 일별거래상세요청
        분류: 국내주식 - 종목정보
        """
        req = DailyTransactionRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt)
        raw_response = self.core.call("ka10015", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyTransaction(**raw_response)

    def low_report(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", ntl_tp: str = "", high_low_close_tp: str = "", stk_cnd: str = "", trde_qty_tp: str = "", crd_cnd: str = "", updown_incls: str = "", dt: str = "", stex_tp: str = "") -> LowReport:
        """
        [ka10016] 신고저가요청
        분류: 국내주식 - 종목정보
        """
        req = LowReportRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, ntl_tp=ntl_tp, high_low_close_tp=high_low_close_tp, stk_cnd=stk_cnd, trde_qty_tp=trde_qty_tp, crd_cnd=crd_cnd, updown_incls=updown_incls, dt=dt, stex_tp=stex_tp)
        raw_response = self.core.call("ka10016", **req.model_dump(by_alias=True, exclude_none=True))
        return LowReport(**raw_response)

    def upper_lower_limits(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", updown_tp: str = "", sort_tp: str = "", stk_cnd: str = "", trde_qty_tp: str = "", crd_cnd: str = "", trde_gold_tp: str = "", stex_tp: str = "") -> UpperLowerLimits:
        """
        [ka10017] 상하한가요청
        분류: 국내주식 - 종목정보
        """
        req = UpperLowerLimitsRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, updown_tp=updown_tp, sort_tp=sort_tp, stk_cnd=stk_cnd, trde_qty_tp=trde_qty_tp, crd_cnd=crd_cnd, trde_gold_tp=trde_gold_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10017", **req.model_dump(by_alias=True, exclude_none=True))
        return UpperLowerLimits(**raw_response)

    def high_low_price_proximity(self, cont_yn: str = "", next_key: str = "", high_low_tp: str = "", alacc_rt: str = "", mrkt_tp: str = "", trde_qty_tp: str = "", stk_cnd: str = "", crd_cnd: str = "", stex_tp: str = "") -> HighLowPriceProximity:
        """
        [ka10018] 고저가근접요청
        분류: 국내주식 - 종목정보
        """
        req = HighLowPriceProximityRequest(cont_yn=cont_yn, next_key=next_key, high_low_tp=high_low_tp, alacc_rt=alacc_rt, mrkt_tp=mrkt_tp, trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, crd_cnd=crd_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10018", **req.model_dump(by_alias=True, exclude_none=True))
        return HighLowPriceProximity(**raw_response)

    def sudden_price_fluctuation(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", flu_tp: str = "", tm_tp: str = "", tm: str = "", trde_qty_tp: str = "", stk_cnd: str = "", crd_cnd: str = "", pric_cnd: str = "", updown_incls: str = "", stex_tp: str = "") -> SuddenPriceFluctuation:
        """
        [ka10019] 가격급등락요청
        분류: 국내주식 - 종목정보
        """
        req = SuddenPriceFluctuationRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, flu_tp=flu_tp, tm_tp=tm_tp, tm=tm, trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, crd_cnd=crd_cnd, pric_cnd=pric_cnd, updown_incls=updown_incls, stex_tp=stex_tp)
        raw_response = self.core.call("ka10019", **req.model_dump(by_alias=True, exclude_none=True))
        return SuddenPriceFluctuation(**raw_response)

    def transaction_volume_update(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", cycle_tp: str = "", trde_qty_tp: str = "", stex_tp: str = "") -> TransactionVolumeUpdate:
        """
        [ka10024] 거래량갱신요청
        분류: 국내주식 - 종목정보
        """
        req = TransactionVolumeUpdateRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, cycle_tp=cycle_tp, trde_qty_tp=trde_qty_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10024", **req.model_dump(by_alias=True, exclude_none=True))
        return TransactionVolumeUpdate(**raw_response)

    def concentration_properties_sale(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", prps_cnctr_rt: str = "", cur_prc_entry: str = "", prpscnt: str = "", cycle_tp: str = "", stex_tp: str = "") -> ConcentrationPropertiesSale:
        """
        [ka10025] 매물대집중요청
        분류: 국내주식 - 종목정보
        """
        req = ConcentrationPropertiesSaleRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, prps_cnctr_rt=prps_cnctr_rt, cur_prc_entry=cur_prc_entry, prpscnt=prpscnt, cycle_tp=cycle_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10025", **req.model_dump(by_alias=True, exclude_none=True))
        return ConcentrationPropertiesSale(**raw_response)

    def high_low_per(self, cont_yn: str = "", next_key: str = "", pertp: str = "", stex_tp: str = "") -> HighLowPer:
        """
        [ka10026] 고저PER요청
        분류: 국내주식 - 종목정보
        """
        req = HighLowPerRequest(cont_yn=cont_yn, next_key=next_key, pertp=pertp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10026", **req.model_dump(by_alias=True, exclude_none=True))
        return HighLowPer(**raw_response)

    def fluctuation_rate_compared_market_price(self, cont_yn: str = "", next_key: str = "", sort_tp: str = "", trde_qty_cnd: str = "", mrkt_tp: str = "", updown_incls: str = "", stk_cnd: str = "", crd_cnd: str = "", trde_prica_cnd: str = "", flu_cnd: str = "", stex_tp: str = "") -> FluctuationRateComparedMarketPrice:
        """
        [ka10028] 시가대비등락률요청
        분류: 국내주식 - 종목정보
        """
        req = FluctuationRateComparedMarketPriceRequest(cont_yn=cont_yn, next_key=next_key, sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd, mrkt_tp=mrkt_tp, updown_incls=updown_incls, stk_cnd=stk_cnd, crd_cnd=crd_cnd, trde_prica_cnd=trde_prica_cnd, flu_cnd=flu_cnd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10028", **req.model_dump(by_alias=True, exclude_none=True))
        return FluctuationRateComparedMarketPrice(**raw_response)

    def transaction_price_analysis(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "", qry_dt_tp: str = "", pot_tp: str = "", dt: str = "", sort_base: str = "", mmcm_cd: str = "", stex_tp: str = "") -> TransactionPriceAnalysis:
        """
        [ka10043] 거래원매물대분석요청
        분류: 국내주식 - 종목정보
        """
        req = TransactionPriceAnalysisRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt, qry_dt_tp=qry_dt_tp, pot_tp=pot_tp, dt=dt, sort_base=sort_base, mmcm_cd=mmcm_cd, stex_tp=stex_tp)
        raw_response = self.core.call("ka10043", **req.model_dump(by_alias=True, exclude_none=True))
        return TransactionPriceAnalysis(**raw_response)

    def trader_instantaneous_trading_volume(self, cont_yn: str = "", next_key: str = "", mmcm_cd: str = "", stk_cd: str = "", mrkt_tp: str = "", qty_tp: str = "", pric_tp: str = "", stex_tp: str = "") -> TraderInstantaneousTradingVolume:
        """
        [ka10052] 거래원순간거래량요청
        분류: 국내주식 - 종목정보
        """
        req = TraderInstantaneousTradingVolumeRequest(cont_yn=cont_yn, next_key=next_key, mmcm_cd=mmcm_cd, stk_cd=stk_cd, mrkt_tp=mrkt_tp, qty_tp=qty_tp, pric_tp=pric_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10052", **req.model_dump(by_alias=True, exclude_none=True))
        return TraderInstantaneousTradingVolume(**raw_response)

    def items_activate_volatility_mitigation_device(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", bf_mkrt_tp: str = "", stk_cd: str = "", motn_tp: str = "", skip_stk: str = "", trde_qty_tp: str = "", min_trde_qty: str = "", max_trde_qty: str = "", trde_prica_tp: str = "", min_trde_prica: str = "", max_trde_prica: str = "", motn_drc: str = "", stex_tp: str = "") -> ItemsActivateVolatilityMitigationDevice:
        """
        [ka10054] 변동성완화장치발동종목요청
        분류: 국내주식 - 종목정보
        """
        req = ItemsActivateVolatilityMitigationDeviceRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, bf_mkrt_tp=bf_mkrt_tp, stk_cd=stk_cd, motn_tp=motn_tp, skip_stk=skip_stk, trde_qty_tp=trde_qty_tp, min_trde_qty=min_trde_qty, max_trde_qty=max_trde_qty, trde_prica_tp=trde_prica_tp, min_trde_prica=min_trde_prica, max_trde_prica=max_trde_prica, motn_drc=motn_drc, stex_tp=stex_tp)
        raw_response = self.core.call("ka10054", **req.model_dump(by_alias=True, exclude_none=True))
        return ItemsActivateVolatilityMitigationDevice(**raw_response)

    def settlement_day_before_day(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tdy_pred: str = "") -> SettlementDayBeforeDay:
        """
        [ka10055] 당일전일체결량요청
        분류: 국내주식 - 종목정보
        """
        req = SettlementDayBeforeDayRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tdy_pred=tdy_pred)
        raw_response = self.core.call("ka10055", **req.model_dump(by_alias=True, exclude_none=True))
        return SettlementDayBeforeDay(**raw_response)

    def daily_trading_items_by_investor(self, cont_yn: str = "", next_key: str = "", strt_dt: str = "", end_dt: str = "", trde_tp: str = "", mrkt_tp: str = "", invsr_tp: str = "", stex_tp: str = "") -> DailyTradingItemsByInvestor:
        """
        [ka10058] 투자자별일별매매종목요청
        분류: 국내주식 - 종목정보
        """
        req = DailyTradingItemsByInvestorRequest(cont_yn=cont_yn, next_key=next_key, strt_dt=strt_dt, end_dt=end_dt, trde_tp=trde_tp, mrkt_tp=mrkt_tp, invsr_tp=invsr_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka10058", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyTradingItemsByInvestor(**raw_response)

    def requests_by_item_investor_institution(self, cont_yn: str = "", next_key: str = "", dt: str = "", stk_cd: str = "", amt_qty_tp: str = "", trde_tp: str = "", unit_tp: str = "") -> RequestsByItemInvestorInstitution:
        """
        [ka10059] 종목별투자자기관별요청
        분류: 국내주식 - 종목정보
        """
        req = RequestsByItemInvestorInstitutionRequest(cont_yn=cont_yn, next_key=next_key, dt=dt, stk_cd=stk_cd, amt_qty_tp=amt_qty_tp, trde_tp=trde_tp, unit_tp=unit_tp)
        raw_response = self.core.call("ka10059", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestsByItemInvestorInstitution(**raw_response)

    def total_by_item_investor_institution(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", strt_dt: str = "", end_dt: str = "", amt_qty_tp: str = "", trde_tp: str = "", unit_tp: str = "") -> TotalByItemInvestorInstitution:
        """
        [ka10061] 종목별투자자기관별합계요청
        분류: 국내주식 - 종목정보
        """
        req = TotalByItemInvestorInstitutionRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt, amt_qty_tp=amt_qty_tp, trde_tp=trde_tp, unit_tp=unit_tp)
        raw_response = self.core.call("ka10061", **req.model_dump(by_alias=True, exclude_none=True))
        return TotalByItemInvestorInstitution(**raw_response)

    def settlement_day_before_same_day(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tdy_pred: str = "", tic_min: str = "", tm: str = "") -> SettlementDayBeforeSameDay:
        """
        [ka10084] 당일전일체결요청
        분류: 국내주식 - 종목정보
        """
        req = SettlementDayBeforeSameDayRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tdy_pred=tdy_pred, tic_min=tic_min, tm=tm)
        raw_response = self.core.call("ka10084", **req.model_dump(by_alias=True, exclude_none=True))
        return SettlementDayBeforeSameDay(**raw_response)

    def information_items_interest(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> InformationItemsInterest:
        """
        [ka10095] 관심종목정보요청
        분류: 국내주식 - 종목정보
        """
        req = InformationItemsInterestRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10095", **req.model_dump(by_alias=True, exclude_none=True))
        return InformationItemsInterest(**raw_response)

    def stock_information_list(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "") -> StockInformationList:
        """
        [ka10099] 종목정보 리스트
        분류: 국내주식 - 종목정보
        """
        req = StockInformationListRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp)
        raw_response = self.core.call("ka10099", **req.model_dump(by_alias=True, exclude_none=True))
        return StockInformationList(**raw_response)

    def check_stock_information(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> CheckStockInformation:
        """
        [ka10100] 종목정보 조회
        분류: 국내주식 - 종목정보
        """
        req = CheckStockInformationRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10100", **req.model_dump(by_alias=True, exclude_none=True))
        return CheckStockInformation(**raw_response)

    def industry_code_list(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "") -> IndustryCodeList:
        """
        [ka10101] 업종코드 리스트
        분류: 국내주식 - 종목정보
        """
        req = IndustryCodeListRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp)
        raw_response = self.core.call("ka10101", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryCodeList(**raw_response)

    def member_company_list(self, cont_yn: str = "", next_key: str = "") -> MemberCompanyList:
        """
        [ka10102] 회원사 리스트
        분류: 국내주식 - 종목정보
        """
        req = MemberCompanyListRequest(cont_yn=cont_yn, next_key=next_key)
        raw_response = self.core.call("ka10102", **req.model_dump(by_alias=True, exclude_none=True))
        return MemberCompanyList(**raw_response)

    def top50_program_net_purchases(self, cont_yn: str = "", next_key: str = "", trde_upper_tp: str = "", amt_qty_tp: str = "", mrkt_tp: str = "", stex_tp: str = "") -> Top50ProgramNetPurchases:
        """
        [ka90003] 프로그램순매수상위50요청
        분류: 국내주식 - 종목정보
        """
        req = Top50ProgramNetPurchasesRequest(cont_yn=cont_yn, next_key=next_key, trde_upper_tp=trde_upper_tp, amt_qty_tp=amt_qty_tp, mrkt_tp=mrkt_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka90003", **req.model_dump(by_alias=True, exclude_none=True))
        return Top50ProgramNetPurchases(**raw_response)

    def program_trading_by_item(self, cont_yn: str = "", next_key: str = "", dt: str = "", mrkt_tp: str = "", stex_tp: str = "") -> ProgramTradingByItem:
        """
        [ka90004] 종목별프로그램매매현황요청
        분류: 국내주식 - 종목정보
        """
        req = ProgramTradingByItemRequest(cont_yn=cont_yn, next_key=next_key, dt=dt, mrkt_tp=mrkt_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka90004", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingByItem(**raw_response)

    def credit_loan_available_items(self, cont_yn: str = "", next_key: str = "", crd_stk_grde_tp: str = "", mrkt_deal_tp: str = "", stk_cd: str = "") -> CreditLoanAvailableItems:
        """
        [kt20016] 신용융자 가능종목요청
        분류: 국내주식 - 종목정보
        """
        req = CreditLoanAvailableItemsRequest(cont_yn=cont_yn, next_key=next_key, crd_stk_grde_tp=crd_stk_grde_tp, mrkt_deal_tp=mrkt_deal_tp, stk_cd=stk_cd)
        raw_response = self.core.call("kt20016", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditLoanAvailableItems(**raw_response)

    def credit_loan_availability(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> CreditLoanAvailability:
        """
        [kt20017] 신용융자 가능문의
        분류: 국내주식 - 종목정보
        """
        req = CreditLoanAvailabilityRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("kt20017", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditLoanAvailability(**raw_response)

    def stock_purchase_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", stk_cd: str = "", ord_qty: str = "", ord_uv: str = "", trde_tp: str = "", cond_uv: str = "") -> StockPurchaseOrder:
        """
        [kt10000] 주식 매수주문
        분류: 국내주식 - 주문
        """
        req = StockPurchaseOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, stk_cd=stk_cd, ord_qty=ord_qty, ord_uv=ord_uv, trde_tp=trde_tp, cond_uv=cond_uv)
        raw_response = self.core.call("kt10000", **req.model_dump(by_alias=True, exclude_none=True))
        return StockPurchaseOrder(**raw_response)

    def stock_sell_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", stk_cd: str = "", ord_qty: str = "", ord_uv: str = "", trde_tp: str = "", cond_uv: str = "") -> StockSellOrder:
        """
        [kt10001] 주식 매도주문
        분류: 국내주식 - 주문
        """
        req = StockSellOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, stk_cd=stk_cd, ord_qty=ord_qty, ord_uv=ord_uv, trde_tp=trde_tp, cond_uv=cond_uv)
        raw_response = self.core.call("kt10001", **req.model_dump(by_alias=True, exclude_none=True))
        return StockSellOrder(**raw_response)

    def stock_correction_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", orig_ord_no: str = "", stk_cd: str = "", mdfy_qty: str = "", mdfy_uv: str = "", mdfy_cond_uv: str = "") -> StockCorrectionOrder:
        """
        [kt10002] 주식 정정주문
        분류: 국내주식 - 주문
        """
        req = StockCorrectionOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, orig_ord_no=orig_ord_no, stk_cd=stk_cd, mdfy_qty=mdfy_qty, mdfy_uv=mdfy_uv, mdfy_cond_uv=mdfy_cond_uv)
        raw_response = self.core.call("kt10002", **req.model_dump(by_alias=True, exclude_none=True))
        return StockCorrectionOrder(**raw_response)

    def stock_cancellation_order(self, cont_yn: str = "", next_key: str = "", dmst_stex_tp: str = "", orig_ord_no: str = "", stk_cd: str = "", cncl_qty: str = "") -> StockCancellationOrder:
        """
        [kt10003] 주식 취소주문
        분류: 국내주식 - 주문
        """
        req = StockCancellationOrderRequest(cont_yn=cont_yn, next_key=next_key, dmst_stex_tp=dmst_stex_tp, orig_ord_no=orig_ord_no, stk_cd=stk_cd, cncl_qty=cncl_qty)
        raw_response = self.core.call("kt10003", **req.model_dump(by_alias=True, exclude_none=True))
        return StockCancellationOrder(**raw_response)

    def gold_spot_purchase_order(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", ord_qty: str = "", ord_uv: str = "", trde_tp: str = "") -> GoldSpotPurchaseOrder:
        """
        [kt50000] 금현물 매수주문
        분류: 국내주식 - 주문
        """
        req = GoldSpotPurchaseOrderRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, ord_qty=ord_qty, ord_uv=ord_uv, trde_tp=trde_tp)
        raw_response = self.core.call("kt50000", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotPurchaseOrder(**raw_response)

    def gold_spot_sell_order(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", ord_qty: str = "", ord_uv: str = "", trde_tp: str = "") -> GoldSpotSellOrder:
        """
        [kt50001] 금현물 매도주문
        분류: 국내주식 - 주문
        """
        req = GoldSpotSellOrderRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, ord_qty=ord_qty, ord_uv=ord_uv, trde_tp=trde_tp)
        raw_response = self.core.call("kt50001", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotSellOrder(**raw_response)

    def spot_gold_correction_order(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", orig_ord_no: str = "", mdfy_qty: str = "", mdfy_uv: str = "") -> SpotGoldCorrectionOrder:
        """
        [kt50002] 금현물 정정주문
        분류: 국내주식 - 주문
        """
        req = SpotGoldCorrectionOrderRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, orig_ord_no=orig_ord_no, mdfy_qty=mdfy_qty, mdfy_uv=mdfy_uv)
        raw_response = self.core.call("kt50002", **req.model_dump(by_alias=True, exclude_none=True))
        return SpotGoldCorrectionOrder(**raw_response)

    def gold_spot_cancellation_order(self, cont_yn: str = "", next_key: str = "", orig_ord_no: str = "", stk_cd: str = "", cncl_qty: str = "") -> GoldSpotCancellationOrder:
        """
        [kt50003] 금현물 취소주문
        분류: 국내주식 - 주문
        """
        req = GoldSpotCancellationOrderRequest(cont_yn=cont_yn, next_key=next_key, orig_ord_no=orig_ord_no, stk_cd=stk_cd, cncl_qty=cncl_qty)
        raw_response = self.core.call("kt50003", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotCancellationOrder(**raw_response)

    def chart_by_item_investor_institution(self, cont_yn: str = "", next_key: str = "", dt: str = "", stk_cd: str = "", amt_qty_tp: str = "", trde_tp: str = "", unit_tp: str = "") -> ChartByItemInvestorInstitution:
        """
        [ka10060] 종목별투자자기관별차트요청
        분류: 국내주식 - 차트
        """
        req = ChartByItemInvestorInstitutionRequest(cont_yn=cont_yn, next_key=next_key, dt=dt, stk_cd=stk_cd, amt_qty_tp=amt_qty_tp, trde_tp=trde_tp, unit_tp=unit_tp)
        raw_response = self.core.call("ka10060", **req.model_dump(by_alias=True, exclude_none=True))
        return ChartByItemInvestorInstitution(**raw_response)

    def intraday_investor_specific_trading_chart(self, cont_yn: str = "", next_key: str = "", mrkt_tp: str = "", amt_qty_tp: str = "", trde_tp: str = "", stk_cd: str = "") -> IntradayInvestorSpecificTradingChart:
        """
        [ka10064] 장중투자자별매매차트요청
        분류: 국내주식 - 차트
        """
        req = IntradayInvestorSpecificTradingChartRequest(cont_yn=cont_yn, next_key=next_key, mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp, trde_tp=trde_tp, stk_cd=stk_cd)
        raw_response = self.core.call("ka10064", **req.model_dump(by_alias=True, exclude_none=True))
        return IntradayInvestorSpecificTradingChart(**raw_response)

    def stock_tick_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "", upd_stkpc_tp: str = "") -> StockTickChart:
        """
        [ka10079] 주식틱차트조회요청
        분류: 국내주식 - 차트
        """
        req = StockTickChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka10079", **req.model_dump(by_alias=True, exclude_none=True))
        return StockTickChart(**raw_response)

    def stock_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "", upd_stkpc_tp: str = "", base_dt: str = "") -> StockChart:
        """
        [ka10080] 주식분봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = StockChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope, upd_stkpc_tp=upd_stkpc_tp, base_dt=base_dt)
        raw_response = self.core.call("ka10080", **req.model_dump(by_alias=True, exclude_none=True))
        return StockChart(**raw_response)

    def stock_daily_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> StockDailyChart:
        """
        [ka10081] 주식일봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = StockDailyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka10081", **req.model_dump(by_alias=True, exclude_none=True))
        return StockDailyChart(**raw_response)

    def stock_weekly_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> StockWeeklyChart:
        """
        [ka10082] 주식주봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = StockWeeklyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka10082", **req.model_dump(by_alias=True, exclude_none=True))
        return StockWeeklyChart(**raw_response)

    def stock_monthly_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> StockMonthlyChart:
        """
        [ka10083] 주식월봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = StockMonthlyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka10083", **req.model_dump(by_alias=True, exclude_none=True))
        return StockMonthlyChart(**raw_response)

    def stock_annual_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> StockAnnualChart:
        """
        [ka10094] 주식년봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = StockAnnualChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka10094", **req.model_dump(by_alias=True, exclude_none=True))
        return StockAnnualChart(**raw_response)

    def industry_tick_chart(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "", tic_scope: str = "") -> IndustryTickChart:
        """
        [ka20004] 업종틱차트조회요청
        분류: 국내주식 - 차트
        """
        req = IndustryTickChartRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd, tic_scope=tic_scope)
        raw_response = self.core.call("ka20004", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryTickChart(**raw_response)

    def industry_division(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "", tic_scope: str = "", base_dt: str = "") -> IndustryDivision:
        """
        [ka20005] 업종분봉조회요청
        분류: 국내주식 - 차트
        """
        req = IndustryDivisionRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd, tic_scope=tic_scope, base_dt=base_dt)
        raw_response = self.core.call("ka20005", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryDivision(**raw_response)

    def industry_daily_salary(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "", base_dt: str = "") -> IndustryDailySalary:
        """
        [ka20006] 업종일봉조회요청
        분류: 국내주식 - 차트
        """
        req = IndustryDailySalaryRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd, base_dt=base_dt)
        raw_response = self.core.call("ka20006", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryDailySalary(**raw_response)

    def industry_salary(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "", base_dt: str = "") -> IndustrySalary:
        """
        [ka20007] 업종주봉조회요청
        분류: 국내주식 - 차트
        """
        req = IndustrySalaryRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd, base_dt=base_dt)
        raw_response = self.core.call("ka20007", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustrySalary(**raw_response)

    def industry_monthly_salary(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "", base_dt: str = "") -> IndustryMonthlySalary:
        """
        [ka20008] 업종월봉조회요청
        분류: 국내주식 - 차트
        """
        req = IndustryMonthlySalaryRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd, base_dt=base_dt)
        raw_response = self.core.call("ka20008", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryMonthlySalary(**raw_response)

    def industry_year_salary(self, cont_yn: str = "", next_key: str = "", inds_cd: str = "", base_dt: str = "") -> IndustryYearSalary:
        """
        [ka20019] 업종년봉조회요청
        분류: 국내주식 - 차트
        """
        req = IndustryYearSalaryRequest(cont_yn=cont_yn, next_key=next_key, inds_cd=inds_cd, base_dt=base_dt)
        raw_response = self.core.call("ka20019", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryYearSalary(**raw_response)

    def gold_spot_tick_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "", upd_stkpc_tp: str = "") -> GoldSpotTickChart:
        """
        [ka50079] 금현물틱차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotTickChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka50079", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotTickChart(**raw_response)

    def gold_spot_fractional_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "", upd_stkpc_tp: str = "") -> GoldSpotFractionalChart:
        """
        [ka50080] 금현물분봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotFractionalChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka50080", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotFractionalChart(**raw_response)

    def gold_spot_daily_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> GoldSpotDailyChart:
        """
        [ka50081] 금현물일봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotDailyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka50081", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDailyChart(**raw_response)

    def gold_spot_weekly_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> GoldSpotWeeklyChart:
        """
        [ka50082] 금현물주봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotWeeklyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka50082", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotWeeklyChart(**raw_response)

    def gold_spot_monthly_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", base_dt: str = "", upd_stkpc_tp: str = "") -> GoldSpotMonthlyChart:
        """
        [ka50083] 금현물월봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotMonthlyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp)
        raw_response = self.core.call("ka50083", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotMonthlyChart(**raw_response)

    def gold_spot_daily_tick_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "") -> GoldSpotDailyTickChart:
        """
        [ka50091] 금현물당일틱차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotDailyTickChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope)
        raw_response = self.core.call("ka50091", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDailyTickChart(**raw_response)

    def gold_spot_daily_chart(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", tic_scope: str = "") -> GoldSpotDailyChart:
        """
        [ka50092] 금현물당일분봉차트조회요청
        분류: 국내주식 - 차트
        """
        req = GoldSpotDailyChartRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, tic_scope=tic_scope)
        raw_response = self.core.call("ka50092", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDailyChart(**raw_response)

    def requests_by_theme_group(self, cont_yn: str = "", next_key: str = "", qry_tp: str = "", stk_cd: str = "", date_tp: str = "", thema_nm: str = "", flu_pl_amt_tp: str = "", stex_tp: str = "") -> RequestsByThemeGroup:
        """
        [ka90001] 테마그룹별요청
        분류: 국내주식 - 테마
        """
        req = RequestsByThemeGroupRequest(cont_yn=cont_yn, next_key=next_key, qry_tp=qry_tp, stk_cd=stk_cd, date_tp=date_tp, thema_nm=thema_nm, flu_pl_amt_tp=flu_pl_amt_tp, stex_tp=stex_tp)
        raw_response = self.core.call("ka90001", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestsByThemeGroup(**raw_response)

    def theme_items(self, cont_yn: str = "", next_key: str = "", date_tp: str = "", thema_grp_cd: str = "", stex_tp: str = "") -> ThemeItems:
        """
        [ka90002] 테마구성종목요청
        분류: 국내주식 - 테마
        """
        req = ThemeItemsRequest(cont_yn=cont_yn, next_key=next_key, date_tp=date_tp, thema_grp_cd=thema_grp_cd, stex_tp=stex_tp)
        raw_response = self.core.call("ka90002", **req.model_dump(by_alias=True, exclude_none=True))
        return ThemeItems(**raw_response)

    def elw_daily_sensitivity_indicator(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> ElwDailySensitivityIndicator:
        """
        [ka10048] ELW일별민감도지표요청
        분류: 국내주식 - ELW
        """
        req = ElwDailySensitivityIndicatorRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10048", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwDailySensitivityIndicator(**raw_response)

    def elw_sensitivity_indicator(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> ElwSensitivityIndicator:
        """
        [ka10050] ELW민감도지표요청
        분류: 국내주식 - ELW
        """
        req = ElwSensitivityIndicatorRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka10050", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwSensitivityIndicator(**raw_response)

    def sudden_fluctuation_elw_price(self, cont_yn: str = "", next_key: str = "", flu_tp: str = "", tm_tp: str = "", tm: str = "", trde_qty_tp: str = "", isscomp_cd: str = "", bsis_aset_cd: str = "", rght_tp: str = "", lpcd: str = "", trde_end_elwskip: str = "") -> SuddenFluctuationElwPrice:
        """
        [ka30001] ELW가격급등락요청
        분류: 국내주식 - ELW
        """
        req = SuddenFluctuationElwPriceRequest(cont_yn=cont_yn, next_key=next_key, flu_tp=flu_tp, tm_tp=tm_tp, tm=tm, trde_qty_tp=trde_qty_tp, isscomp_cd=isscomp_cd, bsis_aset_cd=bsis_aset_cd, rght_tp=rght_tp, lpcd=lpcd, trde_end_elwskip=trde_end_elwskip)
        raw_response = self.core.call("ka30001", **req.model_dump(by_alias=True, exclude_none=True))
        return SuddenFluctuationElwPrice(**raw_response)

    def elw_net_sales_top_by_trader(self, cont_yn: str = "", next_key: str = "", isscomp_cd: str = "", trde_qty_tp: str = "", trde_tp: str = "", dt: str = "", trde_end_elwskip: str = "") -> ElwNetSalesTopByTrader:
        """
        [ka30002] 거래원별ELW순매매상위요청
        분류: 국내주식 - ELW
        """
        req = ElwNetSalesTopByTraderRequest(cont_yn=cont_yn, next_key=next_key, isscomp_cd=isscomp_cd, trde_qty_tp=trde_qty_tp, trde_tp=trde_tp, dt=dt, trde_end_elwskip=trde_end_elwskip)
        raw_response = self.core.call("ka30002", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwNetSalesTopByTrader(**raw_response)

    def daily_trend_elwlp_holdings(self, cont_yn: str = "", next_key: str = "", bsis_aset_cd: str = "", base_dt: str = "") -> DailyTrendElwlpHoldings:
        """
        [ka30003] ELWLP보유일별추이요청
        분류: 국내주식 - ELW
        """
        req = DailyTrendElwlpHoldingsRequest(cont_yn=cont_yn, next_key=next_key, bsis_aset_cd=bsis_aset_cd, base_dt=base_dt)
        raw_response = self.core.call("ka30003", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyTrendElwlpHoldings(**raw_response)

    def elw_disparity_rate(self, cont_yn: str = "", next_key: str = "", isscomp_cd: str = "", bsis_aset_cd: str = "", rght_tp: str = "", lpcd: str = "", trde_end_elwskip: str = "") -> ElwDisparityRate:
        """
        [ka30004] ELW괴리율요청
        분류: 국내주식 - ELW
        """
        req = ElwDisparityRateRequest(cont_yn=cont_yn, next_key=next_key, isscomp_cd=isscomp_cd, bsis_aset_cd=bsis_aset_cd, rght_tp=rght_tp, lpcd=lpcd, trde_end_elwskip=trde_end_elwskip)
        raw_response = self.core.call("ka30004", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwDisparityRate(**raw_response)

    def elw_condition_search(self, cont_yn: str = "", next_key: str = "", isscomp_cd: str = "", bsis_aset_cd: str = "", rght_tp: str = "", lpcd: str = "", sort_tp: str = "") -> ElwConditionSearch:
        """
        [ka30005] ELW조건검색요청
        분류: 국내주식 - ELW
        """
        req = ElwConditionSearchRequest(cont_yn=cont_yn, next_key=next_key, isscomp_cd=isscomp_cd, bsis_aset_cd=bsis_aset_cd, rght_tp=rght_tp, lpcd=lpcd, sort_tp=sort_tp)
        raw_response = self.core.call("ka30005", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwConditionSearch(**raw_response)

    def elw_fluctuation_rate_ranking(self, cont_yn: str = "", next_key: str = "", sort_tp: str = "", rght_tp: str = "", trde_end_skip: str = "") -> ElwFluctuationRateRanking:
        """
        [ka30009] ELW등락율순위요청
        분류: 국내주식 - ELW
        """
        req = ElwFluctuationRateRankingRequest(cont_yn=cont_yn, next_key=next_key, sort_tp=sort_tp, rght_tp=rght_tp, trde_end_skip=trde_end_skip)
        raw_response = self.core.call("ka30009", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwFluctuationRateRanking(**raw_response)

    def elw_remaining_balance_ranking(self, cont_yn: str = "", next_key: str = "", sort_tp: str = "", rght_tp: str = "", trde_end_skip: str = "") -> ElwRemainingBalanceRanking:
        """
        [ka30010] ELW잔량순위요청
        분류: 국내주식 - ELW
        """
        req = ElwRemainingBalanceRankingRequest(cont_yn=cont_yn, next_key=next_key, sort_tp=sort_tp, rght_tp=rght_tp, trde_end_skip=trde_end_skip)
        raw_response = self.core.call("ka30010", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwRemainingBalanceRanking(**raw_response)

    def elw_proximity_rate(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> ElwProximityRate:
        """
        [ka30011] ELW근접율요청
        분류: 국내주식 - ELW
        """
        req = ElwProximityRateRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka30011", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwProximityRate(**raw_response)

    def detailed_information_elw_items(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> DetailedInformationElwItems:
        """
        [ka30012] ELW종목상세정보요청
        분류: 국내주식 - ELW
        """
        req = DetailedInformationElwItemsRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka30012", **req.model_dump(by_alias=True, exclude_none=True))
        return DetailedInformationElwItems(**raw_response)

    def etf_return_rate(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "", etfobjt_idex_cd: str = "", dt: str = "") -> EtfReturnRate:
        """
        [ka40001] ETF수익율요청
        분류: 국내주식 - ETF
        """
        req = EtfReturnRateRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd, etfobjt_idex_cd=etfobjt_idex_cd, dt=dt)
        raw_response = self.core.call("ka40001", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfReturnRate(**raw_response)

    def etf_item_information(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfItemInformation:
        """
        [ka40002] ETF종목정보요청
        분류: 국내주식 - ETF
        """
        req = EtfItemInformationRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40002", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfItemInformation(**raw_response)

    def etf_daily_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfDailyTrend:
        """
        [ka40003] ETF일별추이요청
        분류: 국내주식 - ETF
        """
        req = EtfDailyTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40003", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfDailyTrend(**raw_response)

    def full_etf(self, cont_yn: str = "", next_key: str = "", txon_type: str = "", navpre: str = "", mngmcomp: str = "", txon_yn: str = "", trace_idex: str = "", stex_tp: str = "") -> FullEtf:
        """
        [ka40004] ETF전체시세요청
        분류: 국내주식 - ETF
        """
        req = FullEtfRequest(cont_yn=cont_yn, next_key=next_key, txon_type=txon_type, navpre=navpre, mngmcomp=mngmcomp, txon_yn=txon_yn, trace_idex=trace_idex, stex_tp=stex_tp)
        raw_response = self.core.call("ka40004", **req.model_dump(by_alias=True, exclude_none=True))
        return FullEtf(**raw_response)

    def etf_time_zone_trend(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfTimeZoneTrend:
        """
        [ka40006] ETF시간대별추이요청
        분류: 국내주식 - ETF
        """
        req = EtfTimeZoneTrendRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40006", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTimeZoneTrend(**raw_response)

    def etf_trading_by_time_slot(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfTradingByTimeSlot:
        """
        [ka40007] ETF시간대별체결요청
        분류: 국내주식 - ETF
        """
        req = EtfTradingByTimeSlotRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40007", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTradingByTimeSlot(**raw_response)

    def etf_transaction_by_date(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfTransactionByDate:
        """
        [ka40008] ETF일자별체결요청
        분류: 국내주식 - ETF
        """
        req = EtfTransactionByDateRequest(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40008", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTransactionByDate(**raw_response)

    def etf_trading_by_time_slot1(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfTradingByTimeSlot1:
        """
        [ka40009] ETF시간대별체결요청
        분류: 국내주식 - ETF
        """
        req = EtfTradingByTimeSlot1Request(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40009", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTradingByTimeSlot1(**raw_response)

    def etf_time_zone_trend_request1(self, cont_yn: str = "", next_key: str = "", stk_cd: str = "") -> EtfTimeZoneTrendRequest1:
        """
        [ka40010] ETF시간대별추이요청
        분류: 국내주식 - ETF
        """
        req = EtfTimeZoneTrendRequest1Request(cont_yn=cont_yn, next_key=next_key, stk_cd=stk_cd)
        raw_response = self.core.call("ka40010", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTimeZoneTrendRequest1(**raw_response)

# ====================================================================
# 3. Registry (동적 호출을 위한 매핑)
# ====================================================================

API_ID_TO_METHOD: Dict[str, str] = {
    "au10001": "issue_access_token",
    "au10002": "revoke_access_token",
    "ka00001": "account_number",
    "ka01690": "daily_balance_return_rate",
    "ka10072": "realized_profit_loss_by_date_item_date",
    "ka10073": "realized_profit_loss_by_date_item_period",
    "ka10074": "realized_profit_loss_by_date",
    "ka10075": "non_confirmation",
    "ka10076": "conclusion",
    "ka10077": "same_day_realized_profit_loss",
    "ka10085": "account_yield",
    "ka10088": "unfilled_split_order_details",
    "ka10170": "same_day_sales_log",
    "kt00001": "detailed_deposit",
    "kt00002": "daily_estimated_deposited_asset",
    "kt00003": "estimated_asset",
    "kt00004": "account_evaluation",
    "kt00005": "transaction_balance",
    "kt00007": "order_details_by_account",
    "kt00008": "next_day_payment_schedule_details_by_account",
    "kt00009": "order_execution_by_account",
    "kt00010": "order_withdrawal_amount",
    "kt00011": "quantity_available_order_by_margin_rate",
    "kt00012": "quantity_available_order_by_credit_deposit_rate",
    "kt00013": "margin_details",
    "kt00015": "comprehensive_consignment_transaction_details",
    "kt00016": "detailed_daily_account_returns",
    "kt00017": "daily_by_account",
    "kt00018": "account_evaluation_balance_details",
    "kt50020": "check_gold_spot_balance",
    "kt50021": "gold_spot_deposit",
    "kt50030": "all_gold_spot_orders",
    "kt50031": "gold_spot_order_execution",
    "kt50032": "gold_spot_transaction_history",
    "kt50075": "gold_spot_non_trading",
    "ka10014": "short_selling_trend",
    "ka10008": "foreign_stock_trading_trends_by_item",
    "ka10009": "stock_institution",
    "ka10131": "continuous_trading_by_institutional_foreigners",
    "ka52301": "current_gold_spot_investors",
    "ka10068": "loan_lending_transaction_trend",
    "ka10069": "top10_borrowing_stocks",
    "ka20068": "loan_lending_transaction_trend_by_item",
    "ka90012": "loan_transaction_details",
    "ka10020": "higher_quota_balance",
    "ka10021": "sudden_increase_quotation_balance",
    "ka10022": "sudden_increase_remaining_capacity",
    "ka10023": "sudden_increase_trading_volume",
    "ka10027": "higher_fluctuation_rate_compared_previous_day",
    "ka10029": "higher_expected_transaction_rate",
    "ka10030": "high_transaction_volume_day",
    "ka10031": "previous_day_highest_trading_volume",
    "ka10032": "higher_transaction_amount",
    "ka10033": "higher_credit_ratio",
    "ka10034": "external_transaction_top_sales_by_period",
    "ka10035": "foreign_continuous_net_sales_top",
    "ka10036": "top_foreign_limit_burnout_rate_increase",
    "ka10037": "foreign_over_counter_sales",
    "ka10038": "ranking_securities_companies_by_stock",
    "ka10039": "top_trading_by_securities_company",
    "ka10040": "same_day_major_transaction",
    "ka10042": "net_buying_trader_ranking",
    "ka10053": "same_day_high_withdrawal",
    "ka10062": "same_net_sales_ranking",
    "ka10065": "intraday_trading_by_investor",
    "ka10098": "ranking_out_hours_single_price_fluctuation_rate",
    "ka90009": "foreign_institutional_trading_top",
    "ka10004": "stock_quote",
    "ka10005": "stock_weekly_monthly_hourly_minutes",
    "ka10006": "stock_time",
    "ka10007": "price_information",
    "ka10011": "all_new_stock_warrants",
    "ka10044": "daily_institutional_trading_items",
    "ka10045": "institutional_trading_trend_by_item",
    "ka10046": "fastening_strength_trend_by_time",
    "ka10047": "daily_tightening_strength_trend",
    "ka10063": "intraday_investor_specific_trading",
    "ka10066": "trading_by_investor_after_market_close",
    "ka10078": "stock_trading_trends_by_securities_company",
    "ka10086": "daily_stock",
    "ka10087": "single_after_hours",
    "ka50010": "gold_spot_trading_trend",
    "ka50012": "spot_gold_daily_trend",
    "ka50087": "gold_spot_expected_transaction",
    "ka50100": "gold_spot_price_information",
    "ka50101": "gold_spot_quote",
    "ka90005": "program_trading_trend_by_time_zone",
    "ka90006": "program_trading_profit_balance_trend",
    "ka90007": "cumulative_program_trading_trend",
    "ka90008": "program_trading_trend_by_item_time",
    "ka90010": "program_trading_trend_date",
    "ka90013": "daily_program_trading_trend_items",
    "kt10006": "credit_buy_order",
    "kt10007": "credit_sell_order",
    "kt10008": "credit_correction_order",
    "kt10009": "credit_cancellation_order",
    "00": "order_execution",
    "04": "balance",
    "0A": "stock_momentum",
    "0B": "stock_signing",
    "0C": "stock_preferred_price",
    "0D": "stock_quote_balance",
    "0E": "stock_after_hours_quote",
    "0F": "stock_day_trader",
    "0G": "etf_nav",
    "0H": "stock_expected_execution",
    "0I": "international_gold_conversion_price",
    "0J": "sector_index",
    "0U": "industry_fluctuations",
    "0g": "stock_item_information",
    "0m": "elw_theorist",
    "0s": "long_start_time",
    "0u": "elw_indicator",
    "0w": "stock_program_trading",
    "1h": "activate_disable_vi",
    "ka10010": "industry_program",
    "ka10051": "investor_net_purchase_by_industry",
    "ka20001": "current_industry",
    "ka20002": "stocks_by_industry",
    "ka20003": "all_industry_indices",
    "ka20009": "industry_current_price_daily",
    "ka10171": "condition_search_list",
    "ka10172": "conditional_search_general",
    "ka10173": "real_time_conditional_search",
    "ka10174": "conditional_search_real_time_cancellation",
    "ka00198": "real_time_item_ranking",
    "ka10001": "basic_stock_information",
    "ka10002": "stock_exchange",
    "ka10003": "conclusion_information",
    "ka10013": "credit_trading_trend",
    "ka10015": "daily_transaction",
    "ka10016": "low_report",
    "ka10017": "upper_lower_limits",
    "ka10018": "high_low_price_proximity",
    "ka10019": "sudden_price_fluctuation",
    "ka10024": "transaction_volume_update",
    "ka10025": "concentration_properties_sale",
    "ka10026": "high_low_per",
    "ka10028": "fluctuation_rate_compared_market_price",
    "ka10043": "transaction_price_analysis",
    "ka10052": "trader_instantaneous_trading_volume",
    "ka10054": "items_activate_volatility_mitigation_device",
    "ka10055": "settlement_day_before_day",
    "ka10058": "daily_trading_items_by_investor",
    "ka10059": "requests_by_item_investor_institution",
    "ka10061": "total_by_item_investor_institution",
    "ka10084": "settlement_day_before_same_day",
    "ka10095": "information_items_interest",
    "ka10099": "stock_information_list",
    "ka10100": "check_stock_information",
    "ka10101": "industry_code_list",
    "ka10102": "member_company_list",
    "ka90003": "top50_program_net_purchases",
    "ka90004": "program_trading_by_item",
    "kt20016": "credit_loan_available_items",
    "kt20017": "credit_loan_availability",
    "kt10000": "stock_purchase_order",
    "kt10001": "stock_sell_order",
    "kt10002": "stock_correction_order",
    "kt10003": "stock_cancellation_order",
    "kt50000": "gold_spot_purchase_order",
    "kt50001": "gold_spot_sell_order",
    "kt50002": "spot_gold_correction_order",
    "kt50003": "gold_spot_cancellation_order",
    "ka10060": "chart_by_item_investor_institution",
    "ka10064": "intraday_investor_specific_trading_chart",
    "ka10079": "stock_tick_chart",
    "ka10080": "stock_chart",
    "ka10081": "stock_daily_chart",
    "ka10082": "stock_weekly_chart",
    "ka10083": "stock_monthly_chart",
    "ka10094": "stock_annual_chart",
    "ka20004": "industry_tick_chart",
    "ka20005": "industry_division",
    "ka20006": "industry_daily_salary",
    "ka20007": "industry_salary",
    "ka20008": "industry_monthly_salary",
    "ka20019": "industry_year_salary",
    "ka50079": "gold_spot_tick_chart",
    "ka50080": "gold_spot_fractional_chart",
    "ka50081": "gold_spot_daily_chart",
    "ka50082": "gold_spot_weekly_chart",
    "ka50083": "gold_spot_monthly_chart",
    "ka50091": "gold_spot_daily_tick_chart",
    "ka50092": "gold_spot_daily_chart",
    "ka90001": "requests_by_theme_group",
    "ka90002": "theme_items",
    "ka10048": "elw_daily_sensitivity_indicator",
    "ka10050": "elw_sensitivity_indicator",
    "ka30001": "sudden_fluctuation_elw_price",
    "ka30002": "elw_net_sales_top_by_trader",
    "ka30003": "daily_trend_elwlp_holdings",
    "ka30004": "elw_disparity_rate",
    "ka30005": "elw_condition_search",
    "ka30009": "elw_fluctuation_rate_ranking",
    "ka30010": "elw_remaining_balance_ranking",
    "ka30011": "elw_proximity_rate",
    "ka30012": "detailed_information_elw_items",
    "ka40001": "etf_return_rate",
    "ka40002": "etf_item_information",
    "ka40003": "etf_daily_trend",
    "ka40004": "full_etf",
    "ka40006": "etf_time_zone_trend",
    "ka40007": "etf_trading_by_time_slot",
    "ka40008": "etf_transaction_by_date",
    "ka40009": "etf_trading_by_time_slot1",
    "ka40010": "etf_time_zone_trend_request1",
}

API_ID_TO_REQ_MODEL: Dict[str, Type[BaseModel]] = {
    "au10001": IssueAccessTokenRequest,
    "au10002": RevokeAccessTokenRequest,
    "ka00001": AccountNumberRequest,
    "ka01690": DailyBalanceReturnRateRequest,
    "ka10072": RealizedProfitLossByDateItemDateRequest,
    "ka10073": RealizedProfitLossByDateItemPeriodRequest,
    "ka10074": RealizedProfitLossByDateRequest,
    "ka10075": NonConfirmationRequest,
    "ka10076": ConclusionRequest,
    "ka10077": SameDayRealizedProfitLossRequest,
    "ka10085": AccountYieldRequest,
    "ka10088": UnfilledSplitOrderDetailsRequest,
    "ka10170": SameDaySalesLogRequest,
    "kt00001": DetailedDepositRequest,
    "kt00002": DailyEstimatedDepositedAssetRequest,
    "kt00003": EstimatedAssetRequest,
    "kt00004": AccountEvaluationRequest,
    "kt00005": TransactionBalanceRequest,
    "kt00007": OrderDetailsByAccountRequest,
    "kt00008": NextDayPaymentScheduleDetailsByAccountRequest,
    "kt00009": OrderExecutionByAccountRequest,
    "kt00010": OrderWithdrawalAmountRequest,
    "kt00011": QuantityAvailableOrderByMarginRateRequest,
    "kt00012": QuantityAvailableOrderByCreditDepositRateRequest,
    "kt00013": MarginDetailsRequest,
    "kt00015": ComprehensiveConsignmentTransactionDetailsRequest,
    "kt00016": DetailedDailyAccountReturnsRequest,
    "kt00017": DailyByAccountRequest,
    "kt00018": AccountEvaluationBalanceDetailsRequest,
    "kt50020": CheckGoldSpotBalanceRequest,
    "kt50021": GoldSpotDepositRequest,
    "kt50030": AllGoldSpotOrdersRequest,
    "kt50031": GoldSpotOrderExecutionRequest,
    "kt50032": GoldSpotTransactionHistoryRequest,
    "kt50075": GoldSpotNonTradingRequest,
    "ka10014": ShortSellingTrendRequest,
    "ka10008": ForeignStockTradingTrendsByItemRequest,
    "ka10009": StockInstitutionRequest,
    "ka10131": ContinuousTradingByInstitutionalForeignersRequest,
    "ka52301": CurrentGoldSpotInvestorsRequest,
    "ka10068": LoanLendingTransactionTrendRequest,
    "ka10069": Top10BorrowingStocksRequest,
    "ka20068": LoanLendingTransactionTrendByItemRequest,
    "ka90012": LoanTransactionDetailsRequest,
    "ka10020": HigherQuotaBalanceRequest,
    "ka10021": SuddenIncreaseQuotationBalanceRequest,
    "ka10022": SuddenIncreaseRemainingCapacityRequest,
    "ka10023": SuddenIncreaseTradingVolumeRequest,
    "ka10027": HigherFluctuationRateComparedPreviousDayRequest,
    "ka10029": HigherExpectedTransactionRateRequest,
    "ka10030": HighTransactionVolumeDayRequest,
    "ka10031": PreviousDayHighestTradingVolumeRequest,
    "ka10032": HigherTransactionAmountRequest,
    "ka10033": HigherCreditRatioRequest,
    "ka10034": ExternalTransactionTopSalesByPeriodRequest,
    "ka10035": ForeignContinuousNetSalesTopRequest,
    "ka10036": TopForeignLimitBurnoutRateIncreaseRequest,
    "ka10037": ForeignOverCounterSalesRequest,
    "ka10038": RankingSecuritiesCompaniesByStockRequest,
    "ka10039": TopTradingBySecuritiesCompanyRequest,
    "ka10040": SameDayMajorTransactionRequest,
    "ka10042": NetBuyingTraderRankingRequest,
    "ka10053": SameDayHighWithdrawalRequest,
    "ka10062": SameNetSalesRankingRequest,
    "ka10065": IntradayTradingByInvestorRequest,
    "ka10098": RankingOutHoursSinglePriceFluctuationRateRequest,
    "ka90009": ForeignInstitutionalTradingTopRequest,
    "ka10004": StockQuoteRequest,
    "ka10005": StockWeeklyMonthlyHourlyMinutesRequest,
    "ka10006": StockTimeRequest,
    "ka10007": PriceInformationRequest,
    "ka10011": AllNewStockWarrantsRequest,
    "ka10044": DailyInstitutionalTradingItemsRequest,
    "ka10045": InstitutionalTradingTrendByItemRequest,
    "ka10046": FasteningStrengthTrendByTimeRequest,
    "ka10047": DailyTighteningStrengthTrendRequest,
    "ka10063": IntradayInvestorSpecificTradingRequest,
    "ka10066": TradingByInvestorAfterMarketCloseRequest,
    "ka10078": StockTradingTrendsBySecuritiesCompanyRequest,
    "ka10086": DailyStockRequest,
    "ka10087": SingleAfterHoursRequest,
    "ka50010": GoldSpotTradingTrendRequest,
    "ka50012": SpotGoldDailyTrendRequest,
    "ka50087": GoldSpotExpectedTransactionRequest,
    "ka50100": GoldSpotPriceInformationRequest,
    "ka50101": GoldSpotQuoteRequest,
    "ka90005": ProgramTradingTrendByTimeZoneRequest,
    "ka90006": ProgramTradingProfitBalanceTrendRequest,
    "ka90007": CumulativeProgramTradingTrendRequest,
    "ka90008": ProgramTradingTrendByItemTimeRequest,
    "ka90010": ProgramTradingTrendDateRequest,
    "ka90013": DailyProgramTradingTrendItemsRequest,
    "kt10006": CreditBuyOrderRequest,
    "kt10007": CreditSellOrderRequest,
    "kt10008": CreditCorrectionOrderRequest,
    "kt10009": CreditCancellationOrderRequest,
    "00": OrderExecutionRequest,
    "04": BalanceRequest,
    "0A": StockMomentumRequest,
    "0B": StockSigningRequest,
    "0C": StockPreferredPriceRequest,
    "0D": StockQuoteBalanceRequest,
    "0E": StockAfterHoursQuoteRequest,
    "0F": StockDayTraderRequest,
    "0G": EtfNavRequest,
    "0H": StockExpectedExecutionRequest,
    "0I": InternationalGoldConversionPriceRequest,
    "0J": SectorIndexRequest,
    "0U": IndustryFluctuationsRequest,
    "0g": StockItemInformationRequest,
    "0m": ElwTheoristRequest,
    "0s": LongStartTimeRequest,
    "0u": ElwIndicatorRequest,
    "0w": StockProgramTradingRequest,
    "1h": ActivateDisableViRequest,
    "ka10010": IndustryProgramRequest,
    "ka10051": InvestorNetPurchaseByIndustryRequest,
    "ka20001": CurrentIndustryRequest,
    "ka20002": StocksByIndustryRequest,
    "ka20003": AllIndustryIndicesRequest,
    "ka20009": IndustryCurrentPriceDailyRequest,
    "ka10171": ConditionSearchListRequest,
    "ka10172": ConditionalSearchGeneralRequest,
    "ka10173": RealTimeConditionalSearchRequest,
    "ka10174": ConditionalSearchRealTimeCancellationRequest,
    "ka00198": RealTimeItemRankingRequest,
    "ka10001": BasicStockInformationRequest,
    "ka10002": StockExchangeRequest,
    "ka10003": ConclusionInformationRequest,
    "ka10013": CreditTradingTrendRequest,
    "ka10015": DailyTransactionRequest,
    "ka10016": LowReportRequest,
    "ka10017": UpperLowerLimitsRequest,
    "ka10018": HighLowPriceProximityRequest,
    "ka10019": SuddenPriceFluctuationRequest,
    "ka10024": TransactionVolumeUpdateRequest,
    "ka10025": ConcentrationPropertiesSaleRequest,
    "ka10026": HighLowPerRequest,
    "ka10028": FluctuationRateComparedMarketPriceRequest,
    "ka10043": TransactionPriceAnalysisRequest,
    "ka10052": TraderInstantaneousTradingVolumeRequest,
    "ka10054": ItemsActivateVolatilityMitigationDeviceRequest,
    "ka10055": SettlementDayBeforeDayRequest,
    "ka10058": DailyTradingItemsByInvestorRequest,
    "ka10059": RequestsByItemInvestorInstitutionRequest,
    "ka10061": TotalByItemInvestorInstitutionRequest,
    "ka10084": SettlementDayBeforeSameDayRequest,
    "ka10095": InformationItemsInterestRequest,
    "ka10099": StockInformationListRequest,
    "ka10100": CheckStockInformationRequest,
    "ka10101": IndustryCodeListRequest,
    "ka10102": MemberCompanyListRequest,
    "ka90003": Top50ProgramNetPurchasesRequest,
    "ka90004": ProgramTradingByItemRequest,
    "kt20016": CreditLoanAvailableItemsRequest,
    "kt20017": CreditLoanAvailabilityRequest,
    "kt10000": StockPurchaseOrderRequest,
    "kt10001": StockSellOrderRequest,
    "kt10002": StockCorrectionOrderRequest,
    "kt10003": StockCancellationOrderRequest,
    "kt50000": GoldSpotPurchaseOrderRequest,
    "kt50001": GoldSpotSellOrderRequest,
    "kt50002": SpotGoldCorrectionOrderRequest,
    "kt50003": GoldSpotCancellationOrderRequest,
    "ka10060": ChartByItemInvestorInstitutionRequest,
    "ka10064": IntradayInvestorSpecificTradingChartRequest,
    "ka10079": StockTickChartRequest,
    "ka10080": StockChartRequest,
    "ka10081": StockDailyChartRequest,
    "ka10082": StockWeeklyChartRequest,
    "ka10083": StockMonthlyChartRequest,
    "ka10094": StockAnnualChartRequest,
    "ka20004": IndustryTickChartRequest,
    "ka20005": IndustryDivisionRequest,
    "ka20006": IndustryDailySalaryRequest,
    "ka20007": IndustrySalaryRequest,
    "ka20008": IndustryMonthlySalaryRequest,
    "ka20019": IndustryYearSalaryRequest,
    "ka50079": GoldSpotTickChartRequest,
    "ka50080": GoldSpotFractionalChartRequest,
    "ka50081": GoldSpotDailyChartRequest,
    "ka50082": GoldSpotWeeklyChartRequest,
    "ka50083": GoldSpotMonthlyChartRequest,
    "ka50091": GoldSpotDailyTickChartRequest,
    "ka50092": GoldSpotDailyChartRequest,
    "ka90001": RequestsByThemeGroupRequest,
    "ka90002": ThemeItemsRequest,
    "ka10048": ElwDailySensitivityIndicatorRequest,
    "ka10050": ElwSensitivityIndicatorRequest,
    "ka30001": SuddenFluctuationElwPriceRequest,
    "ka30002": ElwNetSalesTopByTraderRequest,
    "ka30003": DailyTrendElwlpHoldingsRequest,
    "ka30004": ElwDisparityRateRequest,
    "ka30005": ElwConditionSearchRequest,
    "ka30009": ElwFluctuationRateRankingRequest,
    "ka30010": ElwRemainingBalanceRankingRequest,
    "ka30011": ElwProximityRateRequest,
    "ka30012": DetailedInformationElwItemsRequest,
    "ka40001": EtfReturnRateRequest,
    "ka40002": EtfItemInformationRequest,
    "ka40003": EtfDailyTrendRequest,
    "ka40004": FullEtfRequest,
    "ka40006": EtfTimeZoneTrendRequest,
    "ka40007": EtfTradingByTimeSlotRequest,
    "ka40008": EtfTransactionByDateRequest,
    "ka40009": EtfTradingByTimeSlot1Request,
    "ka40010": EtfTimeZoneTrendRequest1Request,
}

API_ID_TO_RES_MODEL: Dict[str, Type[BaseModel]] = {
    "au10001": IssueAccessToken,
    "au10002": RevokeAccessToken,
    "ka00001": AccountNumber,
    "ka01690": DailyBalanceReturnRate,
    "ka10072": RealizedProfitLossByDateItemDate,
    "ka10073": RealizedProfitLossByDateItemPeriod,
    "ka10074": RealizedProfitLossByDate,
    "ka10075": NonConfirmation,
    "ka10076": Conclusion,
    "ka10077": SameDayRealizedProfitLoss,
    "ka10085": AccountYield,
    "ka10088": UnfilledSplitOrderDetails,
    "ka10170": SameDaySalesLog,
    "kt00001": DetailedDeposit,
    "kt00002": DailyEstimatedDepositedAsset,
    "kt00003": EstimatedAsset,
    "kt00004": AccountEvaluation,
    "kt00005": TransactionBalance,
    "kt00007": OrderDetailsByAccount,
    "kt00008": NextDayPaymentScheduleDetailsByAccount,
    "kt00009": OrderExecutionByAccount,
    "kt00010": OrderWithdrawalAmount,
    "kt00011": QuantityAvailableOrderByMarginRate,
    "kt00012": QuantityAvailableOrderByCreditDepositRate,
    "kt00013": MarginDetails,
    "kt00015": ComprehensiveConsignmentTransactionDetails,
    "kt00016": DetailedDailyAccountReturns,
    "kt00017": DailyByAccount,
    "kt00018": AccountEvaluationBalanceDetails,
    "kt50020": CheckGoldSpotBalance,
    "kt50021": GoldSpotDeposit,
    "kt50030": AllGoldSpotOrders,
    "kt50031": GoldSpotOrderExecution,
    "kt50032": GoldSpotTransactionHistory,
    "kt50075": GoldSpotNonTrading,
    "ka10014": ShortSellingTrend,
    "ka10008": ForeignStockTradingTrendsByItem,
    "ka10009": StockInstitution,
    "ka10131": ContinuousTradingByInstitutionalForeigners,
    "ka52301": CurrentGoldSpotInvestors,
    "ka10068": LoanLendingTransactionTrend,
    "ka10069": Top10BorrowingStocks,
    "ka20068": LoanLendingTransactionTrendByItem,
    "ka90012": LoanTransactionDetails,
    "ka10020": HigherQuotaBalance,
    "ka10021": SuddenIncreaseQuotationBalance,
    "ka10022": SuddenIncreaseRemainingCapacity,
    "ka10023": SuddenIncreaseTradingVolume,
    "ka10027": HigherFluctuationRateComparedPreviousDay,
    "ka10029": HigherExpectedTransactionRate,
    "ka10030": HighTransactionVolumeDay,
    "ka10031": PreviousDayHighestTradingVolume,
    "ka10032": HigherTransactionAmount,
    "ka10033": HigherCreditRatio,
    "ka10034": ExternalTransactionTopSalesByPeriod,
    "ka10035": ForeignContinuousNetSalesTop,
    "ka10036": TopForeignLimitBurnoutRateIncrease,
    "ka10037": ForeignOverCounterSales,
    "ka10038": RankingSecuritiesCompaniesByStock,
    "ka10039": TopTradingBySecuritiesCompany,
    "ka10040": SameDayMajorTransaction,
    "ka10042": NetBuyingTraderRanking,
    "ka10053": SameDayHighWithdrawal,
    "ka10062": SameNetSalesRanking,
    "ka10065": IntradayTradingByInvestor,
    "ka10098": RankingOutHoursSinglePriceFluctuationRate,
    "ka90009": ForeignInstitutionalTradingTop,
    "ka10004": StockQuote,
    "ka10005": StockWeeklyMonthlyHourlyMinutes,
    "ka10006": StockTime,
    "ka10007": PriceInformation,
    "ka10011": AllNewStockWarrants,
    "ka10044": DailyInstitutionalTradingItems,
    "ka10045": InstitutionalTradingTrendByItem,
    "ka10046": FasteningStrengthTrendByTime,
    "ka10047": DailyTighteningStrengthTrend,
    "ka10063": IntradayInvestorSpecificTrading,
    "ka10066": TradingByInvestorAfterMarketClose,
    "ka10078": StockTradingTrendsBySecuritiesCompany,
    "ka10086": DailyStock,
    "ka10087": SingleAfterHours,
    "ka50010": GoldSpotTradingTrend,
    "ka50012": SpotGoldDailyTrend,
    "ka50087": GoldSpotExpectedTransaction,
    "ka50100": GoldSpotPriceInformation,
    "ka50101": GoldSpotQuote,
    "ka90005": ProgramTradingTrendByTimeZone,
    "ka90006": ProgramTradingProfitBalanceTrend,
    "ka90007": CumulativeProgramTradingTrend,
    "ka90008": ProgramTradingTrendByItemTime,
    "ka90010": ProgramTradingTrendDate,
    "ka90013": DailyProgramTradingTrendItems,
    "kt10006": CreditBuyOrder,
    "kt10007": CreditSellOrder,
    "kt10008": CreditCorrectionOrder,
    "kt10009": CreditCancellationOrder,
    "00": OrderExecution,
    "04": Balance,
    "0A": StockMomentum,
    "0B": StockSigning,
    "0C": StockPreferredPrice,
    "0D": StockQuoteBalance,
    "0E": StockAfterHoursQuote,
    "0F": StockDayTrader,
    "0G": EtfNav,
    "0H": StockExpectedExecution,
    "0I": InternationalGoldConversionPrice,
    "0J": SectorIndex,
    "0U": IndustryFluctuations,
    "0g": StockItemInformation,
    "0m": ElwTheorist,
    "0s": LongStartTime,
    "0u": ElwIndicator,
    "0w": StockProgramTrading,
    "1h": ActivateDisableVi,
    "ka10010": IndustryProgram,
    "ka10051": InvestorNetPurchaseByIndustry,
    "ka20001": CurrentIndustry,
    "ka20002": StocksByIndustry,
    "ka20003": AllIndustryIndices,
    "ka20009": IndustryCurrentPriceDaily,
    "ka10171": ConditionSearchList,
    "ka10172": ConditionalSearchGeneral,
    "ka10173": RealTimeConditionalSearch,
    "ka10174": ConditionalSearchRealTimeCancellation,
    "ka00198": RealTimeItemRanking,
    "ka10001": BasicStockInformation,
    "ka10002": StockExchange,
    "ka10003": ConclusionInformation,
    "ka10013": CreditTradingTrend,
    "ka10015": DailyTransaction,
    "ka10016": LowReport,
    "ka10017": UpperLowerLimits,
    "ka10018": HighLowPriceProximity,
    "ka10019": SuddenPriceFluctuation,
    "ka10024": TransactionVolumeUpdate,
    "ka10025": ConcentrationPropertiesSale,
    "ka10026": HighLowPer,
    "ka10028": FluctuationRateComparedMarketPrice,
    "ka10043": TransactionPriceAnalysis,
    "ka10052": TraderInstantaneousTradingVolume,
    "ka10054": ItemsActivateVolatilityMitigationDevice,
    "ka10055": SettlementDayBeforeDay,
    "ka10058": DailyTradingItemsByInvestor,
    "ka10059": RequestsByItemInvestorInstitution,
    "ka10061": TotalByItemInvestorInstitution,
    "ka10084": SettlementDayBeforeSameDay,
    "ka10095": InformationItemsInterest,
    "ka10099": StockInformationList,
    "ka10100": CheckStockInformation,
    "ka10101": IndustryCodeList,
    "ka10102": MemberCompanyList,
    "ka90003": Top50ProgramNetPurchases,
    "ka90004": ProgramTradingByItem,
    "kt20016": CreditLoanAvailableItems,
    "kt20017": CreditLoanAvailability,
    "kt10000": StockPurchaseOrder,
    "kt10001": StockSellOrder,
    "kt10002": StockCorrectionOrder,
    "kt10003": StockCancellationOrder,
    "kt50000": GoldSpotPurchaseOrder,
    "kt50001": GoldSpotSellOrder,
    "kt50002": SpotGoldCorrectionOrder,
    "kt50003": GoldSpotCancellationOrder,
    "ka10060": ChartByItemInvestorInstitution,
    "ka10064": IntradayInvestorSpecificTradingChart,
    "ka10079": StockTickChart,
    "ka10080": StockChart,
    "ka10081": StockDailyChart,
    "ka10082": StockWeeklyChart,
    "ka10083": StockMonthlyChart,
    "ka10094": StockAnnualChart,
    "ka20004": IndustryTickChart,
    "ka20005": IndustryDivision,
    "ka20006": IndustryDailySalary,
    "ka20007": IndustrySalary,
    "ka20008": IndustryMonthlySalary,
    "ka20019": IndustryYearSalary,
    "ka50079": GoldSpotTickChart,
    "ka50080": GoldSpotFractionalChart,
    "ka50081": GoldSpotDailyChart,
    "ka50082": GoldSpotWeeklyChart,
    "ka50083": GoldSpotMonthlyChart,
    "ka50091": GoldSpotDailyTickChart,
    "ka50092": GoldSpotDailyChart,
    "ka90001": RequestsByThemeGroup,
    "ka90002": ThemeItems,
    "ka10048": ElwDailySensitivityIndicator,
    "ka10050": ElwSensitivityIndicator,
    "ka30001": SuddenFluctuationElwPrice,
    "ka30002": ElwNetSalesTopByTrader,
    "ka30003": DailyTrendElwlpHoldings,
    "ka30004": ElwDisparityRate,
    "ka30005": ElwConditionSearch,
    "ka30009": ElwFluctuationRateRanking,
    "ka30010": ElwRemainingBalanceRanking,
    "ka30011": ElwProximityRate,
    "ka30012": DetailedInformationElwItems,
    "ka40001": EtfReturnRate,
    "ka40002": EtfItemInformation,
    "ka40003": EtfDailyTrend,
    "ka40004": FullEtf,
    "ka40006": EtfTimeZoneTrend,
    "ka40007": EtfTradingByTimeSlot,
    "ka40008": EtfTransactionByDate,
    "ka40009": EtfTradingByTimeSlot1,
    "ka40010": EtfTimeZoneTrendRequest1,
}
