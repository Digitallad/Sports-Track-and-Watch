"""
Rugby Atlas - Timezone Utilities
Handles timezone conversions for fixtures and user locations
"""
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from ..core.logging import get_logger

logger = get_logger(__name__)


class TimezoneConverter:
    """
    Utility class for timezone conversions.
    Converts fixture times between UTC and user timezones.
    """
    
    @staticmethod
    def utc_to_timezone(dt: datetime, timezone: str) -> datetime:
        """
        Convert UTC datetime to a specific timezone.
        
        Args:
            dt: Datetime in UTC
            timezone: IANA timezone string (e.g., "Europe/London")
        
        Returns:
            Datetime in the target timezone
        """
        try:
            if dt.tzinfo is None:
                # Assume UTC if no timezone info
                dt = dt.replace(tzinfo=ZoneInfo("UTC"))
            
            target_tz = ZoneInfo(timezone)
            return dt.astimezone(target_tz)
        except Exception as e:
            logger.error(f"Timezone conversion error: {e}")
            return dt
    
    @staticmethod
    def timezone_to_utc(dt: datetime, timezone: str) -> datetime:
        """
        Convert a timezone-aware datetime to UTC.
        
        Args:
            dt: Datetime in a specific timezone
            timezone: IANA timezone string
        
        Returns:
            Datetime in UTC
        """
        try:
            if dt.tzinfo is None:
                source_tz = ZoneInfo(timezone)
                dt = dt.replace(tzinfo=source_tz)
            
            utc_tz = ZoneInfo("UTC")
            return dt.astimezone(utc_tz)
        except Exception as e:
            logger.error(f"Timezone conversion error: {e}")
            return dt
    
    @staticmethod
    def get_timezone_offset(timezone: str) -> int:
        """
        Get the UTC offset for a timezone in seconds.
        
        Args:
            timezone: IANA timezone string
        
        Returns:
            Offset in seconds
        """
        try:
            tz = ZoneInfo(timezone)
            now = datetime.now(tz)
            return int(now.utcoffset().total_seconds())
        except Exception as e:
            logger.error(f"Error getting timezone offset: {e}")
            return 0


def get_user_timezone(territory_code: Optional[str] = None) -> str:
    """
    Get the appropriate timezone for a user based on territory.
    This is a placeholder - in production, this would query the database.
    
    Args:
        territory_code: Territory code (e.g., "GB", "US")
    
    Returns:
        IANA timezone string
    """
    # Placeholder mapping
    timezone_map = {
        "GB": "Europe/London",
        "FR": "Europe/Paris",
        "US": "America/New_York",
        "AU": "Australia/Sydney",
        "NZ": "Pacific/Auckland",
        "ZA": "Africa/Johannesburg",
        "IE": "Europe/Dublin",
    }
    
    return timezone_map.get(territory_code, "UTC")
