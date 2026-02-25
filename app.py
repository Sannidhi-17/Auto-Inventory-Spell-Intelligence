import streamlit as st
import pandas as pd

from utils.fuzzy_match import fuzzy_match, load_master_parts
from utils.confidence import decide_tier
from utils.genai_correction import llama_correct
from utils.update_master import add_to_master


st.title("🚗  Automotive Part Spell Checker")

# -----------------------------
# Initialize Session State
# -----------------------------
if "checked" not in st.session_state:
    st.session_state.checked = False

if "manual_step" not in st.session_state:
    st.session_state.manual_step = 1

if "match" not in st.session_state:
    st.session_state.match = None

if "score" not in st.session_state:
    st.session_state.score = None

if "decision" not in st.session_state:
    st.session_state.decision = None


# -----------------------------
# User Input
# -----------------------------
input_part = st.text_input("Enter Automotive Part Name")

# -----------------------------
# Button Click
# -----------------------------
if st.button("Check Spelling"):

    if input_part.strip() == "":
        st.warning("Please enter a part name.")
    else:
        match, score = fuzzy_match(input_part)
        decision = decide_tier(score)

        # Store in session state
        st.session_state.match = match
        st.session_state.score = score
        st.session_state.decision = decision
        st.session_state.checked = True
        st.session_state.manual_step = 1


# -----------------------------
# Show Results (Outside Button)
# -----------------------------
if st.session_state.checked:

    match = st.session_state.match
    score = st.session_state.score
    decision = st.session_state.decision

    # ----------------------------------
    # 1️⃣ ACCEPT (High Confidence)
    # ----------------------------------
    if decision == "ACCEPT":
        st.write(f"Fuzzy Match: {match}")
        st.write(f"Confidence Score: {score}")
        st.success(f"✅ Corrected: {match}")

    # ----------------------------------
    # 2️⃣ GENAI (Medium Confidence)
    # ----------------------------------
    elif decision == "GENAI":
        st.warning("⚡️ Sending to GenAI for smarter correction...")

        ai_response = llama_correct(input_part)

        st.success(f"✅ AI Corrected: {ai_response}")

        # Add to master list if new
        added = add_to_master(ai_response)
        if added:
            st.info(f"📝 Added '{ai_response}' to master_parts.csv")
        else:
            st.info("Word already exists in master list.")

    # ----------------------------------
    # 3️⃣ MANUAL REVIEW (Low Confidence)
    # ----------------------------------
    else:
        st.error("⁉️ Low Confidence → Manual Review Required")

        # STEP 1
        if st.session_state.manual_step == 1:

            user_correct = st.radio(
                f"You entered '{input_part}'. Is this correct?",
                ["Yes", "No"],
                index=None,
                key="user_correct_radio"
            )

            if user_correct == "Yes":
                st.success("✅ Word is correct. No changes needed.")
                added = add_to_master(input_part)

                if added:
                    st.success(f"📝 '{input_part}' added to master_parts.csv")
                else:
                    st.info("Word already exists in master list.")

                # Reset flow
                st.session_state.manual_step = 1

            elif user_correct == "No":
                st.session_state.manual_step = 2
                st.rerun()

        # STEP 2
        elif st.session_state.manual_step == 2:

            user_wants_to_fix = st.radio(
                "Would you like to correct the spelling?",
                ["Yes", "No"],
                index=None,
                key="user_fix_radio"
            )

            if user_wants_to_fix == "No":
                st.info("No changes made.")

            elif user_wants_to_fix == "Yes":
                st.session_state.manual_step = 3
                st.rerun()

        # STEP 3
        elif st.session_state.manual_step == 3:

            corrected_input = st.text_input(
                "Enter Corrected Spelling",
                key="corrected_input_text"
            )

            if corrected_input:
                added = add_to_master(corrected_input)

                if added:
                    st.success(f"📝 '{corrected_input}' added to master_parts.csv")
                else:
                    st.info("Word already exists in master list.")

                # Reset manual flow after adding
                st.session_state.manual_step = 1


    # ----------------------------------
    # Reset Button (Optional but useful)
    # ----------------------------------
    if st.button("🔄 Check Another Word"):
        st.session_state.checked = False
        st.session_state.manual_step = 1
        st.session_state.match = None
        st.session_state.score = None
        st.session_state.decision = None
        
        # ✅ Clear input field
        st.session_state.input_part_text = ""

        st.rerun()

# -----------------------------
# Download Master Parts CSV
# -----------------------------
master_file_path = "master_parts.csv"  # Path to your master list

try:
    master_df = pd.read_csv(master_file_path)
    csv_data = master_df.to_csv(index=False).encode('utf-8')  # convert to bytes
    st.download_button(
        label="💾  Download Master Parts CSV",
        data=csv_data,
        file_name="master_parts.csv",
        mime="text/csv"
    )
except FileNotFoundError:
    st.warning("Master parts file not found. No file to download yet.")