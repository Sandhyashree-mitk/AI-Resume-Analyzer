import pandas as pd


def recommend_courses(missing_skills):

    df = pd.read_csv("courses.csv")

    recommendations = []

    for skill in missing_skills:

        result = df[
            df["Skill"].str.lower() == skill.lower()
        ]

        if not result.empty:

            recommendations.append(
                {
                    "Skill": skill,
                    "Course": result.iloc[0]["Course"],
                    "Platform": result.iloc[0]["Platform"]
                }
            )

    return recommendations