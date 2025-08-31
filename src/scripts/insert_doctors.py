from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
doctors = [
    {
        "username": "dr_sneha_derm1",
        "name": "Dr. Sneha Kapoor",
        "specialization": "Dermatologist",
        "hospital": "SkinCare Clinic, Delhi",
        "email": "sneha.derm1@example.com",
        "phone": "+91-9812345671"
    },
    {
        "username": "dr_raj_derm2",
        "name": "Dr. Raj Malhotra",
        "specialization": "Dermatologist",
        "hospital": "GlowSkin Hospital, Mumbai",
        "email": "raj.derm2@example.com",
        "phone": "+91-9812345672"
    },
    {
        "username": "dr_priya_derm3",
        "name": "Dr. Priya Sharma",
        "specialization": "Dermatologist",
        "hospital": "DermaCare Center, Bangalore",
        "email": "priya.derm3@example.com",
        "phone": "+91-9812345673"
    },
    {
        "username": "dr_kiran_derm4",
        "name": "Dr. Kiran Nair",
        "specialization": "Dermatologist",
        "hospital": "Aesthetic Skin Clinic, Hyderabad",
        "email": "kiran.derm4@example.com",
        "phone": "+91-9812345674"
    },
    {
        "username": "dr_anita_derm5",
        "name": "Dr. Anita Gupta",
        "specialization": "Dermatologist",
        "hospital": "HealthySkin Hospital, Pune",
        "email": "anita.derm5@example.com",
        "phone": "+91-9812345675"
    },
    {
        "username": "dr_amit_all1",
        "name": "Dr. Amit Joshi",
        "specialization": "Allergist",
        "hospital": "Allergy & Asthma Center, Delhi",
        "email": "amit.all1@example.com",
        "phone": "+91-9812345681"
    },
    {
        "username": "dr_megha_all2",
        "name": "Dr. Megha Patel",
        "specialization": "Allergist",
        "hospital": "ImmunoCare Clinic, Mumbai",
        "email": "megha.all2@example.com",
        "phone": "+91-9812345682"
    },
    {
        "username": "dr_vivek_all3",
        "name": "Dr. Vivek Reddy",
        "specialization": "Allergist",
        "hospital": "AsthmaCare Hospital, Bangalore",
        "email": "vivek.all3@example.com",
        "phone": "+91-9812345683"
    },
    {
        "username": "dr_kavita_all4",
        "name": "Dr. Kavita Sinha",
        "specialization": "Allergist",
        "hospital": "Allergy Relief Center, Chennai",
        "email": "kavita.all4@example.com",
        "phone": "+91-9812345684"
    },
    {
        "username": "dr_sunil_all5",
        "name": "Dr. Sunil Verma",
        "specialization": "Allergist",
        "hospital": "Immunology Clinic, Pune",
        "email": "sunil.all5@example.com",
        "phone": "+91-9812345685"
    },
    {
        "username": "dr_sara_collins",
        "name": "Dr. Sara Collins",
        "specialization": "Gastroenterologist",
        "experience": 9,
    "hospital": "Global Health Institute",
    "location": "Bengaluru, India",
    "contact": "sara.collins@ghi.in"
    },
  {
    "username": "dr_ian_clark",
    "name": "Dr. Ian Clark",
    "specialization": "Gastroenterologist",
    "experience": 12,
    "hospital": "Fortis Healthcare",
    "location": "New Delhi, India",
    "contact": "ian.clark@fortis.in"
  },
  {
    "username": "dr_pooja_nair",
    "name": "Dr. Pooja Nair",
    "specialization": "Gastroenterologist",
    "experience": 15,
    "hospital": "Apollo Hospitals",
    "location": "Chennai, India",
    "contact": "pooja.nair@apollo.in"
  },
  {
    "username": "dr_hassan_khan",
    "name": "Dr. Hassan Khan",
    "specialization": "Gastroenterologist",
    "experience": 8,
    "hospital": "Manipal Hospitals",
    "location": "Hyderabad, India",
    "contact": "hassan.khan@manipal.in"
  },
  {
    "username": "dr_zoe_foster",
    "name": "Dr. Zoe Foster",
    "specialization": "Gastroenterologist",
    "experience": 10,
    "hospital": "Sunshine Medical Center",
    "location": "Mumbai, India",
    "contact": "zoe.foster@sunshine.in"
  },
  {
    "username": "dr_vikram_patel",
    "name": "Dr. Vikram Patel",
    "specialization": "Hepatologist",
    "experience": 14,
    "hospital": "Liver Care Institute",
    "location": "Pune, India",
    "contact": "vikram.patel@lci.in"
  },
  {
    "username": "dr_emily_hughes",
    "name": "Dr. Emily Hughes",
    "specialization": "Hepatologist",
    "experience": 10,
    "hospital": "Fortis Liver Center",
    "location": "Delhi, India",
    "contact": "emily.hughes@fortis.in"
  },
  {
    "username": "dr_rajiv_menon",
    "name": "Dr. Rajiv Menon",
    "specialization": "Hepatologist",
    "experience": 11,
    "hospital": "Apollo Hospitals",
    "location": "Chennai, India",
    "contact": "rajiv.menon@apollo.in"
  },
  {
    "username": "dr_nora_white",
    "name": "Dr. Nora White",
    "specialization": "Hepatologist",
    "experience": 9,
    "hospital": "Max Healthcare",
    "location": "New Delhi, India",
    "contact": "nora.white@max.in"
  },
  {
    "username": "dr_ashok_gupta",
    "name": "Dr. Ashok Gupta",
    "specialization": "Hepatologist",
    "experience": 13,
    "hospital": "Manipal Hospitals",
    "location": "Hyderabad, India",
    "contact": "ashok.gupta@manipal.in"
  },
  {
    "username": "dr_sophie_anderson",
    "name": "Dr. Sophie Anderson",
    "specialization": "Osteopathic",
    "experience": 7,
    "hospital": "Holistic Health Center",
    "location": "Bengaluru, India",
    "contact": "sophie.anderson@hhc.in"
  },
  {
    "username": "dr_rahul_singh",
    "name": "Dr. Rahul Singh",
    "specialization": "Osteopathic",
    "experience": 10,
    "hospital": "Wellness Medical Center",
    "location": "Pune, India",
    "contact": "rahul.singh@wellness.in"
  },
  {
    "username": "dr_claire_martin",
    "name": "Dr. Claire Martin",
    "specialization": "Osteopathic",
    "experience": 12,
    "hospital": "Global Health Institute",
    "location": "Delhi, India",
    "contact": "claire.martin@ghi.in"
  },
  {
    "username": "dr_vani_reddy",
    "name": "Dr. Vani Reddy",
    "specialization": "Osteopathic",
    "experience": 8,
    "hospital": "Apollo Hospitals",
    "location": "Chennai, India",
    "contact": "vani.reddy@apollo.in"
  },
  {
    "username": "dr_adam_patel",
    "name": "Dr. Adam Patel",
    "specialization": "Osteopathic",
    "experience": 11,
    "hospital": "Sunrise Health Center",
    "location": "Mumbai, India",
    "contact": "adam.patel@sunrise.in"
  },
  {
    "username": "dr_miller_ent",
    "name": "Dr. Nathan Miller",
    "specialization": "Otolaryngologist",
    "email": "nathan.miller@example.com",
    "phone": "+91-9988776655",
    "experience": 12,
    "hospital": "ENT Care Hospital, Hyderabad"
  },
  {
    "username": "dr_singh_ent",
    "name": "Dr. Priya Singh",
    "specialization": "Otolaryngologist",
    "email": "priya.singh@example.com",
    "phone": "+91-9876541111",
    "experience": 15,
    "hospital": "Voice & Hearing Clinic, Delhi"
  },
  {
    "username": "dr_white_ent",
    "name": "Dr. James White",
    "specialization": "Otolaryngologist",
    "email": "james.white@example.com",
    "phone": "+91-9788882222",
    "experience": 8,
    "hospital": "Sound Health ENT, Bengaluru"
  },
  {
    "username": "dr_tanwar_ent",
    "name": "Dr. Meera Tanwar",
    "specialization": "Otolaryngologist",
    "email": "meera.tanwar@example.com",
    "phone": "+91-9123458765",
    "experience": 11,
    "hospital": "Sinus & Allergy Center, Pune"
  },
  {
    "username": "dr_kapoor_ent",
    "name": "Dr. Rohan Kapoor",
    "specialization": "Otolaryngologist",
    "email": "rohan.kapoor@example.com",
    "phone": "+91-9997773332",
    "experience": 14,
    "hospital": "City ENT Specialists, Chennai"
  },

  {
    "username": "dr_malhotra_derm",
    "name": "Dr. Kavita Malhotra",
    "specialization": "Dermatologist",
    "email": "kavita.malhotra@example.com",
    "phone": "+91-9811112244",
    "experience": 10,
    "hospital": "Skin Glow Clinic, Delhi"
  },
  {
    "username": "dr_brown_derm",
    "name": "Dr. Michael Brown",
    "specialization": "Dermatologist",
    "email": "michael.brown@example.com",
    "phone": "+91-9822225566",
    "experience": 13,
    "hospital": "Advanced Dermatology, Bengaluru"
  },
  {
    "username": "dr_reddy_derm",
    "name": "Dr. Anjali Reddy",
    "specialization": "Dermatologist",
    "email": "anjali.reddy@example.com",
    "phone": "+91-9777778888",
    "experience": 9,
    "hospital": "Clear Skin Clinic, Hyderabad"
  },
  {
    "username": "dr_johnson_derm",
    "name": "Dr. Sarah Johnson",
    "specialization": "Dermatologist",
    "email": "sarah.johnson@example.com",
    "phone": "+91-9123412345",
    "experience": 7,
    "hospital": "SkinCare Solutions, Pune"
  },
  {
    "username": "dr_shah_derm",
    "name": "Dr. Vivek Shah",
    "specialization": "Dermatologist",
    "email": "vivek.shah@example.com",
    "phone": "+91-9876654321",
    "experience": 15,
    "hospital": "City Skin Specialists, Ahmedabad"
  },

  {
    "username": "dr_jain_gyn",
    "name": "Dr. Neha Jain",
    "specialization": "Gynecologist",
    "email": "neha.jain@example.com",
    "phone": "+91-9001122334",
    "experience": 12,
    "hospital": "Women’s Care Clinic, Mumbai"
  },
  {
    "username": "dr_thomas_gyn",
    "name": "Dr. Emily Thomas",
    "specialization": "Gynecologist",
    "email": "emily.thomas@example.com",
    "phone": "+91-9345678123",
    "experience": 8,
    "hospital": "Mother & Child Hospital, Bengaluru"
  },
  {
    "username": "dr_verma_gyn",
    "name": "Dr. Shalini Verma",
    "specialization": "Gynecologist",
    "email": "shalini.verma@example.com",
    "phone": "+91-9654321890",
    "experience": 11,
    "hospital": "City Gynecology Center, Delhi"
  },
  {
    "username": "dr_roberts_gyn",
    "name": "Dr. Laura Roberts",
    "specialization": "Gynecologist",
    "email": "laura.roberts@example.com",
    "phone": "+91-9765432109",
    "experience": 14,
    "hospital": "Advanced Women’s Health, Chennai"
  },
  {
    "username": "dr_patel_gyn",
    "name": "Dr. Manisha Patel",
    "specialization": "Gynecologist",
    "email": "manisha.patel@example.com",
    "phone": "+91-9123456781",
    "experience": 10,
    "hospital": "Lotus Women’s Hospital, Ahmedabad"
  },
  {
    "username": "der100",
    "name": "Dr. Anjali Mehta",
    "specialization": "Dermatologist",
    "email": "anjali.mehta@hospital.com",
    "phone": "+91-6355751656",
    "location": "Mumbai, India",
    "years_of_experience": 30,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "all101",
    "name": "Dr. Rohan Kapoor",
    "specialization": "Allergist",
    "email": "rohan.kapoor@hospital.com",
    "phone": "+91-6185758198",
    "location": "Delhi, India",
    "years_of_experience": 16,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "gas102",
    "name": "Dr. Priya Sharma",
    "specialization": "Gastroenterologist",
    "email": "priya.sharma@hospital.com",
    "phone": "+91-7985601683",
    "location": "Mumbai, India",
    "years_of_experience": 25,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "hep103",
    "name": "Dr. Vikram Desai",
    "specialization": "Hepatologist",
    "email": "vikram.desai@hospital.com",
    "phone": "+91-7451452653",
    "location": "Jaipur, India",
    "years_of_experience": 10,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "ost104",
    "name": "Dr. Kavita Nair",
    "specialization": "Osteopathic",
    "email": "kavita.nair@hospital.com",
    "phone": "+91-8337583780",
    "location": "Bangalore, India",
    "years_of_experience": 13,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "end105",
    "name": "Dr. Amitabh Sinha",
    "specialization": "Endocrinologist",
    "email": "amitabh.sinha@hospital.com",
    "phone": "+91-6424529853",
    "location": "Jaipur, India",
    "years_of_experience": 33,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "pul106",
    "name": "Dr. Sunita Iyer",
    "specialization": "Pulmonologist",
    "email": "sunita.iyer@hospital.com",
    "phone": "+91-8465911154",
    "location": "Ahmedabad, India",
    "years_of_experience": 4,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "car107",
    "name": "Dr. Rajesh Khanna",
    "specialization": "Cardiologist",
    "email": "rajesh.khanna@hospital.com",
    "phone": "+91-8826535231",
    "location": "Kolkata, India",
    "years_of_experience": 31,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "neu108",
    "name": "Dr. Sneha Bhatia",
    "specialization": "Neurologist",
    "email": "sneha.bhatia@hospital.com",
    "phone": "+91-9422203431",
    "location": "Pune, India",
    "years_of_experience": 23,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "int109",
    "name": "Dr. Manoj Joshi",
    "specialization": "Internal Medicine",
    "email": "manoj.joshi@hospital.com",
    "phone": "+91-8048680748",
    "location": "Hyderabad, India",
    "years_of_experience": 15,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "ped110",
    "name": "Dr. Pooja Agarwal",
    "specialization": "Pediatrician",
    "email": "pooja.agarwal@hospital.com",
    "phone": "+91-9207195232",
    "location": "Kolkata, India",
    "years_of_experience": 18,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "gen111",
    "name": "Dr. Siddharth Menon",
    "specialization": "General Physician",
    "email": "siddharth.menon@hospital.com",
    "phone": "+91-6799530481",
    "location": "Chennai, India",
    "years_of_experience": 25,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "phl112",
    "name": "Dr. Shreya Kulkarni",
    "specialization": "Phlebologist",
    "email": "shreya.kulkarni@hospital.com",
    "phone": "+91-7055769601",
    "location": "Chennai, India",
    "years_of_experience": 18,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "rhe113",
    "name": "Dr. Arjun Reddy",
    "specialization": "Rheumatologist",
    "email": "arjun.reddy@hospital.com",
    "phone": "+91-8998829372",
    "location": "Chennai, India",
    "years_of_experience": 24,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "oto114",
    "name": "Dr. Nisha Verma",
    "specialization": "Otolaryngologist",
    "email": "nisha.verma@hospital.com",
    "phone": "+91-8329737178",
    "location": "Kolkata, India",
    "years_of_experience": 30,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "gyn115",
    "name": "Dr. Suresh Patil",
    "specialization": "Gynecologist",
    "email": "suresh.patil@hospital.com",
    "phone": "+91-6258684286",
    "location": "Chennai, India",
    "years_of_experience": 34,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "ort116",
    "name": "Dr. Meena Rao",
    "specialization": "Orthopedic",
    "email": "meena.rao@hospital.com",
    "phone": "+91-8449989074",
    "location": "Jaipur, India",
    "years_of_experience": 22,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "onc117",
    "name": "Dr. Karan Malhotra",
    "specialization": "Oncologist",
    "email": "karan.malhotra@hospital.com",
    "phone": "+91-7989538008",
    "location": "Bangalore, India",
    "years_of_experience": 11,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "nep118",
    "name": "Dr. Neha Saxena",
    "specialization": "Nephrologist",
    "email": "neha.saxena@hospital.com",
    "phone": "+91-7780517193",
    "location": "Hyderabad, India",
    "years_of_experience": 22,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "psy119",
    "name": "Dr. Ajay Trivedi",
    "specialization": "Psychiatrist",
    "email": "ajay.trivedi@hospital.com",
    "phone": "+91-9981848607",
    "location": "Jaipur, India",
    "years_of_experience": 10,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "uro120",
    "name": "Dr. Divya Ghosh",
    "specialization": "Urologist",
    "email": "divya.ghosh@hospital.com",
    "phone": "+91-6567165723",
    "location": "Bangalore, India",
    "years_of_experience": 8,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "oph121",
    "name": "Dr. Rakesh Chawla",
    "specialization": "Ophthalmologist",
    "email": "rakesh.chawla@hospital.com",
    "phone": "+91-8734271665",
    "location": "Pune, India",
    "years_of_experience": 8,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "den122",
    "name": "Dr. Alok Pandey",
    "specialization": "Dentist",
    "email": "alok.pandey@hospital.com",
    "phone": "+91-6562255531",
    "location": "Pune, India",
    "years_of_experience": 19,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "rad123",
    "name": "Dr. Geeta Pillai",
    "specialization": "Radiologist",
    "email": "geeta.pillai@hospital.com",
    "phone": "+91-7291323188",
    "location": "Bangalore, India",
    "years_of_experience": 23,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "pat124",
    "name": "Dr. Vivek Jain",
    "specialization": "Pathologist",
    "email": "vivek.jain@hospital.com",
    "phone": "+91-7994235106",
    "location": "Jaipur, India",
    "years_of_experience": 33,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "ane125",
    "name": "Dr. Tanya Mukherjee",
    "specialization": "Anesthesiologist",
    "email": "tanya.mukherjee@hospital.com",
    "phone": "+91-7906568128",
    "location": "Bangalore, India",
    "years_of_experience": 13,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "ger126",
    "name": "Dr. Deepak Chauhan",
    "specialization": "Geriatrician",
    "email": "deepak.chauhan@hospital.com",
    "phone": "+91-7162727863",
    "location": "Kolkata, India",
    "years_of_experience": 35,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "imm127",
    "name": "Dr. Swati Kaur",
    "specialization": "Immunologist",
    "email": "swati.kaur@hospital.com",
    "phone": "+91-9766323434",
    "location": "Chennai, India",
    "years_of_experience": 16,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "pla128",
    "name": "Dr. Rahul Bhargava",
    "specialization": "Plastic Surgeon",
    "email": "rahul.bhargava@hospital.com",
    "phone": "+91-6462604557",
    "location": "Mumbai, India",
    "years_of_experience": 17,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "spo129",
    "name": "Dr. Ishita Shukla",
    "specialization": "Sports Medicine",
    "email": "ishita.shukla@hospital.com",
    "phone": "+91-8016821209",
    "location": "Lucknow, India",
    "years_of_experience": 9,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "inf130",
    "name": "Dr. Mohit Bansal",
    "specialization": "Infectious Disease",
    "email": "mohit.bansal@hospital.com",
    "phone": "+91-6012047750",
    "location": "Chennai, India",
    "years_of_experience": 33,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "fam131",
    "name": "Dr. Seema Rathi",
    "specialization": "Family Physician",
    "email": "seema.rathi@hospital.com",
    "phone": "+91-9119573599",
    "location": "Ahmedabad, India",
    "years_of_experience": 35,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "occ132",
    "name": "Dr. Parth Gupta",
    "specialization": "Occupational Medicine",
    "email": "parth.gupta@hospital.com",
    "phone": "+91-7309297614",
    "location": "Mumbai, India",
    "years_of_experience": 34,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "eme133",
    "name": "Dr. Lata Krishnan",
    "specialization": "Emergency Medicine",
    "email": "lata.krishnan@hospital.com",
    "phone": "+91-8083481474",
    "location": "Chennai, India",
    "years_of_experience": 11,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "sle134",
    "name": "Dr. Sameer Rawat",
    "specialization": "Sleep Specialist",
    "email": "sameer.rawat@hospital.com",
    "phone": "+91-6182186950",
    "location": "Delhi, India",
    "years_of_experience": 30,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "dia135",
    "name": "Dr. Komal Deshmukh",
    "specialization": "Diabetologist",
    "email": "komal.deshmukh@hospital.com",
    "phone": "+91-9354331398",
    "location": "Lucknow, India",
    "years_of_experience": 9,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "pai136",
    "name": "Dr. Harish Kulkarni",
    "specialization": "Pain Management",
    "email": "harish.kulkarni@hospital.com",
    "phone": "+91-7726725231",
    "location": "Lucknow, India",
    "years_of_experience": 23,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "reh137",
    "name": "Dr. Shalini Dutta",
    "specialization": "Rehabilitation Specialist",
    "email": "shalini.dutta@hospital.com",
    "phone": "+91-9254983821",
    "location": "Kolkata, India",
    "years_of_experience": 15,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "pal138",
    "name": "Dr. Nikhil Ahuja",
    "specialization": "Palliative Care",
    "email": "nikhil.ahuja@hospital.com",
    "phone": "+91-6566688451",
    "location": "Chennai, India",
    "years_of_experience": 6,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "10:00-12:00",
        "16:00-18:00"
      ]
    }
  },
  {
    "username": "pub139",
    "name": "Dr. Kritika Joshi",
    "specialization": "Public Health",
    "email": "kritika.joshi@hospital.com",
    "phone": "+91-8940735710",
    "location": "Jaipur, India",
    "years_of_experience": 7,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "cli140",
    "name": "Dr. Ashwin Raina",
    "specialization": "Clinical Pharmacologist",
    "email": "ashwin.raina@hospital.com",
    "phone": "+91-7560434494",
    "location": "Pune, India",
    "years_of_experience": 16,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "gen141",
    "name": "Dr. Ritu Kapoor",
    "specialization": "Geneticist",
    "email": "ritu.kapoor@hospital.com",
    "phone": "+91-7537526956",
    "location": "Hyderabad, India",
    "years_of_experience": 32,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "and142",
    "name": "Dr. Ankur Saxena",
    "specialization": "Andrologist",
    "email": "ankur.saxena@hospital.com",
    "phone": "+91-8000564935",
    "location": "Ahmedabad, India",
    "years_of_experience": 21,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "vas143",
    "name": "Dr. Sonali Kaul",
    "specialization": "Vascular Surgeon",
    "email": "sonali.kaul@hospital.com",
    "phone": "+91-9655651723",
    "location": "Hyderabad, India",
    "years_of_experience": 8,
    "availability": {
      "days": [
        "Tue",
        "Thu",
        "Sat"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "spi144",
    "name": "Dr. Dinesh Yadav",
    "specialization": "Spine Specialist",
    "email": "dinesh.yadav@hospital.com",
    "phone": "+91-8306090656",
    "location": "Delhi, India",
    "years_of_experience": 24,
    "availability": {
      "days": [
        "Mon",
        "Tue",
        "Thu"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "obs145",
    "name": "Dr. Meghna Jaiswal",
    "specialization": "Obstetrician",
    "email": "meghna.jaiswal@hospital.com",
    "phone": "+91-8776696606",
    "location": "Mumbai, India",
    "years_of_experience": 27,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "spe146",
    "name": "Dr. Pankaj Tiwari",
    "specialization": "Speech Therapist",
    "email": "pankaj.tiwari@hospital.com",
    "phone": "+91-7330659429",
    "location": "Lucknow, India",
    "years_of_experience": 5,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "09:00-11:00",
        "15:00-17:00"
      ]
    }
  },
  {
    "username": "nut147",
    "name": "Dr. Rohit Vora",
    "specialization": "Nutritionist",
    "email": "rohit.vora@hospital.com",
    "phone": "+91-9963268917",
    "location": "Delhi, India",
    "years_of_experience": 12,
    "availability": {
      "days": [
        "Wed",
        "Fri",
        "Sun"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  },
  {
    "username": "hom148",
    "name": "Dr. Snehal Pawar",
    "specialization": "Homeopathic Doctor",
    "email": "snehal.pawar@hospital.com",
    "phone": "+91-7681981240",
    "location": "Lucknow, India",
    "years_of_experience": 15,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "08:00-10:00",
        "14:00-16:00"
      ]
    }
  },
  {
    "username": "ayu149",
    "name": "Dr. Chirag Shah",
    "specialization": "Ayurvedic Doctor",
    "email": "chirag.shah@hospital.com",
    "phone": "+91-8386975799",
    "location": "Hyderabad, India",
    "years_of_experience": 30,
    "availability": {
      "days": [
        "Mon",
        "Wed",
        "Fri"
      ],
      "time_slots": [
        "11:00-13:00",
        "17:00-19:00"
      ]
    }
  }
]

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vitavoice"]
doctors_col = db["doctors"]

# Insert only if not already present (avoid duplicates)
for doc in doctors:
    if not doctors_col.find_one({"username": doc["username"]}):
        doctors_col.insert_one(doc)
        print(f"Inserted {doc['name']}")
    else:
        print(f"Skipped {doc['name']} (already exists)")