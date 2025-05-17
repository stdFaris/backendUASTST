from enum import Enum

class PartnerRole(str, Enum):
    PEMBANTU = "pembantu"
    TUKANG_KEBUN = "tukang_kebun"
    TUKANG_PIJAT = "tukang_pijat"

class BookingType(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class MatchSortCriteria(str, Enum):
    RATING = "rating"
    EXPERIENCE = "experience"
    PRICE = "price"