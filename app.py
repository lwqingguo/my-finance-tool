import streamlit as st
import yfinance as yf
import pandas as pd

# 页面配置
st.set_page_config(page_title="财务诊断专家", layout="wide")
st.title("📊 财务实时分析与决策系统")

# 侧边栏：输入代码
ticker_input = st.sidebar.text_input("输入股票代码 (如: NVDA, AAPL, 700.HK)", "NVDA")

if ticker_input:
    stock = yf.Ticker(ticker_input)
    
    # 获取年度数据
    try:
        df = stock.financials
        # 诊断逻辑：ROE 和 净利润率
        info = stock.info
        name = info.get('longName', '未知公司')
        current_price = info.get('currentPrice', 'N/A')
        
        st.header(f"{name} ({ticker_input}) - 当前股价: ${current_price}")
        
        # 核心指标计算
        cols = st.columns(3)
        with cols[0]:
            roe = info.get('returnOnEquity', 0) * 100
            st.metric("ROE (净资产收益率)", f"{roe:.2f}%", delta=">15% 为优" if roe > 15 else "")
        with cols[1]:
            margin = info.get('profitMargins', 0) * 100
            st.metric("销售净利率", f"{margin:.2f}%")
        with cols[2]:
            pe = info.get('trailingPE', 0)
            st.metric("动态 PE (估值)", f"{pe:.2f}")

        # 趋势图表
        st.subheader("营收与利润增长趋势")
        plot_data = df.loc[['Total Revenue', 'Net Income']].T
        st.line_chart(plot_data)
        
        # 专家决策建议
        st.divider()
        st.subheader("🤖 财务专家诊断意见")
        if roe > 15 and margin > 10:
            st.success("✅ 该公司盈利能力极强，具备高度关注价值。")
        elif roe < 5:
            st.error("⚠️ 盈利能力偏弱，需谨慎观察资产减值风险。")
        else:
            st.warning("🧐 表现平平，建议对比同行业竞争对手后再做决定。")

    except Exception as e:
        st.error(f"解析出错：请输入正确的股票代码。港股请加后缀（如 0700.HK）")
