import streamlit as st
import pickle

# Page config
st.set_page_config(page_title='💰 Premium Predictor', layout='centered')

# Custom title with styling
st.markdown("""
    <h2 style='text-align: center; color: #4CAF50;'>💡 Health Insurance Premium Prediction</h2>
    <p style='text-align: center; color: gray;'>Estimate your health insurance cost based on your lifestyle and profile</p>
    <hr style='border:1px solid #ddd'/>
""", unsafe_allow_html=True)

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

# Layout in columns
col1, col2 = st.columns(2)

with col1:
    age = st.number_input('👤 Enter your Age:', min_value=0, max_value=120, value=30, step=1, placeholder="Eg: 30")
    bmi = st.number_input('⚖️ Enter your BMI:', min_value=10.0, max_value=50.0, value=25.0, step=0.1, placeholder="Eg: 22.5")
    children = st.number_input('👶 Enter Number of Children:', min_value=0, max_value=10, value=0, step=1, placeholder="Eg: 2")

with col2:
    gender = st.radio('🚻 Gender:', options=['Male', 'Female'], horizontal=True)
    smoker = st.radio('🚬 Do you Smoke?', options=['No', 'Yes'], horizontal=True)

# Tooltip help message
with st.expander("ℹ️ How is the premium calculated?"):
    st.write("""
    Premium is calculated based on:
    - Age
    - Body Mass Index (BMI)
    - Number of children
    - Gender
    - Smoking habits
    """)

# Check for valid inputs before enabling button
can_predict = age > 0 and bmi > 0 and children >= 0

# Predict button
predict_btn = st.button('🔍 Predict My Premium', disabled=not can_predict)

if predict_btn:
    # Encoding categorical variables
    gender_val = 0 if gender.upper() == 'MALE' else 1
    smoker_val = 0 if smoker.upper() == 'NO' else 1

    X_test = [[age, bmi, children, gender_val, smoker_val]]
    predicted_premium = round(model.predict(X_test)[0], 2)

    # Display result with some styling
    st.markdown(f"""
        <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #e0f7fa, #fce4ec); 
                    border-radius: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #333;'>🎯 Your Estimated Annual Premium is:</h3>
            <h1 style='color: #E91E63;'>${predicted_premium}</h1>
        </div>
    """, unsafe_allow_html=True)
