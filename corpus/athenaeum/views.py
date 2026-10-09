from django.shortcuts import render

# Athenaeum has no models and no database -- the page is static. The edition
# lives here rather than inline in the template so that next year's update is
# this list instead of four hundred lines of duplicated markup, and so the
# timeline cannot drift out of step with the speaker cards.

EDITION = {
    "dates": "6th - 11th October, 2026",
    "tagline": "A Week of Talks Across the Societies",
    "about": (
        "The Athenaeum talks are conducted every year as part of the IEEE week, "
        "from 6th to 11th October. Speakers from various fields talk about "
        "interesting topics, emerging technologies and amazing research. Each "
        "society invites speakers of more or less their own domain."
    ),
}

# topic, affiliation, time, image, session_link and resources_link are filled
# in as they are confirmed; the template simply leaves out whatever is still
# blank. Cards stay deliberately short -- topic, speaker, designation, when and
# the link -- so the grid reads evenly.
SPEAKERS = [
    {
        "name": "Pranav Durai",
        "topic": "What Should a Robot Learn?",
        "affiliation": (
            "Co-Founder & CTO, FRNTL | Research Fellow, Stanford University "
            "School of Medicine | Ex-Senior Computer Vision Engineer, OpenCV"
        ),
        "hosted_by": "Piston / InterSIG",
        "society": "RAS",
        "date": "Tuesday, 6th October, 2026",
        "time": "6:00 PM - 7:30 PM IST",
        "platform": "Google Meet",
        "image": "img/athenaeum/Pranav_Durai.png",
        "session_link": "https://meet.google.com/kfs-btrt-zne",
        "link_label": "Join on Google Meet",
        "resources_link": "",
        "tentative": False,
    },
    {
        "name": "Achinthya Krishna Bheemaguli",
        "topic": (
            "Accelerating Materials Discovery with Foundational Machine "
            "Learned Interatomic Potentials"
        ),
        "affiliation": (
            "PhD Scholar, Indian Institute of Science (IISc) | BTech "
            "Metallurgical & Materials Engineering, NITK '25 | Ex-MITACS GRI"
        ),
        "hosted_by": "Piston",
        "society": "",
        "date": "7th October, 2026",
        "time": "6:00 PM - 7:30 PM IST",
        "platform": "Google Meet",
        "image": "img/athenaeum/Achintya_Krishna.png",
        "session_link": "https://meet.google.com/gnp-mmna-kpm",
        "link_label": "Join on Google Meet",
        "resources_link": "",
        "tentative": False,
    },
    {
        "name": "Mohammad Aadil Shabier",
        "topic": (
            "Navigating Open Source: Insights from My GSoC Journey at "
            "Inkscape and Waycrate"
        ),
        "affiliation": (
            "SDE-2, Cohesity | Ex-Intern, Sprinklr | BTech CSE, NITK '25 | "
            "GSoC '25, Waycrate | GSoC '22, Inkscape"
        ),
        "hosted_by": "CompSoc",
        "society": "",
        "date": "8th October, 2026",
        "time": "6:00 PM - 7:00 PM IST",
        "platform": "Google Meet",
        "image": "img/athenaeum/Mohammad_Aadil.png",
        "session_link": "https://meet.google.com/vga-dxnh-vrr",
        "link_label": "Join on Google Meet",
        "resources_link": "",
        "tentative": False,
    },
    {
        "name": "Vignesh Karthik",
        "topic": "Technology That Powers You - Analog Electronics",
        "affiliation": (
            "Analog Designer, Texas Instruments | GSoC '24, ASIC Design | "
            "BTech ECE, NITK '25"
        ),
        "hosted_by": "Diode",
        "society": "",
        "date": "Saturday, 10th October, 2026",
        "time": "11:00 AM - 12:00 PM IST",
        "platform": "Google Meet",
        "image": "img/athenaeum/Vignesh_Karthik.png",
        "session_link": "https://meet.google.com/gmp-agtp-duo",
        "link_label": "Join on Google Meet",
        "resources_link": "",
        "tentative": False,
    },
    {
        "name": "Rishabh Mishra",
        "topic": ("Beyond Placements: Navigating Careers in VLSI & Embedded Systems"),
        "affiliation": (
            "Senior R&D Engineer, Barco | Ex-NVIDIA, AMD, Xilinx & Synopsys | "
            "BITS Pilani & BHU Alumnus | VLSI & Embedded Career Mentor"
        ),
        "hosted_by": "Diode",
        "society": "CASS",
        "date": "Saturday, 10th October, 2026",
        "time": "5:00 PM IST",
        "venue": "LHC-C CR12",
        "image": "img/athenaeum/Rishabh_Mishra.png",
        "session_link": "",
        "resources_link": "",
        "tentative": False,
    },
    {
        "name": "Nishant Shetty",
        "topic": "",
        "affiliation": "",
        "hosted_by": "Diode",
        "society": "SPS",
        "date": "11th October, 2026",
        "time": "",
        "image": "",
        "session_link": "",
        "resources_link": "",
        "tentative": False,
    },
]

# Side events such as the quiz. The section is hidden while this is empty.
EVENTS = []

# Who to contact. Names are left out until the current post-holders are known;
# the section falls back to the address alone.
CONTACTS = []
CONTACT_EMAIL = "ieee@nitk.edu.in"


def home(request):
    return render(
        request,
        "athenaeum/home.html",
        {
            "edition": EDITION,
            "speakers": SPEAKERS,
            "events": EVENTS,
            "contacts": CONTACTS,
            "contact_email": CONTACT_EMAIL,
        },
    )
