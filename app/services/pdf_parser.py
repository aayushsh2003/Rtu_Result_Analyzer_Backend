import pdfplumber
import re

def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

    data = {}

    # ========== Basic Info ==========
    # College
    college_match = re.search(r'College Name:\s*(.+)', text)
    data['college'] = college_match.group(1).strip() if college_match else ""

    # Roll No & Enrollment No
    roll_match = re.search(r'Roll No\s*:\s*(\S+)', text)
    enroll_match = re.search(r'Enrollment No\s*:\s*(\S+)', text)
    data['roll_no'] = roll_match.group(1).strip() if roll_match else ""
    data['enrollment_no'] = enroll_match.group(1).strip() if enroll_match else ""

    # Name & Father's Name
    name_match = re.search(r'Name\s*:\s*(.*?)\s+Father\'s Name\s*:\s*(.+)', text)
    if name_match:
        data['name'] = name_match.group(1).strip()
        data['father_name'] = name_match.group(2).strip()
    else:
        data['name'] = ""
        data['father_name'] = ""

    # Remarks
    remarks_match = re.search(r'REMARKS\s*:\s*(\w+)', text)
    data['remarks'] = remarks_match.group(1) if remarks_match else "N/A"

    # ========== Subject Extraction ==========
    subject_data = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # DEBUG print to inspect actual line format
        print("DEBUG LINE:", repr(line))

        parts = line.split()

        # Must contain at least: title, code, marks, grade
        if len(parts) < 4:
            continue

        grade = parts[-1]
        if not re.match(r'^[A-Z][\+\-]*$', grade):  # Grade must be like A++, B+, etc.
            continue

        # Check for midterm and endterm marks
        try:
            if len(parts) >= 5 and re.match(r'^\d{1,3}$', parts[-3]):
                # Full: title code mid end grade
                course_code = parts[-4]
                midterm = int(parts[-3])
                endterm = int(parts[-2])
                course_title = ' '.join(parts[:-4])
            else:
                # Short: title code mid grade (e.g., Sodeca)
                course_code = parts[-3]
                midterm = int(parts[-2])
                endterm = 0
                course_title = ' '.join(parts[:-3])
        except ValueError as e:
            print(f"Error parsing marks: {e} in line: {line}")
            continue  # Skip this line if there's an error

        subject_data.append({
            'course_title': course_title.strip(),
            'course_code': course_code.strip(),
            'midterm_marks': midterm,
            'endterm_marks': endterm,
            'grade': grade.strip()
        })

    data['subjects'] = subject_data
    return data


# import pdfplumber
# import re

# def extract_pdf_data(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         first_page = pdf.pages[0]
#         text = first_page.extract_text()

#     data = {}

#     # ======= Extract College =======
#     data['college'] = re.search(r'College Name: (.+)', text).group(1).strip()
#     data['roll_no'] = re.search(r'Roll No\s*:\s*(\S+)', text).group(1).strip()
#     data['enrollment_no'] = re.search(r'Enrollment No\s*:\s*(\S+)', text).group(1).strip()

#     name_match = re.search(r'Name\s*:\s*(.*?)\s+Father\'s Name\s*:\s*(.+)', text)
#     if name_match:
#         data['name'] = name_match.group(1).strip()
#         data['father_name'] = name_match.group(2).strip()
#     else:
#         data['name'] = ""
#         data['father_name'] = ""

#     remarks_match = re.search(r'REMARKS\s*:\s*(\w+)', text)
#     data['remarks'] = remarks_match.group(1) if remarks_match else "N/A"

#     # ======= Subject extraction (line-by-line) =======
#     subject_data = []
#     lines = text.split('\n')

#     # Updated pattern to exactly match the debug lines
#     full_pattern = re.compile(r'^(.+?)\s+(\d{4,6}-\d{2})\s+(\d{1,3})\s+(\d{1,3})\s+([A-Z\+\-]+)$')
#     short_pattern = re.compile(r'^(.+?)\s+(\d{4,6}-\d{2})\s+(\d{1,3})\s+([A-Z\+\-]+)$')

#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue

#         match_full = full_pattern.match(line)
#         match_short = short_pattern.match(line)

#         if match_full:
#             subject_data.append({
#                 'course_title': match_full.group(1).strip(),
#                 'course_code': match_full.group(2).strip(),
#                 'midterm_marks': int(match_full.group(3)),
#                 'endterm_marks': int(match_full.group(4)),
#                 'grade': match_full.group(5).strip()
#             })
#         elif match_short:
#             subject_data.append({
#                 'course_title': match_short.group(1).strip(),
#                 'course_code': match_short.group(2).strip(),
#                 'midterm_marks': int(match_short.group(3)),
#                 'endterm_marks': 0,
#                 'grade': match_short.group(4).strip()
#             })

#     data['subjects'] = subject_data
#     return data
# import pdfplumber
# import re

# def extract_pdf_data(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         first_page = pdf.pages[0]
#         text = first_page.extract_text()

#     data = {}

#     # ========== Basic Info ==========
#     # College
#     college_match = re.search(r'College Name: (.+)', text)
#     data['college'] = college_match.group(1).strip() if college_match else ""

#     # Roll No & Enrollment No
#     roll_match = re.search(r'Roll No\s*:\s*(\S+)', text)
#     enroll_match = re.search(r'Enrollment No\s*:\s*(\S+)', text)
#     data['roll_no'] = roll_match.group(1).strip() if roll_match else ""
#     data['enrollment_no'] = enroll_match.group(1).strip() if enroll_match else ""

#     # Name & Father's Name
#     name_match = re.search(r'Name\s*:\s*(.*?)\s+Father\'s Name\s*:\s*(.+)', text)
#     if name_match:
#         data['name'] = name_match.group(1).strip()
#         data['father_name'] = name_match.group(2).strip()
#     else:
#         data['name'] = ""
#         data['father_name'] = ""

#     # Remarks
#     remarks_match = re.search(r'REMARKS\s*:\s*(\w+)', text)
#     data['remarks'] = remarks_match.group(1) if remarks_match else "N/A"

#     # ========== Subject Extraction ==========
#     subject_data = []
#     lines = text.split('\n')

#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue

#         # DEBUG print to inspect actual line format
#         # print("DEBUG LINE:", repr(line))

#         parts = line.split()

#         # Must contain at least: title, code, marks, grade
#         if len(parts) < 4:
#             continue

#         grade = parts[-1]
#         if not re.match(r'^[A-Z][\+\-]*$', grade):  # Grade must be like A++, B+, etc.
#             continue

#         # Determine if line includes mid+end or only mid
#         if len(parts) >= 5 and re.match(r'\d{1,3}', parts[-3]):
#             # Full: title code mid end grade
#             course_code = parts[-4]
#             midterm = int(parts[-3])
#             endterm = int(parts[-2])
#             course_title = ' '.join(parts[:-4])
#         else:
#             # Short: title code mid grade (e.g., Sodeca)
#             course_code = parts[-3]
#             midterm = int(parts[-2])
#             endterm = 0
#             course_title = ' '.join(parts[:-3])

#         subject_data.append({
#             'course_title': course_title.strip(),
#             'course_code': course_code.strip(),
#             'midterm_marks': midterm,
#             'endterm_marks': endterm,
#             'grade': grade.strip()
#         })

#     data['subjects'] = subject_data
#     return data


# import pdfplumber
# import re

# def extract_pdf_data(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         first_page = pdf.pages[0]
#         text = first_page.extract_text()

#     data = {}

#     # ========== Basic Info ==========
#     # College
#     college_match = re.search(r'College Name:\s*(.+)', text)
#     data['college'] = college_match.group(1).strip() if college_match else ""

#     # Roll No & Enrollment No
#     roll_match = re.search(r'Roll No\s*:\s*(\S+)', text)
#     enroll_match = re.search(r'Enrollment No\s*:\s*(\S+)', text)
#     data['roll_no'] = roll_match.group(1).strip() if roll_match else ""
#     data['enrollment_no'] = enroll_match.group(1).strip() if enroll_match else ""

#     # Name & Father's Name
#     name_match = re.search(r'Name\s*:\s*(.*?)\s+Father\'s Name\s*:\s*(.+)', text)
#     if name_match:
#         data['name'] = name_match.group(1).strip()
#         data['father_name'] = name_match.group(2).strip()
#     else:
#         data['name'] = ""
#         data['father_name'] = ""

#     # Remarks
#     remarks_match = re.search(r'REMARKS\s*:\s*(\w+)', text)
#     data['remarks'] = remarks_match.group(1) if remarks_match else "N/A"

#     # ========== Subject Extraction ==========
#     subject_data = []
#     lines = text.split('\n')

#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue

#         # DEBUG print to inspect actual line format
#         print("DEBUG LINE:", repr(line))

#         parts = line.split()

#         # Must contain at least: title, code, marks, grade
#         if len(parts) < 4:
#             continue

#         grade = parts[-1]
#         if not re.match(r'^[A-Z][\+\-]*$', grade):  # Grade must be like A++, B+, etc.
#             continue

#         # Determine if line includes mid+end or only mid
#         if len(parts) >= 5 and re.match(r'\d{1,3}', parts[-3]):
#             # Full: title code mid end grade
#             course_code = parts[-4]
#             midterm = int(parts[-3])
#             endterm = int(parts[-2])
#             course_title = ' '.join(parts[:-4])
#         else:
#             # Short: title code mid grade (e.g., Sodeca)
#             course_code = parts[-3]
#             midterm = int(parts[-2])
#             endterm = 0
#             course_title = ' '.join(parts[:-3])

#         subject_data.append({
#             'course_title': course_title.strip(),
#             'course_code': course_code.strip(),
#             'midterm_marks': midterm,
#             'endterm_marks': endterm,
#             'grade': grade.strip()
#         })

#     data['subjects'] = subject_data
#     return data

