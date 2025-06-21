
import streamlit as st
import pandas as pd
import os

EXCEL_FILE = 'HARMONICS_data_template.xlsx'

st.title("HARMONICS Data Collection and Update Form")

# Load existing data
if os.path.exists(EXCEL_FILE):
    df_existing = pd.read_excel(EXCEL_FILE)
else:
    st.error("Excel file not found.")
    st.stop()

columns = df_existing.columns
dropdown_options = {
    "Sex": ["Male", "Female"],
    "AIS_Grade": ["A", "B", "C", "D"],
    "Surgery_Type": ["Sphincterotomy", "Augmentation", "Bricker"],
    "Diary_Returned_Pre": ["Yes", "No"],
    "ABPM_Data_Valid_Pre": ["Yes", "No"],
    "Bladder_Routine_Pre": ["Yes", "No"],
    "Bowel_Routine_Pre": ["Yes", "No"],
    "Diabetes": ["Yes", "No"],
    "Hypercholesterolemia": ["Yes", "No"],
    "Family_History_CAD": ["Yes", "No"],
    "Metabolic_Syndrome": ["Yes", "No"],
    "Obesity": ["Yes", "No"]
}

# Select patient ID
st.sidebar.header("Patient Lookup")
patient_id = st.sidebar.text_input("Enter Patient_ID to view/edit:")

record_index = None
record_data = {}

if patient_id:
    if patient_id in df_existing["Patient_ID"].astype(str).values:
        record_index = df_existing[df_existing["Patient_ID"].astype(str) == patient_id].index[0]
        st.sidebar.success(f"Record for Patient_ID {patient_id} found.")
        record_data = df_existing.loc[record_index].to_dict()
    else:
        st.sidebar.warning("Patient_ID not found. A new entry will be created.")

# Input form
with st.form("data_entry_form"):
    st.write("### Patient Data Entry")
    data = {}
    for col in columns:
        default_val = record_data.get(col, "")
        if col in dropdown_options:
            data[col] = st.selectbox(f"{col}:", dropdown_options[col], index=dropdown_options[col].index(default_val) if default_val in dropdown_options[col] else 0)
        elif "Date" in col or "Time" in col:
            data[col] = st.text_input(f"{col} (YYYY-MM-DD or HH:MM):", value=default_val)
        elif "Score" in col or "SBP" in col or "DBP" in col or "Number" in col or "Percent" in col:
            try:
                default_val = float(default_val)
            except:
                default_val = 0.0
            data[col] = st.number_input(f"{col}:", value=default_val)
        else:
            data[col] = st.text_input(f"{col}:", value=default_val)

    submitted = st.form_submit_button("Submit")

if submitted:
    df_new = pd.DataFrame([data])
    if record_index is not None:
        for col in columns:
            df_existing.at[record_index, col] = data[col]
    else:
        df_existing = pd.concat([df_existing, df_new], ignore_index=True)
    df_existing.to_excel(EXCEL_FILE, index=False)
    st.success("Data saved successfully!")
