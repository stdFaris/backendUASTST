from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, customers, partners, bookings, reviews, notifications
import os
import uvicorn
from src.database.session import engine, SessionLocal
from src.models.base import Base
from src.models.partner import Partner
from src.schemas.enums import PartnerRole
from src.utils.dummy_data import generate_dummy_partners
import json

app = FastAPI()

# Konfigurasi CORS
origins = [
    "https://santairumah.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Fungsi untuk inisialisasi database dengan dummy data jika kosong
def initialize_database():
    # Membuat tabel di database jika belum ada
    Base.metadata.create_all(bind=engine)
    
    # Membuat session database
    db = SessionLocal()
    try:
        # Cek apakah ada data partner di database
        partner_count = db.query(Partner).count()
        
        # Jika database kosong (tidak ada partner), tambahkan dummy data
        if partner_count == 0:
            print("Database kosong. Menambahkan dummy data...")
            
            # Generate dummy data - maksimal 150 partner, minimal 2 per peran per kecamatan
            dummy_partners = generate_dummy_partners(max_partners=75, min_per_category_per_kecamatan=1)
            
            # Masukkan ke database
            for partner_data in dummy_partners:
                # Konversi enum ke string untuk penyimpanan JSON
                role_str = partner_data["role"].value if isinstance(partner_data["role"], PartnerRole) else partner_data["role"]
                
                # Konversi preferred_booking_type ke string jika merupakan enum
                booking_type = partner_data["preferred_booking_type"]
                booking_type_str = booking_type.value if hasattr(booking_type, "value") else booking_type
                
                # Pastikan specializations disimpan sebagai JSON yang valid
                specializations_data = partner_data["specializations"]
                
                # Pastikan pricing disimpan sebagai JSON yang valid
                pricing_data = partner_data["pricing"]
                
                # Buat objek Partner dengan data yang telah dikonversi
                partner = Partner(
                    full_name=partner_data["full_name"],
                    role=role_str,  # Gunakan string
                    experience_years=partner_data["experience_years"],
                    rating=partner_data["rating"],
                    total_reviews=partner_data["total_reviews"],
                    specializations=specializations_data,
                    pricing=pricing_data,
                    kecamatan=partner_data["kecamatan"],
                    is_available=partner_data["is_available"],
                    profile_image=partner_data["profile_image"],
                    preferred_booking_type=booking_type_str,  # Gunakan string
                    languages=partner_data["languages"],
                    profile_description=partner_data["profile_description"]
                )
                db.add(partner)
            
            # Commit semua perubahan sekaligus
            db.commit()
            print(f"Berhasil menambahkan {len(dummy_partners)} dummy partners ke database.")
        else:
            print(f"Database sudah memiliki {partner_count} partner. Tidak perlu menambahkan dummy data.")
    
    except Exception as e:
        print(f"Error saat inisialisasi database: {e}")
        # Jika terjadi error, tambahkan detail lebih banyak untuk debugging
        import traceback
        print(traceback.format_exc())
        db.rollback()
    finally:
        db.close()

# Panggil fungsi inisialisasi database saat aplikasi di-start
@app.on_event("startup")
async def startup_event():
    initialize_database()

# Include routers
app.include_router(auth.router)
app.include_router(customers.router) 
app.include_router(partners.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Service Booking API"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
