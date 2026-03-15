import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg') # 必须保留，防止白屏
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(page_title="Task 2.4 Metrics Visualization", layout="wide")
st.title("📊 Task 2.4: 统计数据可视化 (柱状图版)")
st.markdown("请分别截取下方的图表，填入作业文档对应的框中。")
st.markdown("---")

# ==========================================
# 2. 数据处理
# ==========================================
try:
    df = pd.read_csv("results.csv")
    df['Score'] = pd.to_numeric(df['Score'])
except Exception as e:
    st.error(f"数据读取错误: {e}")
    st.stop()

# 计算指标
total_marks = df['Score'].sum()
average_score = round(df['Score'].mean(), 2)
median_score = round(df['Score'].median(), 2)
mean_score = round(df['Score'].mean(), 2)

# ==========================================
# 3. 定义画图函数 (避免重复代码)
# ==========================================
def plot_single_bar(label, value, color, max_y=None):
    """
    绘制单个柱状图的通用函数
    """
    fig, ax = plt.subplots(figsize=(5, 6)) # 设置画布大小
    
    # 画柱子
    sns.barplot(x=[label], y=[value], color=color, ax=ax)
    
    # 设置Y轴高度 (留出一点空间给数字)
    if max_y:
        ax.set_ylim(0, max_y)
    else:
        ax.set_ylim(0, value * 1.2) 
        
    # 在柱子上方标出具体数字 (重点！)
    ax.text(0, value + (value * 0.02), f"{value}", 
            ha='center', va='bottom', fontsize=20, fontweight='bold')
    
    # 去掉多余的边框，让图更好看
    sns.despine()
    ax.set_ylabel("Value")
    
    return fig

# ==========================================
# 4. 展示图表区域
# ==========================================

# --- 第一行：Total Marks (数值很大，单独放) ---
st.subheader("1. Screenshot of Total Marks")
col1, col_space = st.columns([1, 2]) # 左边放图，右边留空
with col1:
    # 蓝色柱子
    fig1 = plot_single_bar("Total Marks", total_marks, "#4c72b0") 
    st.pyplot(fig1)

st.divider()

# --- 第二行：Average, Median, Mean (数值很小，并排显示) ---
st.subheader("2. Metrics (Average, Median, Mean)")
col2, col3, col4 = st.columns(3)

# 设定统一的 Y 轴高度 (满分4分)，这样图表比例才真实
max_score_scale = 4.5 

with col2:
    st.write("**Screenshot of Average**")
    # 绿色柱子
    fig2 = plot_single_bar("Average", average_score, "#55a868", max_y=max_score_scale)
    st.pyplot(fig2)

with col3:
    st.write("**Screenshot of Median**")
    # 黄色柱子
    fig3 = plot_single_bar("Median", median_score, "#f1c40f", max_y=max_score_scale)
    st.pyplot(fig3)

with col4:
    st.write("**Screenshot of Mean**")
    # 红色柱子
    fig4 = plot_single_bar("Mean", mean_score, "#c44e52", max_y=max_score_scale)
    st.pyplot(fig4)

# ==========================================
# 5. 原始数据表 (备用)
# ==========================================
with st.expander("查看原始数据"):
    st.dataframe(df)
