| 한글 이름 | As-Is (이전 이름) | To-Be (개선된 이름) |
| :--- | :--- | :--- |
| 접근토큰 발급 | `❌ access_token_issuance` | **`✅ issue_access_token`** |
| 접근토큰폐기 | `❌ discard_access_token` | **`✅ revoke_access_token`** |
| 계좌번호조회 | `account_number` | `account_number` |
| 일별잔고수익률 | `daily_balance_return_rate` | `daily_balance_return_rate` |
| 일자별종목별실현손익요청_일자 | `❌ realized_prit_loss_by_date_item_date` | **`✅ realized_profit_loss_by_date_item_date`** |
| 일자별종목별실현손익요청_기간 | `❌ realized_prit_loss_by_date_item_period` | **`✅ realized_profit_loss_by_date_item_period`** |
| 일자별실현손익요청 | `❌ realized_prit_loss_by_date` | **`✅ realized_profit_loss_by_date`** |
| 미체결요청 | `non_confirmation` | `non_confirmation` |
| 체결요청 | `conclusion` | `conclusion` |
| 당일실현손익상세요청 | `❌ same_day_realized_prit_loss` | **`✅ same_day_realized_profit_loss`** |
| 계좌수익률요청 | `account_yield` | `account_yield` |
| 미체결 분할주문 상세 | `❌ unfilled_splitder` | **`✅ unfilled_split_order_details`** |
| 당일매매일지요청 | `same_day_sales_log` | `same_day_sales_log` |
| 예수금상세현황요청 | `detailed_deposit` | `detailed_deposit` |
| 일별추정예탁자산현황요청 | `daily_estimated_deposited_asset` | `daily_estimated_deposited_asset` |
| 추정자산조회요청 | `estimated_asset` | `estimated_asset` |
| 계좌평가현황요청 | `account_evaluation` | `account_evaluation` |
| 체결잔고요청 | `transaction_balance` | `transaction_balance` |
| 계좌별주문체결내역상세요청 | `❌ onder_by_account` | **`✅ order_details_by_account`** |
| 계좌별익일결제예정내역요청 | `❌ next_day_payment_schedule_each_account` | **`✅ next_day_payment_schedule_details_by_account`** |
| 계좌별주문체결현황요청 | `❌ der_execution_by_account` | **`✅ order_execution_by_account`** |
| 주문인출가능금액요청 | `❌ der_withdrawal_amount` | **`✅ order_withdrawal_amount`** |
| 증거금율별주문가능수량조회요청 | `❌ to_quantity_availableder_by_margin_rate` | **`✅ quantity_available_order_by_margin_rate`** |
| 신용보증금율별주문가능수량조회요청 | `❌ to_quantity_availableder_by_credit_deposit_rate` | **`✅ quantity_available_order_by_credit_deposit_rate`** |
| 증거금세부내역조회요청 | `❌ margin` | **`✅ margin_details`** |
| 위탁종합거래내역요청 | `❌ comprehensive_consignment_transaction` | **`✅ comprehensive_consignment_transaction_details`** |
| 일별계좌수익률상세현황요청 | `detailed_daily_account_returns` | `detailed_daily_account_returns` |
| 계좌별당일현황요청 | `❌ daily_each_account` | **`✅ daily_by_account`** |
| 계좌평가잔고내역요청 | `❌ account_evaluation_balance` | **`✅ account_evaluation_balance_details`** |
| 금현물 잔고확인 | `check_gold_spot_balance` | `check_gold_spot_balance` |
| 금현물 예수금 | `gold_spot_deposit` | `gold_spot_deposit` |
| 금현물 주문체결전체조회 | `❌ view_all_gold_spotders` | **`✅ all_gold_spot_orders`** |
| 금현물 주문체결조회 | `❌ gold_spotder_execution` | **`✅ gold_spot_order_execution`** |
| 금현물 거래내역조회 | `gold_spot_transaction_history` | `gold_spot_transaction_history` |
| 금현물 미체결조회 | `gold_spot_non_trading` | `gold_spot_non_trading` |
| 공매도추이요청 | `short_selling_trend` | `short_selling_trend` |
| 주식외국인종목별매매동향 | `❌ eign_stock_trading_trends_by_item` | **`✅ foreign_stock_trading_trends_by_item`** |
| 주식기관요청 | `stock_institution` | `stock_institution` |
| 기관외국인연속매매현황요청 | `❌ continuous_trading_by_institutionaleigners` | **`✅ continuous_trading_by_institutional_foreigners`** |
| 금현물투자자현황 | `current_gold_spot_investors` | `current_gold_spot_investors` |
| 대차거래추이요청 | `loan_lending_transaction_trend` | `loan_lending_transaction_trend` |
| 대차거래상위10종목요청 | `top10_borrowing_stocks` | `top10_borrowing_stocks` |
| 대차거래추이요청(종목별) | `loan_lending_transaction_trend_by_item` | `loan_lending_transaction_trend_by_item` |
| 대차거래내역요청 | `❌ loan_transaction` | **`✅ loan_transaction_details`** |
| 호가잔량상위요청 | `higher_quota_balance` | `higher_quota_balance` |
| 호가잔량급증요청 | `❌ sudden_increase_in_quotation_balance` | **`✅ sudden_increase_quotation_balance`** |
| 잔량율급증요청 | `❌ sudden_increase_in_remaining_capacity` | **`✅ sudden_increase_remaining_capacity`** |
| 거래량급증요청 | `❌ sudden_increase_in_trading_volume` | **`✅ sudden_increase_trading_volume`** |
| 전일대비등락률상위요청 | `❌ higher_fluctuation_rate_compared_to_the_previous_day` | **`✅ higher_fluctuation_rate_compared_previous_day`** |
| 예상체결등락률상위요청 | `higher_expected_transaction_rate` | `higher_expected_transaction_rate` |
| 당일거래량상위요청 | `❌ high_transaction_volume_the_day` | **`✅ high_transaction_volume_day`** |
| 전일거래량상위요청 | `❌ the_previous_day_s_highest_trading_volume` | **`✅ previous_day_highest_trading_volume`** |
| 거래대금상위요청 | `higher_transaction_amount` | `higher_transaction_amount` |
| 신용비율상위요청 | `higher_credit_ratio` | `higher_credit_ratio` |
| 외인기간별매매상위요청 | `external_transaction_top_sales_by_period` | `external_transaction_top_sales_by_period` |
| 외인연속순매매상위요청 | `❌ eign_continuous_net_sales_top` | **`✅ foreign_continuous_net_sales_top`** |
| 외인한도소진율증가상위 | `❌ topeign_limit_burnout_rate_increase` | **`✅ top_foreign_limit_burnout_rate_increase`** |
| 외국계창구매매상위요청 | `❌ eign_over_the_counter_sales` | **`✅ foreign_over_counter_sales`** |
| 종목별증권사순위요청 | `ranking_securities_companies_by_stock` | `ranking_securities_companies_by_stock` |
| 증권사별매매상위요청 | `top_trading_by_securities_company` | `top_trading_by_securities_company` |
| 당일주요거래원요청 | `same_day_major_transaction` | `same_day_major_transaction` |
| 순매수거래원순위요청 | `net_buying_trader_ranking` | `net_buying_trader_ranking` |
| 당일상위이탈원요청 | `same_day_high_withdrawal` | `same_day_high_withdrawal` |
| 동일순매매순위요청 | `same_net_sales_ranking` | `same_net_sales_ranking` |
| 장중투자자별매매상위요청 | `intraday_trading_by_investor` | `intraday_trading_by_investor` |
| 시간외단일가등락율순위요청 | `ranking_out_hours_single_price_fluctuation_rate` | `ranking_out_hours_single_price_fluctuation_rate` |
| 외국인기관매매상위요청 | `❌ eign_institutional_trading_top` | **`✅ foreign_institutional_trading_top`** |
| 주식호가요청 | `stock_quote` | `stock_quote` |
| 주식일주월시분요청 | `stock_weekly_monthly_hourly_minutes` | `stock_weekly_monthly_hourly_minutes` |
| 주식시분요청 | `stock_time` | `stock_time` |
| 시세표성정보요청 | `❌ price_inmation` | **`✅ price_information`** |
| 신주인수권전체시세요청 | `❌ to_view_all_new_stock_warrants` | **`✅ all_new_stock_warrants`** |
| 일별기관매매종목요청 | `daily_institutional_trading_items` | `daily_institutional_trading_items` |
| 종목별기관매매추이요청 | `institutional_trading_trend_by_item` | `institutional_trading_trend_by_item` |
| 체결강도추이시간별요청 | `fastening_strength_trend_by_time` | `fastening_strength_trend_by_time` |
| 체결강도추이일별요청 | `daily_tightening_strength_trend` | `daily_tightening_strength_trend` |
| 장중투자자별매매요청 | `intraday_investor_specific_trading` | `intraday_investor_specific_trading` |
| 장마감후투자자별매매요청 | `trading_by_investor_after_market_close` | `trading_by_investor_after_market_close` |
| 증권사별종목매매동향요청 | `stock_trading_trends_by_securities_company` | `stock_trading_trends_by_securities_company` |
| 일별주가요청 | `daily_stock` | `daily_stock` |
| 시간외단일가요청 | `single_after_hours` | `single_after_hours` |
| 금현물체결추이 | `gold_spot_trading_trend` | `gold_spot_trading_trend` |
| 금현물일별추이 | `spot_gold_daily_trend` | `spot_gold_daily_trend` |
| 금현물예상체결 | `gold_spot_expected_transaction` | `gold_spot_expected_transaction` |
| 금현물 시세정보 | `❌ gold_spot_price_inmation` | **`✅ gold_spot_price_information`** |
| 금현물 호가 | `gold_spot_quote` | `gold_spot_quote` |
| 프로그램매매추이요청 시간대별 | `program_trading_trend_by_time_zone` | `program_trading_trend_by_time_zone` |
| 프로그램매매차익잔고추이요청 | `❌ program_trading_prit_balance_trend` | **`✅ program_trading_profit_balance_trend`** |
| 프로그램매매누적추이요청 | `cumulative_program_trading_trend` | `cumulative_program_trading_trend` |
| 종목시간별프로그램매매추이요청 | `program_trading_trend_by_item_time` | `program_trading_trend_by_item_time` |
| 프로그램매매추이요청 일자별 | `program_trading_trend_date` | `program_trading_trend_date` |
| 종목일별프로그램매매추이요청 | `daily_program_trading_trend_items` | `daily_program_trading_trend_items` |
| 신용 매수주문 | `❌ credit_buyder` | **`✅ credit_buy_order`** |
| 신용 매도주문 | `❌ credit_sellder` | **`✅ credit_sell_order`** |
| 신용 정정주문 | `❌ credit_correctionder` | **`✅ credit_correction_order`** |
| 신용 취소주문 | `❌ credit_cancellationder` | **`✅ credit_cancellation_order`** |
| 주문체결 | `❌ der_execution` | **`✅ order_execution`** |
| 잔고 | `balance` | `balance` |
| 주식기세 | `stock_momentum` | `stock_momentum` |
| 주식체결 | `stock_signing` | `stock_signing` |
| 주식우선호가 | `stock_preferred_price` | `stock_preferred_price` |
| 주식호가잔량 | `stock_quote_balance` | `stock_quote_balance` |
| 주식시간외호가 | `stock_after_hours_quote` | `stock_after_hours_quote` |
| 주식당일거래원 | `stock_day_trader` | `stock_day_trader` |
| ETF NAV | `etf_nav` | `etf_nav` |
| 주식예상체결 | `stock_expected_execution` | `stock_expected_execution` |
| 국제금환산가격 | `international_gold_conversion_price` | `international_gold_conversion_price` |
| 업종지수 | `sector_index` | `sector_index` |
| 업종등락 | `industry_fluctuations` | `industry_fluctuations` |
| 주식종목정보 | `❌ stock_item_inmation` | **`✅ stock_item_information`** |
| ELW 이론가 | `elw_theorist` | `elw_theorist` |
| 장시작시간 | `long_start_time` | `long_start_time` |
| ELW 지표 | `elw_indicator` | `elw_indicator` |
| 종목프로그램매매 | `stock_program_trading` | `stock_program_trading` |
| VI발동/해제 | `activate_disable_vi` | `activate_disable_vi` |
| 업종프로그램요청 | `industry_program` | `industry_program` |
| 업종별투자자순매수요청 | `investor_net_purchase_by_industry` | `investor_net_purchase_by_industry` |
| 업종현재가요청 | `current_industry` | `current_industry` |
| 업종별주가요청 | `stocks_by_industry` | `stocks_by_industry` |
| 전업종지수요청 | `all_industry_indices` | `all_industry_indices` |
| 업종현재가일별요청 | `industry_current_price_daily` | `industry_current_price_daily` |
| 조건검색 목록조회 | `condition_search_list` | `condition_search_list` |
| 조건검색 요청 일반 | `conditional_search_general` | `conditional_search_general` |
| 조건검색 요청 실시간 | `real_time_conditional_search` | `real_time_conditional_search` |
| 조건검색 실시간 해제 | `conditional_search_real_time_cancellation` | `conditional_search_real_time_cancellation` |
| 실시간종목조회순위 | `real_time_item_ranking` | `real_time_item_ranking` |
| 주식기본정보요청 | `❌ basic_stock_inmation` | **`✅ basic_stock_information`** |
| 주식거래원요청 | `stock_exchange` | `stock_exchange` |
| 체결정보요청 | `❌ conclusion_inmation` | **`✅ conclusion_information`** |
| 신용매매동향요청 | `credit_trading_trend` | `credit_trading_trend` |
| 일별거래상세요청 | `daily_transaction` | `daily_transaction` |
| 신고저가요청 | `low_report` | `low_report` |
| 상하한가요청 | `upper_lower_limits` | `upper_lower_limits` |
| 고저가근접요청 | `high_low_price_proximity` | `high_low_price_proximity` |
| 가격급등락요청 | `sudden_price_fluctuation` | `sudden_price_fluctuation` |
| 거래량갱신요청 | `transaction_volume_update` | `transaction_volume_update` |
| 매물대집중요청 | `concentration_properties_sale` | `concentration_properties_sale` |
| 고저PER요청 | `high_low_per` | `high_low_per` |
| 시가대비등락률요청 | `❌ fluctuation_rate_compared_to_market_price` | **`✅ fluctuation_rate_compared_market_price`** |
| 거래원매물대분석요청 | `transaction_price_analysis` | `transaction_price_analysis` |
| 거래원순간거래량요청 | `trader_instantaneous_trading_volume` | `trader_instantaneous_trading_volume` |
| 변동성완화장치발동종목요청 | `❌ items_to_activate_volatility_mitigation_device` | **`✅ items_activate_volatility_mitigation_device`** |
| 당일전일체결량요청 | `❌ settlement_the_day_bee_the_day` | **`✅ settlement_day_before_day`** |
| 투자자별일별매매종목요청 | `daily_trading_items_by_investor` | `daily_trading_items_by_investor` |
| 종목별투자자기관별요청 | `❌ s_by_item_investor_institution` | **`✅ requests_by_item_investor_institution`** |
| 종목별투자자기관별합계요청 | `total_by_item_investor_institution` | `total_by_item_investor_institution` |
| 당일전일체결요청 | `❌ settlement_the_day_bee_the_same_day` | **`✅ settlement_day_before_same_day`** |
| 관심종목정보요청 | `❌ inmation_on_items_interest` | **`✅ information_items_interest`** |
| 종목정보 리스트 | `❌ stock_inmation_list` | **`✅ stock_information_list`** |
| 종목정보 조회 | `❌ check_stock_inmation` | **`✅ check_stock_information`** |
| 업종코드 리스트 | `industry_code_list` | `industry_code_list` |
| 회원사 리스트 | `member_company_list` | `member_company_list` |
| 프로그램순매수상위50요청 | `top50_program_net_purchases` | `top50_program_net_purchases` |
| 종목별프로그램매매현황요청 | `program_trading_by_item` | `program_trading_by_item` |
| 신용융자 가능종목요청 | `credit_loan_available_items` | `credit_loan_available_items` |
| 신용융자 가능문의 | `credit_loan_availability` | `credit_loan_availability` |
| 주식 매수주문 | `❌ stock_purchaseder` | **`✅ stock_purchase_order`** |
| 주식 매도주문 | `❌ stock_sellder` | **`✅ stock_sell_order`** |
| 주식 정정주문 | `❌ stock_correctionder` | **`✅ stock_correction_order`** |
| 주식 취소주문 | `❌ stock_cancellationder` | **`✅ stock_cancellation_order`** |
| 금현물 매수주문 | `❌ gold_spot_purchaseder` | **`✅ gold_spot_purchase_order`** |
| 금현물 매도주문 | `❌ gold_spot_sellder` | **`✅ gold_spot_sell_order`** |
| 금현물 정정주문 | `❌ spot_gold_correctionder` | **`✅ spot_gold_correction_order`** |
| 금현물 취소주문 | `❌ gold_spot_cancellationder` | **`✅ gold_spot_cancellation_order`** |
| 종목별투자자기관별차트요청 | `chart_by_item_investor_institution` | `chart_by_item_investor_institution` |
| 장중투자자별매매차트요청 | `intraday_investor_specific_trading_chart` | `intraday_investor_specific_trading_chart` |
| 주식틱차트조회요청 | `stock_tick_chart` | `stock_tick_chart` |
| 주식분봉차트조회요청 | `❌ to_view_stock_chart` | **`✅ stock_chart`** |
| 주식일봉차트조회요청 | `stock_daily_chart` | `stock_daily_chart` |
| 주식주봉차트조회요청 | `stock_weekly_chart` | `stock_weekly_chart` |
| 주식월봉차트조회요청 | `stock_monthly_chart` | `stock_monthly_chart` |
| 주식년봉차트조회요청 | `stock_annual_chart` | `stock_annual_chart` |
| 업종틱차트조회요청 | `industry_tick_chart` | `industry_tick_chart` |
| 업종분봉조회요청 | `industry_division` | `industry_division` |
| 업종일봉조회요청 | `industry_daily_salary` | `industry_daily_salary` |
| 업종주봉조회요청 | `industry_salary` | `industry_salary` |
| 업종월봉조회요청 | `industry_monthly_salary` | `industry_monthly_salary` |
| 업종년봉조회요청 | `industry_year_salary` | `industry_year_salary` |
| 금현물틱차트조회요청 | `gold_spot_tick_chart` | `gold_spot_tick_chart` |
| 금현물분봉차트조회요청 | `gold_spot_fractional_chart` | `gold_spot_fractional_chart` |
| 금현물일봉차트조회요청 | `gold_spot_daily_chart` | `gold_spot_daily_chart` |
| 금현물주봉차트조회요청 | `gold_spot_weekly_chart` | `gold_spot_weekly_chart` |
| 금현물월봉차트조회요청 | `gold_spot_monthly_chart` | `gold_spot_monthly_chart` |
| 금현물당일틱차트조회요청 | `gold_spot_daily_tick_chart` | `gold_spot_daily_tick_chart` |
| 금현물당일분봉차트조회요청 | `❌ to_view_gold_spot_daily_chart` | **`✅ gold_spot_daily_chart`** |
| 테마그룹별요청 | `❌ s_by_theme_group` | **`✅ requests_by_theme_group`** |
| 테마구성종목요청 | `theme_items` | `theme_items` |
| ELW일별민감도지표요청 | `elw_daily_sensitivity_indicator` | `elw_daily_sensitivity_indicator` |
| ELW민감도지표요청 | `elw_sensitivity_indicator` | `elw_sensitivity_indicator` |
| ELW가격급등락요청 | `❌ sudden_fluctuation_in_elw_price` | **`✅ sudden_fluctuation_elw_price`** |
| 거래원별ELW순매매상위요청 | `elw_net_sales_top_by_trader` | `elw_net_sales_top_by_trader` |
| ELWLP보유일별추이요청 | `daily_trend_elwlp_holdings` | `daily_trend_elwlp_holdings` |
| ELW괴리율요청 | `elw_disparity_rate` | `elw_disparity_rate` |
| ELW조건검색요청 | `elw_condition_search` | `elw_condition_search` |
| ELW등락율순위요청 | `elw_fluctuation_rate_ranking` | `elw_fluctuation_rate_ranking` |
| ELW잔량순위요청 | `elw_remaining_balance_ranking` | `elw_remaining_balance_ranking` |
| ELW근접율요청 | `elw_proximity_rate` | `elw_proximity_rate` |
| ELW종목상세정보요청 | `❌ detailed_inmation_on_elw_items` | **`✅ detailed_information_elw_items`** |
| ETF수익율요청 | `etf_return_rate` | `etf_return_rate` |
| ETF종목정보요청 | `❌ etf_item_inmation` | **`✅ etf_item_information`** |
| ETF일별추이요청 | `etf_daily_trend` | `etf_daily_trend` |
| ETF전체시세요청 | `❌ full_etf_view` | **`✅ full_etf`** |
| ETF시간대별추이요청 | `etf_time_zone_trend` | `etf_time_zone_trend` |
| ETF시간대별체결요청 | `etf_trading_by_time_slot` | `etf_trading_by_time_slot` |
| ETF일자별체결요청 | `etf_transaction_by_date` | `etf_transaction_by_date` |
| ETF시간대별체결요청 | `etf_trading_by_time_slot1` | `etf_trading_by_time_slot1` |
| ETF시간대별추이요청 | `❌ etf_time_zone_trend1` | **`✅ etf_time_zone_trend_request1`** |
