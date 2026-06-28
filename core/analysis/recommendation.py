def get_recommendation(ats_score):

    if ats_score >= 80:

        return (
            "Strong Candidate",
            "✅"
        )

    elif ats_score >= 60:

        return (
            "Moderate Candidate",
            "⚠️"
        )

    else:

        return (
            "Weak Candidate",
            "❌"
        )