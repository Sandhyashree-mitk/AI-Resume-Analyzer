import pandas as pd
import os
from datetime import datetime


def save_history(
    name,
    email,
    score,
    skills,
    certifications
):

    filename = "history.csv"

    data = {
        "Date": [datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
        "Name": [name],
        "Email": [email],
        "ATS Score": [score],
        "Skills Count": [len(skills)],
        "Certificates Count": [0 if certifications == ["Not Found"] else len(certifications)]
    }

    new_row = pd.DataFrame(data)

    if os.path.exists(filename):
        old_data = pd.read_csv(filename)
        updated_data = pd.concat([old_data, new_row], ignore_index=True)
    else:
        updated_data = new_row

    updated_data.to_csv(filename, index=False)