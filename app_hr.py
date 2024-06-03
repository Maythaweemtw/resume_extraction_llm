import os
import csv
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate
import json

def load_resumes(filename="resumes.csv"):
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=["Name", "Email", "Phone", "Education", "Employment", "Skills"])

def match_skills(candidate_skills, required_skills, temperature=1.0):
    matched_skills = set(candidate_skills).intersection(required_skills)
    unmatched_skills = set(required_skills) - matched_skills
    total_required = len(required_skills)
    matched_count = len(matched_skills)

    if temperature > 1:
        # Allow for flexible skill matching, considering similar skills
        for skill in unmatched_skills:
            for candidate_skill in candidate_skills:
                if skill.lower() in candidate_skill.lower() or candidate_skill.lower() in skill.lower():
                    matched_skills.add(candidate_skill)
                    matched_count += 1
                    break

    return matched_skills, matched_count / total_required * 100

def main():
    load_dotenv()

    st.write("# HR Skill Matching Tool")

    st.write("### Enter Required Skills")
    required_skills_input = st.text_area("Required Skills (comma-separated)", "")
    temperature = st.slider("Temperature (0 for exact match, higher for flexible match)", 0.0, 20.0, 1.0)

    if st.button("Analyze Candidates"):
        if required_skills_input:
            required_skills = [skill.strip() for skill in required_skills_input.split(",")]
            resumes = load_resumes()

            results = []

            for idx, row in resumes.iterrows():
                candidate_skills = row["Skills"].split(", ")
                matched_skills, match_percentage = match_skills(candidate_skills, required_skills, temperature)
                
                results.append({
                    "Name": row["Name"],
                    "Email": row["Email"],
                    "Matched Skills": ", ".join(matched_skills),
                    "Match Percentage": match_percentage
                })

            results_df = pd.DataFrame(results)

            st.write("## Candidate Match Results")
            st.dataframe(results_df)

if __name__ == '__main__':
    main()
