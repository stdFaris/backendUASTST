import random
from typing import List, Dict, Any
from src.schemas.enums import PartnerRole, BookingType

# Daftar kecamatan
KECAMATAN_LIST = [
    "Menteng", "Kemang", "Kebayoran Baru", "Senayan", "Tebet",
    "Kuningan", "Sudirman", "Thamrin", "Pantai Indah Kapuk", "Kelapa Gading"
]

# Daftar nama-nama Indonesia untuk dummy data
FIRST_NAMES = [
    "Agus", "Budi", "Cahya", "Dewi", "Eko", "Fitri", "Gina", "Hadi", "Indah", "Joko", 
    "Kartika", "Lina", "Marwan", "Nina", "Oki", "Putri", "Rama", "Siti", "Tono", "Umar", 
    "Vina", "Wawan", "Yanti", "Zainal", "Anisa", "Bambang", "Citra", "Dodi", "Endang", "Faisal",
    "Gunawan", "Hesti", "Irfan", "Joni", "Kurnia", "Laila", "Maya", "Nadia", "Oscar", "Pandu",
    "Qori", "Ratna", "Surya", "Tari", "Ujang", "Vira", "Wati", "Yusuf", "Zara", "Andi",
    "Bayu", "Cantika", "Danu", "Erna", "Ferdi", "Gita", "Hendra", "Ira", "Juli", "Kiki"
]

LAST_NAMES = [
    "Wijaya", "Kusuma", "Sanjaya", "Gunawan", "Pratama", "Putri", "Utama", "Saputra", "Nugraha", "Permana",
    "Hidayat", "Santoso", "Wibowo", "Suryanto", "Hartono", "Setiawan", "Putra", "Susanto", "Purnama", "Haryanto",
    "Wahyuni", "Handayani", "Lestari", "Puspita", "Safitri", "Yuliana", "Nuraini", "Rahayu", "Maulana", "Fadillah",
    "Firdaus", "Irawan", "Hasan", "Ramadhan", "Sulistyo", "Budiman", "Rahman", "Abdullah", "Ibrahim", "Anwar"
]

# Specializations berdasarkan peran
SPECIALIZATIONS = {
    PartnerRole.PEMBANTU: [
        "Memasak", "Membersihkan Rumah", "Mencuci dan Menyetrika", "Menjaga Anak", "Merawat Lansia", 
        "Masakan Indonesia", "Masakan Internasional", "Menjaga Bayi", "Kebersihan Mendalam", "Merapikan Barang"
    ],
    PartnerRole.TUKANG_KEBUN: [
        "Merawat Tanaman Hias", "Memotong Rumput", "Menata Taman", "Pemupukan", "Mengatasi Hama", 
        "Merancang Taman", "Merawat Kolam", "Tanaman Indoor", "Tanaman Outdoor", "Hidroponik"
    ],
    PartnerRole.TUKANG_PIJAT: [
        "Pijat Tradisional", "Akupresur", "Pijat Refleksi", "Pijat Terapi", "Pijat Relaksasi", 
        "Pijat Olahraga", "Pijat Aromaterapi", "Pijat Batu Panas", "Thai Massage", "Swedish Massage"
    ]
}

# Bahasa yang dikuasai
LANGUAGES = ["Indonesia", "Inggris", "Jawa", "Sunda", "Mandarin", "Batak", "Melayu", "Bugis", "Minang", "Bali"]

# Deskripsi profil berdasarkan peran
PROFILE_DESCRIPTIONS = {
    PartnerRole.PEMBANTU: [
        "Pembantu rumah tangga berpengalaman dengan keahlian dalam memasak makanan Indonesia.",
        "Siap membantu membersihkan rumah dan merawat anak-anak dengan penuh tanggung jawab.",
        "Pembantu profesional dengan pengalaman merawat lansia dan membersihkan rumah.",
        "Ahli memasak dan merapikan rumah dengan standar kebersihan tinggi.",
        "Pembantu rumah tangga yang teliti, cekatan, dan ramah dalam menjalankan tugas sehari-hari.",
        "Berpengalaman dalam mengurus rumah tangga besar dengan beberapa anggota keluarga.",
        "Pembantu serba bisa dengan keahlian khusus memasak hidangan sehat.",
        "Memiliki kemampuan merawat anak dan bayi dengan penuh perhatian dan kasih sayang.",
        "Pembantu teliti dengan standar kebersihan tinggi dan ahli dalam mencuci dan menyetrika pakaian.",
        "Pekerja keras dengan pengalaman mengelola rumah tangga profesional dan terorganisir."
    ],
    PartnerRole.TUKANG_KEBUN: [
        "Tukang kebun profesional dengan keahlian dalam desain dan perawatan taman.",
        "Ahli tanaman hias dan penataan taman dengan sentuhan estetika.",
        "Tukang kebun berpengalaman yang ahli dalam penanganan hama dan pemupukan.",
        "Spesialis tanaman tropis dan perawatan taman berkelanjutan.",
        "Tukang kebun dengan pengetahuan luas tentang berbagai jenis tanaman dan cara perawatannya.",
        "Ahli dalam merancang taman minimalis modern dan hemat air.",
        "Spesialis tanaman indoor dan perawatan taman vertikal.",
        "Tukang kebun dengan keahlian khusus dalam sistem hidroponik dan aquaponik.",
        "Berpengalaman dalam merawat kebun buah dan sayur organik.",
        "Tukang kebun profesional dengan fokus pada kebun ramah lingkungan dan berkelanjutan."
    ],
    PartnerRole.TUKANG_PIJAT: [
        "Terapis pijat profesional dengan keahlian dalam pijat tradisional Indonesia.",
        "Ahli pijat refleksi dengan pendekatan holistik untuk kesehatan.",
        "Terapis berpengalaman dalam pijat terapi untuk cedera olahraga dan pemulihan.",
        "Spesialis pijat relaksasi dengan teknik aromaterapi.",
        "Terapis pijat dengan sertifikasi dalam berbagai teknik pijat internasional.",
        "Ahli dalam pijat terapi untuk mengatasi nyeri kronis dan ketegangan otot.",
        "Terapis dengan pendekatan menyeluruh untuk kesehatan fisik dan mental melalui pijat.",
        "Spesialis pijat untuk ibu hamil dan pasca melahirkan.",
        "Terapis profesional dengan fokus pada pijat untuk meningkatkan sirkulasi darah.",
        "Ahli pijat dengan pengalaman khusus menangani stres dan kelelahan kronis."
    ]
}

def generate_dummy_partners(max_partners: int = 150, min_per_category_per_kecamatan: int = 2) -> List[Dict[str, Any]]:
    """
    Generate dummy partner data with specified maximum count and minimum distribution across roles and kecamatan
    
    Args:
        max_partners: Maximum number of partners to generate
        min_per_category_per_kecamatan: Minimum number of partners per role per kecamatan
        
    Returns:
        List of partner data dictionaries
    """
    partners = []
    
    # Calculate how many partners we need for minimum distribution
    min_required = len(KECAMATAN_LIST) * len([PartnerRole.PEMBANTU, PartnerRole.TUKANG_KEBUN, PartnerRole.TUKANG_PIJAT]) * min_per_category_per_kecamatan
    
    # Ensure we have at least the minimum number per role per kecamatan
    for kecamatan in KECAMATAN_LIST:
        for role in [PartnerRole.PEMBANTU, PartnerRole.TUKANG_KEBUN, PartnerRole.TUKANG_PIJAT]:
            for _ in range(min_per_category_per_kecamatan):
                partner = _generate_random_partner(role, kecamatan)
                partners.append(partner)
    
    # Calculate remaining slots
    remaining_slots = max_partners - min_required
    
    # Fill remaining slots with random partners if there are any remaining slots
    if remaining_slots > 0:
        for _ in range(remaining_slots):
            random_role = random.choice([PartnerRole.PEMBANTU, PartnerRole.TUKANG_KEBUN, PartnerRole.TUKANG_PIJAT])
            random_kecamatan = random.choice(KECAMATAN_LIST)
            partner = _generate_random_partner(random_role, random_kecamatan)
            partners.append(partner)
    
    # Shuffle the list to mix the partners
    random.shuffle(partners)
    
    return partners

def _generate_random_partner(role: PartnerRole, kecamatan: str) -> Dict[str, Any]:
    """Generate a single random partner with specified role and kecamatan"""
    
    if role == PartnerRole.PEMBANTU:
        hourly_base = random.randint(30000, 50000)
    elif role == PartnerRole.TUKANG_KEBUN:
        hourly_base = random.randint(40000, 60000)
    else:
        hourly_base = random.randint(80000, 150000)
    
    daily_rate = hourly_base * 8 * 0.9
    monthly_rate = daily_rate * 22 * 0.8
    
    experience_years = random.randint(1, 15)
    rating_base = min(4.0 + (experience_years / 10), 5.0)
    rating = round(max(3.0, min(5.0, rating_base + random.uniform(-0.5, 0.5))), 1)
    total_reviews = random.randint(experience_years * 2, experience_years * 20)
    
    role_specializations = random.sample(SPECIALIZATIONS[role], random.randint(2, 4))
    spoken_languages = random.sample(LANGUAGES, random.randint(1, 3))
    preferred_booking = random.choice(list(BookingType))
    profile_desc = random.choice(PROFILE_DESCRIPTIONS[role])
    
    gender = random.choice(["men", "women"])
    profile_image = f"https://randomuser.me/api/portraits/{gender}/{random.randint(1, 99)}.jpg"
    full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    
    price_modifier = 1.0 + (rating - 3.0) * 0.1 + (experience_years / 50)
    hourly_rate = int(hourly_base * price_modifier)
    daily_rate = int(daily_rate * price_modifier)
    monthly_rate = int(monthly_rate * price_modifier)
    monthly_rate = min(monthly_rate, hourly_rate * 160)

    return {
        "full_name": full_name,
        "role": role,
        "experience_years": experience_years,
        "rating": rating,
        "total_reviews": total_reviews,
        "specializations": role_specializations,  # ✅ Sudah benar, langsung list
        "primary_specialization": random.choice(role_specializations),  # opsional
        "pricing": {
            "hourly_rate": hourly_rate,
            "daily_rate": daily_rate,
            "monthly_rate": monthly_rate
        },
        "kecamatan": kecamatan,
        "is_available": random.random() > 0.1,
        "profile_image": profile_image,
        "preferred_booking_type": preferred_booking,
        "languages": spoken_languages,
        "profile_description": profile_desc
    }