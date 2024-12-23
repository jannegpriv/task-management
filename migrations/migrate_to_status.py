from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DATABASE_URL = f'postgresql://{os.getenv("DB_USER", "postgres")}:{os.getenv("DB_PASSWORD", "postgres")}@{os.getenv("DB_HOST", "db")}/{os.getenv("DB_NAME", "taskmanagement")}'
engine = create_engine(DATABASE_URL)

def migrate():
    with engine.connect() as conn:
        # Create the TaskStatus enum type
        conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE taskstatus AS ENUM ('TODO', 'IN_PROGRESS', 'DONE');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))
        
        # Add status column if it doesn't exist
        conn.execute(text("""
            DO $$ BEGIN
                ALTER TABLE tasks 
                ADD COLUMN status taskstatus DEFAULT 'TODO'::taskstatus;
            EXCEPTION
                WHEN duplicate_column THEN null;
            END $$;
        """))
        
        # Check if completed column exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = 'tasks' 
                AND column_name = 'completed'
            );
        """))
        has_completed = result.scalar()
        
        if has_completed:
            # Update status based on completed field
            conn.execute(text("""
                UPDATE tasks 
                SET status = CASE 
                    WHEN completed = true THEN 'DONE'::taskstatus 
                    ELSE 'TODO'::taskstatus 
                END;
            """))
            
            # Drop completed column
            conn.execute(text("""
                ALTER TABLE tasks 
                DROP COLUMN completed;
            """))
        
        conn.commit()

if __name__ == '__main__':
    migrate()
