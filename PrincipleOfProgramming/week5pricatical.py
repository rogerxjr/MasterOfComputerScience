import streamlit as st  # 导入 streamlit 库，并简写为 st

# # 1. st.title() -> 网页的大标题，字体最大
# st.title("Hello Streamlit - By [你的名字]") 

# # 2. st.header() -> 二级标题，比 title 小一点
# st.header("About Me")

# # 3. st.text() -> 显示普通文本，就像 Python 的 print()，但在网页上显示
# # 题目要求显示 3 个事实
# st.text("Fact 1: I am a Master's student.")
# st.text("Fact 2: I love coding.")
# st.text("Fact 3: I missed the last class but I am catching up!")

# # 4. st.success() -> 显示一个绿色的提示框，通常用于表示操作成功
# st.success("Welcome to my first Streamlit app!")

# --- Task 2: Simple Calculator ---
st.divider()  # 加一条分割线，把 Task 1 和 Task 2 分开
st.header("Task 2: Simple Calculator")

# 1. 输入两个数字
col1, col2 = st.columns(2)  # 创建两列，让输入框并排显示
with col1:
    num1 = st.number_input("Enter first number", value=0.0)
with col2:
    num2 = st.number_input("Enter second number", value=0.0)

# 2. 选择操作符
operation = st.selectbox("Choose operation", ["Add", "Subtract", "Multiply", "Divide"])

# 3. 点击按钮进行计算
if st.button("Calculate"):
    result = 0
    
    if operation == "Add":
        result = num1 + num2
        st.success(f"Result: {result}")
        
    elif operation == "Subtract":
        result = num1 - num2
        st.success(f"Result: {result}")
        
    elif operation == "Multiply":
        result = num1 * num2
        st.success(f"Result: {result}")
        
    elif operation == "Divide":
        if num2 == 0:
            st.error("Error: Cannot divide by zero!")
        else:
            result = num1 / num2
            st.success(f"Result: {result}")
