import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def create_ats_cv(filepath, name, email, phone, location, summary, experience, education, skills, languages, visa):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Fonts
    font_normal = "Helvetica"
    font_bold = "Helvetica-Bold"
    
    y = height - 50
    margin_left = 50
    
    # Header
    c.setFont(font_bold, 24)
    c.drawString(margin_left, y, name)
    y -= 20
    
    c.setFont(font_normal, 10)
    c.drawString(margin_left, y, f"{email} | {phone} | {location}")
    y -= 30
    
    # Summary
    c.setFont(font_bold, 12)
    c.drawString(margin_left, y, "PROFESSIONAL SUMMARY")
    c.line(margin_left, y-2, width - margin_left, y-2)
    y -= 15
    
    c.setFont(font_normal, 10)
    # wrap text simple implementation
    import textwrap
    wrapped_summary = textwrap.wrap(summary, width=100)
    for line in wrapped_summary:
        c.drawString(margin_left, y, line)
        y -= 15
    y -= 10
    
    # Experience
    c.setFont(font_bold, 12)
    c.drawString(margin_left, y, "WORK EXPERIENCE")
    c.line(margin_left, y-2, width - margin_left, y-2)
    y -= 15
    
    for job in experience:
        c.setFont(font_bold, 10)
        c.drawString(margin_left, y, job['title'])
        c.setFont(font_normal, 10)
        c.drawRightString(width - margin_left, y, job['dates'])
        y -= 15
        
        c.setFont(font_bold, 10)
        c.drawString(margin_left, y, job['company'])
        y -= 15
        
        c.setFont(font_normal, 10)
        for bullet in job['bullets']:
            wrapped_bullet = textwrap.wrap(bullet, width=95)
            c.drawString(margin_left + 10, y, f"• {wrapped_bullet[0]}")
            y -= 15
            for extra_line in wrapped_bullet[1:]:
                c.drawString(margin_left + 20, y, extra_line)
                y -= 15
        y -= 5

    # Education
    c.setFont(font_bold, 12)
    c.drawString(margin_left, y, "EDUCATION")
    c.line(margin_left, y-2, width - margin_left, y-2)
    y -= 15
    
    for edu in education:
        c.setFont(font_bold, 10)
        c.drawString(margin_left, y, edu['degree'])
        c.setFont(font_normal, 10)
        c.drawRightString(width - margin_left, y, edu['year'])
        y -= 15
        c.drawString(margin_left, y, edu['school'])
        y -= 20

    # Skills
    c.setFont(font_bold, 12)
    c.drawString(margin_left, y, "SKILLS & CERTIFICATIONS")
    c.line(margin_left, y-2, width - margin_left, y-2)
    y -= 15
    c.setFont(font_normal, 10)
    wrapped_skills = textwrap.wrap(skills, width=100)
    for line in wrapped_skills:
        c.drawString(margin_left, y, line)
        y -= 15
    y -= 10

    # Languages
    c.setFont(font_bold, 12)
    c.drawString(margin_left, y, "LANGUAGES")
    c.line(margin_left, y-2, width - margin_left, y-2)
    y -= 15
    c.setFont(font_normal, 10)
    c.drawString(margin_left, y, languages)
    y -= 25

    # Visa
    if visa:
        c.setFont(font_bold, 12)
        c.drawString(margin_left, y, "VISA & WORK ELIGIBILITY")
        c.line(margin_left, y-2, width - margin_left, y-2)
        y -= 15
        c.setFont(font_normal, 10)
        c.drawString(margin_left, y, visa)

    c.save()


def generate_all_cvs():
    output_dir = "sample_data"
    os.makedirs(output_dir, exist_ok=True)
    
    candidates = [
        # 1. PASS - Perfect match
        {
            "filename": "01_John_Doe_Pass.pdf",
            "name": "JOHN DOE",
            "email": "john.doe@email.com",
            "phone": "+971-50-1234567",
            "location": "Dubai, UAE",
            "summary": "Award-winning Executive Sous Chef with 6 years of experience in luxury fine dining. Proven track record in Brigade Management, elevating food quality, and optimizing food costs.",
            "experience": [
                {
                    "title": "Executive Sous Chef",
                    "company": "The Ritz Luxury Hotel, Dubai",
                    "dates": "Jan 2018 - Present",
                    "bullets": [
                        "Managed a brigade of 25 chefs across 4 fine dining outlets.",
                        "Responsible for food cost & yield, ensuring 28% food cost targets were consistently met.",
                        "Maintained HACCP Level 3 standards across all kitchens with 100% audit pass rates.",
                        "Collaborated with Executive Chef to develop seasonal menus featuring Halal Compliance."
                    ]
                }
            ],
            "education": [{"degree": "Bachelor of Culinary Arts", "school": "Le Cordon Bleu, Paris", "year": "2015"}],
            "skills": "HACCP Level 3 Certified, Brigade Management, Food Cost & Yield, Michelin / Gault&Millau Experience, Halal Compliance.",
            "languages": "English (Professional Proficiency / C1), French (Intermediate).",
            "visa": "UAE Golden Visa holder, fully eligible to work."
        },
        # 2. FAIL - Low Experience
        {
            "filename": "02_Jane_Smith_Fail.pdf",
            "name": "JANE SMITH",
            "email": "jane.smith@email.com",
            "phone": "+44-7700-900123",
            "location": "London, UK",
            "summary": "Passionate Commis Chef with 2 years of experience in bustling urban cafes. Eager to learn and grow in a fine dining environment.",
            "experience": [
                {
                    "title": "Commis Chef",
                    "company": "The Corner Cafe, London",
                    "dates": "Mar 2022 - Present",
                    "bullets": [
                        "Prepared basic meals and assisted in menu planning.",
                        "Managed inventory and daily stock taking routines.",
                        "Maintained a clean and safe kitchen environment."
                    ]
                }
            ],
            "education": [{"degree": "Diploma in Culinary Arts", "school": "London Culinary Institute", "year": "2021"}],
            "skills": "Basic Cooking, Food Safety, Inventory Management, Teamwork.",
            "languages": "English (Fluent / C2).",
            "visa": "UK Citizen."
        },
        # 3. REVIEW - Unknown Visa
        {
            "filename": "03_Michael_Johnson_Review.pdf",
            "name": "MICHAEL JOHNSON",
            "email": "michael.j@email.com",
            "phone": "+1-212-555-0199",
            "location": "New York, USA",
            "summary": "Dynamic Head Chef with 9 years of comprehensive fine dining experience. Highly skilled in brigade management and food cost control.",
            "experience": [
                {
                    "title": "Head Chef",
                    "company": "Le Bernardin Fine Dining, New York",
                    "dates": "Feb 2015 - Jan 2024",
                    "bullets": [
                        "Led a brigade of 30+ staff in a Michelin-starred environment.",
                        "Controlled Food Cost & Yield strictly, saving the restaurant 15% annually.",
                        "Maintained strict HACCP Level 3 compliance."
                    ]
                }
            ],
            "education": [{"degree": "Associate in Culinary Arts", "school": "CIA New York", "year": "2014"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost, Menu Development, Michelin Experience.",
            "languages": "English (Native / C2).",
            "visa": "" # Deliberately empty
        },
        # 4. PASS - 10 years exp
        {
            "filename": "04_Ahmed_Al_Maktoum_Pass.pdf",
            "name": "AHMED AL MAKTOUM",
            "email": "ahmed.maktoum@email.ae",
            "phone": "+971-55-9876543",
            "location": "Abu Dhabi, UAE",
            "summary": "Accomplished Culinary Director with over 10 years of progressive experience in Middle Eastern luxury hospitality.",
            "experience": [
                {
                    "title": "Culinary Director",
                    "company": "Emirates Palace, Abu Dhabi",
                    "dates": "Aug 2014 - Present",
                    "bullets": [
                        "Oversee 8 luxury dining outlets, including a Michelin-starred signature restaurant.",
                        "Direct brigade management of over 50 culinary professionals.",
                        "Strict adherence to Halal compliance, HACCP Level 3, and advanced food cost metrics."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Management", "school": "Dubai Tourism College", "year": "2012"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience, Halal Compliance.",
            "languages": "Arabic (Native), English (C1).",
            "visa": "UAE Citizen."
        },
        # 5. FAIL - Wrong Industry
        {
            "filename": "05_Emily_Chen_Fail.pdf",
            "name": "EMILY CHEN",
            "email": "emily.chen@tech.com",
            "phone": "+1-415-555-0100",
            "location": "San Francisco, USA",
            "summary": "Senior Software Engineer with 6 years of experience building scalable backend services. Looking to transition into a new career path.",
            "experience": [
                {
                    "title": "Senior Backend Engineer",
                    "company": "Tech Innovations Inc.",
                    "dates": "Jul 2018 - Present",
                    "bullets": [
                        "Developed RESTful APIs using Python and FastAPI.",
                        "Managed a team of 5 junior developers.",
                        "Optimized database queries resulting in a 30% performance increase."
                    ]
                }
            ],
            "education": [{"degree": "BSc Computer Science", "school": "Stanford University", "year": "2018"}],
            "skills": "Python, API Design, Team Management, SQL, Agile.",
            "languages": "English (C2).",
            "visa": "US Citizen."
        },
        # 6. REVIEW - Missing Michelin
        {
            "filename": "06_Carlos_Rodriguez_Review.pdf",
            "name": "CARLOS RODRIGUEZ",
            "email": "crodriguez@email.es",
            "phone": "+34-600-123456",
            "location": "Madrid, Spain",
            "summary": "Dedicated Sous Chef with 8 years of experience in high-volume luxury catering.",
            "experience": [
                {
                    "title": "Sous Chef",
                    "company": "Grand Hotel Madrid",
                    "dates": "May 2016 - Present",
                    "bullets": [
                        "Supervised brigade management of 15 cooks during peak banquet operations.",
                        "Ensured strict food cost & yield margins.",
                        "Maintained HACCP Level 3 certification for the entire kitchen."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Arts", "school": "Madrid Culinary School", "year": "2015"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Spanish Cuisine.",
            "languages": "Spanish (Native), English (C1).",
            "visa": "Willing to relocate, requires visa sponsorship."
        },
        # 7. PASS - French Chef
        {
            "filename": "07_Pierre_Dubois_Pass.pdf",
            "name": "PIERRE DUBOIS",
            "email": "pierre.dubois@email.fr",
            "phone": "+971-52-1112233",
            "location": "Dubai, UAE",
            "summary": "Classical French-trained Executive Sous Chef with 6 years of fine dining expertise.",
            "experience": [
                {
                    "title": "Executive Sous Chef",
                    "company": "L'Atelier Dubai",
                    "dates": "2018 - 2024",
                    "bullets": [
                        "Maintained 1 Michelin Star standards continuously.",
                        "Executed precise brigade management for a team of 20.",
                        "Optimized food cost & yield by sourcing local high-quality ingredients.",
                        "Certified in HACCP Level 3 and Halal Compliance."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Diploma", "school": "Paul Bocuse Institute", "year": "2017"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience, Halal Compliance.",
            "languages": "French (Native), English (C1).",
            "visa": "UAE Employment Visa eligible."
        },
        # 8. FAIL - Language
        {
            "filename": "08_Liam_OConnor_Fail.pdf",
            "name": "LIAM O'CONNOR",
            "email": "liam.o@email.ie",
            "phone": "+353-87-1234567",
            "location": "Dublin, Ireland",
            "summary": "Experienced Chef with 5 years in fine dining.",
            "experience": [
                {
                    "title": "Sous Chef",
                    "company": "The Dubliner Michelin Resto",
                    "dates": "2019 - Present",
                    "bullets": [
                        "Assisted in Michelin-level food preparation.",
                        "Managed brigade of 10 staff.",
                        "Certified HACCP Level 3 and responsible for food costs."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Arts", "school": "Dublin Tech", "year": "2018"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience.",
            "languages": "English (Basic / B1), Irish (Fluent).",
            "visa": "Eligible for UAE Visa."
        },
        # 9. REVIEW - Experience unclear
        {
            "filename": "09_Aisha_Khan_Review.pdf",
            "name": "AISHA KHAN",
            "email": "aisha.k@email.com",
            "phone": "+92-300-1234567",
            "location": "Karachi, Pakistan",
            "summary": "Culinary professional with diverse experience in hotel kitchens.",
            "experience": [
                {
                    "title": "Chef de Partie",
                    "company": "Luxury Hotel Karachi",
                    "dates": "Recent",
                    "bullets": [
                        "Worked on various stations.",
                        "Ensured Halal compliance and HACCP Level 3 standards.",
                        "Helped with food cost and brigade management."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Diploma", "school": "Karachi Culinary", "year": "2020"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost, Halal Compliance.",
            "languages": "Urdu (Native), English (C1).",
            "visa": "Eligible for UAE visa."
        },
        # 10. PASS - Strong Candidate
        {
            "filename": "10_Fatima_Zahra_Pass.pdf",
            "name": "FATIMA ZAHRA",
            "email": "fatima.z@email.ma",
            "phone": "+212-600-123456",
            "location": "Casablanca, Morocco",
            "summary": "Executive Sous Chef with 7 years of luxury hotel experience. Focused on excellence and team leadership.",
            "experience": [
                {
                    "title": "Executive Sous Chef",
                    "company": "Four Seasons Casablanca",
                    "dates": "Jan 2017 - Present",
                    "bullets": [
                        "Co-lead culinary operations (Michelin / Gault&Millau standard).",
                        "Brigade management of 35 chefs.",
                        "Strict control over food cost & yield.",
                        "HACCP Level 3 Certified."
                    ]
                }
            ],
            "education": [{"degree": "Advanced Culinary Arts", "school": "Morocco Culinary Institute", "year": "2015"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience, Halal Compliance.",
            "languages": "Arabic (Native), French (Fluent), English (C1).",
            "visa": "Requires Visa Sponsorship (Eligible)."
        },
        # 11. FAIL - Missing HACCP
        {
            "filename": "11_David_Kim_Fail.pdf",
            "name": "DAVID KIM",
            "email": "david.kim@email.kr",
            "phone": "+82-10-1234-5678",
            "location": "Seoul, South Korea",
            "summary": "Innovative Chef with 6 years of experience in high-end Asian fusion.",
            "experience": [
                {
                    "title": "Sous Chef",
                    "company": "Seoul Fusion (Michelin 1 Star)",
                    "dates": "2018 - 2024",
                    "bullets": [
                        "Managed a brigade of 15 chefs.",
                        "Maintained excellent food cost and yield ratios.",
                        "Developed seasonal menus."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Arts", "school": "Seoul Culinary", "year": "2017"}],
            "skills": "Brigade Management, Food Cost, Menu Design, Michelin Experience.",
            "languages": "Korean (Native), English (C1).",
            "visa": "Eligible for UAE Employment Visa."
        },
        # 12. PASS - Highly Experienced
        {
            "filename": "12_Marco_Rossi_Pass.pdf",
            "name": "MARCO ROSSI",
            "email": "marco.rossi@email.it",
            "phone": "+39-333-1234567",
            "location": "Milan, Italy",
            "summary": "Culinary veteran with 12 years of fine dining experience across Europe.",
            "experience": [
                {
                    "title": "Executive Chef",
                    "company": "Osteria Milano (2 Michelin Stars)",
                    "dates": "2012 - 2024",
                    "bullets": [
                        "Oversee all culinary operations.",
                        "Extensive brigade management experience (40+).",
                        "Expert in food cost & yield optimization.",
                        "Certified HACCP Level 3."
                    ]
                }
            ],
            "education": [{"degree": "Master Chef Diploma", "school": "Italian Culinary Academy", "year": "2010"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience.",
            "languages": "Italian (Native), English (C2).",
            "visa": "Eligible for UAE Visa."
        },
        # 13. REVIEW - Partial Skills
        {
            "filename": "13_Sarah_Connor_Review.pdf",
            "name": "SARAH CONNOR",
            "email": "sarah.c@email.com",
            "phone": "+1-310-555-0188",
            "location": "Los Angeles, USA",
            "summary": "Creative culinary professional with 5 years of fine dining experience.",
            "experience": [
                {
                    "title": "Chef de Cuisine",
                    "company": "LA Fine Dining",
                    "dates": "2019 - Present",
                    "bullets": [
                        "Crafted Michelin-quality dishes.",
                        "Maintained HACCP Level 3 safety protocols.",
                        "Analyzed food cost & yield."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Arts", "school": "CIA", "year": "2018"}],
            "skills": "HACCP Level 3, Food Cost & Yield, Michelin Experience.",
            "languages": "English (Native / C2).",
            "visa": "Eligible for UAE Visa."
        },
        # 14. FAIL - Low Experience
        {
            "filename": "14_Viktor_Ivanov_Fail.pdf",
            "name": "VIKTOR IVANOV",
            "email": "viktor.i@email.ru",
            "phone": "+7-900-123-45-67",
            "location": "Moscow, Russia",
            "summary": "Rising star in the culinary world with 3 years of intensive fine dining experience.",
            "experience": [
                {
                    "title": "Sous Chef",
                    "company": "Moscow Elite Restaurant",
                    "dates": "2021 - Present",
                    "bullets": [
                        "Assisted in Brigade Management.",
                        "Ensured HACCP Level 3 compliance.",
                        "Gained Michelin/Gault&Millau experience.",
                        "Monitored Food Cost & Yield."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Arts", "school": "Moscow Food Academy", "year": "2020"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience.",
            "languages": "Russian (Native), English (C1).",
            "visa": "Eligible for UAE Visa."
        },
        # 15. PASS - Another Strong Candidate
        {
            "filename": "15_Kenji_Sato_Pass.pdf",
            "name": "KENJI SATO",
            "email": "kenji.sato@email.jp",
            "phone": "+81-90-1234-5678",
            "location": "Tokyo, Japan",
            "summary": "Dedicated Executive Sous Chef with 8 years of experience in Michelin-starred environments.",
            "experience": [
                {
                    "title": "Executive Sous Chef",
                    "company": "Tokyo Fine Dining",
                    "dates": "2016 - 2024",
                    "bullets": [
                        "Maintained 2 Michelin stars for 5 consecutive years.",
                        "Led a multicultural brigade of 25 chefs (Brigade Management).",
                        "Implemented strict HACCP Level 3 and Food Cost & Yield controls."
                    ]
                }
            ],
            "education": [{"degree": "Culinary Mastery", "school": "Tokyo Culinary Academy", "year": "2015"}],
            "skills": "HACCP Level 3, Brigade Management, Food Cost & Yield, Michelin Experience.",
            "languages": "Japanese (Native), English (C1).",
            "visa": "Eligible for UAE Visa."
        }
    ]

    for cand in candidates:
        filepath = os.path.join(output_dir, cand['filename'])
        create_ats_cv(
            filepath,
            cand['name'],
            cand['email'],
            cand['phone'],
            cand['location'],
            cand['summary'],
            cand['experience'],
            cand['education'],
            cand['skills'],
            cand['languages'],
            cand['visa']
        )
        print(f"Created {filepath}")

if __name__ == "__main__":
    generate_all_cvs()
