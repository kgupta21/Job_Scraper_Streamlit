import streamlit as st
import csv
from jobspy import scrape_jobs
import pandas as pd

# Streamlit App
st.title("Job Finder")
st.write("This app finds job listings from various platforms based on your input criteria.")

# User Inputs
site_name = st.multiselect("Select Job Sites", ["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"], default=["indeed", "linkedin"])
search_term = st.text_input("Job Search Term", "project manager environment")
google_search_term = st.text_input("Google Search Term", "project manager environmental jobs near Ottawa since last month")
location = st.text_input("Job Location", "Ottawa, Ontario")
results_wanted = st.number_input("Number of Results Wanted", min_value=1, max_value=100, value=20, step=1)
hours_old = st.number_input("Max Age of Job Postings (in hours)", min_value=1, value=720, step=1)
country_indeed = st.text_input("Country for Indeed Search", "Canada")

# Button to Trigger Scraping
if st.button("Find Jobs"):
    try:
        # Scraping Jobs
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed
        )

        st.success(f"Found {len(jobs)} jobs.")

        # Display Jobs
        st.write("### Job Listings")
        st.dataframe(jobs)

        # Convert to CSV for Download
        csv_file = "jobs.csv"
        jobs.to_csv(csv_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

        # File Download
        with open(csv_file, "rb") as file:
            st.download_button(
                label="Download Jobs as CSV",
                data=file,
                file_name="jobs.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
