from core.analysis.recommendation import (
    get_recommendation
)

scores = [90, 70, 45]

for score in scores:

    recommendation, emoji = (
        get_recommendation(score)
    )

    print(
        f"{score} -> "
        f"{recommendation} "
        f"{emoji}"
    )