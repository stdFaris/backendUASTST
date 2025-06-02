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
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS Configuration - Lebih permisif untuk debugging
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://santairumah.netlify.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Middleware untuk logging requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Origin: {request.headers.get('origin', 'No origin')}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "environment": os.getenv("ENVIRONMENT", "development"),
        "port": os.getenv("PORT", "8000")
    }

# Fungsi untuk inisialisasi database dengan dummy data jika kosong
def initialize_database():
    try:
        logger.info("Starting database initialization...")
        # Membuat tabel di database jika belum ada
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Membuat session database
        db = SessionLocal()
        try:
            # Cek apakah ada data partner di database
            partner_count = db.query(Partner).count()
            logger.info(f"Found {partner_count} existing partners in database")
            
            # Jika database kosong (tidak ada partner), tambahkan dummy data
            if partner_count == 0:
                logger.info("Database kosong. Menambahkan dummy data...")
                
                # Generate dummy data - maksimal 150 partner, minimal 2 per peran per kecamatan
                dummy_partners = generate_dummy_partners(max_partners=75, min_per_category_per_kecamatan=1)
                logger.info(f"Generated {len(dummy_partners)} dummy partners")
                
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
                logger.info(f"Berhasil menambahkan {len(dummy_partners)} dummy partners ke database.")
            else:
                logger.info(f"Database sudah memiliki {partner_count} partner. Tidak perlu menambahkan dummy data.")
        
        except Exception as e:
            logger.error(f"Error saat mengisi dummy data: {e}")
            db.rollback()
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Critical error saat inisialisasi database: {e}")
        # Jangan biarkan aplikasi crash
        import traceback
        logger.error(traceback.format_exc())

# Panggil fungsi inisialisasi database saat aplikasi di-start
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Port: {os.getenv('PORT', '8000')}")
    initialize_database()
    logger.info("Application startup completed")

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

# Test CORS endpoint
@app.options("/auth/login")
async def options_auth_login():
    return {"message": "CORS preflight successful"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
