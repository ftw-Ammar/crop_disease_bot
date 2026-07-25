# ============================================
# 🌿 Crop Disease Diagnosis Chatbot
# ============================================

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load API key from .env file
load_dotenv()

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="Crop Disease Assistant",
    page_icon="🌿",
    layout="centered"
)

# ============================================
# Custom CSS for better styling
# ============================================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E7D32;
    }
    .sub-header {
        text-align: center;
        color: #558B2F;
        font-style: italic;
    }
    .warning-box {
        background-color: #FFF3E0;
        border-left: 5px solid #FF6F00;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Header Section
# ============================================
st.markdown('<h1 class="main-header">🌿 Crop Disease Diagnosis Chatbot</h1>', 
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-powered plant doctor for healthy harvests</p>', 
            unsafe_allow_html=True)

# ============================================
# Quick Tips Section (Sidebar)
# ============================================
with st.sidebar:
    st.header("📋 Quick Tips")
    st.markdown("""
    **How to describe symptoms:**
    - 🌾 Crop type (rice, wheat, corn, etc.)
    - 🍃 Affected part (leaves, stem, roots, fruit)
    - 🟡 Color changes (yellow, brown, black spots)
    - 📐 Pattern (wilting, curling, spots, rot)
    - 🌧️ Weather conditions
    - 📅 When you noticed it
    
    **Common diseases covered:**
    - Leaf Blight
    - Powdery Mildew
    - Rust Disease
    - Root Rot
    - Bacterial Wilt
    - Downy Mildew
    - Anthracnose
    - Mosaic Virus
    """)
    
    st.divider()
    
    st.markdown("### 🚨 Emergency Signs")
    st.warning("""
    Seek expert help if:
    - Whole field is affected
    - Rapid spreading
    - Unknown symptoms
    - Crop is dying quickly
    """)

# ============================================
# Main Input Area
# ============================================
st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.markdown("""
### 👨‍🌾 Describe Your Crop Problem
Tell me about your crop and what you're observing. The more details you provide, 
the better I can help diagnose the issue.
""")

# Example questions to guide users
with st.expander("📝 Example Questions You Can Ask"):
    st.markdown("""
    - "My tomato leaves have yellow spots and are curling. What could it be?"
    - "There's white powder on my cucumber leaves. How do I treat it?"
    - "Rice plants are turning brown from the tips. Is this a disease?"
    - "What are common wheat rust symptoms and treatments?"
    - "How can I prevent fungal diseases in my vegetable garden?"
    """)

# User input
crop_problem = st.text_area(
    "Describe the symptoms you're seeing:",
    placeholder="Example: My potato plants have dark brown spots on the leaves and the stems are turning black. It started after heavy rains last week...",
    height=150
)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# Diagnosis Options
# ============================================
col1, col2 = st.columns(2)

with col1:
    diagnosis_type = st.radio(
        "What type of help do you need?",
        ["🔍 Identify Disease", "💊 Treatment Only", "🛡️ Prevention Tips"],
        index=0
    )

with col2:
    severity = st.select_slider(
        "How severe is the problem?",
        options=["Mild", "Moderate", "Severe", "Critical"],
        value="Moderate"
    )

# ============================================
# AI Diagnosis Button
# ============================================
st.divider()

diagnose_button = st.button("🌿 Diagnose My Crop", type="primary", use_container_width=True)

# ============================================
# AI Processing
# ============================================
if diagnose_button:
    if not crop_problem.strip():
        st.error("⚠️ Please describe the symptoms you're observing in your crop.")
    else:
        # Show processing message
        with st.spinner("🔬 Analyzing your crop symptoms... Please wait..."):
            
            # Create LLM with appropriate settings
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.3,  # Lower for more accurate diagnosis
            )
            
            # Build diagnosis-specific prompt
            base_prompt = """
You are an expert Plant Pathologist and Agricultural Scientist with 20 years of experience in crop disease diagnosis.
Your role is to help farmers identify crop diseases from symptoms and provide actionable treatment plans.

IMPORTANT RULES:
1. Only answer questions related to crop diseases, plant health, and farming.
2. If the user asks about anything unrelated to agriculture, reply:
   "I'm a Crop Disease Specialist. I can only help with plant diseases and crop health questions."
3. Always include a disclaimer that severe cases need professional field inspection.
4. Be specific about treatment methods, including both organic and chemical options where appropriate.

The user's crop problem severity level is: {severity}
The type of help requested is: {diagnosis_type}
"""
            
            # Adjust prompt based on diagnosis type
            if "Identify" in diagnosis_type:
                prompt_addition = """
Focus on DISEASE IDENTIFICATION.
For the symptoms described, provide:
1. 🎯 LIKELY DISEASE(S): List the 2-3 most probable diseases with confidence levels
2. 🔍 KEY IDENTIFYING FEATURES: Specific visual symptoms that confirm each disease
3. 🧪 CONFIRMATION METHODS: Simple field tests to verify the diagnosis
4. 📸 WHAT TO LOOK FOR: How the disease progresses if untreated
"""
            elif "Treatment" in diagnosis_type:
                prompt_addition = """
Focus on TREATMENT METHODS.
For the symptoms described, provide:
1. 💊 IMMEDIATE TREATMENT: Step-by-step emergency actions to take right now
2. 🌿 ORGANIC SOLUTIONS: Natural remedies and biological controls
3. 🧪 CHEMICAL TREATMENTS: Specific fungicides/pesticides with application rates
4. ⏰ TREATMENT SCHEDULE: When and how often to apply treatments
5. ⚠️ SAFETY PRECAUTIONS: Protective measures during treatment
"""
            else:
                prompt_addition = """
Focus on PREVENTION STRATEGIES.
For the symptoms described, provide:
1. 🛡️ PREVENTIVE MEASURES: How to avoid this disease in future seasons
2. 🌱 RESISTANT VARIETIES: Crop varieties resistant to this disease
3. 🔄 CROP ROTATION PLAN: Suggested rotation to break disease cycle
4. 🌍 SOIL MANAGEMENT: Soil treatments to prevent recurrence
5. 📅 SEASONAL CALENDAR: Preventive spray schedule
"""

            full_prompt = base_prompt + prompt_addition + """
Current symptoms described by farmer:
{symptoms}

IMPORTANT: Structure your response clearly with emojis and simple language that farmers can easily understand.
End with: "🌻 Remember: For severe outbreaks affecting large areas, please consult your local agricultural extension office for field inspection."
"""
            
            # Create prompt template
            prompt = ChatPromptTemplate.from_template(full_prompt)
            
            # Create and run chain
            chain = prompt | llm
            
            try:
                response = chain.invoke({
                    "symptoms": crop_problem,
                    "severity": severity,
                    "diagnosis_type": diagnosis_type
                })
                
                # Display Results
                st.divider()
                st.markdown("## 📊 Diagnosis Results")
                
                # Success message with diagnosis
                st.success("✅ Analysis Complete! Here's what I found:")
                
                # Display the AI response in a formatted container
                with st.container():
                    st.markdown(response.content)
                
                # Additional Resources Section
                st.divider()
                st.markdown("### 📚 Additional Resources")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **🆘 Emergency Contact**
                    - Local Agriculture Office
                    - Plant Clinic
                    - Krishi Vigyan Kendra
                    """)
                
                with col2:
                    st.info("""
                    **📱 Mobile Apps**
                    - Plantix
                    - Crop Doctor
                    - AgriApp
                    """)
                
                with col3:
                    st.info("""
                    **📖 Learn More**
                    - ICAR Website
                    - Agriculture University
                    - Farming Communities
                    """)
                
                # Feedback section
                st.divider()
                feedback = st.radio(
                    "Was this diagnosis helpful?",
                    ["👍 Yes, very helpful!", "🤔 Somewhat helpful", "👎 Not helpful"],
                    horizontal=True
                )
                
                if feedback == "👎 Not helpful":
                    st.text_area("Help us improve! What was missing?", 
                                placeholder="Tell us what additional information you needed...")
                
            except Exception as e:
                st.error(f"❌ Error during diagnosis: {str(e)}")
                st.info("💡 Tip: Make sure your GROQ_API_KEY is correctly set in the .env file")

# ============================================
# Footer
# ============================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌿 Crop Disease Chatbot | Powered by AI | For educational purposes</p>
    <p style='font-size: 0.8em;'>⚠️ This tool provides general guidance. Always consult agricultural experts for confirmed diagnosis.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Features Showcase (Collapsible)
# ============================================
with st.expander("🌟 Features of this Chatbot"):
    st.markdown("""
    - ✅ **Symptom-Based Diagnosis**: Identifies diseases from visual descriptions
    - ✅ **Treatment Plans**: Both organic and chemical treatment options
    - ✅ **Prevention Strategies**: Long-term disease management
    - ✅ **Severity Assessment**: Tailored advice based on severity
    - ✅ **Farmer-Friendly Language**: Simple, practical guidance
    - ✅ **Safety Guidelines**: Proper handling and application instructions
    """)