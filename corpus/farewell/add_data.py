import random
import string

from farewell.models import Senior

names = [
    "Harish Ravi Kale",
    "Madhan Raj R",
    "Mohite Manthan Ravindra",
    "Amandeep Singh",
    "Mehul Todi",
    "Rakshith M",
    "Rohan Kamat",
    "Ashish Bharath",
    "Kavya Bhat",
    "Madhav Kumar",
    "Tejas Sankpal",
    "Sathvik Hebbar",
    "Shashank SM",
    "Vikas Keshavamurthy Bhat",
    "Gaurav Kumar",
    "Shannon Britney Carlo",
    "Anirudh Prabhakaran",
    "Jaya Srivastava",
    "Palgun N P",
    "R S Muthukumar",
    "Raghuram Kannan",
    "Utkarsh Mahajan",
    "Vasanth M",
    "Inbasekaran Perumal",
    "K A Gaganashree",
    "Meghna Uppuluri",
    "Nikhil P Reddy",
    "Pranav M Koundinya",
    "Vaishali S",
    "Hrishikesh Kulkarni",
    "Anirudh Singh Solanki",
    "Ashrith DR",
    "DEEPANSHU GUPTA",
    "Dharaneedaran K S",
    "Apurva S",
    "RISHEE K",
    "Dhruvil Lakhtaria",
    "Mohan Gunakara Nayak",
    "Pranav R S",
    "Radhika Chhabra",
    "Tejaswi Hegde",
    "Advaith Prasad Curpod",
    "Akheel Muhammed",
    "Anurag Kumar",
    "Harish Gumnur",
    "Mohammed Ayman Nawaz",
    "Swetha Mary Thomas",
    "Vinayak Vatsalya J",
    "Aryan Amit Barsainyan",
    "Himanshu S Garud",
    "Kshamaa Acharya B",
    "Rupankar Das",
    "SHRIRAMU A R",
    "Siddh Narhari",
    "ANANNYA RAO",
    "Shivani Chanda",
    "Abhilash Bharadwaj",
    "SHASHANK H S",
    "Saee Sholapurkar",
    "Sunaina Sunil",
    "Juvva Srinithya",
    "Raghwendra Pratap Yadav",
    "Sukrit Dass T M",
]

email_addresses = [
    "harishravikale.201ch024@nitk.edu.in",
    "madhanrajr.201ch029@nitk.edu.in",
    "manthanrmohite.201ch036@nitk.edu.in",
    "amandeepsingh.201cs107@nitk.edu.in",
    "mehultodi.201cs133@nitk.edu.in",
    "rakshith.201cs146@nitk.edu.in",
    "rohankamat.201cs147@nitk.edu.in",
    "ashishbharath.201cs208@nitk.edu.in",
    "kavyabhat.201cs225@nitk.edu.in",
    "madhavkumar.201cs228@nitk.edu.in",
    "sankpaltejas.201cs253@nitk.edu.in",
    "sathvikhebbar.201cs254@nitk.edu.in",
    "shash.201cs257@nitk.edu.in",
    "vikaskeshavamurthybhat.201cs266@nitk.edu.in",
    "gauravkumar.201cv117@nitk.edu.in",
    "shannonbritneycarlo.201cv249@nitk.edu.in",
    "anirudhprabhakaran.201ec106@nitk.edu.in",
    "jayasrivastava.201ec124@nitk.edu.in",
    "palgun.201ec141@nitk.edu.in",
    "rsmuthukumar.201ec149@nitk.edu.in",
    "raghuram.201ec150@nitk.edu.in",
    "ut.201ec164@nitk.edu.in",
    "vasanth.201ec165@nitk.edu.in",
    "inba.201ec226@nitk.edu.in",
    "gaganashree.201ec228@nitk.edu.in",
    "meghna.201ec237@nitk.edu.in",
    "nikhilreddy.201ec241@nitk.edu.in",
    "pranavmkoundinya.201ec247@nitk.edu.in",
    "vaish.201ee263@nitk.edu.in",
    "kulkarnihrishikeshprahlad.201ee101@nitk.edu.in",
    "anirudhsinghsolanki.201ee107@nitk.edu.in",
    "ashrithdr.201ee117@nitk.edu.in",
    "deepanshugupta.201ee119@nitk.edu.in",
    "dharaneedaranks.201ee120@nitk.edu.in",
    "apurva.201ee209@nitk.edu.in",
    "risheek.201ee244@nitk.edu.in",
    "dhruvillakhtaria.201it119@nitk.edu.in",
    "mohannayak.201it137@nitk.edu.in",
    "pranavrs.201it143@nitk.edu.in",
    "radhika.201it144@nitk.edu.in",
    "tejaswihegde.201it163@nitk.edu.in",
    "advaithprasadcurpod.201it204@nitk.edu.in",
    "akheelmuhammed.201it206@nitk.edu.in",
    "anuragkumar.201it209@nitk.edu.in",
    "gumnurharish.201it223@nitk.edu.in",
    "mohammedaymannawaz.201it236@nitk.edu.in",
    "swethathomas.201it262@nitk.edu.in",
    "vinayakvatsalyaj.201it266@nitk.edu.in",
    "aryanab.201me110@nitk.edu.in",
    "himan.201me122@nitk.edu.in",
    "kshamaaacharyab.201me128@nitk.edu.in",
    "rupankar.201me148@nitk.edu.in",
    "shriramuar.201me155@nitk.edu.in",
    "siddhnarhari.201me156@nitk.edu.in",
    "anannya.201me209@nitk.edu.in",
    "shivani.201me215@nitk.edu.in",
    "abhilashbharadwaj.201me227@nitk.edu.in",
    "shashankhs.201me252@nitk.edu.in",
    "saeesholapurkar.201me253@nitk.edu.in",
    "sunainasunil.201me357@nitk.edu.in",
    "juvvasrinithya.201mt023@nitk.edu.in",
    "raghw.201mt044@nitk.edu.in",
    "tmsdass.201mt056@nitk.edu.in",
]

# test
# names = [
#     'Vignaraj',
#     'Aditya Srihari'
# ]

# email_addresses = [
#     'vignarajpai@gmail.com',
#     'adithyasriharirao.211me203@nitk.edu.in',
# ]

# clear the Senior table
Senior.objects.all().delete()
print("Cleared the Senior table")

url_ids = []

for name in names:
    url_id = "".join(random.choices(string.ascii_letters + string.digits, k=5))
    # make sure its unique
    while url_id in url_ids:
        url_id = "".join(random.choices(string.ascii_letters + string.digits, k=5))
    url_ids.append(url_id)

print("Generated unique url_ids")


for name, url_id, email_address in zip(names, url_ids, email_addresses):
    Senior.objects.create(
        name=name,
        url_id=url_id,
        email_id=email_address,
        coming_farewell=False,
        coming_afterparty=False,
    )

print("Added data to the Senior table")
