"""
Fix auth_provider enum issue in database
This script ensures auth_provider is properly stored as VARCHAR
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    exit(1)

print("Fixing auth_provider enum issue...")
print(f"Connecting to database...")

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    print("[OK] Connected to database")

    # Check current data type
    cursor.execute("""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'auth_provider'
    """)
    result = cursor.fetchone()
    print(f"Current auth_provider type: {result[0] if result else 'NOT FOUND'}")

    # Ensure it's VARCHAR (not enum type)
    print("  -> Ensuring auth_provider is VARCHAR...", end=" ")
    cursor.execute("""
        ALTER TABLE users
        ALTER COLUMN auth_provider TYPE VARCHAR
        USING auth_provider::VARCHAR
    """)
    conn.commit()
    print("[DONE]")

    # Update any NULL values to 'email'
    print("  -> Setting default values...", end=" ")
    cursor.execute("""
        UPDATE users
        SET auth_provider = 'email'
        WHERE auth_provider IS NULL OR auth_provider = ''
    """)
    conn.commit()
    print("[DONE]")

    print("\n[SUCCESS] Auth provider issue fixed!")
    print("\nPlease restart your backend server.")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"\n[FAILED] Fix failed: {e}")
    exit(1)
