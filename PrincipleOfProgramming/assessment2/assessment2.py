import streamlit as st
import pandas as pd
import os
import time

# ==========================================
# 1. Core Functions
# ==========================================
def load_questions(filename="questions.txt"):
    """Load questions from the text file."""
    questions = []
    if not os.path.exists(filename):
        st.error(f"Error: File '{filename}' not found. Please check the path.")
        return []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            # Ensure the line has enough parts (Type|Q|Opt1|Opt2|Opt3|Opt4|Ans|Img)
            if len(parts) < 7: continue
            
            q_data = {
                "type": parts[0],
                "question": parts[1],
                "options": [parts[2], parts[3], parts[4], parts[5]],
                "answer": parts[6],
                "image": parts[7] if len(parts) >= 8 else None
            }
            questions.append(q_data)
    return questions

def save_result_to_csv(name, score, answers):
    """Append user result to CSV file."""
    file_exists = os.path.exists("results.csv")
    
    # Prepare data dictionary
    data = {
        "Name": [name],
        "Score": [score],
        "Q1_Ans": [answers[0]] if len(answers) > 0 else [""],
        "Q2_Ans": [answers[1]] if len(answers) > 1 else [""],
        "Q3_Ans": [answers[2]] if len(answers) > 2 else [""],
        "Q4_Ans": [answers[3]] if len(answers) > 3 else [""]
    }
    df = pd.DataFrame(data)
    
    # Append to CSV (header=True only if file doesn't exist)
    df.to_csv("results.csv", mode='a', header=not file_exists, index=False)

# ==========================================
# 2. Streamlit UI Logic
# ==========================================
def main():
    # Page Configuration
    st.set_page_config(page_title="Malaysia Food Quiz", page_icon="🍜")
    
    st.title("🇲🇾 Malaysia Food Knowledge Quiz")
    st.markdown("Test your knowledge about local Malaysian delicacies!")

    # --- Initialize Session State ---
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'quiz_finished' not in st.session_state:
        st.session_state.quiz_finished = False
    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions()

    questions = st.session_state.questions

    # Check if questions loaded successfully
    if not questions:
        st.warning("No questions loaded. Please check 'questions.txt'.")
        return

    # --- Phase 1: User Login ---
    if 'user_name' not in st.session_state:
        with st.container():
            st.subheader("Welcome")
            name_input = st.text_input("Please enter your name to start:", key="name_input_box")
            if st.button("Start Quiz"):
                if name_input.strip():
                    st.session_state.user_name = name_input.strip()
                    st.rerun()
                else:
                    st.warning("Name cannot be empty!")
        return

    # --- Phase 3: Quiz Finished ---
    if st.session_state.quiz_finished:
        st.balloons() # Fun effect
        st.success(f"🎉 Congratulations, {st.session_state.user_name}!")
        
        # Display Score
        st.metric(label="Final Score", value=f"{st.session_state.score} / {len(questions)}")
        
        st.write("### Your Answer History:")
        st.write(st.session_state.user_answers)
        
        st.info("Click the button below to save your result and reset for the next student.")
        
        # Save Button
        if st.button("Save Result & Next User"):
            save_result_to_csv(
                st.session_state.user_name, 
                st.session_state.score, 
                st.session_state.user_answers
            )
            st.success("Data successfully saved to results.csv!")
            time.sleep(1)
            
            # Reset Session State
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return

    # --- Phase 2: Quiz Loop ---
    idx = st.session_state.current_q
    q = questions[idx]

    # Progress Bar
    progress = (idx) / len(questions)
    st.progress(progress)
    st.subheader(f"Question {idx + 1} of {len(questions)}")

    # Display Question
    st.markdown(f"**{q['question']}**")

    # Display Image (if Type B)
    if q['type'] == "Type B" and q['image']:
        if os.path.exists(q['image']):
            st.image(q['image'], caption="Please refer to the image above", width=400)
        else:
            st.error(f"Image not found: {q['image']}")

    # Options (Radio Button)
    user_choice = st.radio("Select your answer:", q['options'], index=None, key=f"q_{idx}")

    # Submit Button
    if st.button("Submit Answer"):
        if not user_choice:
            st.warning("Please select an option first!")
        else:
            # Record Answer
            st.session_state.user_answers.append(user_choice)
            
            # Check Answer
            if user_choice == q['answer']:
                st.session_state.score += 1
                st.toast("✅ Correct!", icon="🎉")
            else:
                st.toast(f"❌ Incorrect! The correct answer was: {q['answer']}", icon="⚠️")
            
            # Move to next question
            time.sleep(1) # Short pause to see the toast
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
            else:
                st.session_state.quiz_finished = True
            
            st.rerun()

if __name__ == "__main__":
    main()
