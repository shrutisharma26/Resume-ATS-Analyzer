SECTIONS = {
    "education": [
        "education",
        "academic"
    ],

    "experience": [
        "experience",
        "work experience",
        "employment"
    ],

    "projects": [
        "projects",
        "project"
    ],

    "skills": [
        "skills",
        "technical skills",
        "tech stack"
    ],

    "certifications": [
        "certification",
        "certifications"
    ],

    "achievements": [
        "achievement",
        "achievements"
    ]
}


def check_sections(text):

    text = text.lower()

    present = []

    missing = []

    for section, keywords in (
            SECTIONS.items()):

        found = False

        for keyword in keywords:

            if keyword in text:
                found = True
                break

        if found:
            present.append(section)

        else:
            missing.append(section)

    return present, missing