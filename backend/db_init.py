
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional


from database import Base, engine
import models
import auth

def init_db(db_path: Optional[str] = None):
    """
    Initialize the database with all required tables and create an initial admin user
    
    Args:
        db_path (Optional[str]): Custom database path. If None, uses default from database.py
    """
    try:

        Base.metadata.create_all(bind=engine)
        

        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        

        existing_admin = db.query(models.User).filter(models.User.is_admin == True).first()
        
        if not existing_admin:

            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin_password')
            

            hashed_password = auth.get_password_hash(admin_password)
            

            admin_user = models.User(
                username=admin_username,
                hashed_password=hashed_password,
                is_admin=True
            )
            
            db.add(admin_user)
            db.commit()
            
        

        db.close()
        

    
    except Exception as e:
        sys.exit(1)


def main():
    """
    CLI for database management
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="File Sharing Database Management")
    parser.add_argument(
        'action', 
        choices=['init', 'reset', 'test'], 
        help='Database management action'
    )
    
    args = parser.parse_args()
    
    if args.action == 'init':
        init_db()

if __name__ == '__main__':
    main()