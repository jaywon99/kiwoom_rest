from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Dict, Any, List, Type, Annotated, Callable, Union
from .client import KiwoomClient

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

class AccessTokenIssuanceRequest(BaseModel):
    """[au10001] 접근토큰 발급 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    grant_type: SafeStr = Field(default="", description="grant_type client_credentials 입력")
    appkey: SafeStr = Field(default="", description="앱키")
    secretkey: SafeStr = Field(default="", description="시크릿키")

class AccessTokenIssuanceResponse(BaseModel):
    """[au10001] 접근토큰 발급 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    expires_dt: SafeStr = Field(default="", description="만료일")
    token_type: SafeStr = Field(default="", description="토큰타입")
    token: SafeStr = Field(default="", description="접근토큰")

class DiscardAccessTokenRequest(BaseModel):
    """[au10002] 접근토큰폐기 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    appkey: SafeStr = Field(default="", description="앱키")
    secretkey: SafeStr = Field(default="", description="시크릿키")
    token: SafeStr = Field(default="", description="접근토큰")

class DiscardAccessTokenResponse(BaseModel):
    """[au10002] 접근토큰폐기 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    pass

class AccountNumberInquiryRequest(BaseModel):
    """[ka00001] 계좌번호조회 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class AccountNumberInquiryResponse(BaseModel):
    """[ka00001] 계좌번호조회 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acctNo: SafeStr = Field(default="", description="계좌번호")

class DailyBalanceReturnRateRequest(BaseModel):
    """[ka01690] 일별잔고수익률 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_dt: SafeStr = Field(default="", description="조회일자")

class DailyBalanceReturnRateResponse_DayBalRt(BaseModel):
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

class DailyBalanceReturnRateResponse(BaseModel):
    """[ka01690] 일별잔고수익률 응답 모델"""
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
    day_bal_rt: Annotated[List[DailyBalanceReturnRateResponse_DayBalRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별잔고수익률")

class RealizedProfitLossRequestByDateItemDateRequest(BaseModel):
    """[ka10072] 일자별종목별실현손익요청_일자 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")

class RealizedProfitLossRequestByDateItemDateResponse_DtStkDivRlztPl(BaseModel):
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

class RealizedProfitLossRequestByDateItemDateResponse(BaseModel):
    """[ka10072] 일자별종목별실현손익요청_일자 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dt_stk_div_rlzt_pl: Annotated[List[RealizedProfitLossRequestByDateItemDateResponse_DtStkDivRlztPl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일자별종목별실현손익")

class RealizedProfitLossRequestByDateAndItemPeriodRequest(BaseModel):
    """[ka10073] 일자별종목별실현손익요청_기간 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")

class RealizedProfitLossRequestByDateAndItemPeriodResponse_DtStkRlztPl(BaseModel):
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

class RealizedProfitLossRequestByDateAndItemPeriodResponse(BaseModel):
    """[ka10073] 일자별종목별실현손익요청_기간 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dt_stk_rlzt_pl: Annotated[List[RealizedProfitLossRequestByDateAndItemPeriodResponse_DtStkRlztPl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일자별종목별실현손익")

class RequestForRealizedProfitOrLossByDateRequest(BaseModel):
    """[ka10074] 일자별실현손익요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자")
    end_dt: SafeStr = Field(default="", description="종료일자")

class RequestForRealizedProfitOrLossByDateResponse_DtRlztPl(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    buy_amt: SafeStr = Field(default="", description="매수금액")
    sell_amt: SafeStr = Field(default="", description="매도금액")
    tdy_sel_pl: SafeStr = Field(default="", description="당일매도손익")
    tdy_trde_cmsn: SafeStr = Field(default="", description="당일매매수수료")
    tdy_trde_tax: SafeStr = Field(default="", description="당일매매세금")

class RequestForRealizedProfitOrLossByDateResponse(BaseModel):
    """[ka10074] 일자별실현손익요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_buy_amt: SafeStr = Field(default="", description="총매수금액")
    tot_sell_amt: SafeStr = Field(default="", description="총매도금액")
    rlzt_pl: SafeStr = Field(default="", description="실현손익")
    trde_cmsn: SafeStr = Field(default="", description="매매수수료")
    trde_tax: SafeStr = Field(default="", description="매매세금")
    dt_rlzt_pl: Annotated[List[RequestForRealizedProfitOrLossByDateResponse_DtRlztPl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일자별실현손익")

class NonConfirmationRequestRequest(BaseModel):
    """[ka10075] 미체결요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    all_stk_tp: SafeStr = Field(default="", description="전체종목구분 0:전체, 1:종목")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:전체, 1:매도, 2:매수")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")

class NonConfirmationRequestResponse_Oso(BaseModel):
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

class NonConfirmationRequestResponse(BaseModel):
    """[ka10075] 미체결요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    oso: Annotated[List[NonConfirmationRequestResponse_Oso], BeforeValidator(_force_list)] = Field(default_factory=list, description="미체결")

class ConclusionRequestRequest(BaseModel):
    """[ka10076] 체결요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    qry_tp: SafeStr = Field(default="", description="조회구분 0:전체, 1:종목")
    sell_tp: SafeStr = Field(default="", description="매도수구분 0:전체, 1:매도, 2:매수")
    ord_no: SafeStr = Field(default="", description="주문번호 검색 기준 값으로 입력한 주문번호 보다 과거에 체결된 내역이 조회됩니다.")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")

class ConclusionRequestResponse_Cntr(BaseModel):
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

class ConclusionRequestResponse(BaseModel):
    """[ka10076] 체결요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr: Annotated[List[ConclusionRequestResponse_Cntr], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결")

class RequestForSameDayRealizedProfitAndLossRequest(BaseModel):
    """[ka10077] 당일실현손익상세요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class RequestForSameDayRealizedProfitAndLossResponse_TdyRlztPlDtl(BaseModel):
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

class RequestForSameDayRealizedProfitAndLossResponse(BaseModel):
    """[ka10077] 당일실현손익상세요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_rlzt_pl: SafeStr = Field(default="", description="당일실현손익")
    tdy_rlzt_pl_dtl: Annotated[List[RequestForSameDayRealizedProfitAndLossResponse_TdyRlztPlDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일실현손익상세")

class AccountYieldRequestRequest(BaseModel):
    """[ka10085] 계좌수익률요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stex_tp: SafeStr = Field(default="", description="거래소구분 0 : 통합, 1 : KRX, 2 : NXT")

class AccountYieldRequestResponse_AcntPrftRt(BaseModel):
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

class AccountYieldRequestResponse(BaseModel):
    """[ka10085] 계좌수익률요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_prft_rt: Annotated[List[AccountYieldRequestResponse_AcntPrftRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌수익률")

class UnfilledSplitOrderDetailsRequest(BaseModel):
    """[ka10088] 미체결 분할주문 상세 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    ord_no: SafeStr = Field(default="", description="주문번호")

class UnfilledSplitOrderDetailsResponse_Osop(BaseModel):
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

class UnfilledSplitOrderDetailsResponse(BaseModel):
    """[ka10088] 미체결 분할주문 상세 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    osop: Annotated[List[UnfilledSplitOrderDetailsResponse_Osop], BeforeValidator(_force_list)] = Field(default_factory=list, description="미체결분할주문리스트")

class SameDaySalesLogRequestRequest(BaseModel):
    """[ka10170] 당일매매일지요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD(공백입력시 금일데이터,최근 2개월까지 제공)")
    ottks_tp: SafeStr = Field(default="", description="단주구분 1:당일매수에 대한 당일매도,2:당일매도 전체")
    ch_crd_tp: SafeStr = Field(default="", description="현금신용구분 0:전체, 1:현금매매만, 2:신용매매만")

class SameDaySalesLogRequestResponse_TdyTrdeDiary(BaseModel):
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

class SameDaySalesLogRequestResponse(BaseModel):
    """[ka10170] 당일매매일지요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_sell_amt: SafeStr = Field(default="", description="총매도금액")
    tot_buy_amt: SafeStr = Field(default="", description="총매수금액")
    tot_cmsn_tax: SafeStr = Field(default="", description="총수수료_세금")
    tot_exct_amt: SafeStr = Field(default="", description="총정산금액")
    tot_pl_amt: SafeStr = Field(default="", description="총손익금액")
    tot_prft_rt: SafeStr = Field(default="", description="총수익률")
    tdy_trde_diary: Annotated[List[SameDaySalesLogRequestResponse_TdyTrdeDiary], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일매매일지")

class RequestDetailedStatusOfDepositRequest(BaseModel):
    """[kt00001] 예수금상세현황요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="조회구분 3:추정조회, 2:일반조회")

class RequestDetailedStatusOfDepositResponse_StkEntrPrst(BaseModel):
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

class RequestDetailedStatusOfDepositResponse(BaseModel):
    """[kt00001] 예수금상세현황요청 응답 모델"""
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
    stk_entr_prst: Annotated[List[RequestDetailedStatusOfDepositResponse_StkEntrPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별예수금")

class DailyEstimatedDepositedAssetStatusRequestRequest(BaseModel):
    """[kt00002] 일별추정예탁자산현황요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    start_dt: SafeStr = Field(default="", description="시작조회기간 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료조회기간 YYYYMMDD")

class DailyEstimatedDepositedAssetStatusRequestResponse_DalyPrsmDpstAsetAmtPrst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    entr: SafeStr = Field(default="", description="예수금")
    grnt_use_amt: SafeStr = Field(default="", description="담보대출금")
    crd_loan: SafeStr = Field(default="", description="신용융자금")
    ls_grnt: SafeStr = Field(default="", description="대주담보금")
    repl_amt: SafeStr = Field(default="", description="대용금")
    prsm_dpst_aset_amt: SafeStr = Field(default="", description="추정예탁자산")
    prsm_dpst_aset_amt_bncr_skip: SafeStr = Field(default="", description="추정예탁자산수익증권제외")

class DailyEstimatedDepositedAssetStatusRequestResponse(BaseModel):
    """[kt00002] 일별추정예탁자산현황요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_prsm_dpst_aset_amt_prst: Annotated[List[DailyEstimatedDepositedAssetStatusRequestResponse_DalyPrsmDpstAsetAmtPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별추정예탁자산현황")

class EstimatedAssetInquiryRequestRequest(BaseModel):
    """[kt00003] 추정자산조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="상장폐지조회구분 0:전체, 1:상장폐지종목제외")

class EstimatedAssetInquiryRequestResponse(BaseModel):
    """[kt00003] 추정자산조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prsm_dpst_aset_amt: SafeStr = Field(default="", description="추정예탁자산")

class RequestForAccountEvaluationStatusRequest(BaseModel):
    """[kt00004] 계좌평가현황요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="상장폐지조회구분 0:전체, 1:상장폐지종목제외")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드")

class RequestForAccountEvaluationStatusResponse_StkAcntEvltPrst(BaseModel):
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

class RequestForAccountEvaluationStatusResponse(BaseModel):
    """[kt00004] 계좌평가현황요청 응답 모델"""
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
    stk_acnt_evlt_prst: Annotated[List[RequestForAccountEvaluationStatusResponse_StkAcntEvltPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별계좌평가현황")

class RequestForTransactionBalanceRequest(BaseModel):
    """[kt00005] 체결잔고요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드")

class RequestForTransactionBalanceResponse_StkCntrRemn(BaseModel):
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

class RequestForTransactionBalanceResponse(BaseModel):
    """[kt00005] 체결잔고요청 응답 모델"""
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
    stk_cntr_remn: Annotated[List[RequestForTransactionBalanceResponse_StkCntrRemn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별체결잔고")

class RequestDetailsOnOrderDetailsByAccountRequest(BaseModel):
    """[kt00007] 계좌별주문체결내역상세요청 요청 모델"""
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

class RequestDetailsOnOrderDetailsByAccountResponse_AcntOrdCntrPrpsDtl(BaseModel):
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

class RequestDetailsOnOrderDetailsByAccountResponse(BaseModel):
    """[kt00007] 계좌별주문체결내역상세요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_cntr_prps_dtl: Annotated[List[RequestDetailsOnOrderDetailsByAccountResponse_AcntOrdCntrPrpsDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결내역상세")

class RequestNextDayPaymentScheduleDetailsForEachAccountRequest(BaseModel):
    """[kt00008] 계좌별익일결제예정내역요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dcd_seq: SafeStr = Field(default="", description="시작결제번호")

class RequestNextDayPaymentScheduleDetailsForEachAccountResponse_AcntNxdySetlFrcsPrpsArray(BaseModel):
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

class RequestNextDayPaymentScheduleDetailsForEachAccountResponse(BaseModel):
    """[kt00008] 계좌별익일결제예정내역요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_dt: SafeStr = Field(default="", description="매매일자")
    setl_dt: SafeStr = Field(default="", description="결제일자")
    sell_amt_sum: SafeStr = Field(default="", description="매도정산합")
    buy_amt_sum: SafeStr = Field(default="", description="매수정산합")
    acnt_nxdy_setl_frcs_prps_array: Annotated[List[RequestNextDayPaymentScheduleDetailsForEachAccountResponse_AcntNxdySetlFrcsPrpsArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별익일결제예정내역배열")

class RequestForOrderExecutionStatusByAccountRequest(BaseModel):
    """[kt00009] 계좌별주문체결현황요청 요청 모델"""
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

class RequestForOrderExecutionStatusByAccountResponse_AcntOrdCntrPrstArray(BaseModel):
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

class RequestForOrderExecutionStatusByAccountResponse(BaseModel):
    """[kt00009] 계좌별주문체결현황요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sell_grntl_engg_amt: SafeStr = Field(default="", description="매도약정금액")
    buy_engg_amt: SafeStr = Field(default="", description="매수약정금액")
    engg_amt: SafeStr = Field(default="", description="약정금액")
    acnt_ord_cntr_prst_array: Annotated[List[RequestForOrderExecutionStatusByAccountResponse_AcntOrdCntrPrstArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결현황배열")

class RequestForOrderWithdrawalAmountRequest(BaseModel):
    """[kt00010] 주문인출가능금액요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    io_amt: SafeStr = Field(default="", description="입출금액")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:매도, 2:매수")
    trde_qty: SafeStr = Field(default="", description="매매수량")
    uv: SafeStr = Field(default="", description="매수가격")
    exp_buy_unp: SafeStr = Field(default="", description="예상매수단가")

class RequestForOrderWithdrawalAmountResponse(BaseModel):
    """[kt00010] 주문인출가능금액요청 응답 모델"""
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

class RequestToInquiryQuantityAvailableForOrderByMarginRateRequest(BaseModel):
    """[kt00011] 증거금율별주문가능수량조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    uv: SafeStr = Field(default="", description="매수가격")

class RequestToInquiryQuantityAvailableForOrderByMarginRateResponse(BaseModel):
    """[kt00011] 증거금율별주문가능수량조회요청 응답 모델"""
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

class RequestToInquiryQuantityAvailableForOrderByCreditDepositRateRequest(BaseModel):
    """[kt00012] 신용보증금율별주문가능수량조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목번호")
    uv: SafeStr = Field(default="", description="매수가격")

class RequestToInquiryQuantityAvailableForOrderByCreditDepositRateResponse(BaseModel):
    """[kt00012] 신용보증금율별주문가능수량조회요청 응답 모델"""
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

class MarginDetailsInquiryRequestRequest(BaseModel):
    """[kt00013] 증거금세부내역조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class MarginDetailsInquiryRequestResponse(BaseModel):
    """[kt00013] 증거금세부내역조회요청 응답 모델"""
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

class RequestForComprehensiveConsignmentTransactionDetailsRequest(BaseModel):
    """[kt00015] 위탁종합거래내역요청 요청 모델"""
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

class RequestForComprehensiveConsignmentTransactionDetailsResponse_TrstOvrlTrdePrpsArray(BaseModel):
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

class RequestForComprehensiveConsignmentTransactionDetailsResponse(BaseModel):
    """[kt00015] 위탁종합거래내역요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trst_ovrl_trde_prps_array: Annotated[List[RequestForComprehensiveConsignmentTransactionDetailsResponse_TrstOvrlTrdePrpsArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="위탁종합거래내역배열")

class RequestForDetailedStatusOfDailyAccountReturnsRequest(BaseModel):
    """[kt00016] 일별계좌수익률상세현황요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    fr_dt: SafeStr = Field(default="", description="평가시작일")
    to_dt: SafeStr = Field(default="", description="평가종료일")

class RequestForDetailedStatusOfDailyAccountReturnsResponse(BaseModel):
    """[kt00016] 일별계좌수익률상세현황요청 응답 모델"""
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

class RequestDailyStatusForEachAccountRequest(BaseModel):
    """[kt00017] 계좌별당일현황요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class RequestDailyStatusForEachAccountResponse(BaseModel):
    """[kt00017] 계좌별당일현황요청 응답 모델"""
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

class RequestForAccountEvaluationBalanceDetailsRequest(BaseModel):
    """[kt00018] 계좌평가잔고내역요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:합산, 2:개별")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드")

class RequestForAccountEvaluationBalanceDetailsResponse_AcntEvltRemnIndvTot(BaseModel):
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

class RequestForAccountEvaluationBalanceDetailsResponse(BaseModel):
    """[kt00018] 계좌평가잔고내역요청 응답 모델"""
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
    acnt_evlt_remn_indv_tot: Annotated[List[RequestForAccountEvaluationBalanceDetailsResponse_AcntEvltRemnIndvTot], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌평가잔고개별합산")

class CheckGoldSpotBalanceRequest(BaseModel):
    """[kt50020] 금현물 잔고확인 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class CheckGoldSpotBalanceResponse_GoldAcntEvltPrst(BaseModel):
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

class CheckGoldSpotBalanceResponse(BaseModel):
    """[kt50020] 금현물 잔고확인 응답 모델"""
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
    gold_acnt_evlt_prst: Annotated[List[CheckGoldSpotBalanceResponse_GoldAcntEvltPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물계좌평가현황")

class GoldSpotDepositRequest(BaseModel):
    """[kt50021] 금현물 예수금 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class GoldSpotDepositResponse(BaseModel):
    """[kt50021] 금현물 예수금 응답 모델"""
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

class ViewAllGoldSpotOrdersRequest(BaseModel):
    """[kt50030] 금현물 주문체결전체조회 요청 모델"""
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

class ViewAllGoldSpotOrdersResponse_AcntOrdCntrPrst(BaseModel):
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

class ViewAllGoldSpotOrdersResponse(BaseModel):
    """[kt50030] 금현물 주문체결전체조회 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_cntr_prst: Annotated[List[ViewAllGoldSpotOrdersResponse_AcntOrdCntrPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결현황")

class GoldSpotOrderExecutionInquiryRequest(BaseModel):
    """[kt50031] 금현물 주문체결조회 요청 모델"""
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

class GoldSpotOrderExecutionInquiryResponse_AcntOrdCntrPrpsDtl(BaseModel):
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

class GoldSpotOrderExecutionInquiryResponse(BaseModel):
    """[kt50031] 금현물 주문체결조회 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_cntr_prps_dtl: Annotated[List[GoldSpotOrderExecutionInquiryResponse_AcntOrdCntrPrpsDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문체결내역상세")

class GoldSpotTransactionHistoryInquiryRequest(BaseModel):
    """[kt50032] 금현물 거래내역조회 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자")
    end_dt: SafeStr = Field(default="", description="종료일자")
    tp: SafeStr = Field(default="", description="구분 0:전체, 1:입출금, 2:출고, 3:매매, 4:매수, 5:매도, 6:입금, 7:출금")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class GoldSpotTransactionHistoryInquiryResponse_GoldTrdeHist(BaseModel):
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

class GoldSpotTransactionHistoryInquiryResponse(BaseModel):
    """[kt50032] 금현물 거래내역조회 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_print: SafeStr = Field(default="", description="계좌번호 계좌번호 출력용")
    gold_trde_hist: Annotated[List[GoldSpotTransactionHistoryInquiryResponse_GoldTrdeHist], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물거래내역")

class GoldSpotNonTradingInquiryRequest(BaseModel):
    """[kt50075] 금현물 미체결조회 요청 모델"""
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

class GoldSpotNonTradingInquiryResponse_AcntOrdOsoPrst(BaseModel):
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

class GoldSpotNonTradingInquiryResponse(BaseModel):
    """[kt50075] 금현물 미체결조회 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    acnt_ord_oso_prst: Annotated[List[GoldSpotNonTradingInquiryResponse_AcntOrdOsoPrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="계좌별주문미체결현황")

class ShortSellingTrendRequestRequest(BaseModel):
    """[ka10014] 공매도추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tm_tp: SafeStr = Field(default="", description="시간구분 0:시작일, 1:기간")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")

class ShortSellingTrendRequestResponse_ShrtsTrnsn(BaseModel):
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

class ShortSellingTrendRequestResponse(BaseModel):
    """[ka10014] 공매도추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    shrts_trnsn: Annotated[List[ShortSellingTrendRequestResponse_ShrtsTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="공매도추이")

class ForeignStockTradingTrendsByItemRequest(BaseModel):
    """[ka10008] 주식외국인종목별매매동향 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class ForeignStockTradingTrendsByItemResponse_StkFrgnr(BaseModel):
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

class ForeignStockTradingTrendsByItemResponse(BaseModel):
    """[ka10008] 주식외국인종목별매매동향 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_frgnr: Annotated[List[ForeignStockTradingTrendsByItemResponse_StkFrgnr], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식외국인")

class StockInstitutionRequestRequest(BaseModel):
    """[ka10009] 주식기관요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockInstitutionRequestResponse(BaseModel):
    """[ka10009] 주식기관요청 응답 모델"""
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

class RequestForStatusOfContinuousTradingByInstitutionalForeignersRequest(BaseModel):
    """[ka10131] 기관외국인연속매매현황요청 요청 모델"""
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

class RequestForStatusOfContinuousTradingByInstitutionalForeignersResponse_OrgnFrgnrContTrdePrst(BaseModel):
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

class RequestForStatusOfContinuousTradingByInstitutionalForeignersResponse(BaseModel):
    """[ka10131] 기관외국인연속매매현황요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    orgn_frgnr_cont_trde_prst: Annotated[List[RequestForStatusOfContinuousTradingByInstitutionalForeignersResponse_OrgnFrgnrContTrdePrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="기관외국인연속매매현황")

class CurrentStatusOfGoldSpotInvestorsRequest(BaseModel):
    """[ka52301] 금현물투자자현황 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class CurrentStatusOfGoldSpotInvestorsResponse_InveTradStat(BaseModel):
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

class CurrentStatusOfGoldSpotInvestorsResponse(BaseModel):
    """[ka52301] 금현물투자자현황 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inve_trad_stat: Annotated[List[CurrentStatusOfGoldSpotInvestorsResponse_InveTradStat], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물투자자현황")

class RequestForLoanLendingTransactionTrendRequest(BaseModel):
    """[ka10068] 대차거래추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    all_tp: SafeStr = Field(default="", description="전체구분 1: 전체표시")

class RequestForLoanLendingTransactionTrendResponse_DbrtTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    dbrt_trde_irds: SafeStr = Field(default="", description="대차거래증감")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class RequestForLoanLendingTransactionTrendResponse(BaseModel):
    """[ka10068] 대차거래추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_trnsn: Annotated[List[RequestForLoanLendingTransactionTrendResponse_DbrtTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래추이")

class RequestForTop10BorrowingStocksRequest(BaseModel):
    """[ka10069] 대차거래상위10종목요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")

class RequestForTop10BorrowingStocksResponse_DbrtTrdeUpper10Stk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class RequestForTop10BorrowingStocksResponse(BaseModel):
    """[ka10069] 대차거래상위10종목요청 응답 모델"""
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
    dbrt_trde_upper_10stk: Annotated[List[RequestForTop10BorrowingStocksResponse_DbrtTrdeUpper10Stk], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래상위10종목")

class RequestForLoanLendingTransactionTrendByItemRequest(BaseModel):
    """[ka20068] 대차거래추이요청(종목별) 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    all_tp: SafeStr = Field(default="", description="전체구분 0:종목코드 입력종목만 표시")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class RequestForLoanLendingTransactionTrendByItemResponse_DbrtTrdeTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    dbrt_trde_irds: SafeStr = Field(default="", description="대차거래증감")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class RequestForLoanLendingTransactionTrendByItemResponse(BaseModel):
    """[ka20068] 대차거래추이요청(종목별) 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_trnsn: Annotated[List[RequestForLoanLendingTransactionTrendByItemResponse_DbrtTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래추이")

class RequestForLoanTransactionDetailsRequest(BaseModel):
    """[ka90012] 대차거래내역요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")

class RequestForLoanTransactionDetailsResponse_DbrtTrdePrps(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_nm: SafeStr = Field(default="", description="종목명")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    dbrt_trde_cntrcnt: SafeStr = Field(default="", description="대차거래체결주수")
    dbrt_trde_rpy: SafeStr = Field(default="", description="대차거래상환주수")
    rmnd: SafeStr = Field(default="", description="잔고주수")
    remn_amt: SafeStr = Field(default="", description="잔고금액")

class RequestForLoanTransactionDetailsResponse(BaseModel):
    """[ka90012] 대차거래내역요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    dbrt_trde_prps: Annotated[List[RequestForLoanTransactionDetailsResponse_DbrtTrdePrps], BeforeValidator(_force_list)] = Field(default_factory=list, description="대차거래내역")

class RequestForHigherQuotaBalanceRequest(BaseModel):
    """[ka10020] 호가잔량상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:순매수잔량순, 2:순매도잔량순, 3:매수비율순, 4:매도비율순")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0000:장시작전(0주이상), 0010:만주이상, 0050:5만주이상, 00100:10만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForHigherQuotaBalanceResponse_BidReqUpper(BaseModel):
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

class RequestForHigherQuotaBalanceResponse(BaseModel):
    """[ka10020] 호가잔량상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    bid_req_upper: Annotated[List[RequestForHigherQuotaBalanceResponse_BidReqUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="호가잔량상위")

class RequestForSuddenIncreaseInQuotationBalanceRequest(BaseModel):
    """[ka10021] 호가잔량급증요청 요청 모델"""
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

class RequestForSuddenIncreaseInQuotationBalanceResponse_BidReqSdnin(BaseModel):
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

class RequestForSuddenIncreaseInQuotationBalanceResponse(BaseModel):
    """[ka10021] 호가잔량급증요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    bid_req_sdnin: Annotated[List[RequestForSuddenIncreaseInQuotationBalanceResponse_BidReqSdnin], BeforeValidator(_force_list)] = Field(default_factory=list, description="호가잔량급증")

class RequestForSuddenIncreaseInRemainingCapacityRequest(BaseModel):
    """[ka10022] 잔량율급증요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    rt_tp: SafeStr = Field(default="", description="비율구분 1:매수/매도비율, 2:매도/매수비율")
    tm_tp: SafeStr = Field(default="", description="시간구분 분 입력")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForSuddenIncreaseInRemainingCapacityResponse_ReqRtSdnin(BaseModel):
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

class RequestForSuddenIncreaseInRemainingCapacityResponse(BaseModel):
    """[ka10022] 잔량율급증요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    req_rt_sdnin: Annotated[List[RequestForSuddenIncreaseInRemainingCapacityResponse_ReqRtSdnin], BeforeValidator(_force_list)] = Field(default_factory=list, description="잔량율급증")

class RequestForSuddenIncreaseInTradingVolumeRequest(BaseModel):
    """[ka10023] 거래량급증요청 요청 모델"""
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

class RequestForSuddenIncreaseInTradingVolumeResponse_TrdeQtySdnin(BaseModel):
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

class RequestForSuddenIncreaseInTradingVolumeResponse(BaseModel):
    """[ka10023] 거래량급증요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_qty_sdnin: Annotated[List[RequestForSuddenIncreaseInTradingVolumeResponse_TrdeQtySdnin], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래량급증")

class RequestForHigherFluctuationRateComparedToThePreviousDayRequest(BaseModel):
    """[ka10027] 전일대비등락률상위요청 요청 모델"""
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

class RequestForHigherFluctuationRateComparedToThePreviousDayResponse_PredPreFluRtUpper(BaseModel):
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

class RequestForHigherFluctuationRateComparedToThePreviousDayResponse(BaseModel):
    """[ka10027] 전일대비등락률상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pred_pre_flu_rt_upper: Annotated[List[RequestForHigherFluctuationRateComparedToThePreviousDayResponse_PredPreFluRtUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="전일대비등락률상위")

class RequestForHigherExpectedTransactionRateRequest(BaseModel):
    """[ka10029] 예상체결등락률상위요청 요청 모델"""
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

class RequestForHigherExpectedTransactionRateResponse_ExpCntrFluRtUpper(BaseModel):
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

class RequestForHigherExpectedTransactionRateResponse(BaseModel):
    """[ka10029] 예상체결등락률상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    exp_cntr_flu_rt_upper: Annotated[List[RequestForHigherExpectedTransactionRateResponse_ExpCntrFluRtUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="예상체결등락률상위")

class HighTransactionVolumeRequestForTheDayRequest(BaseModel):
    """[ka10030] 당일거래량상위요청 요청 모델"""
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

class HighTransactionVolumeRequestForTheDayResponse_TdyTrdeQtyUpper(BaseModel):
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

class HighTransactionVolumeRequestForTheDayResponse(BaseModel):
    """[ka10030] 당일거래량상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_trde_qty_upper: Annotated[List[HighTransactionVolumeRequestForTheDayResponse_TdyTrdeQtyUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일거래량상위")

class RequestForThePreviousDaySHighestTradingVolumeRequest(BaseModel):
    """[ka10031] 전일거래량상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:전일거래량 상위100종목, 2:전일거래대금 상위100종목")
    rank_strt: SafeStr = Field(default="", description="순위시작 0 ~ 100 값 중에  조회를 원하는 순위 시작값")
    rank_end: SafeStr = Field(default="", description="순위끝 0 ~ 100 값 중에  조회를 원하는 순위 끝값")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForThePreviousDaySHighestTradingVolumeResponse_PredTrdeQtyUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")

class RequestForThePreviousDaySHighestTradingVolumeResponse(BaseModel):
    """[ka10031] 전일거래량상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pred_trde_qty_upper: Annotated[List[RequestForThePreviousDaySHighestTradingVolumeResponse_PredTrdeQtyUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="전일거래량상위")

class RequestForHigherTransactionAmountRequest(BaseModel):
    """[ka10032] 거래대금상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    mang_stk_incls: SafeStr = Field(default="", description="관리종목포함 0:관리종목 미포함, 1:관리종목 포함")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForHigherTransactionAmountResponse_TrdePricaUpper(BaseModel):
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

class RequestForHigherTransactionAmountResponse(BaseModel):
    """[ka10032] 거래대금상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_prica_upper: Annotated[List[RequestForHigherTransactionAmountResponse_TrdePricaUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래대금상위")

class RequestForHigherCreditRatioRequest(BaseModel):
    """[ka10033] 신용비율상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체조회, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기")
    updown_incls: SafeStr = Field(default="", description="상하한포함 0:상하한 미포함, 1:상하한포함")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForHigherCreditRatioResponse_CrdRtUpper(BaseModel):
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

class RequestForHigherCreditRatioResponse(BaseModel):
    """[ka10033] 신용비율상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_rt_upper: Annotated[List[RequestForHigherCreditRatioResponse_CrdRtUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="신용비율상위")

class ExternalTransactionTopSalesRequestByPeriodRequest(BaseModel):
    """[ka10034] 외인기간별매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매도, 2:순매수, 3:순매매")
    dt: SafeStr = Field(default="", description="기간 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ExternalTransactionTopSalesRequestByPeriodResponse_ForDtTrdeUpper(BaseModel):
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

class ExternalTransactionTopSalesRequestByPeriodResponse(BaseModel):
    """[ka10034] 외인기간별매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    for_dt_trde_upper: Annotated[List[ExternalTransactionTopSalesRequestByPeriodResponse_ForDtTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외인기간별매매상위")

class ForeignContinuousNetSalesTopRequestRequest(BaseModel):
    """[ka10035] 외인연속순매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:연속순매도, 2:연속순매수")
    base_dt_tp: SafeStr = Field(default="", description="기준일구분 0:당일기준, 1:전일기준")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ForeignContinuousNetSalesTopRequestResponse_ForContNettrdeUpper(BaseModel):
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

class ForeignContinuousNetSalesTopRequestResponse(BaseModel):
    """[ka10035] 외인연속순매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    for_cont_nettrde_upper: Annotated[List[ForeignContinuousNetSalesTopRequestResponse_ForContNettrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외인연속순매매상위")

class TopForeignLimitBurnoutRateIncreaseRequest(BaseModel):
    """[ka10036] 외인한도소진율증가상위 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    dt: SafeStr = Field(default="", description="기간 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class TopForeignLimitBurnoutRateIncreaseResponse_ForLimitExhRtIncrsUpper(BaseModel):
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

class TopForeignLimitBurnoutRateIncreaseResponse(BaseModel):
    """[ka10036] 외인한도소진율증가상위 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    for_limit_exh_rt_incrs_upper: Annotated[List[TopForeignLimitBurnoutRateIncreaseResponse_ForLimitExhRtIncrsUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외인한도소진율증가상위")

class ForeignOverTheCounterSalesRequestRequest(BaseModel):
    """[ka10037] 외국계창구매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    dt: SafeStr = Field(default="", description="기간 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도, 3:매수, 4:매도")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:금액, 2:수량")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ForeignOverTheCounterSalesRequestResponse_FrgnWicketTrdeUpper(BaseModel):
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

class ForeignOverTheCounterSalesRequestResponse(BaseModel):
    """[ka10037] 외국계창구매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    frgn_wicket_trde_upper: Annotated[List[ForeignOverTheCounterSalesRequestResponse_FrgnWicketTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외국계창구매매상위")

class RequestRankingOfSecuritiesCompaniesByStockRequest(BaseModel):
    """[ka10038] 종목별증권사순위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:순매도순위정렬, 2:순매수순위정렬")
    dt: SafeStr = Field(default="", description="기간 1:전일, 4:5일, 9:10일, 19:20일, 39:40일, 59:60일, 119:120일")

class RequestRankingOfSecuritiesCompaniesByStockResponse_StkSecRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    mmcm_nm: SafeStr = Field(default="", description="회원사명")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    acc_netprps_qty: SafeStr = Field(default="", description="누적순매수수량")

class RequestRankingOfSecuritiesCompaniesByStockResponse(BaseModel):
    """[ka10038] 종목별증권사순위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    rank_1: SafeStr = Field(default="", description="순위1")
    rank_2: SafeStr = Field(default="", description="순위2")
    rank_3: SafeStr = Field(default="", description="순위3")
    prid_trde_qty: SafeStr = Field(default="", description="기간중거래량")
    stk_sec_rank: Annotated[List[RequestRankingOfSecuritiesCompaniesByStockResponse_StkSecRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별증권사순위")

class TopTradingRequestBySecuritiesCompanyRequest(BaseModel):
    """[ka10039] 증권사별매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체, 5:5000주, 10:1만주, 50:5만주, 100:10만주, 500:50만주, 1000: 100만주")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    dt: SafeStr = Field(default="", description="기간 1:전일, 5:5일, 10:10일, 60:60일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TopTradingRequestBySecuritiesCompanyResponse_SecTrdeUpper(BaseModel):
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

class TopTradingRequestBySecuritiesCompanyResponse(BaseModel):
    """[ka10039] 증권사별매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sec_trde_upper: Annotated[List[TopTradingRequestBySecuritiesCompanyResponse_SecTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="증권사별매매상위")

class SameDayMajorTransactionRequestRequest(BaseModel):
    """[ka10040] 당일주요거래원요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SameDayMajorTransactionRequestResponse_TdyMainTrdeOri(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sel_scesn_tm: SafeStr = Field(default="", description="매도이탈시간")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    sel_upper_scesn_ori: SafeStr = Field(default="", description="매도상위이탈원")
    buy_scesn_tm: SafeStr = Field(default="", description="매수이탈시간")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    buy_upper_scesn_ori: SafeStr = Field(default="", description="매수상위이탈원")
    qry_dt: SafeStr = Field(default="", description="조회일자")
    qry_tm: SafeStr = Field(default="", description="조회시간")

class SameDayMajorTransactionRequestResponse(BaseModel):
    """[ka10040] 당일주요거래원요청 응답 모델"""
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
    tdy_main_trde_ori: Annotated[List[SameDayMajorTransactionRequestResponse_TdyMainTrdeOri], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일주요거래원")

class NetBuyingTraderRankingRequestRequest(BaseModel):
    """[ka10042] 순매수거래원순위요청 요청 모델"""
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

class NetBuyingTraderRankingRequestResponse_NetprpsTrdeOriRank(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rank: SafeStr = Field(default="", description="순위")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드")
    mmcm_nm: SafeStr = Field(default="", description="회원사명")

class NetBuyingTraderRankingRequestResponse(BaseModel):
    """[ka10042] 순매수거래원순위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    netprps_trde_ori_rank: Annotated[List[NetBuyingTraderRankingRequestResponse_NetprpsTrdeOriRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="순매수거래원순위")

class RequestForSameDayHighWithdrawalRequest(BaseModel):
    """[ka10053] 당일상위이탈원요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class RequestForSameDayHighWithdrawalResponse_TdyUpperScesnOri(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sel_scesn_tm: SafeStr = Field(default="", description="매도이탈시간")
    sell_qty: SafeStr = Field(default="", description="매도수량")
    sel_upper_scesn_ori: SafeStr = Field(default="", description="매도상위이탈원")
    buy_scesn_tm: SafeStr = Field(default="", description="매수이탈시간")
    buy_qty: SafeStr = Field(default="", description="매수수량")
    buy_upper_scesn_ori: SafeStr = Field(default="", description="매수상위이탈원")
    qry_dt: SafeStr = Field(default="", description="조회일자")
    qry_tm: SafeStr = Field(default="", description="조회시간")

class RequestForSameDayHighWithdrawalResponse(BaseModel):
    """[ka10053] 당일상위이탈원요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_upper_scesn_ori: Annotated[List[RequestForSameDayHighWithdrawalResponse_TdyUpperScesnOri], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일상위이탈원")

class RequestForSameNetSalesRankingRequest(BaseModel):
    """[ka10062] 동일순매매순위요청 요청 모델"""
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

class RequestForSameNetSalesRankingResponse_EqlNettrdeRank(BaseModel):
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

class RequestForSameNetSalesRankingResponse(BaseModel):
    """[ka10062] 동일순매매순위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    eql_nettrde_rank: Annotated[List[RequestForSameNetSalesRankingResponse_EqlNettrdeRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="동일순매매순위")

class IntradayTradingRequestByInvestorRequest(BaseModel):
    """[ka10065] 장중투자자별매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    orgn_tp: SafeStr = Field(default="", description="기관구분 9000:외국인, 9100:외국계, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")

class IntradayTradingRequestByInvestorResponse_OpmrInvsrTrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    sel_qty: SafeStr = Field(default="", description="매도량 매도금액/매도량")
    buy_qty: SafeStr = Field(default="", description="매수량 매수금액/매수량")
    netslmt: SafeStr = Field(default="", description="순매도 순매수/순매도(금액/수량)")

class IntradayTradingRequestByInvestorResponse(BaseModel):
    """[ka10065] 장중투자자별매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opmr_invsr_trde_upper: Annotated[List[IntradayTradingRequestByInvestorResponse_OpmrInvsrTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매상위")

class RequestForRankingOfOutOfHoursSinglePriceFluctuationRateRequest(BaseModel):
    """[ka10098] 시간외단일가등락율순위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체,001:코스피,101:코스닥")
    sort_base: SafeStr = Field(default="", description="정렬기준 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합")
    stk_cnd: SafeStr = Field(default="", description="종목조건 0:전체조회,1:관리종목제외,2:정리매매종목제외,3:우선주제외,4:관리종목우선주제외,5:증100제외,6:증100만보기,7:증40만보기,8:증30만보기,9:증20만보기,12:증50만보기,13:증60만보기,14:ETF제외,15:스팩제외,16:ETF+ETN제외,17:ETN제외")
    trde_qty_cnd: SafeStr = Field(default="", description="거래량조건 0:전체조회, 10:백주이상,50:5백주이상,100;천주이상, 500:5천주이상, 1000:만주이상, 5000:5만주이상, 10000:10만주이상")
    crd_cnd: SafeStr = Field(default="", description="신용조건 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 8:신용대주, 5:신용한도초과제외")
    trde_prica: SafeStr = Field(default="", description="거래대금 0:전체조회, 5:5백만원이상,10:1천만원이상, 30:3천만원이상, 50:5천만원이상, 100:1억원이상, 300:3억원이상, 500:5억원이상, 1000:10억원이상, 3000:30억원이상, 5000:50억원이상, 10000:100억원이상")

class RequestForRankingOfOutOfHoursSinglePriceFluctuationRateResponse_OvtSigpricFluRtRank(BaseModel):
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

class RequestForRankingOfOutOfHoursSinglePriceFluctuationRateResponse(BaseModel):
    """[ka10098] 시간외단일가등락율순위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ovt_sigpric_flu_rt_rank: Annotated[List[RequestForRankingOfOutOfHoursSinglePriceFluctuationRateResponse_OvtSigpricFluRtRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="시간외단일가등락율순위")

class ForeignInstitutionalTradingTopRequestRequest(BaseModel):
    """[ka90009] 외국인기관매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액(천만), 2:수량(천)")
    qry_dt_tp: SafeStr = Field(default="", description="조회일자구분 0:조회일자 미포함, 1:조회일자 포함")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD(연도4자리, 월 2자리, 일 2자리 형식)")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class ForeignInstitutionalTradingTopRequestResponse_FrgnrOrgnTrdeUpper(BaseModel):
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

class ForeignInstitutionalTradingTopRequestResponse(BaseModel):
    """[ka90009] 외국인기관매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    frgnr_orgn_trde_upper: Annotated[List[ForeignInstitutionalTradingTopRequestResponse_FrgnrOrgnTrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="외국인기관매매상위")

class StockQuoteRequestRequest(BaseModel):
    """[ka10004] 주식호가요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockQuoteRequestResponse(BaseModel):
    """[ka10004] 주식호가요청 응답 모델"""
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

class StockWeeklyMonthlyAndHourlyMinutesRequestRequest(BaseModel):
    """[ka10005] 주식일주월시분요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockWeeklyMonthlyAndHourlyMinutesRequestResponse_StkDdwkmm(BaseModel):
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

class StockWeeklyMonthlyAndHourlyMinutesRequestResponse(BaseModel):
    """[ka10005] 주식일주월시분요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_ddwkmm: Annotated[List[StockWeeklyMonthlyAndHourlyMinutesRequestResponse_StkDdwkmm], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식일주월시분")

class StockTimeRequestRequest(BaseModel):
    """[ka10006] 주식시분요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockTimeRequestResponse(BaseModel):
    """[ka10006] 주식시분요청 응답 모델"""
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

class RequestForPriceInformationRequest(BaseModel):
    """[ka10007] 시세표성정보요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class RequestForPriceInformationResponse(BaseModel):
    """[ka10007] 시세표성정보요청 응답 모델"""
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

class RequestToViewAllNewStockWarrantsRequest(BaseModel):
    """[ka10011] 신주인수권전체시세요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    newstk_recvrht_tp: SafeStr = Field(default="", description="신주인수권구분 00:전체, 05:신주인수권증권, 07:신주인수권증서")

class RequestToViewAllNewStockWarrantsResponse_NewstkRecvrhtMrpr(BaseModel):
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

class RequestToViewAllNewStockWarrantsResponse(BaseModel):
    """[ka10011] 신주인수권전체시세요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    newstk_recvrht_mrpr: Annotated[List[RequestToViewAllNewStockWarrantsResponse_NewstkRecvrhtMrpr], BeforeValidator(_force_list)] = Field(default_factory=list, description="신주인수권시세")

class RequestForDailyInstitutionalTradingItemsRequest(BaseModel):
    """[ka10044] 일별기관매매종목요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매도, 2:순매수")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForDailyInstitutionalTradingItemsResponse_DalyOrgnTrdeStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    netprps_qty: SafeStr = Field(default="", description="순매수수량")
    netprps_amt: SafeStr = Field(default="", description="순매수금액")

class RequestForDailyInstitutionalTradingItemsResponse(BaseModel):
    """[ka10044] 일별기관매매종목요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_orgn_trde_stk: Annotated[List[RequestForDailyInstitutionalTradingItemsResponse_DalyOrgnTrdeStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별기관매매종목")

class RequestForInstitutionalTradingTrendByItemRequest(BaseModel):
    """[ka10045] 종목별기관매매추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    orgn_prsm_unp_tp: SafeStr = Field(default="", description="기관추정단가구분 1:매수단가, 2:매도단가")
    for_prsm_unp_tp: SafeStr = Field(default="", description="외인추정단가구분 1:매수단가, 2:매도단가")

class RequestForInstitutionalTradingTrendByItemResponse_StkOrgnTrdeTrnsn(BaseModel):
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

class RequestForInstitutionalTradingTrendByItemResponse(BaseModel):
    """[ka10045] 종목별기관매매추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    orgn_prsm_avg_pric: SafeStr = Field(default="", description="기관추정평균가")
    for_prsm_avg_pric: SafeStr = Field(default="", description="외인추정평균가")
    stk_orgn_trde_trnsn: Annotated[List[RequestForInstitutionalTradingTrendByItemResponse_StkOrgnTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별기관매매추이")

class RequestForFasteningStrengthTrendByTimeRequest(BaseModel):
    """[ka10046] 체결강도추이시간별요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class RequestForFasteningStrengthTrendByTimeResponse_CntrStrTm(BaseModel):
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

class RequestForFasteningStrengthTrendByTimeResponse(BaseModel):
    """[ka10046] 체결강도추이시간별요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_str_tm: Annotated[List[RequestForFasteningStrengthTrendByTimeResponse_CntrStrTm], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결강도시간별")

class RequestForDailyTighteningStrengthTrendRequest(BaseModel):
    """[ka10047] 체결강도추이일별요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class RequestForDailyTighteningStrengthTrendResponse_CntrStrDaly(BaseModel):
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

class RequestForDailyTighteningStrengthTrendResponse(BaseModel):
    """[ka10047] 체결강도추이일별요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_str_daly: Annotated[List[RequestForDailyTighteningStrengthTrendResponse_CntrStrDaly], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결강도일별")

class IntradayInvestorSpecificTradingRequestRequest(BaseModel):
    """[ka10063] 장중투자자별매매요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1: 금액&수량")
    invsr: SafeStr = Field(default="", description="투자자별 6:외국인, 7:기관계, 1:투신, 0:보험, 2:은행, 3:연기금, 4:국가, 5:기타법인")
    frgn_all: SafeStr = Field(default="", description="외국계전체 1:체크, 0:미체크")
    smtm_netprps_tp: SafeStr = Field(default="", description="동시순매수구분 1:체크, 0:미체크")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class IntradayInvestorSpecificTradingRequestResponse_OpmrInvsrTrde(BaseModel):
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

class IntradayInvestorSpecificTradingRequestResponse(BaseModel):
    """[ka10063] 장중투자자별매매요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opmr_invsr_trde: Annotated[List[IntradayInvestorSpecificTradingRequestResponse_OpmrInvsrTrde], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매")

class RequestForTradingByInvestorAfterMarketCloseRequest(BaseModel):
    """[ka10066] 장마감후투자자별매매요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForTradingByInvestorAfterMarketCloseResponse_OpafInvsrTrde(BaseModel):
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

class RequestForTradingByInvestorAfterMarketCloseResponse(BaseModel):
    """[ka10066] 장마감후투자자별매매요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opaf_invsr_trde: Annotated[List[RequestForTradingByInvestorAfterMarketCloseResponse_OpafInvsrTrde], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매차트")

class RequestForStockTradingTrendsBySecuritiesCompanyRequest(BaseModel):
    """[ka10078] 증권사별종목매매동향요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")

class RequestForStockTradingTrendsBySecuritiesCompanyResponse_SecStkTrdeTrend(BaseModel):
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

class RequestForStockTradingTrendsBySecuritiesCompanyResponse(BaseModel):
    """[ka10078] 증권사별종목매매동향요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    sec_stk_trde_trend: Annotated[List[RequestForStockTradingTrendsBySecuritiesCompanyResponse_SecStkTrdeTrend], BeforeValidator(_force_list)] = Field(default_factory=list, description="증권사별종목매매동향")

class DailyStockRequestRequest(BaseModel):
    """[ka10086] 일별주가요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    qry_dt: SafeStr = Field(default="", description="조회일자 YYYYMMDD")
    indc_tp: SafeStr = Field(default="", description="표시구분 0:수량, 1:금액(백만원)")

class DailyStockRequestResponse_DalyStkpc(BaseModel):
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

class DailyStockRequestResponse(BaseModel):
    """[ka10086] 일별주가요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_stkpc: Annotated[List[DailyStockRequestResponse_DalyStkpc], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별주가")

class SingleRequestAfterHoursRequest(BaseModel):
    """[ka10087] 시간외단일가요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class SingleRequestAfterHoursResponse(BaseModel):
    """[ka10087] 시간외단일가요청 응답 모델"""
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
    """[ka50010] 금현물체결추이 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")

class GoldSpotTradingTrendResponse_GoldCntr(BaseModel):
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

class GoldSpotTradingTrendResponse(BaseModel):
    """[ka50010] 금현물체결추이 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_cntr: Annotated[List[GoldSpotTradingTrendResponse_GoldCntr], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물체결추이")

class SpotGoldDailyTrendRequest(BaseModel):
    """[ka50012] 금현물일별추이 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class SpotGoldDailyTrendResponse_GoldDalyTrnsn(BaseModel):
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

class SpotGoldDailyTrendResponse(BaseModel):
    """[ka50012] 금현물일별추이 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_daly_trnsn: Annotated[List[SpotGoldDailyTrendResponse_GoldDalyTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일별추이")

class GoldSpotExpectedTransactionRequest(BaseModel):
    """[ka50087] 금현물예상체결 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")

class GoldSpotExpectedTransactionResponse_GoldExptExec(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    exp_cntr_pric: SafeStr = Field(default="", description="예상 체결가")
    exp_pred_pre: SafeStr = Field(default="", description="예상 체결가 전일대비")
    exp_flu_rt: SafeStr = Field(default="", description="예상 체결가 등락율")
    exp_acc_trde_qty: SafeStr = Field(default="", description="예상 체결 수량(누적)")
    exp_cntr_trde_qty: SafeStr = Field(default="", description="예상 체결 수량")
    exp_tm: SafeStr = Field(default="", description="예상 체결 시간")
    exp_pre_sig: SafeStr = Field(default="", description="예상 체결가 전일대비기호")
    stex_tp: SafeStr = Field(default="", description="거래소 구분")

class GoldSpotExpectedTransactionResponse(BaseModel):
    """[ka50087] 금현물예상체결 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_expt_exec: Annotated[List[GoldSpotExpectedTransactionResponse_GoldExptExec], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물예상체결")

class GoldSpotPriceInformationRequest(BaseModel):
    """[ka50100] 금현물 시세정보 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class GoldSpotPriceInformationResponse(BaseModel):
    """[ka50100] 금현물 시세정보 응답 모델"""
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
    """[ka50101] 금현물 호가 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class GoldSpotQuoteResponse_GoldBid(BaseModel):
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

class GoldSpotQuoteResponse(BaseModel):
    """[ka50101] 금현물 호가 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gold_bid: Annotated[List[GoldSpotQuoteResponse_GoldBid], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물호가")

class ProgramTradingTrendRequestByTimeZoneRequest(BaseModel):
    """[ka90005] 프로그램매매추이요청 시간대별 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액(백만원), 2:수량(천주)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01, 3일경우:P001_AL01  코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02, 3일경우:P101_AL02")
    min_tic_tp: SafeStr = Field(default="", description="분틱구분 0:틱, 1:분")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingTrendRequestByTimeZoneResponse_PrmTrdeTrnsn(BaseModel):
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

class ProgramTradingTrendRequestByTimeZoneResponse(BaseModel):
    """[ka90005] 프로그램매매추이요청 시간대별 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_trnsn: Annotated[List[ProgramTradingTrendRequestByTimeZoneResponse_PrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매추이")

class ProgramTradingProfitBalanceTrendRequestRequest(BaseModel):
    """[ka90006] 프로그램매매차익잔고추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingProfitBalanceTrendRequestResponse_PrmTrdeDfrtRemnTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    buy_dfrt_trde_qty: SafeStr = Field(default="", description="매수차익거래수량")
    buy_dfrt_trde_amt: SafeStr = Field(default="", description="매수차익거래금액")
    buy_dfrt_trde_irds_amt: SafeStr = Field(default="", description="매수차익거래증감액")
    sel_dfrt_trde_qty: SafeStr = Field(default="", description="매도차익거래수량")
    sel_dfrt_trde_amt: SafeStr = Field(default="", description="매도차익거래금액")
    sel_dfrt_trde_irds_amt: SafeStr = Field(default="", description="매도차익거래증감액")

class ProgramTradingProfitBalanceTrendRequestResponse(BaseModel):
    """[ka90006] 프로그램매매차익잔고추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_dfrt_remn_trnsn: Annotated[List[ProgramTradingProfitBalanceTrendRequestResponse_PrmTrdeDfrtRemnTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매차익잔고추이")

class RequestForCumulativeProgramTradingTrendRequest(BaseModel):
    """[ka90007] 프로그램매매누적추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD (종료일기준 1년간 데이터만 조회가능)")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피 , 1:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class RequestForCumulativeProgramTradingTrendResponse_PrmTrdeAccTrnsn(BaseModel):
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

class RequestForCumulativeProgramTradingTrendResponse(BaseModel):
    """[ka90007] 프로그램매매누적추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_acc_trnsn: Annotated[List[RequestForCumulativeProgramTradingTrendResponse_PrmTrdeAccTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매누적추이")

class RequestForProgramTradingTrendByItemTimeRequest(BaseModel):
    """[ka90008] 종목시간별프로그램매매추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")

class RequestForProgramTradingTrendByItemTimeResponse_StkTmPrmTrdeTrnsn(BaseModel):
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

class RequestForProgramTradingTrendByItemTimeResponse(BaseModel):
    """[ka90008] 종목시간별프로그램매매추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_tm_prm_trde_trnsn: Annotated[List[RequestForProgramTradingTrendByItemTimeResponse_StkTmPrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목시간별프로그램매매추이")

class ProgramTradingTrendRequestDateRequest(BaseModel):
    """[ka90010] 프로그램매매추이요청 일자별 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액(백만원), 2:수량(천주)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01, 3일경우:P001_AL01  코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02, 3일경우:P001_AL02")
    min_tic_tp: SafeStr = Field(default="", description="분틱구분 0:틱, 1:분")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class ProgramTradingTrendRequestDateResponse_PrmTrdeTrnsn(BaseModel):
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

class ProgramTradingTrendRequestDateResponse(BaseModel):
    """[ka90010] 프로그램매매추이요청 일자별 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_trde_trnsn: Annotated[List[ProgramTradingTrendRequestDateResponse_PrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램매매추이")

class RequestDailyProgramTradingTrendForItemsRequest(BaseModel):
    """[ka90013] 종목일별프로그램매매추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    date: SafeStr = Field(default="", description="날짜 YYYYMMDD")

class RequestDailyProgramTradingTrendForItemsResponse_StkDalyPrmTrdeTrnsn(BaseModel):
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

class RequestDailyProgramTradingTrendForItemsResponse(BaseModel):
    """[ka90013] 종목일별프로그램매매추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_daly_prm_trde_trnsn: Annotated[List[RequestDailyProgramTradingTrendForItemsResponse_StkDalyPrmTrdeTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목일별프로그램매매추이")

class CreditBuyOrderRequest(BaseModel):
    """[kt10006] 신용 매수주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class CreditBuyOrderResponse(BaseModel):
    """[kt10006] 신용 매수주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class CreditSellOrderRequest(BaseModel):
    """[kt10007] 신용 매도주문 요청 모델"""
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

class CreditSellOrderResponse(BaseModel):
    """[kt10007] 신용 매도주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class CreditCorrectionOrderRequest(BaseModel):
    """[kt10008] 신용 정정주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    mdfy_uv: SafeStr = Field(default="", description="정정단가")
    mdfy_cond_uv: SafeStr = Field(default="", description="정정조건단가")

class CreditCorrectionOrderResponse(BaseModel):
    """[kt10008] 신용 정정주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class CreditCancellationOrderRequest(BaseModel):
    """[kt10009] 신용 취소주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    cncl_qty: SafeStr = Field(default="", description="취소수량 '0' 입력시 잔량 전부 취소")

class CreditCancellationOrderResponse(BaseModel):
    """[kt10009] 신용 취소주문 응답 모델"""
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
    """[00] 주문체결 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시  0:기존유지안함 1:기존유지(Default)  0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지  해지(REMOVE)시 값 불필요")
    data: Annotated[List[OrderExecutionRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class OrderExecutionResponse_Data_Values(BaseModel):
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

class OrderExecutionResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[OrderExecutionResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class OrderExecutionResponse(BaseModel):
    """[00] 주문체결 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[OrderExecutionResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class BalanceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class BalanceRequest(BaseModel):
    """[04] 잔고 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시   0:기존유지안함 1:기존유지(Default)  0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지  해지(REMOVE)시 값 불필요")
    data: Annotated[List[BalanceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class BalanceResponse_Data_Values(BaseModel):
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

class BalanceResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[BalanceResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class BalanceResponse(BaseModel):
    """[04] 잔고 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[BalanceResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockMomentumRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockMomentumRequest(BaseModel):
    """[0A] 주식기세 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시  0:기존유지안함 1:기존유지(Default)  0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지  해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockMomentumRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockMomentumResponse_Data_Values(BaseModel):
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

class StockMomentumResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockMomentumResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockMomentumResponse(BaseModel):
    """[0A] 주식기세 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지(등록,해지시에만 값 전송,데이터 실시간 수신시 미전송)")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockMomentumResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockSigningRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockSigningRequest(BaseModel):
    """[0B] 주식체결 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockSigningRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockSigningResponse_Data_Values(BaseModel):
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

class StockSigningResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0B,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockSigningResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockSigningResponse(BaseModel):
    """[0B] 주식체결 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockSigningResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockPreferredPriceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockPreferredPriceRequest(BaseModel):
    """[0C] 주식우선호가 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockPreferredPriceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockPreferredPriceResponse_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_27: SafeStr = Field(default="", alias="27", description="(최우선)매도호가")
    n_28: SafeStr = Field(default="", alias="28", description="(최우선)매수호가")

class StockPreferredPriceResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockPreferredPriceResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockPreferredPriceResponse(BaseModel):
    """[0C] 주식우선호가 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockPreferredPriceResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockQuoteBalanceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockQuoteBalanceRequest(BaseModel):
    """[0D] 주식호가잔량 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockQuoteBalanceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockQuoteBalanceResponse_Data_Values(BaseModel):
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

class StockQuoteBalanceResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockQuoteBalanceResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockQuoteBalanceResponse(BaseModel):
    """[0D] 주식호가잔량 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockQuoteBalanceResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockAfterHoursQuoteRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockAfterHoursQuoteRequest(BaseModel):
    """[0E] 주식시간외호가 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockAfterHoursQuoteRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockAfterHoursQuoteResponse_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_21: SafeStr = Field(default="", alias="21", description="호가시간")
    n_131: SafeStr = Field(default="", alias="131", description="시간외매도호가총잔량")
    n_132: SafeStr = Field(default="", alias="132", description="시간외매도호가총잔량직전대비")
    n_135: SafeStr = Field(default="", alias="135", description="시간외매수호가총잔량")
    n_136: SafeStr = Field(default="", alias="136", description="시간외매수호가총잔량직전대비")

class StockAfterHoursQuoteResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 거래소별 종목코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    values: Annotated[List[StockAfterHoursQuoteResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockAfterHoursQuoteResponse(BaseModel):
    """[0E] 주식시간외호가 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockAfterHoursQuoteResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockDayTraderRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockDayTraderRequest(BaseModel):
    """[0F] 주식당일거래원 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockDayTraderRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockDayTraderResponse_Data_Values(BaseModel):
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

class StockDayTraderResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockDayTraderResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockDayTraderResponse(BaseModel):
    """[0F] 주식당일거래원 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockDayTraderResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class EtfNavRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class EtfNavRequest(BaseModel):
    """[0G] ETF NAV 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[EtfNavRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class EtfNavResponse_Data_Values(BaseModel):
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

class EtfNavResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[EtfNavResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class EtfNavResponse(BaseModel):
    """[0G] ETF NAV 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[EtfNavResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockExpectedExecutionRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockExpectedExecutionRequest(BaseModel):
    """[0H] 주식예상체결 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockExpectedExecutionRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockExpectedExecutionResponse_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")
    n_15: SafeStr = Field(default="", alias="15", description="거래량 +는 매수체결, -는 매도체결")
    n_13: SafeStr = Field(default="", alias="13", description="누적거래량")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호")

class StockExpectedExecutionResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockExpectedExecutionResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockExpectedExecutionResponse(BaseModel):
    """[0H] 주식예상체결 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockExpectedExecutionResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class InternationalGoldConversionPriceRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 MGD: 원/g, MGU: $/온스,소수점2자리")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class InternationalGoldConversionPriceRequest(BaseModel):
    """[0I] 국제금환산가격 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[InternationalGoldConversionPriceRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class InternationalGoldConversionPriceResponse_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_10: SafeStr = Field(default="", alias="10", description="현재가")
    n_25: SafeStr = Field(default="", alias="25", description="전일대비기호 1:상한, 2:상승, 3:없음, 4:하한, 5:하락")
    n_11: SafeStr = Field(default="", alias="11", description="전일대비")
    n_12: SafeStr = Field(default="", alias="12", description="등락율")

class InternationalGoldConversionPriceResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0B,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[InternationalGoldConversionPriceResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class InternationalGoldConversionPriceResponse(BaseModel):
    """[0I] 국제금환산가격 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[InternationalGoldConversionPriceResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class SectorIndexRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class SectorIndexRequest(BaseModel):
    """[0J] 업종지수 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[SectorIndexRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class SectorIndexResponse_Data_Values(BaseModel):
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

class SectorIndexResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[SectorIndexResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class SectorIndexResponse(BaseModel):
    """[0J] 업종지수 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[SectorIndexResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class IndustryFluctuationsRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class IndustryFluctuationsRequest(BaseModel):
    """[0U] 업종등락 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[IndustryFluctuationsRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class IndustryFluctuationsResponse_Data_Values(BaseModel):
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

class IndustryFluctuationsResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[IndustryFluctuationsResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class IndustryFluctuationsResponse(BaseModel):
    """[0U] 업종등락 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[IndustryFluctuationsResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockItemInformationRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockItemInformationRequest(BaseModel):
    """[0g] 주식종목정보 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockItemInformationRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockItemInformationResponse_Data_Values(BaseModel):
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

class StockItemInformationResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockItemInformationResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockItemInformationResponse(BaseModel):
    """[0g] 주식종목정보 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockItemInformationResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class ElwTheoristRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class ElwTheoristRequest(BaseModel):
    """[0m] ELW 이론가 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[ElwTheoristRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class ElwTheoristResponse_Data_Values(BaseModel):
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

class ElwTheoristResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[ElwTheoristResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class ElwTheoristResponse(BaseModel):
    """[0m] ELW 이론가 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[ElwTheoristResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class LongStartTimeRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class LongStartTimeRequest(BaseModel):
    """[0s] 장시작시간 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[LongStartTimeRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class LongStartTimeResponse_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_215: SafeStr = Field(default="", alias="215", description="장운영구분 0 : 장시작전 알림(8:40~),  3 : 장시작(09:00),  2 : 장마감 알림(15:20~),  4 : 장마감(15:30),  8 : 정규장마감(거래소 수신시 15:30 이후),  9 : 전체장마감(거래소 수신시 18:00 이후),  a : 시간외 종가매매 시작(15:40),  b : 시간외 종가매매 종료(16:00),  c : 시간외 단일가 시작(16:00),  d : 시간외 단일가 종료(18:00),  e : 선옵 장마감전 동시호가 종료,  f : 선물옵션 장운영시간 알림(조기개장 상품),  o : 선옵 장시작,  s : 선옵 장마감전 동시호가 시작,  P : NXT 프리마켓 시작 알림,  Q : NXT 프리마켓 종료 알림,  R : NXT 메인마켓 시작 알림,  S : NXT 메인마켓 종료 알림,  T : NXT 에프터마켓 단일가 시작 알림,  U : NXT 에프터마켓 시작 알림,  V : NXT 에프터마켓 종료 알림")
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_214: SafeStr = Field(default="", alias="214", description="장시작예상잔여시간")

class LongStartTimeResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[LongStartTimeResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class LongStartTimeResponse(BaseModel):
    """[0s] 장시작시간 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[LongStartTimeResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class ElwIndicatorRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class ElwIndicatorRequest(BaseModel):
    """[0u] ELW 지표 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[ElwIndicatorRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class ElwIndicatorResponse_Data_Values(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    n_20: SafeStr = Field(default="", alias="20", description="체결시간")
    n_666: SafeStr = Field(default="", alias="666", description="ELW패리티")
    n_1211: SafeStr = Field(default="", alias="1211", description="ELW프리미엄")
    n_667: SafeStr = Field(default="", alias="667", description="ELW기어링비율")
    n_668: SafeStr = Field(default="", alias="668", description="ELW손익분기율")
    n_669: SafeStr = Field(default="", alias="669", description="ELW자본지지점")

class ElwIndicatorResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[ElwIndicatorResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class ElwIndicatorResponse(BaseModel):
    """[0u] ELW 지표 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[ElwIndicatorResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class StockProgramTradingRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class StockProgramTradingRequest(BaseModel):
    """[0w] 종목프로그램매매 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[StockProgramTradingRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class StockProgramTradingResponse_Data_Values(BaseModel):
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

class StockProgramTradingResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[StockProgramTradingResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class StockProgramTradingResponse(BaseModel):
    """[0w] 종목프로그램매매 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[StockProgramTradingResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class ActivateDisableViRequest_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    item: SafeListStr = Field(default_factory=list, description="실시간 등록 요소 거래소별 종목코드, 업종코드  (KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    type: SafeListStr = Field(default_factory=list, description="실시간 항목 TR 명(0A,0B....)")

class ActivateDisableViRequest(BaseModel):
    """[1h] VI발동/해제 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 REG : 등록 , REMOVE : 해지")
    grp_no: SafeStr = Field(default="", description="그룹번호")
    refresh: SafeStr = Field(default="", description="기존등록유지여부 등록(REG)시0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지해지(REMOVE)시 값 불필요")
    data: Annotated[List[ActivateDisableViRequest_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록 리스트")

class ActivateDisableViResponse_Data_Values(BaseModel):
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

class ActivateDisableViResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: SafeStr = Field(default="", description="실시간항목 TR 명(0A,0B....)")
    name: SafeStr = Field(default="", description="실시간 항목명")
    item: SafeStr = Field(default="", description="실시간 등록 요소 종목코드")
    values: Annotated[List[ActivateDisableViResponse_Data_Values], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 값 리스트")

class ActivateDisableViResponse(BaseModel):
    """[1h] VI발동/해제 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 통신결과에대한 코드(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송)")
    return_msg: SafeStr = Field(default="", description="결과메시지 통신결과에대한메시지")
    trnm: SafeStr = Field(default="", description="서비스명 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환")
    data: Annotated[List[ActivateDisableViResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간 등록리스트")

class IndustryProgramRequestRequest(BaseModel):
    """[ka10010] 업종프로그램요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class IndustryProgramRequestResponse(BaseModel):
    """[ka10010] 업종프로그램요청 응답 모델"""
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

class InvestorNetPurchaseRequestByIndustryRequest(BaseModel):
    """[ka10051] 업종별투자자순매수요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 코스피:0, 코스닥:1")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 금액:0, 수량:1")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class InvestorNetPurchaseRequestByIndustryResponse_IndsNetprps(BaseModel):
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

class InvestorNetPurchaseRequestByIndustryResponse(BaseModel):
    """[ka10051] 업종별투자자순매수요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_netprps: Annotated[List[InvestorNetPurchaseRequestByIndustryResponse_IndsNetprps], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종별순매수")

class CurrentIndustryRequestRequest(BaseModel):
    """[ka20001] 업종현재가요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피, 1:코스닥, 2:코스피200")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")

class CurrentIndustryRequestResponse_IndsCurPrcTm(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tm_n: SafeStr = Field(default="", description="시간n")
    cur_prc_n: SafeStr = Field(default="", description="현재가n")
    pred_pre_sig_n: SafeStr = Field(default="", description="전일대비기호n")
    pred_pre_n: SafeStr = Field(default="", description="전일대비n")
    flu_rt_n: SafeStr = Field(default="", description="등락률n")
    trde_qty_n: SafeStr = Field(default="", description="거래량n")
    acc_trde_qty_n: SafeStr = Field(default="", description="누적거래량n")

class CurrentIndustryRequestResponse(BaseModel):
    """[ka20001] 업종현재가요청 응답 모델"""
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
    inds_cur_prc_tm: Annotated[List[CurrentIndustryRequestResponse_IndsCurPrcTm], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종현재가_시간별")

class RequestForStocksByIndustryRequest(BaseModel):
    """[ka20002] 업종별주가요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피, 1:코스닥, 2:코스피200")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class RequestForStocksByIndustryResponse_IndsStkpc(BaseModel):
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

class RequestForStocksByIndustryResponse(BaseModel):
    """[ka20002] 업종별주가요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_stkpc: Annotated[List[RequestForStocksByIndustryResponse_IndsStkpc], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종별주가")

class RequestForAllIndustryIndicesRequest(BaseModel):
    """[ka20003] 전업종지수요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 101:종합(KOSDAQ)")

class RequestForAllIndustryIndicesResponse_AllIndsIdex(BaseModel):
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

class RequestForAllIndustryIndicesResponse(BaseModel):
    """[ka20003] 전업종지수요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    all_inds_idex: Annotated[List[RequestForAllIndustryIndicesResponse_AllIndsIdex], BeforeValidator(_force_list)] = Field(default_factory=list, description="전업종지수")

class IndustryCurrentPriceDailyRequestRequest(BaseModel):
    """[ka20009] 업종현재가일별요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피, 1:코스닥, 2:코스피200")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")

class IndustryCurrentPriceDailyRequestResponse_IndsCurPrcDalyRept(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt_n: SafeStr = Field(default="", description="일자n")
    cur_prc_n: SafeStr = Field(default="", description="현재가n")
    pred_pre_sig_n: SafeStr = Field(default="", description="전일대비기호n")
    pred_pre_n: SafeStr = Field(default="", description="전일대비n")
    flu_rt_n: SafeStr = Field(default="", description="등락률n")
    acc_trde_qty_n: SafeStr = Field(default="", description="누적거래량n")

class IndustryCurrentPriceDailyRequestResponse(BaseModel):
    """[ka20009] 업종현재가일별요청 응답 모델"""
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
    inds_cur_prc_daly_rept: Annotated[List[IndustryCurrentPriceDailyRequestResponse_IndsCurPrcDalyRept], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종현재가_일별반복")

class ConditionSearchListInquiryRequest(BaseModel):
    """[ka10171] 조건검색 목록조회 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="TR명 CNSRLST고정값")

class ConditionSearchListInquiryResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    name: SafeStr = Field(default="", description="조건검색식 명")

class ConditionSearchListInquiryResponse(BaseModel):
    """[ka10171] 조건검색 목록조회 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상 : 0")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRLST 고정값")
    data: Annotated[List[ConditionSearchListInquiryResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="조건검색식 목록")

class ConditionalSearchRequestGeneralRequest(BaseModel):
    """[ka10172] 조건검색 요청 일반 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    search_type: SafeStr = Field(default="", description="조회타입 0:조건검색")
    stex_tp: SafeStr = Field(default="", description="거래소구분 K:KRX")
    cont_yn: SafeStr = Field(default="", description="연속조회여부 Y:연속조회요청,N:연속조회미요청")
    next_key: SafeStr = Field(default="", description="연속조회키")

class ConditionalSearchRequestGeneralResponse_Data(BaseModel):
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

class ConditionalSearchRequestGeneralResponse(BaseModel):
    """[ka10172] 조건검색 요청 일반 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상:0 나머지:에러")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    cont_yn: SafeStr = Field(default="", description="연속조회여부 연속 데이터가 존재하는경우 Y, 없으면 N")
    next_key: SafeStr = Field(default="", description="연속조회키 연속조회여부가Y일경우 다음 조회시 필요한 조회값")
    data: Annotated[List[ConditionalSearchRequestGeneralResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="검색결과데이터")

class RealTimeConditionalSearchRequestRequest(BaseModel):
    """[ka10173] 조건검색 요청 실시간 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    search_type: SafeStr = Field(default="", description="조회타입 1: 조건검색+실시간조건검색")
    stex_tp: SafeStr = Field(default="", description="거래소구분 K:KRX")

class RealTimeConditionalSearchRequestResponse_Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    jmcode: SafeStr = Field(default="", description="종목코드")

class RealTimeConditionalSearchRequestResponse(BaseModel):
    """[ka10173] 조건검색 요청 실시간 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상:0 나머지:에러")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRREQ")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")
    data: Annotated[List[RealTimeConditionalSearchRequestResponse_Data], BeforeValidator(_force_list)] = Field(default_factory=list, description="검색결과데이터")

class ConditionalSearchRealTimeCancellationRequest(BaseModel):
    """[ka10174] 조건검색 실시간 해제 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    trnm: SafeStr = Field(default="", description="서비스명 CNSRCLR 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")

class ConditionalSearchRealTimeCancellationResponse(BaseModel):
    """[ka10174] 조건검색 실시간 해제 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    return_code: SafeInt = Field(default=0, description="결과코드 정상:0 나머지:에러")
    return_msg: SafeStr = Field(default="", description="결과메시지 정상인 경우는 메시지 없음")
    trnm: SafeStr = Field(default="", description="서비스명 CNSRCLR 고정값")
    seq: SafeStr = Field(default="", description="조건검색식 일련번호")

class RealTimeItemInquiryRankingRequest(BaseModel):
    """[ka00198] 실시간종목조회순위 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="구분 1:1분, 2:10분, 3:1시간, 4:당일 누적, 5:30초")

class RealTimeItemInquiryRankingResponse_ItemInqRank(BaseModel):
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

class RealTimeItemInquiryRankingResponse(BaseModel):
    """[ka00198] 실시간종목조회순위 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    item_inq_rank: Annotated[List[RealTimeItemInquiryRankingResponse_ItemInqRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="실시간종목조회순위")

class RequestForBasicStockInformationRequest(BaseModel):
    """[ka10001] 주식기본정보요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class RequestForBasicStockInformationResponse(BaseModel):
    """[ka10001] 주식기본정보요청 응답 모델"""
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

class StockExchangeRequestRequest(BaseModel):
    """[ka10002] 주식거래원요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class StockExchangeRequestResponse(BaseModel):
    """[ka10002] 주식거래원요청 응답 모델"""
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

class RequestForConclusionInformationRequest(BaseModel):
    """[ka10003] 체결정보요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class RequestForConclusionInformationResponse_CntrInfr(BaseModel):
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

class RequestForConclusionInformationResponse(BaseModel):
    """[ka10003] 체결정보요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_infr: Annotated[List[RequestForConclusionInformationResponse_CntrInfr], BeforeValidator(_force_list)] = Field(default_factory=list, description="체결정보")

class CreditTradingTrendRequestRequest(BaseModel):
    """[ka10013] 신용매매동향요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    qry_tp: SafeStr = Field(default="", description="조회구분 1:융자, 2:대주")

class CreditTradingTrendRequestResponse_CrdTrdeTrend(BaseModel):
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

class CreditTradingTrendRequestResponse(BaseModel):
    """[ka10013] 신용매매동향요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_trde_trend: Annotated[List[CreditTradingTrendRequestResponse_CrdTrdeTrend], BeforeValidator(_force_list)] = Field(default_factory=list, description="신용매매동향")

class DailyTransactionRequestRequest(BaseModel):
    """[ka10015] 일별거래상세요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")

class DailyTransactionRequestResponse_DalyTrdeDtl(BaseModel):
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

class DailyTransactionRequestResponse(BaseModel):
    """[ka10015] 일별거래상세요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    daly_trde_dtl: Annotated[List[DailyTransactionRequestResponse_DalyTrdeDtl], BeforeValidator(_force_list)] = Field(default_factory=list, description="일별거래상세")

class RequestForLowReportRequest(BaseModel):
    """[ka10016] 신고저가요청 요청 모델"""
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

class RequestForLowReportResponse_NtlPric(BaseModel):
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

class RequestForLowReportResponse(BaseModel):
    """[ka10016] 신고저가요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ntl_pric: Annotated[List[RequestForLowReportResponse_NtlPric], BeforeValidator(_force_list)] = Field(default_factory=list, description="신고저가")

class RequestForUpperAndLowerLimitsRequest(BaseModel):
    """[ka10017] 상하한가요청 요청 모델"""
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

class RequestForUpperAndLowerLimitsResponse_UpdownPric(BaseModel):
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

class RequestForUpperAndLowerLimitsResponse(BaseModel):
    """[ka10017] 상하한가요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    updown_pric: Annotated[List[RequestForUpperAndLowerLimitsResponse_UpdownPric], BeforeValidator(_force_list)] = Field(default_factory=list, description="상하한가")

class HighAndLowPriceProximityRequestRequest(BaseModel):
    """[ka10018] 고저가근접요청 요청 모델"""
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

class HighAndLowPriceProximityRequestResponse_HighLowPricAlacc(BaseModel):
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

class HighAndLowPriceProximityRequestResponse(BaseModel):
    """[ka10018] 고저가근접요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    high_low_pric_alacc: Annotated[List[HighAndLowPriceProximityRequestResponse_HighLowPricAlacc], BeforeValidator(_force_list)] = Field(default_factory=list, description="고저가근접")

class RequestForSuddenPriceFluctuationRequest(BaseModel):
    """[ka10019] 가격급등락요청 요청 모델"""
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

class RequestForSuddenPriceFluctuationResponse_PricJmpflu(BaseModel):
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

class RequestForSuddenPriceFluctuationResponse(BaseModel):
    """[ka10019] 가격급등락요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    pric_jmpflu: Annotated[List[RequestForSuddenPriceFluctuationResponse_PricJmpflu], BeforeValidator(_force_list)] = Field(default_factory=list, description="가격급등락")

class TransactionVolumeUpdateRequestRequest(BaseModel):
    """[ka10024] 거래량갱신요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    cycle_tp: SafeStr = Field(default="", description="주기구분 5:5일, 10:10일, 20:20일, 60:60일, 250:250일")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TransactionVolumeUpdateRequestResponse_TrdeQtyUpdt(BaseModel):
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

class TransactionVolumeUpdateRequestResponse(BaseModel):
    """[ka10024] 거래량갱신요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_qty_updt: Annotated[List[TransactionVolumeUpdateRequestResponse_TrdeQtyUpdt], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래량갱신")

class RequestForConcentrationOfPropertiesForSaleRequest(BaseModel):
    """[ka10025] 매물대집중요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    prps_cnctr_rt: SafeStr = Field(default="", description="매물집중비율 0~100 입력")
    cur_prc_entry: SafeStr = Field(default="", description="현재가진입 0:현재가 매물대 진입 포함안함, 1:현재가 매물대 진입포함")
    prpscnt: SafeStr = Field(default="", description="매물대수 숫자입력")
    cycle_tp: SafeStr = Field(default="", description="주기구분 50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForConcentrationOfPropertiesForSaleResponse_PrpsCnctr(BaseModel):
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

class RequestForConcentrationOfPropertiesForSaleResponse(BaseModel):
    """[ka10025] 매물대집중요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prps_cnctr: Annotated[List[RequestForConcentrationOfPropertiesForSaleResponse_PrpsCnctr], BeforeValidator(_force_list)] = Field(default_factory=list, description="매물대집중")

class RequestForHighAndLowPerRequest(BaseModel):
    """[ka10026] 고저PER요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    pertp: SafeStr = Field(default="", description="PER구분 1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForHighAndLowPerResponse_HighLowPer(BaseModel):
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

class RequestForHighAndLowPerResponse(BaseModel):
    """[ka10026] 고저PER요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    high_low_per: Annotated[List[RequestForHighAndLowPerResponse_HighLowPer], BeforeValidator(_force_list)] = Field(default_factory=list, description="고저PER")

class RequestForFluctuationRateComparedToMarketPriceRequest(BaseModel):
    """[ka10028] 시가대비등락률요청 요청 모델"""
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

class RequestForFluctuationRateComparedToMarketPriceResponse_OpenPricPreFluRt(BaseModel):
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

class RequestForFluctuationRateComparedToMarketPriceResponse(BaseModel):
    """[ka10028] 시가대비등락률요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    open_pric_pre_flu_rt: Annotated[List[RequestForFluctuationRateComparedToMarketPriceResponse_OpenPricPreFluRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="시가대비등락률")

class RequestForTransactionPriceAnalysisRequest(BaseModel):
    """[ka10043] 거래원매물대분석요청 요청 모델"""
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

class RequestForTransactionPriceAnalysisResponse_TrdeOriPrpsAnly(BaseModel):
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

class RequestForTransactionPriceAnalysisResponse(BaseModel):
    """[ka10043] 거래원매물대분석요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_ori_prps_anly: Annotated[List[RequestForTransactionPriceAnalysisResponse_TrdeOriPrpsAnly], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래원매물대분석")

class TraderInstantaneousTradingVolumeRequestRequest(BaseModel):
    """[ka10052] 거래원순간거래량요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mmcm_cd: SafeStr = Field(default="", description="회원사코드 회원사 코드는 ka10102 조회")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:전체, 1:코스피, 2:코스닥, 3:종목")
    qty_tp: SafeStr = Field(default="", description="수량구분 0:전체, 1:1000주, 2:2000주, 3:, 5:, 10:10000주, 30: 30000주, 50: 50000주, 100: 100000주")
    pric_tp: SafeStr = Field(default="", description="가격구분 0:전체, 1:1천원 미만, 8:1천원 이상, 2:1천원 ~ 2천원, 3:2천원 ~ 5천원, 4:5천원 ~ 1만원, 5:1만원 이상")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class TraderInstantaneousTradingVolumeRequestResponse_TrdeOriMontTrdeQty(BaseModel):
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

class TraderInstantaneousTradingVolumeRequestResponse(BaseModel):
    """[ka10052] 거래원순간거래량요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_ori_mont_trde_qty: Annotated[List[TraderInstantaneousTradingVolumeRequestResponse_TrdeOriMontTrdeQty], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래원순간거래량")

class RequestForItemsToActivateVolatilityMitigationDeviceRequest(BaseModel):
    """[ka10054] 변동성완화장치발동종목요청 요청 모델"""
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

class RequestForItemsToActivateVolatilityMitigationDeviceResponse_MotnStk(BaseModel):
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

class RequestForItemsToActivateVolatilityMitigationDeviceResponse(BaseModel):
    """[ka10054] 변동성완화장치발동종목요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    motn_stk: Annotated[List[RequestForItemsToActivateVolatilityMitigationDeviceResponse_MotnStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="발동종목")

class RequestForSettlementTheDayBeforeTheDayRequest(BaseModel):
    """[ka10055] 당일전일체결량요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tdy_pred: SafeStr = Field(default="", description="당일전일 1:당일, 2:전일")

class RequestForSettlementTheDayBeforeTheDayResponse_TdyPredCntrQty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cntr_pric: SafeStr = Field(default="", description="체결가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    cntr_qty: SafeStr = Field(default="", description="체결량")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적거래대금")

class RequestForSettlementTheDayBeforeTheDayResponse(BaseModel):
    """[ka10055] 당일전일체결량요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_pred_cntr_qty: Annotated[List[RequestForSettlementTheDayBeforeTheDayResponse_TdyPredCntrQty], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일전일체결량")

class RequestForDailyTradingItemsByInvestorRequest(BaseModel):
    """[ka10058] 투자자별일별매매종목요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    trde_tp: SafeStr = Field(default="", description="매매구분 순매도:1, 순매수:2")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 001:코스피, 101:코스닥")
    invsr_tp: SafeStr = Field(default="", description="투자자구분 8000:개인, 9000:외국인, 1000:금융투자, 3000:투신, 3100:사모펀드, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForDailyTradingItemsByInvestorResponse_InvsrDalyTrdeStk(BaseModel):
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

class RequestForDailyTradingItemsByInvestorResponse(BaseModel):
    """[ka10058] 투자자별일별매매종목요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    invsr_daly_trde_stk: Annotated[List[RequestForDailyTradingItemsByInvestorResponse_InvsrDalyTrdeStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="투자자별일별매매종목")

class RequestsByItemAndInvestorInstitutionRequest(BaseModel):
    """[ka10059] 종목별투자자기관별요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    unit_tp: SafeStr = Field(default="", description="단위구분 1000:천주, 1:단주")

class RequestsByItemAndInvestorInstitutionResponse_StkInvsrOrgn(BaseModel):
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

class RequestsByItemAndInvestorInstitutionResponse(BaseModel):
    """[ka10059] 종목별투자자기관별요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_invsr_orgn: Annotated[List[RequestsByItemAndInvestorInstitutionResponse_StkInvsrOrgn], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별투자자기관별")

class TotalRequestByItemAndInvestorInstitutionRequest(BaseModel):
    """[ka10061] 종목별투자자기관별합계요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    strt_dt: SafeStr = Field(default="", description="시작일자 YYYYMMDD")
    end_dt: SafeStr = Field(default="", description="종료일자 YYYYMMDD")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수")
    unit_tp: SafeStr = Field(default="", description="단위구분 1000:천주, 1:단주")

class TotalRequestByItemAndInvestorInstitutionResponse_StkInvsrOrgnTot(BaseModel):
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

class TotalRequestByItemAndInvestorInstitutionResponse(BaseModel):
    """[ka10061] 종목별투자자기관별합계요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_invsr_orgn_tot: Annotated[List[TotalRequestByItemAndInvestorInstitutionResponse_StkInvsrOrgnTot], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별투자자기관별합계")

class RequestForSettlementTheDayBeforeTheSameDayRequest(BaseModel):
    """[ka10084] 당일전일체결요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tdy_pred: SafeStr = Field(default="", description="당일전일 당일 : 1, 전일 : 2")
    tic_min: SafeStr = Field(default="", description="틱분 0:틱, 1:분")
    tm: SafeStr = Field(default="", description="시간 조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430")

class RequestForSettlementTheDayBeforeTheSameDayResponse_TdyPredCntr(BaseModel):
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

class RequestForSettlementTheDayBeforeTheSameDayResponse(BaseModel):
    """[ka10084] 당일전일체결요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tdy_pred_cntr: Annotated[List[RequestForSettlementTheDayBeforeTheSameDayResponse_TdyPredCntr], BeforeValidator(_force_list)] = Field(default_factory=list, description="당일전일체결")

class RequestInformationOnItemsOfInterestRequest(BaseModel):
    """[ka10095] 관심종목정보요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)여러개의 종목코드 입력시 | 로 구분")

class RequestInformationOnItemsOfInterestResponse_AtnStkInfr(BaseModel):
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

class RequestInformationOnItemsOfInterestResponse(BaseModel):
    """[ka10095] 관심종목정보요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    atn_stk_infr: Annotated[List[RequestInformationOnItemsOfInterestResponse_AtnStkInfr], BeforeValidator(_force_list)] = Field(default_factory=list, description="관심종목정보")

class StockInformationListRequest(BaseModel):
    """[ka10099] 종목정보 리스트 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0 : 코스피,  10 : 코스닥,  30 : K-OTC,  50 : 코넥스,  60 : ETN,  70 : 손실제한 ETN,  80 : 금현물,  90 : 변동성 ETN,  2 : 인프라투융자,  3 : ELW,  4 : 뮤추얼펀드,  5 : 신주인수권,  6 : 리츠종목,  7 : 신주인수권증서,  8 : ETF,  9 : 하이일드펀드")

class StockInformationListResponse_List(BaseModel):
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

class StockInformationListResponse(BaseModel):
    """[ka10099] 종목정보 리스트 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    list: Annotated[List[StockInformationListResponse_List], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목리스트")

class CheckStockInformationRequest(BaseModel):
    """[ka10100] 종목정보 조회 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class CheckStockInformationResponse(BaseModel):
    """[ka10100] 종목정보 조회 응답 모델"""
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
    """[ka10101] 업종코드 리스트 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 0:코스피(거래소),1:코스닥,2:KOSPI200,4:KOSPI100,7:KRX100(통합지수)")

class IndustryCodeListResponse_List(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    marketCode: SafeStr = Field(default="", description="시장구분코드")
    code: SafeStr = Field(default="", description="코드")
    name: SafeStr = Field(default="", description="업종명")
    group: SafeStr = Field(default="", description="그룹")

class IndustryCodeListResponse(BaseModel):
    """[ka10101] 업종코드 리스트 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    list: Annotated[List[IndustryCodeListResponse_List], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종코드리스트")

class MemberCompanyListRequest(BaseModel):
    """[ka10102] 회원사 리스트 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")

class MemberCompanyListResponse_List(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    code: SafeStr = Field(default="", description="코드")
    name: SafeStr = Field(default="", description="업종명")
    gb: SafeStr = Field(default="", description="구분")

class MemberCompanyListResponse(BaseModel):
    """[ka10102] 회원사 리스트 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    list: Annotated[List[MemberCompanyListResponse_List], BeforeValidator(_force_list)] = Field(default_factory=list, description="회원사코드리스트")

class RequestForTop50ProgramNetPurchasesRequest(BaseModel):
    """[ka90003] 프로그램순매수상위50요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    trde_upper_tp: SafeStr = Field(default="", description="매매상위구분 1:순매도상위, 2:순매수상위")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 P00101:코스피, P10102:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForTop50ProgramNetPurchasesResponse_PrmNetprpsUpper50(BaseModel):
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

class RequestForTop50ProgramNetPurchasesResponse(BaseModel):
    """[ka90003] 프로그램순매수상위50요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    prm_netprps_upper_50: Annotated[List[RequestForTop50ProgramNetPurchasesResponse_PrmNetprpsUpper50], BeforeValidator(_force_list)] = Field(default_factory=list, description="프로그램순매수상위50")

class RequestForProgramTradingStatusByItemRequest(BaseModel):
    """[ka90004] 종목별프로그램매매현황요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 P00101:코스피, P10102:코스닥")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForProgramTradingStatusByItemResponse_StkPrmTrdePrst(BaseModel):
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

class RequestForProgramTradingStatusByItemResponse(BaseModel):
    """[ka90004] 종목별프로그램매매현황요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    tot_1: SafeStr = Field(default="", description="매수체결수량합계")
    tot_2: SafeStr = Field(default="", description="매수체결금액합계")
    tot_3: SafeStr = Field(default="", description="매도체결수량합계")
    tot_4: SafeStr = Field(default="", description="매도체결금액합계")
    tot_5: SafeStr = Field(default="", description="순매수대금합계")
    tot_6: SafeStr = Field(default="", description="합계6")
    stk_prm_trde_prst: Annotated[List[RequestForProgramTradingStatusByItemResponse_StkPrmTrdePrst], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별프로그램매매현황")

class RequestForCreditLoanAvailableItemsRequest(BaseModel):
    """[kt20016] 신용융자 가능종목요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    crd_stk_grde_tp: SafeStr = Field(default="", description="신용종목등급구분 %:전체, A:A군, B:B군, C:C군, D:D군, E:E군")
    mrkt_deal_tp: SafeStr = Field(default="", description="시장거래구분 %:전체, 1:코스피, 0:코스닥")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class RequestForCreditLoanAvailableItemsResponse_CrdLoanPosStk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    crd_assr_rt: SafeStr = Field(default="", description="신용보증금율")
    repl_pric: SafeStr = Field(default="", description="대용가")
    pred_close_pric: SafeStr = Field(default="", description="전일종가")
    crd_limit_over_yn: SafeStr = Field(default="", description="신용한도초과여부")
    crd_limit_over_txt: SafeStr = Field(default="", description="신용한도초과 N:공란,Y:회사한도 초과")

class RequestForCreditLoanAvailableItemsResponse(BaseModel):
    """[kt20016] 신용융자 가능종목요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_loan_able: SafeStr = Field(default="", description="신용융자가능여부")
    crd_loan_pos_stk: Annotated[List[RequestForCreditLoanAvailableItemsResponse_CrdLoanPosStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="신용융자가능종목")

class CreditLoanAvailabilityInquiryRequest(BaseModel):
    """[kt20017] 신용융자 가능문의 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class CreditLoanAvailabilityInquiryResponse(BaseModel):
    """[kt20017] 신용융자 가능문의 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    crd_alow_yn: SafeStr = Field(default="", description="신용가능여부")

class StockPurchaseOrderRequest(BaseModel):
    """[kt10000] 주식 매수주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class StockPurchaseOrderResponse(BaseModel):
    """[kt10000] 주식 매수주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class StockSellOrderRequest(BaseModel):
    """[kt10001] 주식 매도주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)")
    cond_uv: SafeStr = Field(default="", description="조건단가")

class StockSellOrderResponse(BaseModel):
    """[kt10001] 주식 매도주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class StockCorrectionOrderRequest(BaseModel):
    """[kt10002] 주식 정정주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    mdfy_uv: SafeStr = Field(default="", description="정정단가")
    mdfy_cond_uv: SafeStr = Field(default="", description="정정조건단가")

class StockCorrectionOrderResponse(BaseModel):
    """[kt10002] 주식 정정주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분")

class StockCancellationOrderRequest(BaseModel):
    """[kt10003] 주식 취소주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dmst_stex_tp: SafeStr = Field(default="", description="국내거래소구분 KRX,NXT,SOR")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    cncl_qty: SafeStr = Field(default="", description="취소수량 '0' 입력시 잔량 전부 취소")

class StockCancellationOrderResponse(BaseModel):
    """[kt10003] 주식 취소주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    cncl_qty: SafeStr = Field(default="", description="취소수량")

class GoldSpotPurchaseOrderRequest(BaseModel):
    """[kt50000] 금현물 매수주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 00:보통, 10:보통(IOC), 20:보통(FOK)")

class GoldSpotPurchaseOrderResponse(BaseModel):
    """[kt50000] 금현물 매수주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")

class GoldSpotSellOrderRequest(BaseModel):
    """[kt50001] 금현물 매도주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    ord_qty: SafeStr = Field(default="", description="주문수량")
    ord_uv: SafeStr = Field(default="", description="주문단가")
    trde_tp: SafeStr = Field(default="", description="매매구분 00:보통, 10:보통(IOC), 20:보통(FOK)")

class GoldSpotSellOrderResponse(BaseModel):
    """[kt50001] 금현물 매도주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")

class SpotGoldCorrectionOrderRequest(BaseModel):
    """[kt50002] 금현물 정정주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")
    mdfy_uv: SafeStr = Field(default="", description="정정단가")

class SpotGoldCorrectionOrderResponse(BaseModel):
    """[kt50002] 금현물 정정주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    mdfy_qty: SafeStr = Field(default="", description="정정수량")

class GoldSpotCancellationOrderRequest(BaseModel):
    """[kt50003] 금현물 취소주문 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    orig_ord_no: SafeStr = Field(default="", description="원주문번호")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    cncl_qty: SafeStr = Field(default="", description="취소수량 '0' 입력시 잔량 전부 취소")

class GoldSpotCancellationOrderResponse(BaseModel):
    """[kt50003] 금현물 취소주문 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    ord_no: SafeStr = Field(default="", description="주문번호")
    base_orig_ord_no: SafeStr = Field(default="", description="모주문번호")
    cncl_qty: SafeStr = Field(default="", description="취소수량")

class ChartRequestByItemAndInvestorInstitutionRequest(BaseModel):
    """[ka10060] 종목별투자자기관별차트요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    dt: SafeStr = Field(default="", description="일자 YYYYMMDD")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    unit_tp: SafeStr = Field(default="", description="단위구분 1000:천주, 1:단주")

class ChartRequestByItemAndInvestorInstitutionResponse_StkInvsrOrgnChart(BaseModel):
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

class ChartRequestByItemAndInvestorInstitutionResponse(BaseModel):
    """[ka10060] 종목별투자자기관별차트요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_invsr_orgn_chart: Annotated[List[ChartRequestByItemAndInvestorInstitutionResponse_StkInvsrOrgnChart], BeforeValidator(_force_list)] = Field(default_factory=list, description="종목별투자자기관별차트")

class IntradayInvestorSpecificTradingChartRequestRequest(BaseModel):
    """[ka10064] 장중투자자별매매차트요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    mrkt_tp: SafeStr = Field(default="", description="시장구분 000:전체, 001:코스피, 101:코스닥")
    amt_qty_tp: SafeStr = Field(default="", description="금액수량구분 1:금액, 2:수량")
    trde_tp: SafeStr = Field(default="", description="매매구분 0:순매수, 1:매수, 2:매도")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")

class IntradayInvestorSpecificTradingChartRequestResponse_OpmrInvsrTrdeChart(BaseModel):
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

class IntradayInvestorSpecificTradingChartRequestResponse(BaseModel):
    """[ka10064] 장중투자자별매매차트요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    opmr_invsr_trde_chart: Annotated[List[IntradayInvestorSpecificTradingChartRequestResponse_OpmrInvsrTrdeChart], BeforeValidator(_force_list)] = Field(default_factory=list, description="장중투자자별매매차트")

class StockTickChartInquiryRequestRequest(BaseModel):
    """[ka10079] 주식틱차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockTickChartInquiryRequestResponse_StkTicChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")

class StockTickChartInquiryRequestResponse(BaseModel):
    """[ka10079] 주식틱차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    last_tic_cnt: SafeStr = Field(default="", description="마지막틱갯수")
    stk_tic_chart_qry: Annotated[List[StockTickChartInquiryRequestResponse_StkTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식틱차트조회")

class RequestToViewStockChartRequest(BaseModel):
    """[ka10080] 주식분봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class RequestToViewStockChartResponse_StkMinPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 종가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")

class RequestToViewStockChartResponse(BaseModel):
    """[ka10080] 주식분봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_min_pole_chart_qry: Annotated[List[RequestToViewStockChartResponse_StkMinPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식분봉차트조회")

class StockDailyChartInquiryRequestRequest(BaseModel):
    """[ka10081] 주식일봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockDailyChartInquiryRequestResponse_StkDtPoleChartQry(BaseModel):
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

class StockDailyChartInquiryRequestResponse(BaseModel):
    """[ka10081] 주식일봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_dt_pole_chart_qry: Annotated[List[StockDailyChartInquiryRequestResponse_StkDtPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식일봉차트조회")

class StockWeeklyChartInquiryRequestRequest(BaseModel):
    """[ka10082] 주식주봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockWeeklyChartInquiryRequestResponse_StkStkPoleChartQry(BaseModel):
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

class StockWeeklyChartInquiryRequestResponse(BaseModel):
    """[ka10082] 주식주봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_stk_pole_chart_qry: Annotated[List[StockWeeklyChartInquiryRequestResponse_StkStkPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식주봉차트조회")

class StockMonthlyChartInquiryRequestRequest(BaseModel):
    """[ka10083] 주식월봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockMonthlyChartInquiryRequestResponse_StkMthPoleChartQry(BaseModel):
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

class StockMonthlyChartInquiryRequestResponse(BaseModel):
    """[ka10083] 주식월봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_mth_pole_chart_qry: Annotated[List[StockMonthlyChartInquiryRequestResponse_StkMthPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식월봉차트조회")

class StockAnnualChartInquiryRequestRequest(BaseModel):
    """[ka10094] 주식년봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 거래소별 종목코드(KRX:039490,NXT:039490_NX,SOR:039490_AL)")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class StockAnnualChartInquiryRequestResponse_StkYrPoleChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    trde_qty: SafeStr = Field(default="", description="거래량")
    trde_prica: SafeStr = Field(default="", description="거래대금")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")

class StockAnnualChartInquiryRequestResponse(BaseModel):
    """[ka10094] 주식년봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_yr_pole_chart_qry: Annotated[List[StockAnnualChartInquiryRequestResponse_StkYrPoleChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="주식년봉차트조회")

class IndustryTickChartInquiryRequestRequest(BaseModel):
    """[ka20004] 업종틱차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class IndustryTickChartInquiryRequestResponse_IndsTicChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    pred_pre: SafeStr = Field(default="", description="전일대비 현재가 - 전일종가")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비 기호 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")

class IndustryTickChartInquiryRequestResponse(BaseModel):
    """[ka20004] 업종틱차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_tic_chart_qry: Annotated[List[IndustryTickChartInquiryRequestResponse_IndsTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종틱차트조회")

class IndustryDivisionInquiryRequestRequest(BaseModel):
    """[ka20005] 업종분봉조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryDivisionInquiryRequestResponse_IndsMinPoleQry(BaseModel):
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

class IndustryDivisionInquiryRequestResponse(BaseModel):
    """[ka20005] 업종분봉조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_min_pole_qry: Annotated[List[IndustryDivisionInquiryRequestResponse_IndsMinPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종분봉조회")

class IndustryDailySalaryInquiryRequestRequest(BaseModel):
    """[ka20006] 업종일봉조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryDailySalaryInquiryRequestResponse_IndsDtPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustryDailySalaryInquiryRequestResponse(BaseModel):
    """[ka20006] 업종일봉조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_dt_pole_qry: Annotated[List[IndustryDailySalaryInquiryRequestResponse_IndsDtPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종일봉조회")

class RequestForIndustrySalaryInquiryRequest(BaseModel):
    """[ka20007] 업종주봉조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class RequestForIndustrySalaryInquiryResponse_IndsStkPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class RequestForIndustrySalaryInquiryResponse(BaseModel):
    """[ka20007] 업종주봉조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_stk_pole_qry: Annotated[List[RequestForIndustrySalaryInquiryResponse_IndsStkPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종주봉조회")

class IndustryMonthlySalaryInquiryRequestRequest(BaseModel):
    """[ka20008] 업종월봉조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryMonthlySalaryInquiryRequestResponse_IndsMthPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustryMonthlySalaryInquiryRequestResponse(BaseModel):
    """[ka20008] 업종월봉조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_mth_pole_qry: Annotated[List[IndustryMonthlySalaryInquiryRequestResponse_IndsMthPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종월봉조회")

class IndustryYearSalaryInquiryRequestRequest(BaseModel):
    """[ka20019] 업종년봉조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    inds_cd: SafeStr = Field(default="", description="업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class IndustryYearSalaryInquiryRequestResponse_IndsYrPoleQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_qty: SafeStr = Field(default="", description="거래량")
    dt: SafeStr = Field(default="", description="일자")
    open_pric: SafeStr = Field(default="", description="시가 지수 값은 소수점 제거 후 100배 값으로 반환")
    high_pric: SafeStr = Field(default="", description="고가 지수 값은 소수점 제거 후 100배 값으로 반환")
    low_pric: SafeStr = Field(default="", description="저가 지수 값은 소수점 제거 후 100배 값으로 반환")
    trde_prica: SafeStr = Field(default="", description="거래대금")

class IndustryYearSalaryInquiryRequestResponse(BaseModel):
    """[ka20019] 업종년봉조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    inds_cd: SafeStr = Field(default="", description="업종코드")
    inds_yr_pole_qry: Annotated[List[IndustryYearSalaryInquiryRequestResponse_IndsYrPoleQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="업종년봉조회")

class GoldSpotTickChartInquiryRequestRequest(BaseModel):
    """[ka50079] 금현물틱차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotTickChartInquiryRequestResponse_GdsTicChartQry(BaseModel):
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

class GoldSpotTickChartInquiryRequestResponse(BaseModel):
    """[ka50079] 금현물틱차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_tic_chart_qry: Annotated[List[GoldSpotTickChartInquiryRequestResponse_GdsTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물틱차트조회")

class GoldSpotFractionalChartInquiryRequestRequest(BaseModel):
    """[ka50080] 금현물분봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotFractionalChartInquiryRequestResponse_GdsMinChartQry(BaseModel):
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

class GoldSpotFractionalChartInquiryRequestResponse(BaseModel):
    """[ka50080] 금현물분봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_min_chart_qry: Annotated[List[GoldSpotFractionalChartInquiryRequestResponse_GdsMinChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물분봉차트조회")

class GoldSpotDailyChartInquiryRequestRequest(BaseModel):
    """[ka50081] 금현물일봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotDailyChartInquiryRequestResponse_GdsDayChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")
    pred_pre_sig: SafeStr = Field(default="", description="전일대비기호")

class GoldSpotDailyChartInquiryRequestResponse(BaseModel):
    """[ka50081] 금현물일봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_day_chart_qry: Annotated[List[GoldSpotDailyChartInquiryRequestResponse_GdsDayChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotWeeklyChartInquiryRequestRequest(BaseModel):
    """[ka50082] 금현물주봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotWeeklyChartInquiryRequestResponse_GdsWeekChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")

class GoldSpotWeeklyChartInquiryRequestResponse(BaseModel):
    """[ka50082] 금현물주봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_week_chart_qry: Annotated[List[GoldSpotWeeklyChartInquiryRequestResponse_GdsWeekChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotMonthlyChartInquiryRequestRequest(BaseModel):
    """[ka50083] 금현물월봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")
    upd_stkpc_tp: SafeStr = Field(default="", description="수정주가구분 0 or 1")

class GoldSpotMonthlyChartInquiryRequestResponse_GdsMonthChartQry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    acc_trde_qty: SafeStr = Field(default="", description="누적 거래량")
    acc_trde_prica: SafeStr = Field(default="", description="누적 거래대금")
    open_pric: SafeStr = Field(default="", description="시가")
    high_pric: SafeStr = Field(default="", description="고가")
    low_pric: SafeStr = Field(default="", description="저가")
    dt: SafeStr = Field(default="", description="일자")

class GoldSpotMonthlyChartInquiryRequestResponse(BaseModel):
    """[ka50083] 금현물월봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_month_chart_qry: Annotated[List[GoldSpotMonthlyChartInquiryRequestResponse_GdsMonthChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class GoldSpotDailyTickChartInquiryRequestRequest(BaseModel):
    """[ka50091] 금현물당일틱차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class GoldSpotDailyTickChartInquiryRequestResponse_GdsTicChartQry(BaseModel):
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

class GoldSpotDailyTickChartInquiryRequestResponse(BaseModel):
    """[ka50091] 금현물당일틱차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_tic_chart_qry: Annotated[List[GoldSpotDailyTickChartInquiryRequestResponse_GdsTicChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class RequestToViewGoldSpotDailyChartRequest(BaseModel):
    """[ka50092] 금현물당일분봉차트조회요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드 M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g")
    tic_scope: SafeStr = Field(default="", description="틱범위 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱")

class RequestToViewGoldSpotDailyChartResponse_GdsMinChartQry(BaseModel):
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

class RequestToViewGoldSpotDailyChartResponse(BaseModel):
    """[ka50092] 금현물당일분봉차트조회요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    gds_min_chart_qry: Annotated[List[RequestToViewGoldSpotDailyChartResponse_GdsMinChartQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="금현물일봉차트조회")

class RequestsByThemeGroupRequest(BaseModel):
    """[ka90001] 테마그룹별요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    qry_tp: SafeStr = Field(default="", description="검색구분 0:전체검색, 1:테마검색, 2:종목검색")
    stk_cd: SafeStr = Field(default="", description="종목코드 검색하려는 종목코드")
    date_tp: SafeStr = Field(default="", description="날짜구분 n일전 (1일 ~ 99일 날짜입력)")
    thema_nm: SafeStr = Field(default="", description="테마명 검색하려는 테마명")
    flu_pl_amt_tp: SafeStr = Field(default="", description="등락수익구분 1:상위기간수익률, 2:하위기간수익률, 3:상위등락률, 4:하위등락률")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestsByThemeGroupResponse_ThemaGrp(BaseModel):
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

class RequestsByThemeGroupResponse(BaseModel):
    """[ka90001] 테마그룹별요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    thema_grp: Annotated[List[RequestsByThemeGroupResponse_ThemaGrp], BeforeValidator(_force_list)] = Field(default_factory=list, description="테마그룹별")

class RequestForThemeItemsRequest(BaseModel):
    """[ka90002] 테마구성종목요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    date_tp: SafeStr = Field(default="", description="날짜구분 1일 ~ 99일 날짜입력")
    thema_grp_cd: SafeStr = Field(default="", description="테마그룹코드 테마그룹코드 번호")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT 3.통합")

class RequestForThemeItemsResponse_ThemaCompStk(BaseModel):
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

class RequestForThemeItemsResponse(BaseModel):
    """[ka90002] 테마구성종목요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    flu_rt: SafeStr = Field(default="", description="등락률")
    dt_prft_rt: SafeStr = Field(default="", description="기간수익률")
    thema_comp_stk: Annotated[List[RequestForThemeItemsResponse_ThemaCompStk], BeforeValidator(_force_list)] = Field(default_factory=list, description="테마구성종목")

class ElwDailySensitivityIndicatorRequestRequest(BaseModel):
    """[ka10048] ELW일별민감도지표요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class ElwDailySensitivityIndicatorRequestResponse_ElwdalySnstIx(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    iv: SafeStr = Field(default="", description="IV")
    delta: SafeStr = Field(default="", description="델타")
    gam: SafeStr = Field(default="", description="감마")
    theta: SafeStr = Field(default="", description="쎄타")
    vega: SafeStr = Field(default="", description="베가")
    law: SafeStr = Field(default="", description="로")
    lp: SafeStr = Field(default="", description="LP")

class ElwDailySensitivityIndicatorRequestResponse(BaseModel):
    """[ka10048] ELW일별민감도지표요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwdaly_snst_ix: Annotated[List[ElwDailySensitivityIndicatorRequestResponse_ElwdalySnstIx], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW일별민감도지표")

class ElwSensitivityIndicatorRequestRequest(BaseModel):
    """[ka10050] ELW민감도지표요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class ElwSensitivityIndicatorRequestResponse_ElwsnstIxArray(BaseModel):
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

class ElwSensitivityIndicatorRequestResponse(BaseModel):
    """[ka10050] ELW민감도지표요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwsnst_ix_array: Annotated[List[ElwSensitivityIndicatorRequestResponse_ElwsnstIxArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW민감도지표배열")

class RequestForSuddenFluctuationInElwPriceRequest(BaseModel):
    """[ka30001] ELW가격급등락요청 요청 모델"""
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

class RequestForSuddenFluctuationInElwPriceResponse_ElwpricJmpflu(BaseModel):
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

class RequestForSuddenFluctuationInElwPriceResponse(BaseModel):
    """[ka30001] ELW가격급등락요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    base_pric_tm: SafeStr = Field(default="", description="기준가시간")
    elwpric_jmpflu: Annotated[List[RequestForSuddenFluctuationInElwPriceResponse_ElwpricJmpflu], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW가격급등락")

class ElwNetSalesTopRequestByTraderRequest(BaseModel):
    """[ka30002] 거래원별ELW순매매상위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 3자리, 영웅문4 0273화면참조 (교보:001, 신한금융투자:002, 한국투자증권:003, 대신:004, 미래대우:005, ,,,)")
    trde_qty_tp: SafeStr = Field(default="", description="거래량구분 0:전체, 5:5천주, 10:만주, 50:5만주, 100:10만주, 500:50만주, 1000:백만주")
    trde_tp: SafeStr = Field(default="", description="매매구분 1:순매수, 2:순매도")
    dt: SafeStr = Field(default="", description="기간 1:전일, 5:5일, 10:10일, 40:40일, 60:60일")
    trde_end_elwskip: SafeStr = Field(default="", description="거래종료ELW제외 0:포함, 1:제외")

class ElwNetSalesTopRequestByTraderResponse_TrdeOriElwnettrdeUpper(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    stkpc_flu: SafeStr = Field(default="", description="주가등락")
    flu_rt: SafeStr = Field(default="", description="등락율")
    trde_qty: SafeStr = Field(default="", description="거래량")
    netprps: SafeStr = Field(default="", description="순매수")
    buy_trde_qty: SafeStr = Field(default="", description="매수거래량")
    sel_trde_qty: SafeStr = Field(default="", description="매도거래량")

class ElwNetSalesTopRequestByTraderResponse(BaseModel):
    """[ka30002] 거래원별ELW순매매상위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    trde_ori_elwnettrde_upper: Annotated[List[ElwNetSalesTopRequestByTraderResponse_TrdeOriElwnettrdeUpper], BeforeValidator(_force_list)] = Field(default_factory=list, description="거래원별ELW순매매상위")

class RequestDailyTrendOfElwlpHoldingsRequest(BaseModel):
    """[ka30003] ELWLP보유일별추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드")
    base_dt: SafeStr = Field(default="", description="기준일자 YYYYMMDD")

class RequestDailyTrendOfElwlpHoldingsResponse_ElwlppossDalyTrnsn(BaseModel):
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

class RequestDailyTrendOfElwlpHoldingsResponse(BaseModel):
    """[ka30003] ELWLP보유일별추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwlpposs_daly_trnsn: Annotated[List[RequestDailyTrendOfElwlpHoldingsResponse_ElwlppossDalyTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELWLP보유일별추이")

class ElwDisparityRateRequestRequest(BaseModel):
    """[ka30004] ELW괴리율요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200..")
    rght_tp: SafeStr = Field(default="", description="권리구분 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 005: EX, 006: 조기종료콜, 007: 조기종료풋")
    lpcd: SafeStr = Field(default="", description="LP코드 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17")
    trde_end_elwskip: SafeStr = Field(default="", description="거래종료ELW제외 1:거래종료ELW제외, 0:거래종료ELW포함")

class ElwDisparityRateRequestResponse_ElwdisptyRt(BaseModel):
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

class ElwDisparityRateRequestResponse(BaseModel):
    """[ka30004] ELW괴리율요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwdispty_rt: Annotated[List[ElwDisparityRateRequestResponse_ElwdisptyRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW괴리율")

class ElwConditionSearchRequestRequest(BaseModel):
    """[ka30005] ELW조건검색요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    isscomp_cd: SafeStr = Field(default="", description="발행사코드 12자리입력(전체:000000000000, 한국투자증권:000,,,3, 미래대우:000,,,5, 신영:000,,,6, NK투자증권:000,,,12, KB증권:000,,,17)")
    bsis_aset_cd: SafeStr = Field(default="", description="기초자산코드 전체일때만 12자리입력(전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼정전자:005930, KT:030200,,)")
    rght_tp: SafeStr = Field(default="", description="권리구분 0:전체, 1:콜, 2:풋, 3:DC, 4:DP, 5:EX, 6:조기종료콜, 7:조기종료풋")
    lpcd: SafeStr = Field(default="", description="LP코드 전체일때만 12자리입력(전체:000000000000, 한국투자증권:003, 미래대우:005, 신영:006, NK투자증권:012, KB증권:017)")
    sort_tp: SafeStr = Field(default="", description="정렬구분 0:정렬없음, 1:상승율순, 2:상승폭순, 3:하락율순, 4:하락폭순, 5:거래량순, 6:거래대금순, 7:잔존일순")

class ElwConditionSearchRequestResponse_ElwcndQry(BaseModel):
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

class ElwConditionSearchRequestResponse(BaseModel):
    """[ka30005] ELW조건검색요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwcnd_qry: Annotated[List[ElwConditionSearchRequestResponse_ElwcndQry], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW조건검색")

class ElwFluctuationRateRankingRequestRequest(BaseModel):
    """[ka30009] ELW등락율순위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:상승률, 2:상승폭, 3:하락률, 4:하락폭")
    rght_tp: SafeStr = Field(default="", description="권리구분 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 006:조기종료콜, 007:조기종료풋")
    trde_end_skip: SafeStr = Field(default="", description="거래종료제외 1:거래종료제외, 0:거래종료포함")

class ElwFluctuationRateRankingRequestResponse_ElwfluRtRank(BaseModel):
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

class ElwFluctuationRateRankingRequestResponse(BaseModel):
    """[ka30009] ELW등락율순위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwflu_rt_rank: Annotated[List[ElwFluctuationRateRankingRequestResponse_ElwfluRtRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW등락율순위")

class ElwRemainingBalanceRankingRequestRequest(BaseModel):
    """[ka30010] ELW잔량순위요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    sort_tp: SafeStr = Field(default="", description="정렬구분 1:순매수잔량상위, 2: 순매도 잔량상위")
    rght_tp: SafeStr = Field(default="", description="권리구분 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 006: 조기종료콜, 007: 조기종료풋")
    trde_end_skip: SafeStr = Field(default="", description="거래종료제외 1:거래종료제외, 0:거래종료포함")

class ElwRemainingBalanceRankingRequestResponse_ElwreqRank(BaseModel):
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

class ElwRemainingBalanceRankingRequestResponse(BaseModel):
    """[ka30010] ELW잔량순위요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwreq_rank: Annotated[List[ElwRemainingBalanceRankingRequestResponse_ElwreqRank], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW잔량순위")

class ElwProximityRateRequestRequest(BaseModel):
    """[ka30011] ELW근접율요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class ElwProximityRateRequestResponse_ElwalaccRt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stk_cd: SafeStr = Field(default="", description="종목코드")
    stk_nm: SafeStr = Field(default="", description="종목명")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    flu_rt: SafeStr = Field(default="", description="등락율")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    alacc_rt: SafeStr = Field(default="", description="근접율")

class ElwProximityRateRequestResponse(BaseModel):
    """[ka30011] ELW근접율요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    elwalacc_rt: Annotated[List[ElwProximityRateRequestResponse_ElwalaccRt], BeforeValidator(_force_list)] = Field(default_factory=list, description="ELW근접율")

class RequestForDetailedInformationOnElwItemsRequest(BaseModel):
    """[ka30012] ELW종목상세정보요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class RequestForDetailedInformationOnElwItemsResponse(BaseModel):
    """[ka30012] ELW종목상세정보요청 응답 모델"""
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

class EtfReturnRateRequestRequest(BaseModel):
    """[ka40001] ETF수익율요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")
    etfobjt_idex_cd: SafeStr = Field(default="", description="ETF대상지수코드")
    dt: SafeStr = Field(default="", description="기간 0:1주, 1:1달, 2:6개월, 3:1년")

class EtfReturnRateRequestResponse_EtfprftRtLst(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    etfprft_rt: SafeStr = Field(default="", description="ETF수익률")
    cntr_prft_rt: SafeStr = Field(default="", description="체결수익률")
    for_netprps_qty: SafeStr = Field(default="", description="외인순매수수량")
    orgn_netprps_qty: SafeStr = Field(default="", description="기관순매수수량")

class EtfReturnRateRequestResponse(BaseModel):
    """[ka40001] ETF수익율요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfprft_rt_lst: Annotated[List[EtfReturnRateRequestResponse_EtfprftRtLst], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF수익율")

class EtfItemInformationRequestRequest(BaseModel):
    """[ka40002] ETF종목정보요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfItemInformationRequestResponse(BaseModel):
    """[ka40002] ETF종목정보요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_nm: SafeStr = Field(default="", description="종목명")
    etfobjt_idex_nm: SafeStr = Field(default="", description="ETF대상지수명")
    wonju_pric: SafeStr = Field(default="", description="원주가격")
    etftxon_type: SafeStr = Field(default="", description="ETF과세유형")
    etntxon_type: SafeStr = Field(default="", description="ETN과세유형")

class EtfDailyTrendRequestRequest(BaseModel):
    """[ka40003] ETF일별추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfDailyTrendRequestResponse_EtfdalyTrnsn(BaseModel):
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

class EtfDailyTrendRequestResponse(BaseModel):
    """[ka40003] ETF일별추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfdaly_trnsn: Annotated[List[EtfDailyTrendRequestResponse_EtfdalyTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF일별추이")

class RequestFullEtfViewRequest(BaseModel):
    """[ka40004] ETF전체시세요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    txon_type: SafeStr = Field(default="", description="과세유형 0:전체, 1:비과세, 2:보유기간과세, 3:회사형, 4:외국, 5:비과세해외(보유기간관세)")
    navpre: SafeStr = Field(default="", description="NAV대비 0:전체, 1:NAV > 전일종가, 2:NAV < 전일종가")
    mngmcomp: SafeStr = Field(default="", description="운용사 0000:전체, 3020:KODEX(삼성), 3027:KOSEF(키움), 3191:TIGER(미래에셋), 3228:KINDEX(한국투자), 3023:KStar(KB), 3022:아리랑(한화), 9999:기타운용사")
    txon_yn: SafeStr = Field(default="", description="과세여부 0:전체, 1:과세, 2:비과세")
    trace_idex: SafeStr = Field(default="", description="추적지수 0:전체")
    stex_tp: SafeStr = Field(default="", description="거래소구분 1:KRX, 2:NXT, 3:통합")

class RequestFullEtfViewResponse_EtfallMrpr(BaseModel):
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

class RequestFullEtfViewResponse(BaseModel):
    """[ka40004] ETF전체시세요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfall_mrpr: Annotated[List[RequestFullEtfViewResponse_EtfallMrpr], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF전체시세")

class EtfTimeZoneTrendRequestRequest(BaseModel):
    """[ka40006] ETF시간대별추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTimeZoneTrendRequestResponse_EtftislTrnsn(BaseModel):
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

class EtfTimeZoneTrendRequestResponse(BaseModel):
    """[ka40006] ETF시간대별추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_nm: SafeStr = Field(default="", description="종목명")
    etfobjt_idex_nm: SafeStr = Field(default="", description="ETF대상지수명")
    wonju_pric: SafeStr = Field(default="", description="원주가격")
    etftxon_type: SafeStr = Field(default="", description="ETF과세유형")
    etntxon_type: SafeStr = Field(default="", description="ETN과세유형")
    etftisl_trnsn: Annotated[List[EtfTimeZoneTrendRequestResponse_EtftislTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF시간대별추이")

class EtfTradingRequestByTimeSlotRequest(BaseModel):
    """[ka40007] ETF시간대별체결요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTradingRequestByTimeSlotResponse_EtftislCntrArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    stex_tp: SafeStr = Field(default="", description="거래소구분 KRX , NXT , 통합")

class EtfTradingRequestByTimeSlotResponse(BaseModel):
    """[ka40007] ETF시간대별체결요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    stk_cls: SafeStr = Field(default="", description="종목분류")
    stk_nm: SafeStr = Field(default="", description="종목명")
    etfobjt_idex_nm: SafeStr = Field(default="", description="ETF대상지수명")
    etfobjt_idex_cd: SafeStr = Field(default="", description="ETF대상지수코드")
    objt_idex_pre_rt: SafeStr = Field(default="", description="대상지수대비율")
    wonju_pric: SafeStr = Field(default="", description="원주가격")
    etftisl_cntr_array: Annotated[List[EtfTradingRequestByTimeSlotResponse_EtftislCntrArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF시간대별체결배열")

class EtfTransactionRequestByDateRequest(BaseModel):
    """[ka40008] ETF일자별체결요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTransactionRequestByDateResponse_EtfnetprpsQtyArray(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dt: SafeStr = Field(default="", description="일자")
    cur_prc_n: SafeStr = Field(default="", description="현재가n")
    pre_sig_n: SafeStr = Field(default="", description="대비기호n")
    pred_pre_n: SafeStr = Field(default="", description="전일대비n")
    acc_trde_qty: SafeStr = Field(default="", description="누적거래량")
    for_netprps_qty: SafeStr = Field(default="", description="외인순매수수량")
    orgn_netprps_qty: SafeStr = Field(default="", description="기관순매수수량")

class EtfTransactionRequestByDateResponse(BaseModel):
    """[ka40008] ETF일자별체결요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    cntr_tm: SafeStr = Field(default="", description="체결시간")
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    etfnetprps_qty_array: Annotated[List[EtfTransactionRequestByDateResponse_EtfnetprpsQtyArray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF순매수수량배열")

class EtfTradingRequestByTimeSlot1Request(BaseModel):
    """[ka40009] ETF시간대별체결요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTradingRequestByTimeSlot1Response_Etfnavarray(BaseModel):
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

class EtfTradingRequestByTimeSlot1Response(BaseModel):
    """[ka40009] ETF시간대별체결요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etfnavarray: Annotated[List[EtfTradingRequestByTimeSlot1Response_Etfnavarray], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETFNAV배열")

class EtfTimeZoneTrendRequest1Request(BaseModel):
    """[ka40010] ETF시간대별추이요청 요청 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅")
    stk_cd: SafeStr = Field(default="", description="종목코드")

class EtfTimeZoneTrendRequest1Response_EtftislTrnsn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cur_prc: SafeStr = Field(default="", description="현재가")
    pre_sig: SafeStr = Field(default="", description="대비기호")
    pred_pre: SafeStr = Field(default="", description="전일대비")
    trde_qty: SafeStr = Field(default="", description="거래량")
    for_netprps: SafeStr = Field(default="", description="외인순매수")

class EtfTimeZoneTrendRequest1Response(BaseModel):
    """[ka40010] ETF시간대별추이요청 응답 모델"""
    model_config = ConfigDict(populate_by_name=True)
    cont_yn: SafeStr = Field(default="", alias="cont-yn", description="연속조회여부 다음 데이터가 있을시 Y값 전달")
    next_key: SafeStr = Field(default="", alias="next-key", description="연속조회키 다음 데이터가 있을시 다음 키값 전달")
    etftisl_trnsn: Annotated[List[EtfTimeZoneTrendRequest1Response_EtftislTrnsn], BeforeValidator(_force_list)] = Field(default_factory=list, description="ETF시간대별추이")

# ====================================================================
# 2. Typed API Client (타입이 보장되는 클라이언트)
# ====================================================================

class KiwoomTypedClient:
    """
    kwargs 대신 명시적인 Pydantic 모델을 사용하여 API를 호출하는 안전한 클라이언트입니다.
    요청 및 응답 모두 Type Hinting이 적용된 객체를 사용합니다.
    """
    def __init__(self, client: KiwoomClient):
        self.client = client

    async def connect_ws(self, on_message: Callable[[Dict[str, Any]], Any]):
        await self.client.connect_ws(on_message)

    async def disconnect_ws(self):
        await self.client.disconnect_ws()

    def access_token_issuance(self, req: AccessTokenIssuanceRequest) -> AccessTokenIssuanceResponse:
        """[au10001] 접근토큰 발급 (OAuth 인증 - 접근토큰발급)"""
        raw_response = self.client.call("au10001", **req.model_dump(by_alias=True, exclude_none=True))
        return AccessTokenIssuanceResponse(**raw_response)

    def discard_access_token(self, req: DiscardAccessTokenRequest) -> DiscardAccessTokenResponse:
        """[au10002] 접근토큰폐기 (OAuth 인증 - 접근토큰폐기)"""
        raw_response = self.client.call("au10002", **req.model_dump(by_alias=True, exclude_none=True))
        return DiscardAccessTokenResponse(**raw_response)

    def account_number_inquiry(self, req: AccountNumberInquiryRequest) -> AccountNumberInquiryResponse:
        """[ka00001] 계좌번호조회 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka00001", **req.model_dump(by_alias=True, exclude_none=True))
        return AccountNumberInquiryResponse(**raw_response)

    def daily_balance_return_rate(self, req: DailyBalanceReturnRateRequest) -> DailyBalanceReturnRateResponse:
        """[ka01690] 일별잔고수익률 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka01690", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyBalanceReturnRateResponse(**raw_response)

    def realized_profit_loss_request_by_date_item_date(self, req: RealizedProfitLossRequestByDateItemDateRequest) -> RealizedProfitLossRequestByDateItemDateResponse:
        """[ka10072] 일자별종목별실현손익요청_일자 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10072", **req.model_dump(by_alias=True, exclude_none=True))
        return RealizedProfitLossRequestByDateItemDateResponse(**raw_response)

    def realized_profit_loss_request_by_date_and_item_period(self, req: RealizedProfitLossRequestByDateAndItemPeriodRequest) -> RealizedProfitLossRequestByDateAndItemPeriodResponse:
        """[ka10073] 일자별종목별실현손익요청_기간 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10073", **req.model_dump(by_alias=True, exclude_none=True))
        return RealizedProfitLossRequestByDateAndItemPeriodResponse(**raw_response)

    def request_for_realized_profit_or_loss_by_date(self, req: RequestForRealizedProfitOrLossByDateRequest) -> RequestForRealizedProfitOrLossByDateResponse:
        """[ka10074] 일자별실현손익요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10074", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForRealizedProfitOrLossByDateResponse(**raw_response)

    def non_confirmation_request(self, req: NonConfirmationRequestRequest) -> NonConfirmationRequestResponse:
        """[ka10075] 미체결요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10075", **req.model_dump(by_alias=True, exclude_none=True))
        return NonConfirmationRequestResponse(**raw_response)

    def conclusion_request(self, req: ConclusionRequestRequest) -> ConclusionRequestResponse:
        """[ka10076] 체결요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10076", **req.model_dump(by_alias=True, exclude_none=True))
        return ConclusionRequestResponse(**raw_response)

    def request_for_same_day_realized_profit_and_loss(self, req: RequestForSameDayRealizedProfitAndLossRequest) -> RequestForSameDayRealizedProfitAndLossResponse:
        """[ka10077] 당일실현손익상세요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10077", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSameDayRealizedProfitAndLossResponse(**raw_response)

    def account_yield_request(self, req: AccountYieldRequestRequest) -> AccountYieldRequestResponse:
        """[ka10085] 계좌수익률요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10085", **req.model_dump(by_alias=True, exclude_none=True))
        return AccountYieldRequestResponse(**raw_response)

    def unfilled_split_order_details(self, req: UnfilledSplitOrderDetailsRequest) -> UnfilledSplitOrderDetailsResponse:
        """[ka10088] 미체결 분할주문 상세 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10088", **req.model_dump(by_alias=True, exclude_none=True))
        return UnfilledSplitOrderDetailsResponse(**raw_response)

    def same_day_sales_log_request(self, req: SameDaySalesLogRequestRequest) -> SameDaySalesLogRequestResponse:
        """[ka10170] 당일매매일지요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("ka10170", **req.model_dump(by_alias=True, exclude_none=True))
        return SameDaySalesLogRequestResponse(**raw_response)

    def request_detailed_status_of_deposit(self, req: RequestDetailedStatusOfDepositRequest) -> RequestDetailedStatusOfDepositResponse:
        """[kt00001] 예수금상세현황요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00001", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestDetailedStatusOfDepositResponse(**raw_response)

    def daily_estimated_deposited_asset_status_request(self, req: DailyEstimatedDepositedAssetStatusRequestRequest) -> DailyEstimatedDepositedAssetStatusRequestResponse:
        """[kt00002] 일별추정예탁자산현황요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00002", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyEstimatedDepositedAssetStatusRequestResponse(**raw_response)

    def estimated_asset_inquiry_request(self, req: EstimatedAssetInquiryRequestRequest) -> EstimatedAssetInquiryRequestResponse:
        """[kt00003] 추정자산조회요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00003", **req.model_dump(by_alias=True, exclude_none=True))
        return EstimatedAssetInquiryRequestResponse(**raw_response)

    def request_for_account_evaluation_status(self, req: RequestForAccountEvaluationStatusRequest) -> RequestForAccountEvaluationStatusResponse:
        """[kt00004] 계좌평가현황요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00004", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForAccountEvaluationStatusResponse(**raw_response)

    def request_for_transaction_balance(self, req: RequestForTransactionBalanceRequest) -> RequestForTransactionBalanceResponse:
        """[kt00005] 체결잔고요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00005", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForTransactionBalanceResponse(**raw_response)

    def request_details_on_order_details_by_account(self, req: RequestDetailsOnOrderDetailsByAccountRequest) -> RequestDetailsOnOrderDetailsByAccountResponse:
        """[kt00007] 계좌별주문체결내역상세요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00007", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestDetailsOnOrderDetailsByAccountResponse(**raw_response)

    def request_next_day_payment_schedule_details_for_each_account(self, req: RequestNextDayPaymentScheduleDetailsForEachAccountRequest) -> RequestNextDayPaymentScheduleDetailsForEachAccountResponse:
        """[kt00008] 계좌별익일결제예정내역요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00008", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestNextDayPaymentScheduleDetailsForEachAccountResponse(**raw_response)

    def request_for_order_execution_status_by_account(self, req: RequestForOrderExecutionStatusByAccountRequest) -> RequestForOrderExecutionStatusByAccountResponse:
        """[kt00009] 계좌별주문체결현황요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00009", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForOrderExecutionStatusByAccountResponse(**raw_response)

    def request_for_order_withdrawal_amount(self, req: RequestForOrderWithdrawalAmountRequest) -> RequestForOrderWithdrawalAmountResponse:
        """[kt00010] 주문인출가능금액요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00010", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForOrderWithdrawalAmountResponse(**raw_response)

    def request_to_inquiry_quantity_available_for_order_by_margin_rate(self, req: RequestToInquiryQuantityAvailableForOrderByMarginRateRequest) -> RequestToInquiryQuantityAvailableForOrderByMarginRateResponse:
        """[kt00011] 증거금율별주문가능수량조회요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00011", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestToInquiryQuantityAvailableForOrderByMarginRateResponse(**raw_response)

    def request_to_inquiry_quantity_available_for_order_by_credit_deposit_rate(self, req: RequestToInquiryQuantityAvailableForOrderByCreditDepositRateRequest) -> RequestToInquiryQuantityAvailableForOrderByCreditDepositRateResponse:
        """[kt00012] 신용보증금율별주문가능수량조회요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00012", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestToInquiryQuantityAvailableForOrderByCreditDepositRateResponse(**raw_response)

    def margin_details_inquiry_request(self, req: MarginDetailsInquiryRequestRequest) -> MarginDetailsInquiryRequestResponse:
        """[kt00013] 증거금세부내역조회요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00013", **req.model_dump(by_alias=True, exclude_none=True))
        return MarginDetailsInquiryRequestResponse(**raw_response)

    def request_for_comprehensive_consignment_transaction_details(self, req: RequestForComprehensiveConsignmentTransactionDetailsRequest) -> RequestForComprehensiveConsignmentTransactionDetailsResponse:
        """[kt00015] 위탁종합거래내역요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00015", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForComprehensiveConsignmentTransactionDetailsResponse(**raw_response)

    def request_for_detailed_status_of_daily_account_returns(self, req: RequestForDetailedStatusOfDailyAccountReturnsRequest) -> RequestForDetailedStatusOfDailyAccountReturnsResponse:
        """[kt00016] 일별계좌수익률상세현황요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00016", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForDetailedStatusOfDailyAccountReturnsResponse(**raw_response)

    def request_daily_status_for_each_account(self, req: RequestDailyStatusForEachAccountRequest) -> RequestDailyStatusForEachAccountResponse:
        """[kt00017] 계좌별당일현황요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00017", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestDailyStatusForEachAccountResponse(**raw_response)

    def request_for_account_evaluation_balance_details(self, req: RequestForAccountEvaluationBalanceDetailsRequest) -> RequestForAccountEvaluationBalanceDetailsResponse:
        """[kt00018] 계좌평가잔고내역요청 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt00018", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForAccountEvaluationBalanceDetailsResponse(**raw_response)

    def check_gold_spot_balance(self, req: CheckGoldSpotBalanceRequest) -> CheckGoldSpotBalanceResponse:
        """[kt50020] 금현물 잔고확인 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt50020", **req.model_dump(by_alias=True, exclude_none=True))
        return CheckGoldSpotBalanceResponse(**raw_response)

    def gold_spot_deposit(self, req: GoldSpotDepositRequest) -> GoldSpotDepositResponse:
        """[kt50021] 금현물 예수금 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt50021", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDepositResponse(**raw_response)

    def view_all_gold_spot_orders(self, req: ViewAllGoldSpotOrdersRequest) -> ViewAllGoldSpotOrdersResponse:
        """[kt50030] 금현물 주문체결전체조회 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt50030", **req.model_dump(by_alias=True, exclude_none=True))
        return ViewAllGoldSpotOrdersResponse(**raw_response)

    def gold_spot_order_execution_inquiry(self, req: GoldSpotOrderExecutionInquiryRequest) -> GoldSpotOrderExecutionInquiryResponse:
        """[kt50031] 금현물 주문체결조회 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt50031", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotOrderExecutionInquiryResponse(**raw_response)

    def gold_spot_transaction_history_inquiry(self, req: GoldSpotTransactionHistoryInquiryRequest) -> GoldSpotTransactionHistoryInquiryResponse:
        """[kt50032] 금현물 거래내역조회 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt50032", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotTransactionHistoryInquiryResponse(**raw_response)

    def gold_spot_non_trading_inquiry(self, req: GoldSpotNonTradingInquiryRequest) -> GoldSpotNonTradingInquiryResponse:
        """[kt50075] 금현물 미체결조회 (국내주식 - 계좌)"""
        raw_response = self.client.call("kt50075", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotNonTradingInquiryResponse(**raw_response)

    def short_selling_trend_request(self, req: ShortSellingTrendRequestRequest) -> ShortSellingTrendRequestResponse:
        """[ka10014] 공매도추이요청 (국내주식 - 공매도)"""
        raw_response = self.client.call("ka10014", **req.model_dump(by_alias=True, exclude_none=True))
        return ShortSellingTrendRequestResponse(**raw_response)

    def foreign_stock_trading_trends_by_item(self, req: ForeignStockTradingTrendsByItemRequest) -> ForeignStockTradingTrendsByItemResponse:
        """[ka10008] 주식외국인종목별매매동향 (국내주식 - 기관/외국인)"""
        raw_response = self.client.call("ka10008", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignStockTradingTrendsByItemResponse(**raw_response)

    def stock_institution_request(self, req: StockInstitutionRequestRequest) -> StockInstitutionRequestResponse:
        """[ka10009] 주식기관요청 (국내주식 - 기관/외국인)"""
        raw_response = self.client.call("ka10009", **req.model_dump(by_alias=True, exclude_none=True))
        return StockInstitutionRequestResponse(**raw_response)

    def request_for_status_of_continuous_trading_by_institutional_foreigners(self, req: RequestForStatusOfContinuousTradingByInstitutionalForeignersRequest) -> RequestForStatusOfContinuousTradingByInstitutionalForeignersResponse:
        """[ka10131] 기관외국인연속매매현황요청 (국내주식 - 기관/외국인)"""
        raw_response = self.client.call("ka10131", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForStatusOfContinuousTradingByInstitutionalForeignersResponse(**raw_response)

    def current_status_of_gold_spot_investors(self, req: CurrentStatusOfGoldSpotInvestorsRequest) -> CurrentStatusOfGoldSpotInvestorsResponse:
        """[ka52301] 금현물투자자현황 (국내주식 - 기관/외국인)"""
        raw_response = self.client.call("ka52301", **req.model_dump(by_alias=True, exclude_none=True))
        return CurrentStatusOfGoldSpotInvestorsResponse(**raw_response)

    def request_for_loan_lending_transaction_trend(self, req: RequestForLoanLendingTransactionTrendRequest) -> RequestForLoanLendingTransactionTrendResponse:
        """[ka10068] 대차거래추이요청 (국내주식 - 대차거래)"""
        raw_response = self.client.call("ka10068", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForLoanLendingTransactionTrendResponse(**raw_response)

    def request_for_top10_borrowing_stocks(self, req: RequestForTop10BorrowingStocksRequest) -> RequestForTop10BorrowingStocksResponse:
        """[ka10069] 대차거래상위10종목요청 (국내주식 - 대차거래)"""
        raw_response = self.client.call("ka10069", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForTop10BorrowingStocksResponse(**raw_response)

    def request_for_loan_lending_transaction_trend_by_item(self, req: RequestForLoanLendingTransactionTrendByItemRequest) -> RequestForLoanLendingTransactionTrendByItemResponse:
        """[ka20068] 대차거래추이요청(종목별) (국내주식 - 대차거래)"""
        raw_response = self.client.call("ka20068", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForLoanLendingTransactionTrendByItemResponse(**raw_response)

    def request_for_loan_transaction_details(self, req: RequestForLoanTransactionDetailsRequest) -> RequestForLoanTransactionDetailsResponse:
        """[ka90012] 대차거래내역요청 (국내주식 - 대차거래)"""
        raw_response = self.client.call("ka90012", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForLoanTransactionDetailsResponse(**raw_response)

    def request_for_higher_quota_balance(self, req: RequestForHigherQuotaBalanceRequest) -> RequestForHigherQuotaBalanceResponse:
        """[ka10020] 호가잔량상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10020", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForHigherQuotaBalanceResponse(**raw_response)

    def request_for_sudden_increase_in_quotation_balance(self, req: RequestForSuddenIncreaseInQuotationBalanceRequest) -> RequestForSuddenIncreaseInQuotationBalanceResponse:
        """[ka10021] 호가잔량급증요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10021", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSuddenIncreaseInQuotationBalanceResponse(**raw_response)

    def request_for_sudden_increase_in_remaining_capacity(self, req: RequestForSuddenIncreaseInRemainingCapacityRequest) -> RequestForSuddenIncreaseInRemainingCapacityResponse:
        """[ka10022] 잔량율급증요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10022", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSuddenIncreaseInRemainingCapacityResponse(**raw_response)

    def request_for_sudden_increase_in_trading_volume(self, req: RequestForSuddenIncreaseInTradingVolumeRequest) -> RequestForSuddenIncreaseInTradingVolumeResponse:
        """[ka10023] 거래량급증요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10023", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSuddenIncreaseInTradingVolumeResponse(**raw_response)

    def request_for_higher_fluctuation_rate_compared_to_the_previous_day(self, req: RequestForHigherFluctuationRateComparedToThePreviousDayRequest) -> RequestForHigherFluctuationRateComparedToThePreviousDayResponse:
        """[ka10027] 전일대비등락률상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10027", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForHigherFluctuationRateComparedToThePreviousDayResponse(**raw_response)

    def request_for_higher_expected_transaction_rate(self, req: RequestForHigherExpectedTransactionRateRequest) -> RequestForHigherExpectedTransactionRateResponse:
        """[ka10029] 예상체결등락률상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10029", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForHigherExpectedTransactionRateResponse(**raw_response)

    def high_transaction_volume_request_for_the_day(self, req: HighTransactionVolumeRequestForTheDayRequest) -> HighTransactionVolumeRequestForTheDayResponse:
        """[ka10030] 당일거래량상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10030", **req.model_dump(by_alias=True, exclude_none=True))
        return HighTransactionVolumeRequestForTheDayResponse(**raw_response)

    def request_for_the_previous_day_s_highest_trading_volume(self, req: RequestForThePreviousDaySHighestTradingVolumeRequest) -> RequestForThePreviousDaySHighestTradingVolumeResponse:
        """[ka10031] 전일거래량상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10031", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForThePreviousDaySHighestTradingVolumeResponse(**raw_response)

    def request_for_higher_transaction_amount(self, req: RequestForHigherTransactionAmountRequest) -> RequestForHigherTransactionAmountResponse:
        """[ka10032] 거래대금상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10032", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForHigherTransactionAmountResponse(**raw_response)

    def request_for_higher_credit_ratio(self, req: RequestForHigherCreditRatioRequest) -> RequestForHigherCreditRatioResponse:
        """[ka10033] 신용비율상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10033", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForHigherCreditRatioResponse(**raw_response)

    def external_transaction_top_sales_request_by_period(self, req: ExternalTransactionTopSalesRequestByPeriodRequest) -> ExternalTransactionTopSalesRequestByPeriodResponse:
        """[ka10034] 외인기간별매매상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10034", **req.model_dump(by_alias=True, exclude_none=True))
        return ExternalTransactionTopSalesRequestByPeriodResponse(**raw_response)

    def foreign_continuous_net_sales_top_request(self, req: ForeignContinuousNetSalesTopRequestRequest) -> ForeignContinuousNetSalesTopRequestResponse:
        """[ka10035] 외인연속순매매상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10035", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignContinuousNetSalesTopRequestResponse(**raw_response)

    def top_foreign_limit_burnout_rate_increase(self, req: TopForeignLimitBurnoutRateIncreaseRequest) -> TopForeignLimitBurnoutRateIncreaseResponse:
        """[ka10036] 외인한도소진율증가상위 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10036", **req.model_dump(by_alias=True, exclude_none=True))
        return TopForeignLimitBurnoutRateIncreaseResponse(**raw_response)

    def foreign_over_the_counter_sales_request(self, req: ForeignOverTheCounterSalesRequestRequest) -> ForeignOverTheCounterSalesRequestResponse:
        """[ka10037] 외국계창구매매상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10037", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignOverTheCounterSalesRequestResponse(**raw_response)

    def request_ranking_of_securities_companies_by_stock(self, req: RequestRankingOfSecuritiesCompaniesByStockRequest) -> RequestRankingOfSecuritiesCompaniesByStockResponse:
        """[ka10038] 종목별증권사순위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10038", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestRankingOfSecuritiesCompaniesByStockResponse(**raw_response)

    def top_trading_request_by_securities_company(self, req: TopTradingRequestBySecuritiesCompanyRequest) -> TopTradingRequestBySecuritiesCompanyResponse:
        """[ka10039] 증권사별매매상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10039", **req.model_dump(by_alias=True, exclude_none=True))
        return TopTradingRequestBySecuritiesCompanyResponse(**raw_response)

    def same_day_major_transaction_request(self, req: SameDayMajorTransactionRequestRequest) -> SameDayMajorTransactionRequestResponse:
        """[ka10040] 당일주요거래원요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10040", **req.model_dump(by_alias=True, exclude_none=True))
        return SameDayMajorTransactionRequestResponse(**raw_response)

    def net_buying_trader_ranking_request(self, req: NetBuyingTraderRankingRequestRequest) -> NetBuyingTraderRankingRequestResponse:
        """[ka10042] 순매수거래원순위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10042", **req.model_dump(by_alias=True, exclude_none=True))
        return NetBuyingTraderRankingRequestResponse(**raw_response)

    def request_for_same_day_high_withdrawal(self, req: RequestForSameDayHighWithdrawalRequest) -> RequestForSameDayHighWithdrawalResponse:
        """[ka10053] 당일상위이탈원요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10053", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSameDayHighWithdrawalResponse(**raw_response)

    def request_for_same_net_sales_ranking(self, req: RequestForSameNetSalesRankingRequest) -> RequestForSameNetSalesRankingResponse:
        """[ka10062] 동일순매매순위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10062", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSameNetSalesRankingResponse(**raw_response)

    def intraday_trading_request_by_investor(self, req: IntradayTradingRequestByInvestorRequest) -> IntradayTradingRequestByInvestorResponse:
        """[ka10065] 장중투자자별매매상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10065", **req.model_dump(by_alias=True, exclude_none=True))
        return IntradayTradingRequestByInvestorResponse(**raw_response)

    def request_for_ranking_of_out_of_hours_single_price_fluctuation_rate(self, req: RequestForRankingOfOutOfHoursSinglePriceFluctuationRateRequest) -> RequestForRankingOfOutOfHoursSinglePriceFluctuationRateResponse:
        """[ka10098] 시간외단일가등락율순위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka10098", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForRankingOfOutOfHoursSinglePriceFluctuationRateResponse(**raw_response)

    def foreign_institutional_trading_top_request(self, req: ForeignInstitutionalTradingTopRequestRequest) -> ForeignInstitutionalTradingTopRequestResponse:
        """[ka90009] 외국인기관매매상위요청 (국내주식 - 순위정보)"""
        raw_response = self.client.call("ka90009", **req.model_dump(by_alias=True, exclude_none=True))
        return ForeignInstitutionalTradingTopRequestResponse(**raw_response)

    def stock_quote_request(self, req: StockQuoteRequestRequest) -> StockQuoteRequestResponse:
        """[ka10004] 주식호가요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10004", **req.model_dump(by_alias=True, exclude_none=True))
        return StockQuoteRequestResponse(**raw_response)

    def stock_weekly_monthly_and_hourly_minutes_request(self, req: StockWeeklyMonthlyAndHourlyMinutesRequestRequest) -> StockWeeklyMonthlyAndHourlyMinutesRequestResponse:
        """[ka10005] 주식일주월시분요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10005", **req.model_dump(by_alias=True, exclude_none=True))
        return StockWeeklyMonthlyAndHourlyMinutesRequestResponse(**raw_response)

    def stock_time_request(self, req: StockTimeRequestRequest) -> StockTimeRequestResponse:
        """[ka10006] 주식시분요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10006", **req.model_dump(by_alias=True, exclude_none=True))
        return StockTimeRequestResponse(**raw_response)

    def request_for_price_information(self, req: RequestForPriceInformationRequest) -> RequestForPriceInformationResponse:
        """[ka10007] 시세표성정보요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10007", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForPriceInformationResponse(**raw_response)

    def request_to_view_all_new_stock_warrants(self, req: RequestToViewAllNewStockWarrantsRequest) -> RequestToViewAllNewStockWarrantsResponse:
        """[ka10011] 신주인수권전체시세요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10011", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestToViewAllNewStockWarrantsResponse(**raw_response)

    def request_for_daily_institutional_trading_items(self, req: RequestForDailyInstitutionalTradingItemsRequest) -> RequestForDailyInstitutionalTradingItemsResponse:
        """[ka10044] 일별기관매매종목요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10044", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForDailyInstitutionalTradingItemsResponse(**raw_response)

    def request_for_institutional_trading_trend_by_item(self, req: RequestForInstitutionalTradingTrendByItemRequest) -> RequestForInstitutionalTradingTrendByItemResponse:
        """[ka10045] 종목별기관매매추이요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10045", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForInstitutionalTradingTrendByItemResponse(**raw_response)

    def request_for_fastening_strength_trend_by_time(self, req: RequestForFasteningStrengthTrendByTimeRequest) -> RequestForFasteningStrengthTrendByTimeResponse:
        """[ka10046] 체결강도추이시간별요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10046", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForFasteningStrengthTrendByTimeResponse(**raw_response)

    def request_for_daily_tightening_strength_trend(self, req: RequestForDailyTighteningStrengthTrendRequest) -> RequestForDailyTighteningStrengthTrendResponse:
        """[ka10047] 체결강도추이일별요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10047", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForDailyTighteningStrengthTrendResponse(**raw_response)

    def intraday_investor_specific_trading_request(self, req: IntradayInvestorSpecificTradingRequestRequest) -> IntradayInvestorSpecificTradingRequestResponse:
        """[ka10063] 장중투자자별매매요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10063", **req.model_dump(by_alias=True, exclude_none=True))
        return IntradayInvestorSpecificTradingRequestResponse(**raw_response)

    def request_for_trading_by_investor_after_market_close(self, req: RequestForTradingByInvestorAfterMarketCloseRequest) -> RequestForTradingByInvestorAfterMarketCloseResponse:
        """[ka10066] 장마감후투자자별매매요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10066", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForTradingByInvestorAfterMarketCloseResponse(**raw_response)

    def request_for_stock_trading_trends_by_securities_company(self, req: RequestForStockTradingTrendsBySecuritiesCompanyRequest) -> RequestForStockTradingTrendsBySecuritiesCompanyResponse:
        """[ka10078] 증권사별종목매매동향요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10078", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForStockTradingTrendsBySecuritiesCompanyResponse(**raw_response)

    def daily_stock_request(self, req: DailyStockRequestRequest) -> DailyStockRequestResponse:
        """[ka10086] 일별주가요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10086", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyStockRequestResponse(**raw_response)

    def single_request_after_hours(self, req: SingleRequestAfterHoursRequest) -> SingleRequestAfterHoursResponse:
        """[ka10087] 시간외단일가요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka10087", **req.model_dump(by_alias=True, exclude_none=True))
        return SingleRequestAfterHoursResponse(**raw_response)

    def gold_spot_trading_trend(self, req: GoldSpotTradingTrendRequest) -> GoldSpotTradingTrendResponse:
        """[ka50010] 금현물체결추이 (국내주식 - 시세)"""
        raw_response = self.client.call("ka50010", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotTradingTrendResponse(**raw_response)

    def spot_gold_daily_trend(self, req: SpotGoldDailyTrendRequest) -> SpotGoldDailyTrendResponse:
        """[ka50012] 금현물일별추이 (국내주식 - 시세)"""
        raw_response = self.client.call("ka50012", **req.model_dump(by_alias=True, exclude_none=True))
        return SpotGoldDailyTrendResponse(**raw_response)

    def gold_spot_expected_transaction(self, req: GoldSpotExpectedTransactionRequest) -> GoldSpotExpectedTransactionResponse:
        """[ka50087] 금현물예상체결 (국내주식 - 시세)"""
        raw_response = self.client.call("ka50087", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotExpectedTransactionResponse(**raw_response)

    def gold_spot_price_information(self, req: GoldSpotPriceInformationRequest) -> GoldSpotPriceInformationResponse:
        """[ka50100] 금현물 시세정보 (국내주식 - 시세)"""
        raw_response = self.client.call("ka50100", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotPriceInformationResponse(**raw_response)

    def gold_spot_quote(self, req: GoldSpotQuoteRequest) -> GoldSpotQuoteResponse:
        """[ka50101] 금현물 호가 (국내주식 - 시세)"""
        raw_response = self.client.call("ka50101", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotQuoteResponse(**raw_response)

    def program_trading_trend_request_by_time_zone(self, req: ProgramTradingTrendRequestByTimeZoneRequest) -> ProgramTradingTrendRequestByTimeZoneResponse:
        """[ka90005] 프로그램매매추이요청 시간대별 (국내주식 - 시세)"""
        raw_response = self.client.call("ka90005", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingTrendRequestByTimeZoneResponse(**raw_response)

    def program_trading_profit_balance_trend_request(self, req: ProgramTradingProfitBalanceTrendRequestRequest) -> ProgramTradingProfitBalanceTrendRequestResponse:
        """[ka90006] 프로그램매매차익잔고추이요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka90006", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingProfitBalanceTrendRequestResponse(**raw_response)

    def request_for_cumulative_program_trading_trend(self, req: RequestForCumulativeProgramTradingTrendRequest) -> RequestForCumulativeProgramTradingTrendResponse:
        """[ka90007] 프로그램매매누적추이요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka90007", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForCumulativeProgramTradingTrendResponse(**raw_response)

    def request_for_program_trading_trend_by_item_time(self, req: RequestForProgramTradingTrendByItemTimeRequest) -> RequestForProgramTradingTrendByItemTimeResponse:
        """[ka90008] 종목시간별프로그램매매추이요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka90008", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForProgramTradingTrendByItemTimeResponse(**raw_response)

    def program_trading_trend_request_date(self, req: ProgramTradingTrendRequestDateRequest) -> ProgramTradingTrendRequestDateResponse:
        """[ka90010] 프로그램매매추이요청 일자별 (국내주식 - 시세)"""
        raw_response = self.client.call("ka90010", **req.model_dump(by_alias=True, exclude_none=True))
        return ProgramTradingTrendRequestDateResponse(**raw_response)

    def request_daily_program_trading_trend_for_items(self, req: RequestDailyProgramTradingTrendForItemsRequest) -> RequestDailyProgramTradingTrendForItemsResponse:
        """[ka90013] 종목일별프로그램매매추이요청 (국내주식 - 시세)"""
        raw_response = self.client.call("ka90013", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestDailyProgramTradingTrendForItemsResponse(**raw_response)

    def credit_buy_order(self, req: CreditBuyOrderRequest) -> CreditBuyOrderResponse:
        """[kt10006] 신용 매수주문 (국내주식 - 신용주문)"""
        raw_response = self.client.call("kt10006", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditBuyOrderResponse(**raw_response)

    def credit_sell_order(self, req: CreditSellOrderRequest) -> CreditSellOrderResponse:
        """[kt10007] 신용 매도주문 (국내주식 - 신용주문)"""
        raw_response = self.client.call("kt10007", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditSellOrderResponse(**raw_response)

    def credit_correction_order(self, req: CreditCorrectionOrderRequest) -> CreditCorrectionOrderResponse:
        """[kt10008] 신용 정정주문 (국내주식 - 신용주문)"""
        raw_response = self.client.call("kt10008", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditCorrectionOrderResponse(**raw_response)

    def credit_cancellation_order(self, req: CreditCancellationOrderRequest) -> CreditCancellationOrderResponse:
        """[kt10009] 신용 취소주문 (국내주식 - 신용주문)"""
        raw_response = self.client.call("kt10009", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditCancellationOrderResponse(**raw_response)

    async def order_execution(self, req: OrderExecutionRequest):
        """[00] 주문체결 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def balance(self, req: BalanceRequest):
        """[04] 잔고 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_momentum(self, req: StockMomentumRequest):
        """[0A] 주식기세 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_signing(self, req: StockSigningRequest):
        """[0B] 주식체결 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_preferred_price(self, req: StockPreferredPriceRequest):
        """[0C] 주식우선호가 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_quote_balance(self, req: StockQuoteBalanceRequest):
        """[0D] 주식호가잔량 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_after_hours_quote(self, req: StockAfterHoursQuoteRequest):
        """[0E] 주식시간외호가 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_day_trader(self, req: StockDayTraderRequest):
        """[0F] 주식당일거래원 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def etf_nav(self, req: EtfNavRequest):
        """[0G] ETF NAV (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_expected_execution(self, req: StockExpectedExecutionRequest):
        """[0H] 주식예상체결 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def international_gold_conversion_price(self, req: InternationalGoldConversionPriceRequest):
        """[0I] 국제금환산가격 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def sector_index(self, req: SectorIndexRequest):
        """[0J] 업종지수 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def industry_fluctuations(self, req: IndustryFluctuationsRequest):
        """[0U] 업종등락 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_item_information(self, req: StockItemInformationRequest):
        """[0g] 주식종목정보 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def elw_theorist(self, req: ElwTheoristRequest):
        """[0m] ELW 이론가 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def long_start_time(self, req: LongStartTimeRequest):
        """[0s] 장시작시간 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def elw_indicator(self, req: ElwIndicatorRequest):
        """[0u] ELW 지표 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def stock_program_trading(self, req: StockProgramTradingRequest):
        """[0w] 종목프로그램매매 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def activate_disable_vi(self, req: ActivateDisableViRequest):
        """[1h] VI발동/해제 (국내주식 - 실시간시세)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    def industry_program_request(self, req: IndustryProgramRequestRequest) -> IndustryProgramRequestResponse:
        """[ka10010] 업종프로그램요청 (국내주식 - 업종)"""
        raw_response = self.client.call("ka10010", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryProgramRequestResponse(**raw_response)

    def investor_net_purchase_request_by_industry(self, req: InvestorNetPurchaseRequestByIndustryRequest) -> InvestorNetPurchaseRequestByIndustryResponse:
        """[ka10051] 업종별투자자순매수요청 (국내주식 - 업종)"""
        raw_response = self.client.call("ka10051", **req.model_dump(by_alias=True, exclude_none=True))
        return InvestorNetPurchaseRequestByIndustryResponse(**raw_response)

    def current_industry_request(self, req: CurrentIndustryRequestRequest) -> CurrentIndustryRequestResponse:
        """[ka20001] 업종현재가요청 (국내주식 - 업종)"""
        raw_response = self.client.call("ka20001", **req.model_dump(by_alias=True, exclude_none=True))
        return CurrentIndustryRequestResponse(**raw_response)

    def request_for_stocks_by_industry(self, req: RequestForStocksByIndustryRequest) -> RequestForStocksByIndustryResponse:
        """[ka20002] 업종별주가요청 (국내주식 - 업종)"""
        raw_response = self.client.call("ka20002", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForStocksByIndustryResponse(**raw_response)

    def request_for_all_industry_indices(self, req: RequestForAllIndustryIndicesRequest) -> RequestForAllIndustryIndicesResponse:
        """[ka20003] 전업종지수요청 (국내주식 - 업종)"""
        raw_response = self.client.call("ka20003", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForAllIndustryIndicesResponse(**raw_response)

    def industry_current_price_daily_request(self, req: IndustryCurrentPriceDailyRequestRequest) -> IndustryCurrentPriceDailyRequestResponse:
        """[ka20009] 업종현재가일별요청 (국내주식 - 업종)"""
        raw_response = self.client.call("ka20009", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryCurrentPriceDailyRequestResponse(**raw_response)

    async def condition_search_list_inquiry(self, req: ConditionSearchListInquiryRequest):
        """[ka10171] 조건검색 목록조회 (국내주식 - 조건검색)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def conditional_search_request_general(self, req: ConditionalSearchRequestGeneralRequest):
        """[ka10172] 조건검색 요청 일반 (국내주식 - 조건검색)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def real_time_conditional_search_request(self, req: RealTimeConditionalSearchRequestRequest):
        """[ka10173] 조건검색 요청 실시간 (국내주식 - 조건검색)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    async def conditional_search_real_time_cancellation(self, req: ConditionalSearchRealTimeCancellationRequest):
        """[ka10174] 조건검색 실시간 해제 (국내주식 - 조건검색)"""
        await self.client.send_ws(req.model_dump(by_alias=True, exclude_none=True))

    def real_time_item_inquiry_ranking(self, req: RealTimeItemInquiryRankingRequest) -> RealTimeItemInquiryRankingResponse:
        """[ka00198] 실시간종목조회순위 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka00198", **req.model_dump(by_alias=True, exclude_none=True))
        return RealTimeItemInquiryRankingResponse(**raw_response)

    def request_for_basic_stock_information(self, req: RequestForBasicStockInformationRequest) -> RequestForBasicStockInformationResponse:
        """[ka10001] 주식기본정보요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10001", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForBasicStockInformationResponse(**raw_response)

    def stock_exchange_request(self, req: StockExchangeRequestRequest) -> StockExchangeRequestResponse:
        """[ka10002] 주식거래원요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10002", **req.model_dump(by_alias=True, exclude_none=True))
        return StockExchangeRequestResponse(**raw_response)

    def request_for_conclusion_information(self, req: RequestForConclusionInformationRequest) -> RequestForConclusionInformationResponse:
        """[ka10003] 체결정보요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10003", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForConclusionInformationResponse(**raw_response)

    def credit_trading_trend_request(self, req: CreditTradingTrendRequestRequest) -> CreditTradingTrendRequestResponse:
        """[ka10013] 신용매매동향요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10013", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditTradingTrendRequestResponse(**raw_response)

    def daily_transaction_request(self, req: DailyTransactionRequestRequest) -> DailyTransactionRequestResponse:
        """[ka10015] 일별거래상세요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10015", **req.model_dump(by_alias=True, exclude_none=True))
        return DailyTransactionRequestResponse(**raw_response)

    def request_for_low_report(self, req: RequestForLowReportRequest) -> RequestForLowReportResponse:
        """[ka10016] 신고저가요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10016", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForLowReportResponse(**raw_response)

    def request_for_upper_and_lower_limits(self, req: RequestForUpperAndLowerLimitsRequest) -> RequestForUpperAndLowerLimitsResponse:
        """[ka10017] 상하한가요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10017", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForUpperAndLowerLimitsResponse(**raw_response)

    def high_and_low_price_proximity_request(self, req: HighAndLowPriceProximityRequestRequest) -> HighAndLowPriceProximityRequestResponse:
        """[ka10018] 고저가근접요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10018", **req.model_dump(by_alias=True, exclude_none=True))
        return HighAndLowPriceProximityRequestResponse(**raw_response)

    def request_for_sudden_price_fluctuation(self, req: RequestForSuddenPriceFluctuationRequest) -> RequestForSuddenPriceFluctuationResponse:
        """[ka10019] 가격급등락요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10019", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSuddenPriceFluctuationResponse(**raw_response)

    def transaction_volume_update_request(self, req: TransactionVolumeUpdateRequestRequest) -> TransactionVolumeUpdateRequestResponse:
        """[ka10024] 거래량갱신요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10024", **req.model_dump(by_alias=True, exclude_none=True))
        return TransactionVolumeUpdateRequestResponse(**raw_response)

    def request_for_concentration_of_properties_for_sale(self, req: RequestForConcentrationOfPropertiesForSaleRequest) -> RequestForConcentrationOfPropertiesForSaleResponse:
        """[ka10025] 매물대집중요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10025", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForConcentrationOfPropertiesForSaleResponse(**raw_response)

    def request_for_high_and_low_per(self, req: RequestForHighAndLowPerRequest) -> RequestForHighAndLowPerResponse:
        """[ka10026] 고저PER요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10026", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForHighAndLowPerResponse(**raw_response)

    def request_for_fluctuation_rate_compared_to_market_price(self, req: RequestForFluctuationRateComparedToMarketPriceRequest) -> RequestForFluctuationRateComparedToMarketPriceResponse:
        """[ka10028] 시가대비등락률요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10028", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForFluctuationRateComparedToMarketPriceResponse(**raw_response)

    def request_for_transaction_price_analysis(self, req: RequestForTransactionPriceAnalysisRequest) -> RequestForTransactionPriceAnalysisResponse:
        """[ka10043] 거래원매물대분석요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10043", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForTransactionPriceAnalysisResponse(**raw_response)

    def trader_instantaneous_trading_volume_request(self, req: TraderInstantaneousTradingVolumeRequestRequest) -> TraderInstantaneousTradingVolumeRequestResponse:
        """[ka10052] 거래원순간거래량요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10052", **req.model_dump(by_alias=True, exclude_none=True))
        return TraderInstantaneousTradingVolumeRequestResponse(**raw_response)

    def request_for_items_to_activate_volatility_mitigation_device(self, req: RequestForItemsToActivateVolatilityMitigationDeviceRequest) -> RequestForItemsToActivateVolatilityMitigationDeviceResponse:
        """[ka10054] 변동성완화장치발동종목요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10054", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForItemsToActivateVolatilityMitigationDeviceResponse(**raw_response)

    def request_for_settlement_the_day_before_the_day(self, req: RequestForSettlementTheDayBeforeTheDayRequest) -> RequestForSettlementTheDayBeforeTheDayResponse:
        """[ka10055] 당일전일체결량요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10055", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSettlementTheDayBeforeTheDayResponse(**raw_response)

    def request_for_daily_trading_items_by_investor(self, req: RequestForDailyTradingItemsByInvestorRequest) -> RequestForDailyTradingItemsByInvestorResponse:
        """[ka10058] 투자자별일별매매종목요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10058", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForDailyTradingItemsByInvestorResponse(**raw_response)

    def requests_by_item_and_investor_institution(self, req: RequestsByItemAndInvestorInstitutionRequest) -> RequestsByItemAndInvestorInstitutionResponse:
        """[ka10059] 종목별투자자기관별요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10059", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestsByItemAndInvestorInstitutionResponse(**raw_response)

    def total_request_by_item_and_investor_institution(self, req: TotalRequestByItemAndInvestorInstitutionRequest) -> TotalRequestByItemAndInvestorInstitutionResponse:
        """[ka10061] 종목별투자자기관별합계요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10061", **req.model_dump(by_alias=True, exclude_none=True))
        return TotalRequestByItemAndInvestorInstitutionResponse(**raw_response)

    def request_for_settlement_the_day_before_the_same_day(self, req: RequestForSettlementTheDayBeforeTheSameDayRequest) -> RequestForSettlementTheDayBeforeTheSameDayResponse:
        """[ka10084] 당일전일체결요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10084", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSettlementTheDayBeforeTheSameDayResponse(**raw_response)

    def request_information_on_items_of_interest(self, req: RequestInformationOnItemsOfInterestRequest) -> RequestInformationOnItemsOfInterestResponse:
        """[ka10095] 관심종목정보요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10095", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestInformationOnItemsOfInterestResponse(**raw_response)

    def stock_information_list(self, req: StockInformationListRequest) -> StockInformationListResponse:
        """[ka10099] 종목정보 리스트 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10099", **req.model_dump(by_alias=True, exclude_none=True))
        return StockInformationListResponse(**raw_response)

    def check_stock_information(self, req: CheckStockInformationRequest) -> CheckStockInformationResponse:
        """[ka10100] 종목정보 조회 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10100", **req.model_dump(by_alias=True, exclude_none=True))
        return CheckStockInformationResponse(**raw_response)

    def industry_code_list(self, req: IndustryCodeListRequest) -> IndustryCodeListResponse:
        """[ka10101] 업종코드 리스트 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10101", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryCodeListResponse(**raw_response)

    def member_company_list(self, req: MemberCompanyListRequest) -> MemberCompanyListResponse:
        """[ka10102] 회원사 리스트 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka10102", **req.model_dump(by_alias=True, exclude_none=True))
        return MemberCompanyListResponse(**raw_response)

    def request_for_top50_program_net_purchases(self, req: RequestForTop50ProgramNetPurchasesRequest) -> RequestForTop50ProgramNetPurchasesResponse:
        """[ka90003] 프로그램순매수상위50요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka90003", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForTop50ProgramNetPurchasesResponse(**raw_response)

    def request_for_program_trading_status_by_item(self, req: RequestForProgramTradingStatusByItemRequest) -> RequestForProgramTradingStatusByItemResponse:
        """[ka90004] 종목별프로그램매매현황요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("ka90004", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForProgramTradingStatusByItemResponse(**raw_response)

    def request_for_credit_loan_available_items(self, req: RequestForCreditLoanAvailableItemsRequest) -> RequestForCreditLoanAvailableItemsResponse:
        """[kt20016] 신용융자 가능종목요청 (국내주식 - 종목정보)"""
        raw_response = self.client.call("kt20016", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForCreditLoanAvailableItemsResponse(**raw_response)

    def credit_loan_availability_inquiry(self, req: CreditLoanAvailabilityInquiryRequest) -> CreditLoanAvailabilityInquiryResponse:
        """[kt20017] 신용융자 가능문의 (국내주식 - 종목정보)"""
        raw_response = self.client.call("kt20017", **req.model_dump(by_alias=True, exclude_none=True))
        return CreditLoanAvailabilityInquiryResponse(**raw_response)

    def stock_purchase_order(self, req: StockPurchaseOrderRequest) -> StockPurchaseOrderResponse:
        """[kt10000] 주식 매수주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt10000", **req.model_dump(by_alias=True, exclude_none=True))
        return StockPurchaseOrderResponse(**raw_response)

    def stock_sell_order(self, req: StockSellOrderRequest) -> StockSellOrderResponse:
        """[kt10001] 주식 매도주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt10001", **req.model_dump(by_alias=True, exclude_none=True))
        return StockSellOrderResponse(**raw_response)

    def stock_correction_order(self, req: StockCorrectionOrderRequest) -> StockCorrectionOrderResponse:
        """[kt10002] 주식 정정주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt10002", **req.model_dump(by_alias=True, exclude_none=True))
        return StockCorrectionOrderResponse(**raw_response)

    def stock_cancellation_order(self, req: StockCancellationOrderRequest) -> StockCancellationOrderResponse:
        """[kt10003] 주식 취소주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt10003", **req.model_dump(by_alias=True, exclude_none=True))
        return StockCancellationOrderResponse(**raw_response)

    def gold_spot_purchase_order(self, req: GoldSpotPurchaseOrderRequest) -> GoldSpotPurchaseOrderResponse:
        """[kt50000] 금현물 매수주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt50000", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotPurchaseOrderResponse(**raw_response)

    def gold_spot_sell_order(self, req: GoldSpotSellOrderRequest) -> GoldSpotSellOrderResponse:
        """[kt50001] 금현물 매도주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt50001", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotSellOrderResponse(**raw_response)

    def spot_gold_correction_order(self, req: SpotGoldCorrectionOrderRequest) -> SpotGoldCorrectionOrderResponse:
        """[kt50002] 금현물 정정주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt50002", **req.model_dump(by_alias=True, exclude_none=True))
        return SpotGoldCorrectionOrderResponse(**raw_response)

    def gold_spot_cancellation_order(self, req: GoldSpotCancellationOrderRequest) -> GoldSpotCancellationOrderResponse:
        """[kt50003] 금현물 취소주문 (국내주식 - 주문)"""
        raw_response = self.client.call("kt50003", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotCancellationOrderResponse(**raw_response)

    def chart_request_by_item_and_investor_institution(self, req: ChartRequestByItemAndInvestorInstitutionRequest) -> ChartRequestByItemAndInvestorInstitutionResponse:
        """[ka10060] 종목별투자자기관별차트요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10060", **req.model_dump(by_alias=True, exclude_none=True))
        return ChartRequestByItemAndInvestorInstitutionResponse(**raw_response)

    def intraday_investor_specific_trading_chart_request(self, req: IntradayInvestorSpecificTradingChartRequestRequest) -> IntradayInvestorSpecificTradingChartRequestResponse:
        """[ka10064] 장중투자자별매매차트요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10064", **req.model_dump(by_alias=True, exclude_none=True))
        return IntradayInvestorSpecificTradingChartRequestResponse(**raw_response)

    def stock_tick_chart_inquiry_request(self, req: StockTickChartInquiryRequestRequest) -> StockTickChartInquiryRequestResponse:
        """[ka10079] 주식틱차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10079", **req.model_dump(by_alias=True, exclude_none=True))
        return StockTickChartInquiryRequestResponse(**raw_response)

    def request_to_view_stock_chart(self, req: RequestToViewStockChartRequest) -> RequestToViewStockChartResponse:
        """[ka10080] 주식분봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10080", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestToViewStockChartResponse(**raw_response)

    def stock_daily_chart_inquiry_request(self, req: StockDailyChartInquiryRequestRequest) -> StockDailyChartInquiryRequestResponse:
        """[ka10081] 주식일봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10081", **req.model_dump(by_alias=True, exclude_none=True))
        return StockDailyChartInquiryRequestResponse(**raw_response)

    def stock_weekly_chart_inquiry_request(self, req: StockWeeklyChartInquiryRequestRequest) -> StockWeeklyChartInquiryRequestResponse:
        """[ka10082] 주식주봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10082", **req.model_dump(by_alias=True, exclude_none=True))
        return StockWeeklyChartInquiryRequestResponse(**raw_response)

    def stock_monthly_chart_inquiry_request(self, req: StockMonthlyChartInquiryRequestRequest) -> StockMonthlyChartInquiryRequestResponse:
        """[ka10083] 주식월봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10083", **req.model_dump(by_alias=True, exclude_none=True))
        return StockMonthlyChartInquiryRequestResponse(**raw_response)

    def stock_annual_chart_inquiry_request(self, req: StockAnnualChartInquiryRequestRequest) -> StockAnnualChartInquiryRequestResponse:
        """[ka10094] 주식년봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka10094", **req.model_dump(by_alias=True, exclude_none=True))
        return StockAnnualChartInquiryRequestResponse(**raw_response)

    def industry_tick_chart_inquiry_request(self, req: IndustryTickChartInquiryRequestRequest) -> IndustryTickChartInquiryRequestResponse:
        """[ka20004] 업종틱차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka20004", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryTickChartInquiryRequestResponse(**raw_response)

    def industry_division_inquiry_request(self, req: IndustryDivisionInquiryRequestRequest) -> IndustryDivisionInquiryRequestResponse:
        """[ka20005] 업종분봉조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka20005", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryDivisionInquiryRequestResponse(**raw_response)

    def industry_daily_salary_inquiry_request(self, req: IndustryDailySalaryInquiryRequestRequest) -> IndustryDailySalaryInquiryRequestResponse:
        """[ka20006] 업종일봉조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka20006", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryDailySalaryInquiryRequestResponse(**raw_response)

    def request_for_industry_salary_inquiry(self, req: RequestForIndustrySalaryInquiryRequest) -> RequestForIndustrySalaryInquiryResponse:
        """[ka20007] 업종주봉조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka20007", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForIndustrySalaryInquiryResponse(**raw_response)

    def industry_monthly_salary_inquiry_request(self, req: IndustryMonthlySalaryInquiryRequestRequest) -> IndustryMonthlySalaryInquiryRequestResponse:
        """[ka20008] 업종월봉조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka20008", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryMonthlySalaryInquiryRequestResponse(**raw_response)

    def industry_year_salary_inquiry_request(self, req: IndustryYearSalaryInquiryRequestRequest) -> IndustryYearSalaryInquiryRequestResponse:
        """[ka20019] 업종년봉조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka20019", **req.model_dump(by_alias=True, exclude_none=True))
        return IndustryYearSalaryInquiryRequestResponse(**raw_response)

    def gold_spot_tick_chart_inquiry_request(self, req: GoldSpotTickChartInquiryRequestRequest) -> GoldSpotTickChartInquiryRequestResponse:
        """[ka50079] 금현물틱차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50079", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotTickChartInquiryRequestResponse(**raw_response)

    def gold_spot_fractional_chart_inquiry_request(self, req: GoldSpotFractionalChartInquiryRequestRequest) -> GoldSpotFractionalChartInquiryRequestResponse:
        """[ka50080] 금현물분봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50080", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotFractionalChartInquiryRequestResponse(**raw_response)

    def gold_spot_daily_chart_inquiry_request(self, req: GoldSpotDailyChartInquiryRequestRequest) -> GoldSpotDailyChartInquiryRequestResponse:
        """[ka50081] 금현물일봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50081", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDailyChartInquiryRequestResponse(**raw_response)

    def gold_spot_weekly_chart_inquiry_request(self, req: GoldSpotWeeklyChartInquiryRequestRequest) -> GoldSpotWeeklyChartInquiryRequestResponse:
        """[ka50082] 금현물주봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50082", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotWeeklyChartInquiryRequestResponse(**raw_response)

    def gold_spot_monthly_chart_inquiry_request(self, req: GoldSpotMonthlyChartInquiryRequestRequest) -> GoldSpotMonthlyChartInquiryRequestResponse:
        """[ka50083] 금현물월봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50083", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotMonthlyChartInquiryRequestResponse(**raw_response)

    def gold_spot_daily_tick_chart_inquiry_request(self, req: GoldSpotDailyTickChartInquiryRequestRequest) -> GoldSpotDailyTickChartInquiryRequestResponse:
        """[ka50091] 금현물당일틱차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50091", **req.model_dump(by_alias=True, exclude_none=True))
        return GoldSpotDailyTickChartInquiryRequestResponse(**raw_response)

    def request_to_view_gold_spot_daily_chart(self, req: RequestToViewGoldSpotDailyChartRequest) -> RequestToViewGoldSpotDailyChartResponse:
        """[ka50092] 금현물당일분봉차트조회요청 (국내주식 - 차트)"""
        raw_response = self.client.call("ka50092", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestToViewGoldSpotDailyChartResponse(**raw_response)

    def requests_by_theme_group(self, req: RequestsByThemeGroupRequest) -> RequestsByThemeGroupResponse:
        """[ka90001] 테마그룹별요청 (국내주식 - 테마)"""
        raw_response = self.client.call("ka90001", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestsByThemeGroupResponse(**raw_response)

    def request_for_theme_items(self, req: RequestForThemeItemsRequest) -> RequestForThemeItemsResponse:
        """[ka90002] 테마구성종목요청 (국내주식 - 테마)"""
        raw_response = self.client.call("ka90002", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForThemeItemsResponse(**raw_response)

    def elw_daily_sensitivity_indicator_request(self, req: ElwDailySensitivityIndicatorRequestRequest) -> ElwDailySensitivityIndicatorRequestResponse:
        """[ka10048] ELW일별민감도지표요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka10048", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwDailySensitivityIndicatorRequestResponse(**raw_response)

    def elw_sensitivity_indicator_request(self, req: ElwSensitivityIndicatorRequestRequest) -> ElwSensitivityIndicatorRequestResponse:
        """[ka10050] ELW민감도지표요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka10050", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwSensitivityIndicatorRequestResponse(**raw_response)

    def request_for_sudden_fluctuation_in_elw_price(self, req: RequestForSuddenFluctuationInElwPriceRequest) -> RequestForSuddenFluctuationInElwPriceResponse:
        """[ka30001] ELW가격급등락요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30001", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForSuddenFluctuationInElwPriceResponse(**raw_response)

    def elw_net_sales_top_request_by_trader(self, req: ElwNetSalesTopRequestByTraderRequest) -> ElwNetSalesTopRequestByTraderResponse:
        """[ka30002] 거래원별ELW순매매상위요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30002", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwNetSalesTopRequestByTraderResponse(**raw_response)

    def request_daily_trend_of_elwlp_holdings(self, req: RequestDailyTrendOfElwlpHoldingsRequest) -> RequestDailyTrendOfElwlpHoldingsResponse:
        """[ka30003] ELWLP보유일별추이요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30003", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestDailyTrendOfElwlpHoldingsResponse(**raw_response)

    def elw_disparity_rate_request(self, req: ElwDisparityRateRequestRequest) -> ElwDisparityRateRequestResponse:
        """[ka30004] ELW괴리율요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30004", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwDisparityRateRequestResponse(**raw_response)

    def elw_condition_search_request(self, req: ElwConditionSearchRequestRequest) -> ElwConditionSearchRequestResponse:
        """[ka30005] ELW조건검색요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30005", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwConditionSearchRequestResponse(**raw_response)

    def elw_fluctuation_rate_ranking_request(self, req: ElwFluctuationRateRankingRequestRequest) -> ElwFluctuationRateRankingRequestResponse:
        """[ka30009] ELW등락율순위요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30009", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwFluctuationRateRankingRequestResponse(**raw_response)

    def elw_remaining_balance_ranking_request(self, req: ElwRemainingBalanceRankingRequestRequest) -> ElwRemainingBalanceRankingRequestResponse:
        """[ka30010] ELW잔량순위요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30010", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwRemainingBalanceRankingRequestResponse(**raw_response)

    def elw_proximity_rate_request(self, req: ElwProximityRateRequestRequest) -> ElwProximityRateRequestResponse:
        """[ka30011] ELW근접율요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30011", **req.model_dump(by_alias=True, exclude_none=True))
        return ElwProximityRateRequestResponse(**raw_response)

    def request_for_detailed_information_on_elw_items(self, req: RequestForDetailedInformationOnElwItemsRequest) -> RequestForDetailedInformationOnElwItemsResponse:
        """[ka30012] ELW종목상세정보요청 (국내주식 - ELW)"""
        raw_response = self.client.call("ka30012", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestForDetailedInformationOnElwItemsResponse(**raw_response)

    def etf_return_rate_request(self, req: EtfReturnRateRequestRequest) -> EtfReturnRateRequestResponse:
        """[ka40001] ETF수익율요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40001", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfReturnRateRequestResponse(**raw_response)

    def etf_item_information_request(self, req: EtfItemInformationRequestRequest) -> EtfItemInformationRequestResponse:
        """[ka40002] ETF종목정보요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40002", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfItemInformationRequestResponse(**raw_response)

    def etf_daily_trend_request(self, req: EtfDailyTrendRequestRequest) -> EtfDailyTrendRequestResponse:
        """[ka40003] ETF일별추이요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40003", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfDailyTrendRequestResponse(**raw_response)

    def request_full_etf_view(self, req: RequestFullEtfViewRequest) -> RequestFullEtfViewResponse:
        """[ka40004] ETF전체시세요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40004", **req.model_dump(by_alias=True, exclude_none=True))
        return RequestFullEtfViewResponse(**raw_response)

    def etf_time_zone_trend_request(self, req: EtfTimeZoneTrendRequestRequest) -> EtfTimeZoneTrendRequestResponse:
        """[ka40006] ETF시간대별추이요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40006", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTimeZoneTrendRequestResponse(**raw_response)

    def etf_trading_request_by_time_slot(self, req: EtfTradingRequestByTimeSlotRequest) -> EtfTradingRequestByTimeSlotResponse:
        """[ka40007] ETF시간대별체결요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40007", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTradingRequestByTimeSlotResponse(**raw_response)

    def etf_transaction_request_by_date(self, req: EtfTransactionRequestByDateRequest) -> EtfTransactionRequestByDateResponse:
        """[ka40008] ETF일자별체결요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40008", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTransactionRequestByDateResponse(**raw_response)

    def etf_trading_request_by_time_slot1(self, req: EtfTradingRequestByTimeSlot1Request) -> EtfTradingRequestByTimeSlot1Response:
        """[ka40009] ETF시간대별체결요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40009", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTradingRequestByTimeSlot1Response(**raw_response)

    def etf_time_zone_trend_request1(self, req: EtfTimeZoneTrendRequest1Request) -> EtfTimeZoneTrendRequest1Response:
        """[ka40010] ETF시간대별추이요청 (국내주식 - ETF)"""
        raw_response = self.client.call("ka40010", **req.model_dump(by_alias=True, exclude_none=True))
        return EtfTimeZoneTrendRequest1Response(**raw_response)

# ====================================================================
# 3. Registry (동적 호출을 위한 매핑)
# ====================================================================

API_ID_TO_METHOD: Dict[str, str] = {
    "au10001": "access_token_issuance",
    "au10002": "discard_access_token",
    "ka00001": "account_number_inquiry",
    "ka01690": "daily_balance_return_rate",
    "ka10072": "realized_profit_loss_request_by_date_item_date",
    "ka10073": "realized_profit_loss_request_by_date_and_item_period",
    "ka10074": "request_for_realized_profit_or_loss_by_date",
    "ka10075": "non_confirmation_request",
    "ka10076": "conclusion_request",
    "ka10077": "request_for_same_day_realized_profit_and_loss",
    "ka10085": "account_yield_request",
    "ka10088": "unfilled_split_order_details",
    "ka10170": "same_day_sales_log_request",
    "kt00001": "request_detailed_status_of_deposit",
    "kt00002": "daily_estimated_deposited_asset_status_request",
    "kt00003": "estimated_asset_inquiry_request",
    "kt00004": "request_for_account_evaluation_status",
    "kt00005": "request_for_transaction_balance",
    "kt00007": "request_details_on_order_details_by_account",
    "kt00008": "request_next_day_payment_schedule_details_for_each_account",
    "kt00009": "request_for_order_execution_status_by_account",
    "kt00010": "request_for_order_withdrawal_amount",
    "kt00011": "request_to_inquiry_quantity_available_for_order_by_margin_rate",
    "kt00012": "request_to_inquiry_quantity_available_for_order_by_credit_deposit_rate",
    "kt00013": "margin_details_inquiry_request",
    "kt00015": "request_for_comprehensive_consignment_transaction_details",
    "kt00016": "request_for_detailed_status_of_daily_account_returns",
    "kt00017": "request_daily_status_for_each_account",
    "kt00018": "request_for_account_evaluation_balance_details",
    "kt50020": "check_gold_spot_balance",
    "kt50021": "gold_spot_deposit",
    "kt50030": "view_all_gold_spot_orders",
    "kt50031": "gold_spot_order_execution_inquiry",
    "kt50032": "gold_spot_transaction_history_inquiry",
    "kt50075": "gold_spot_non_trading_inquiry",
    "ka10014": "short_selling_trend_request",
    "ka10008": "foreign_stock_trading_trends_by_item",
    "ka10009": "stock_institution_request",
    "ka10131": "request_for_status_of_continuous_trading_by_institutional_foreigners",
    "ka52301": "current_status_of_gold_spot_investors",
    "ka10068": "request_for_loan_lending_transaction_trend",
    "ka10069": "request_for_top10_borrowing_stocks",
    "ka20068": "request_for_loan_lending_transaction_trend_by_item",
    "ka90012": "request_for_loan_transaction_details",
    "ka10020": "request_for_higher_quota_balance",
    "ka10021": "request_for_sudden_increase_in_quotation_balance",
    "ka10022": "request_for_sudden_increase_in_remaining_capacity",
    "ka10023": "request_for_sudden_increase_in_trading_volume",
    "ka10027": "request_for_higher_fluctuation_rate_compared_to_the_previous_day",
    "ka10029": "request_for_higher_expected_transaction_rate",
    "ka10030": "high_transaction_volume_request_for_the_day",
    "ka10031": "request_for_the_previous_day_s_highest_trading_volume",
    "ka10032": "request_for_higher_transaction_amount",
    "ka10033": "request_for_higher_credit_ratio",
    "ka10034": "external_transaction_top_sales_request_by_period",
    "ka10035": "foreign_continuous_net_sales_top_request",
    "ka10036": "top_foreign_limit_burnout_rate_increase",
    "ka10037": "foreign_over_the_counter_sales_request",
    "ka10038": "request_ranking_of_securities_companies_by_stock",
    "ka10039": "top_trading_request_by_securities_company",
    "ka10040": "same_day_major_transaction_request",
    "ka10042": "net_buying_trader_ranking_request",
    "ka10053": "request_for_same_day_high_withdrawal",
    "ka10062": "request_for_same_net_sales_ranking",
    "ka10065": "intraday_trading_request_by_investor",
    "ka10098": "request_for_ranking_of_out_of_hours_single_price_fluctuation_rate",
    "ka90009": "foreign_institutional_trading_top_request",
    "ka10004": "stock_quote_request",
    "ka10005": "stock_weekly_monthly_and_hourly_minutes_request",
    "ka10006": "stock_time_request",
    "ka10007": "request_for_price_information",
    "ka10011": "request_to_view_all_new_stock_warrants",
    "ka10044": "request_for_daily_institutional_trading_items",
    "ka10045": "request_for_institutional_trading_trend_by_item",
    "ka10046": "request_for_fastening_strength_trend_by_time",
    "ka10047": "request_for_daily_tightening_strength_trend",
    "ka10063": "intraday_investor_specific_trading_request",
    "ka10066": "request_for_trading_by_investor_after_market_close",
    "ka10078": "request_for_stock_trading_trends_by_securities_company",
    "ka10086": "daily_stock_request",
    "ka10087": "single_request_after_hours",
    "ka50010": "gold_spot_trading_trend",
    "ka50012": "spot_gold_daily_trend",
    "ka50087": "gold_spot_expected_transaction",
    "ka50100": "gold_spot_price_information",
    "ka50101": "gold_spot_quote",
    "ka90005": "program_trading_trend_request_by_time_zone",
    "ka90006": "program_trading_profit_balance_trend_request",
    "ka90007": "request_for_cumulative_program_trading_trend",
    "ka90008": "request_for_program_trading_trend_by_item_time",
    "ka90010": "program_trading_trend_request_date",
    "ka90013": "request_daily_program_trading_trend_for_items",
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
    "ka10010": "industry_program_request",
    "ka10051": "investor_net_purchase_request_by_industry",
    "ka20001": "current_industry_request",
    "ka20002": "request_for_stocks_by_industry",
    "ka20003": "request_for_all_industry_indices",
    "ka20009": "industry_current_price_daily_request",
    "ka10171": "condition_search_list_inquiry",
    "ka10172": "conditional_search_request_general",
    "ka10173": "real_time_conditional_search_request",
    "ka10174": "conditional_search_real_time_cancellation",
    "ka00198": "real_time_item_inquiry_ranking",
    "ka10001": "request_for_basic_stock_information",
    "ka10002": "stock_exchange_request",
    "ka10003": "request_for_conclusion_information",
    "ka10013": "credit_trading_trend_request",
    "ka10015": "daily_transaction_request",
    "ka10016": "request_for_low_report",
    "ka10017": "request_for_upper_and_lower_limits",
    "ka10018": "high_and_low_price_proximity_request",
    "ka10019": "request_for_sudden_price_fluctuation",
    "ka10024": "transaction_volume_update_request",
    "ka10025": "request_for_concentration_of_properties_for_sale",
    "ka10026": "request_for_high_and_low_per",
    "ka10028": "request_for_fluctuation_rate_compared_to_market_price",
    "ka10043": "request_for_transaction_price_analysis",
    "ka10052": "trader_instantaneous_trading_volume_request",
    "ka10054": "request_for_items_to_activate_volatility_mitigation_device",
    "ka10055": "request_for_settlement_the_day_before_the_day",
    "ka10058": "request_for_daily_trading_items_by_investor",
    "ka10059": "requests_by_item_and_investor_institution",
    "ka10061": "total_request_by_item_and_investor_institution",
    "ka10084": "request_for_settlement_the_day_before_the_same_day",
    "ka10095": "request_information_on_items_of_interest",
    "ka10099": "stock_information_list",
    "ka10100": "check_stock_information",
    "ka10101": "industry_code_list",
    "ka10102": "member_company_list",
    "ka90003": "request_for_top50_program_net_purchases",
    "ka90004": "request_for_program_trading_status_by_item",
    "kt20016": "request_for_credit_loan_available_items",
    "kt20017": "credit_loan_availability_inquiry",
    "kt10000": "stock_purchase_order",
    "kt10001": "stock_sell_order",
    "kt10002": "stock_correction_order",
    "kt10003": "stock_cancellation_order",
    "kt50000": "gold_spot_purchase_order",
    "kt50001": "gold_spot_sell_order",
    "kt50002": "spot_gold_correction_order",
    "kt50003": "gold_spot_cancellation_order",
    "ka10060": "chart_request_by_item_and_investor_institution",
    "ka10064": "intraday_investor_specific_trading_chart_request",
    "ka10079": "stock_tick_chart_inquiry_request",
    "ka10080": "request_to_view_stock_chart",
    "ka10081": "stock_daily_chart_inquiry_request",
    "ka10082": "stock_weekly_chart_inquiry_request",
    "ka10083": "stock_monthly_chart_inquiry_request",
    "ka10094": "stock_annual_chart_inquiry_request",
    "ka20004": "industry_tick_chart_inquiry_request",
    "ka20005": "industry_division_inquiry_request",
    "ka20006": "industry_daily_salary_inquiry_request",
    "ka20007": "request_for_industry_salary_inquiry",
    "ka20008": "industry_monthly_salary_inquiry_request",
    "ka20019": "industry_year_salary_inquiry_request",
    "ka50079": "gold_spot_tick_chart_inquiry_request",
    "ka50080": "gold_spot_fractional_chart_inquiry_request",
    "ka50081": "gold_spot_daily_chart_inquiry_request",
    "ka50082": "gold_spot_weekly_chart_inquiry_request",
    "ka50083": "gold_spot_monthly_chart_inquiry_request",
    "ka50091": "gold_spot_daily_tick_chart_inquiry_request",
    "ka50092": "request_to_view_gold_spot_daily_chart",
    "ka90001": "requests_by_theme_group",
    "ka90002": "request_for_theme_items",
    "ka10048": "elw_daily_sensitivity_indicator_request",
    "ka10050": "elw_sensitivity_indicator_request",
    "ka30001": "request_for_sudden_fluctuation_in_elw_price",
    "ka30002": "elw_net_sales_top_request_by_trader",
    "ka30003": "request_daily_trend_of_elwlp_holdings",
    "ka30004": "elw_disparity_rate_request",
    "ka30005": "elw_condition_search_request",
    "ka30009": "elw_fluctuation_rate_ranking_request",
    "ka30010": "elw_remaining_balance_ranking_request",
    "ka30011": "elw_proximity_rate_request",
    "ka30012": "request_for_detailed_information_on_elw_items",
    "ka40001": "etf_return_rate_request",
    "ka40002": "etf_item_information_request",
    "ka40003": "etf_daily_trend_request",
    "ka40004": "request_full_etf_view",
    "ka40006": "etf_time_zone_trend_request",
    "ka40007": "etf_trading_request_by_time_slot",
    "ka40008": "etf_transaction_request_by_date",
    "ka40009": "etf_trading_request_by_time_slot1",
    "ka40010": "etf_time_zone_trend_request1",
}

API_ID_TO_REQ_MODEL: Dict[str, Type[BaseModel]] = {
    "au10001": AccessTokenIssuanceRequest,
    "au10002": DiscardAccessTokenRequest,
    "ka00001": AccountNumberInquiryRequest,
    "ka01690": DailyBalanceReturnRateRequest,
    "ka10072": RealizedProfitLossRequestByDateItemDateRequest,
    "ka10073": RealizedProfitLossRequestByDateAndItemPeriodRequest,
    "ka10074": RequestForRealizedProfitOrLossByDateRequest,
    "ka10075": NonConfirmationRequestRequest,
    "ka10076": ConclusionRequestRequest,
    "ka10077": RequestForSameDayRealizedProfitAndLossRequest,
    "ka10085": AccountYieldRequestRequest,
    "ka10088": UnfilledSplitOrderDetailsRequest,
    "ka10170": SameDaySalesLogRequestRequest,
    "kt00001": RequestDetailedStatusOfDepositRequest,
    "kt00002": DailyEstimatedDepositedAssetStatusRequestRequest,
    "kt00003": EstimatedAssetInquiryRequestRequest,
    "kt00004": RequestForAccountEvaluationStatusRequest,
    "kt00005": RequestForTransactionBalanceRequest,
    "kt00007": RequestDetailsOnOrderDetailsByAccountRequest,
    "kt00008": RequestNextDayPaymentScheduleDetailsForEachAccountRequest,
    "kt00009": RequestForOrderExecutionStatusByAccountRequest,
    "kt00010": RequestForOrderWithdrawalAmountRequest,
    "kt00011": RequestToInquiryQuantityAvailableForOrderByMarginRateRequest,
    "kt00012": RequestToInquiryQuantityAvailableForOrderByCreditDepositRateRequest,
    "kt00013": MarginDetailsInquiryRequestRequest,
    "kt00015": RequestForComprehensiveConsignmentTransactionDetailsRequest,
    "kt00016": RequestForDetailedStatusOfDailyAccountReturnsRequest,
    "kt00017": RequestDailyStatusForEachAccountRequest,
    "kt00018": RequestForAccountEvaluationBalanceDetailsRequest,
    "kt50020": CheckGoldSpotBalanceRequest,
    "kt50021": GoldSpotDepositRequest,
    "kt50030": ViewAllGoldSpotOrdersRequest,
    "kt50031": GoldSpotOrderExecutionInquiryRequest,
    "kt50032": GoldSpotTransactionHistoryInquiryRequest,
    "kt50075": GoldSpotNonTradingInquiryRequest,
    "ka10014": ShortSellingTrendRequestRequest,
    "ka10008": ForeignStockTradingTrendsByItemRequest,
    "ka10009": StockInstitutionRequestRequest,
    "ka10131": RequestForStatusOfContinuousTradingByInstitutionalForeignersRequest,
    "ka52301": CurrentStatusOfGoldSpotInvestorsRequest,
    "ka10068": RequestForLoanLendingTransactionTrendRequest,
    "ka10069": RequestForTop10BorrowingStocksRequest,
    "ka20068": RequestForLoanLendingTransactionTrendByItemRequest,
    "ka90012": RequestForLoanTransactionDetailsRequest,
    "ka10020": RequestForHigherQuotaBalanceRequest,
    "ka10021": RequestForSuddenIncreaseInQuotationBalanceRequest,
    "ka10022": RequestForSuddenIncreaseInRemainingCapacityRequest,
    "ka10023": RequestForSuddenIncreaseInTradingVolumeRequest,
    "ka10027": RequestForHigherFluctuationRateComparedToThePreviousDayRequest,
    "ka10029": RequestForHigherExpectedTransactionRateRequest,
    "ka10030": HighTransactionVolumeRequestForTheDayRequest,
    "ka10031": RequestForThePreviousDaySHighestTradingVolumeRequest,
    "ka10032": RequestForHigherTransactionAmountRequest,
    "ka10033": RequestForHigherCreditRatioRequest,
    "ka10034": ExternalTransactionTopSalesRequestByPeriodRequest,
    "ka10035": ForeignContinuousNetSalesTopRequestRequest,
    "ka10036": TopForeignLimitBurnoutRateIncreaseRequest,
    "ka10037": ForeignOverTheCounterSalesRequestRequest,
    "ka10038": RequestRankingOfSecuritiesCompaniesByStockRequest,
    "ka10039": TopTradingRequestBySecuritiesCompanyRequest,
    "ka10040": SameDayMajorTransactionRequestRequest,
    "ka10042": NetBuyingTraderRankingRequestRequest,
    "ka10053": RequestForSameDayHighWithdrawalRequest,
    "ka10062": RequestForSameNetSalesRankingRequest,
    "ka10065": IntradayTradingRequestByInvestorRequest,
    "ka10098": RequestForRankingOfOutOfHoursSinglePriceFluctuationRateRequest,
    "ka90009": ForeignInstitutionalTradingTopRequestRequest,
    "ka10004": StockQuoteRequestRequest,
    "ka10005": StockWeeklyMonthlyAndHourlyMinutesRequestRequest,
    "ka10006": StockTimeRequestRequest,
    "ka10007": RequestForPriceInformationRequest,
    "ka10011": RequestToViewAllNewStockWarrantsRequest,
    "ka10044": RequestForDailyInstitutionalTradingItemsRequest,
    "ka10045": RequestForInstitutionalTradingTrendByItemRequest,
    "ka10046": RequestForFasteningStrengthTrendByTimeRequest,
    "ka10047": RequestForDailyTighteningStrengthTrendRequest,
    "ka10063": IntradayInvestorSpecificTradingRequestRequest,
    "ka10066": RequestForTradingByInvestorAfterMarketCloseRequest,
    "ka10078": RequestForStockTradingTrendsBySecuritiesCompanyRequest,
    "ka10086": DailyStockRequestRequest,
    "ka10087": SingleRequestAfterHoursRequest,
    "ka50010": GoldSpotTradingTrendRequest,
    "ka50012": SpotGoldDailyTrendRequest,
    "ka50087": GoldSpotExpectedTransactionRequest,
    "ka50100": GoldSpotPriceInformationRequest,
    "ka50101": GoldSpotQuoteRequest,
    "ka90005": ProgramTradingTrendRequestByTimeZoneRequest,
    "ka90006": ProgramTradingProfitBalanceTrendRequestRequest,
    "ka90007": RequestForCumulativeProgramTradingTrendRequest,
    "ka90008": RequestForProgramTradingTrendByItemTimeRequest,
    "ka90010": ProgramTradingTrendRequestDateRequest,
    "ka90013": RequestDailyProgramTradingTrendForItemsRequest,
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
    "ka10010": IndustryProgramRequestRequest,
    "ka10051": InvestorNetPurchaseRequestByIndustryRequest,
    "ka20001": CurrentIndustryRequestRequest,
    "ka20002": RequestForStocksByIndustryRequest,
    "ka20003": RequestForAllIndustryIndicesRequest,
    "ka20009": IndustryCurrentPriceDailyRequestRequest,
    "ka10171": ConditionSearchListInquiryRequest,
    "ka10172": ConditionalSearchRequestGeneralRequest,
    "ka10173": RealTimeConditionalSearchRequestRequest,
    "ka10174": ConditionalSearchRealTimeCancellationRequest,
    "ka00198": RealTimeItemInquiryRankingRequest,
    "ka10001": RequestForBasicStockInformationRequest,
    "ka10002": StockExchangeRequestRequest,
    "ka10003": RequestForConclusionInformationRequest,
    "ka10013": CreditTradingTrendRequestRequest,
    "ka10015": DailyTransactionRequestRequest,
    "ka10016": RequestForLowReportRequest,
    "ka10017": RequestForUpperAndLowerLimitsRequest,
    "ka10018": HighAndLowPriceProximityRequestRequest,
    "ka10019": RequestForSuddenPriceFluctuationRequest,
    "ka10024": TransactionVolumeUpdateRequestRequest,
    "ka10025": RequestForConcentrationOfPropertiesForSaleRequest,
    "ka10026": RequestForHighAndLowPerRequest,
    "ka10028": RequestForFluctuationRateComparedToMarketPriceRequest,
    "ka10043": RequestForTransactionPriceAnalysisRequest,
    "ka10052": TraderInstantaneousTradingVolumeRequestRequest,
    "ka10054": RequestForItemsToActivateVolatilityMitigationDeviceRequest,
    "ka10055": RequestForSettlementTheDayBeforeTheDayRequest,
    "ka10058": RequestForDailyTradingItemsByInvestorRequest,
    "ka10059": RequestsByItemAndInvestorInstitutionRequest,
    "ka10061": TotalRequestByItemAndInvestorInstitutionRequest,
    "ka10084": RequestForSettlementTheDayBeforeTheSameDayRequest,
    "ka10095": RequestInformationOnItemsOfInterestRequest,
    "ka10099": StockInformationListRequest,
    "ka10100": CheckStockInformationRequest,
    "ka10101": IndustryCodeListRequest,
    "ka10102": MemberCompanyListRequest,
    "ka90003": RequestForTop50ProgramNetPurchasesRequest,
    "ka90004": RequestForProgramTradingStatusByItemRequest,
    "kt20016": RequestForCreditLoanAvailableItemsRequest,
    "kt20017": CreditLoanAvailabilityInquiryRequest,
    "kt10000": StockPurchaseOrderRequest,
    "kt10001": StockSellOrderRequest,
    "kt10002": StockCorrectionOrderRequest,
    "kt10003": StockCancellationOrderRequest,
    "kt50000": GoldSpotPurchaseOrderRequest,
    "kt50001": GoldSpotSellOrderRequest,
    "kt50002": SpotGoldCorrectionOrderRequest,
    "kt50003": GoldSpotCancellationOrderRequest,
    "ka10060": ChartRequestByItemAndInvestorInstitutionRequest,
    "ka10064": IntradayInvestorSpecificTradingChartRequestRequest,
    "ka10079": StockTickChartInquiryRequestRequest,
    "ka10080": RequestToViewStockChartRequest,
    "ka10081": StockDailyChartInquiryRequestRequest,
    "ka10082": StockWeeklyChartInquiryRequestRequest,
    "ka10083": StockMonthlyChartInquiryRequestRequest,
    "ka10094": StockAnnualChartInquiryRequestRequest,
    "ka20004": IndustryTickChartInquiryRequestRequest,
    "ka20005": IndustryDivisionInquiryRequestRequest,
    "ka20006": IndustryDailySalaryInquiryRequestRequest,
    "ka20007": RequestForIndustrySalaryInquiryRequest,
    "ka20008": IndustryMonthlySalaryInquiryRequestRequest,
    "ka20019": IndustryYearSalaryInquiryRequestRequest,
    "ka50079": GoldSpotTickChartInquiryRequestRequest,
    "ka50080": GoldSpotFractionalChartInquiryRequestRequest,
    "ka50081": GoldSpotDailyChartInquiryRequestRequest,
    "ka50082": GoldSpotWeeklyChartInquiryRequestRequest,
    "ka50083": GoldSpotMonthlyChartInquiryRequestRequest,
    "ka50091": GoldSpotDailyTickChartInquiryRequestRequest,
    "ka50092": RequestToViewGoldSpotDailyChartRequest,
    "ka90001": RequestsByThemeGroupRequest,
    "ka90002": RequestForThemeItemsRequest,
    "ka10048": ElwDailySensitivityIndicatorRequestRequest,
    "ka10050": ElwSensitivityIndicatorRequestRequest,
    "ka30001": RequestForSuddenFluctuationInElwPriceRequest,
    "ka30002": ElwNetSalesTopRequestByTraderRequest,
    "ka30003": RequestDailyTrendOfElwlpHoldingsRequest,
    "ka30004": ElwDisparityRateRequestRequest,
    "ka30005": ElwConditionSearchRequestRequest,
    "ka30009": ElwFluctuationRateRankingRequestRequest,
    "ka30010": ElwRemainingBalanceRankingRequestRequest,
    "ka30011": ElwProximityRateRequestRequest,
    "ka30012": RequestForDetailedInformationOnElwItemsRequest,
    "ka40001": EtfReturnRateRequestRequest,
    "ka40002": EtfItemInformationRequestRequest,
    "ka40003": EtfDailyTrendRequestRequest,
    "ka40004": RequestFullEtfViewRequest,
    "ka40006": EtfTimeZoneTrendRequestRequest,
    "ka40007": EtfTradingRequestByTimeSlotRequest,
    "ka40008": EtfTransactionRequestByDateRequest,
    "ka40009": EtfTradingRequestByTimeSlot1Request,
    "ka40010": EtfTimeZoneTrendRequest1Request,
}

API_ID_TO_RES_MODEL: Dict[str, Type[BaseModel]] = {
    "au10001": AccessTokenIssuanceResponse,
    "au10002": DiscardAccessTokenResponse,
    "ka00001": AccountNumberInquiryResponse,
    "ka01690": DailyBalanceReturnRateResponse,
    "ka10072": RealizedProfitLossRequestByDateItemDateResponse,
    "ka10073": RealizedProfitLossRequestByDateAndItemPeriodResponse,
    "ka10074": RequestForRealizedProfitOrLossByDateResponse,
    "ka10075": NonConfirmationRequestResponse,
    "ka10076": ConclusionRequestResponse,
    "ka10077": RequestForSameDayRealizedProfitAndLossResponse,
    "ka10085": AccountYieldRequestResponse,
    "ka10088": UnfilledSplitOrderDetailsResponse,
    "ka10170": SameDaySalesLogRequestResponse,
    "kt00001": RequestDetailedStatusOfDepositResponse,
    "kt00002": DailyEstimatedDepositedAssetStatusRequestResponse,
    "kt00003": EstimatedAssetInquiryRequestResponse,
    "kt00004": RequestForAccountEvaluationStatusResponse,
    "kt00005": RequestForTransactionBalanceResponse,
    "kt00007": RequestDetailsOnOrderDetailsByAccountResponse,
    "kt00008": RequestNextDayPaymentScheduleDetailsForEachAccountResponse,
    "kt00009": RequestForOrderExecutionStatusByAccountResponse,
    "kt00010": RequestForOrderWithdrawalAmountResponse,
    "kt00011": RequestToInquiryQuantityAvailableForOrderByMarginRateResponse,
    "kt00012": RequestToInquiryQuantityAvailableForOrderByCreditDepositRateResponse,
    "kt00013": MarginDetailsInquiryRequestResponse,
    "kt00015": RequestForComprehensiveConsignmentTransactionDetailsResponse,
    "kt00016": RequestForDetailedStatusOfDailyAccountReturnsResponse,
    "kt00017": RequestDailyStatusForEachAccountResponse,
    "kt00018": RequestForAccountEvaluationBalanceDetailsResponse,
    "kt50020": CheckGoldSpotBalanceResponse,
    "kt50021": GoldSpotDepositResponse,
    "kt50030": ViewAllGoldSpotOrdersResponse,
    "kt50031": GoldSpotOrderExecutionInquiryResponse,
    "kt50032": GoldSpotTransactionHistoryInquiryResponse,
    "kt50075": GoldSpotNonTradingInquiryResponse,
    "ka10014": ShortSellingTrendRequestResponse,
    "ka10008": ForeignStockTradingTrendsByItemResponse,
    "ka10009": StockInstitutionRequestResponse,
    "ka10131": RequestForStatusOfContinuousTradingByInstitutionalForeignersResponse,
    "ka52301": CurrentStatusOfGoldSpotInvestorsResponse,
    "ka10068": RequestForLoanLendingTransactionTrendResponse,
    "ka10069": RequestForTop10BorrowingStocksResponse,
    "ka20068": RequestForLoanLendingTransactionTrendByItemResponse,
    "ka90012": RequestForLoanTransactionDetailsResponse,
    "ka10020": RequestForHigherQuotaBalanceResponse,
    "ka10021": RequestForSuddenIncreaseInQuotationBalanceResponse,
    "ka10022": RequestForSuddenIncreaseInRemainingCapacityResponse,
    "ka10023": RequestForSuddenIncreaseInTradingVolumeResponse,
    "ka10027": RequestForHigherFluctuationRateComparedToThePreviousDayResponse,
    "ka10029": RequestForHigherExpectedTransactionRateResponse,
    "ka10030": HighTransactionVolumeRequestForTheDayResponse,
    "ka10031": RequestForThePreviousDaySHighestTradingVolumeResponse,
    "ka10032": RequestForHigherTransactionAmountResponse,
    "ka10033": RequestForHigherCreditRatioResponse,
    "ka10034": ExternalTransactionTopSalesRequestByPeriodResponse,
    "ka10035": ForeignContinuousNetSalesTopRequestResponse,
    "ka10036": TopForeignLimitBurnoutRateIncreaseResponse,
    "ka10037": ForeignOverTheCounterSalesRequestResponse,
    "ka10038": RequestRankingOfSecuritiesCompaniesByStockResponse,
    "ka10039": TopTradingRequestBySecuritiesCompanyResponse,
    "ka10040": SameDayMajorTransactionRequestResponse,
    "ka10042": NetBuyingTraderRankingRequestResponse,
    "ka10053": RequestForSameDayHighWithdrawalResponse,
    "ka10062": RequestForSameNetSalesRankingResponse,
    "ka10065": IntradayTradingRequestByInvestorResponse,
    "ka10098": RequestForRankingOfOutOfHoursSinglePriceFluctuationRateResponse,
    "ka90009": ForeignInstitutionalTradingTopRequestResponse,
    "ka10004": StockQuoteRequestResponse,
    "ka10005": StockWeeklyMonthlyAndHourlyMinutesRequestResponse,
    "ka10006": StockTimeRequestResponse,
    "ka10007": RequestForPriceInformationResponse,
    "ka10011": RequestToViewAllNewStockWarrantsResponse,
    "ka10044": RequestForDailyInstitutionalTradingItemsResponse,
    "ka10045": RequestForInstitutionalTradingTrendByItemResponse,
    "ka10046": RequestForFasteningStrengthTrendByTimeResponse,
    "ka10047": RequestForDailyTighteningStrengthTrendResponse,
    "ka10063": IntradayInvestorSpecificTradingRequestResponse,
    "ka10066": RequestForTradingByInvestorAfterMarketCloseResponse,
    "ka10078": RequestForStockTradingTrendsBySecuritiesCompanyResponse,
    "ka10086": DailyStockRequestResponse,
    "ka10087": SingleRequestAfterHoursResponse,
    "ka50010": GoldSpotTradingTrendResponse,
    "ka50012": SpotGoldDailyTrendResponse,
    "ka50087": GoldSpotExpectedTransactionResponse,
    "ka50100": GoldSpotPriceInformationResponse,
    "ka50101": GoldSpotQuoteResponse,
    "ka90005": ProgramTradingTrendRequestByTimeZoneResponse,
    "ka90006": ProgramTradingProfitBalanceTrendRequestResponse,
    "ka90007": RequestForCumulativeProgramTradingTrendResponse,
    "ka90008": RequestForProgramTradingTrendByItemTimeResponse,
    "ka90010": ProgramTradingTrendRequestDateResponse,
    "ka90013": RequestDailyProgramTradingTrendForItemsResponse,
    "kt10006": CreditBuyOrderResponse,
    "kt10007": CreditSellOrderResponse,
    "kt10008": CreditCorrectionOrderResponse,
    "kt10009": CreditCancellationOrderResponse,
    "00": OrderExecutionResponse,
    "04": BalanceResponse,
    "0A": StockMomentumResponse,
    "0B": StockSigningResponse,
    "0C": StockPreferredPriceResponse,
    "0D": StockQuoteBalanceResponse,
    "0E": StockAfterHoursQuoteResponse,
    "0F": StockDayTraderResponse,
    "0G": EtfNavResponse,
    "0H": StockExpectedExecutionResponse,
    "0I": InternationalGoldConversionPriceResponse,
    "0J": SectorIndexResponse,
    "0U": IndustryFluctuationsResponse,
    "0g": StockItemInformationResponse,
    "0m": ElwTheoristResponse,
    "0s": LongStartTimeResponse,
    "0u": ElwIndicatorResponse,
    "0w": StockProgramTradingResponse,
    "1h": ActivateDisableViResponse,
    "ka10010": IndustryProgramRequestResponse,
    "ka10051": InvestorNetPurchaseRequestByIndustryResponse,
    "ka20001": CurrentIndustryRequestResponse,
    "ka20002": RequestForStocksByIndustryResponse,
    "ka20003": RequestForAllIndustryIndicesResponse,
    "ka20009": IndustryCurrentPriceDailyRequestResponse,
    "ka10171": ConditionSearchListInquiryResponse,
    "ka10172": ConditionalSearchRequestGeneralResponse,
    "ka10173": RealTimeConditionalSearchRequestResponse,
    "ka10174": ConditionalSearchRealTimeCancellationResponse,
    "ka00198": RealTimeItemInquiryRankingResponse,
    "ka10001": RequestForBasicStockInformationResponse,
    "ka10002": StockExchangeRequestResponse,
    "ka10003": RequestForConclusionInformationResponse,
    "ka10013": CreditTradingTrendRequestResponse,
    "ka10015": DailyTransactionRequestResponse,
    "ka10016": RequestForLowReportResponse,
    "ka10017": RequestForUpperAndLowerLimitsResponse,
    "ka10018": HighAndLowPriceProximityRequestResponse,
    "ka10019": RequestForSuddenPriceFluctuationResponse,
    "ka10024": TransactionVolumeUpdateRequestResponse,
    "ka10025": RequestForConcentrationOfPropertiesForSaleResponse,
    "ka10026": RequestForHighAndLowPerResponse,
    "ka10028": RequestForFluctuationRateComparedToMarketPriceResponse,
    "ka10043": RequestForTransactionPriceAnalysisResponse,
    "ka10052": TraderInstantaneousTradingVolumeRequestResponse,
    "ka10054": RequestForItemsToActivateVolatilityMitigationDeviceResponse,
    "ka10055": RequestForSettlementTheDayBeforeTheDayResponse,
    "ka10058": RequestForDailyTradingItemsByInvestorResponse,
    "ka10059": RequestsByItemAndInvestorInstitutionResponse,
    "ka10061": TotalRequestByItemAndInvestorInstitutionResponse,
    "ka10084": RequestForSettlementTheDayBeforeTheSameDayResponse,
    "ka10095": RequestInformationOnItemsOfInterestResponse,
    "ka10099": StockInformationListResponse,
    "ka10100": CheckStockInformationResponse,
    "ka10101": IndustryCodeListResponse,
    "ka10102": MemberCompanyListResponse,
    "ka90003": RequestForTop50ProgramNetPurchasesResponse,
    "ka90004": RequestForProgramTradingStatusByItemResponse,
    "kt20016": RequestForCreditLoanAvailableItemsResponse,
    "kt20017": CreditLoanAvailabilityInquiryResponse,
    "kt10000": StockPurchaseOrderResponse,
    "kt10001": StockSellOrderResponse,
    "kt10002": StockCorrectionOrderResponse,
    "kt10003": StockCancellationOrderResponse,
    "kt50000": GoldSpotPurchaseOrderResponse,
    "kt50001": GoldSpotSellOrderResponse,
    "kt50002": SpotGoldCorrectionOrderResponse,
    "kt50003": GoldSpotCancellationOrderResponse,
    "ka10060": ChartRequestByItemAndInvestorInstitutionResponse,
    "ka10064": IntradayInvestorSpecificTradingChartRequestResponse,
    "ka10079": StockTickChartInquiryRequestResponse,
    "ka10080": RequestToViewStockChartResponse,
    "ka10081": StockDailyChartInquiryRequestResponse,
    "ka10082": StockWeeklyChartInquiryRequestResponse,
    "ka10083": StockMonthlyChartInquiryRequestResponse,
    "ka10094": StockAnnualChartInquiryRequestResponse,
    "ka20004": IndustryTickChartInquiryRequestResponse,
    "ka20005": IndustryDivisionInquiryRequestResponse,
    "ka20006": IndustryDailySalaryInquiryRequestResponse,
    "ka20007": RequestForIndustrySalaryInquiryResponse,
    "ka20008": IndustryMonthlySalaryInquiryRequestResponse,
    "ka20019": IndustryYearSalaryInquiryRequestResponse,
    "ka50079": GoldSpotTickChartInquiryRequestResponse,
    "ka50080": GoldSpotFractionalChartInquiryRequestResponse,
    "ka50081": GoldSpotDailyChartInquiryRequestResponse,
    "ka50082": GoldSpotWeeklyChartInquiryRequestResponse,
    "ka50083": GoldSpotMonthlyChartInquiryRequestResponse,
    "ka50091": GoldSpotDailyTickChartInquiryRequestResponse,
    "ka50092": RequestToViewGoldSpotDailyChartResponse,
    "ka90001": RequestsByThemeGroupResponse,
    "ka90002": RequestForThemeItemsResponse,
    "ka10048": ElwDailySensitivityIndicatorRequestResponse,
    "ka10050": ElwSensitivityIndicatorRequestResponse,
    "ka30001": RequestForSuddenFluctuationInElwPriceResponse,
    "ka30002": ElwNetSalesTopRequestByTraderResponse,
    "ka30003": RequestDailyTrendOfElwlpHoldingsResponse,
    "ka30004": ElwDisparityRateRequestResponse,
    "ka30005": ElwConditionSearchRequestResponse,
    "ka30009": ElwFluctuationRateRankingRequestResponse,
    "ka30010": ElwRemainingBalanceRankingRequestResponse,
    "ka30011": ElwProximityRateRequestResponse,
    "ka30012": RequestForDetailedInformationOnElwItemsResponse,
    "ka40001": EtfReturnRateRequestResponse,
    "ka40002": EtfItemInformationRequestResponse,
    "ka40003": EtfDailyTrendRequestResponse,
    "ka40004": RequestFullEtfViewResponse,
    "ka40006": EtfTimeZoneTrendRequestResponse,
    "ka40007": EtfTradingRequestByTimeSlotResponse,
    "ka40008": EtfTransactionRequestByDateResponse,
    "ka40009": EtfTradingRequestByTimeSlot1Response,
    "ka40010": EtfTimeZoneTrendRequest1Response,
}
