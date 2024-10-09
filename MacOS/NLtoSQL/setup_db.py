import sqlite3

def create_database():
    conn = sqlite3.connect('healthcare_claims.db')
    cursor = conn.cursor()

    # Create table - members
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        insurance_id TEXT
    )
    ''')

    # Create table - Providers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS providers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        specialty TEXT,
        hospital TEXT
    )
    ''')

    # Create table - Claims
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS claims (
        id INTEGER PRIMARY KEY,
        member_id INTEGER,
        provider_id INTEGER,
        claim_date TEXT,
        amount REAL,
        status TEXT,
        FOREIGN KEY(member_id) REFERENCES members(id),
        FOREIGN KEY(provider_id) REFERENCES providers(id)
    )
    ''')

    # Create table - procedures
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS procedures (
        id INTEGER PRIMARY KEY,
        claim_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        FOREIGN KEY(claim_id) REFERENCES claims(id)
    )
    ''')

    # Create table - Diagnosis
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diagnosis (
        id INTEGER PRIMARY KEY,
        claim_id INTEGER,
        diagnosis_code TEXT,
        description TEXT,
        FOREIGN KEY(claim_id) REFERENCES claims(id)
    )
    ''')

    # Insert sample data into members
    cursor.executemany('''
    INSERT INTO members (name, age, gender, insurance_id) VALUES (?, ?, ?, ?)
    ''', [
        ('John Doe', 45, 'M', 'INS12345'),
        ('Jane Smith', 30, 'F', 'INS67890'),
        ('Sam Green', 50, 'M', 'INS23456'),
        ('Emma White', 65, 'F', 'INS34567'),
        ('Chris Black', 40, 'M', 'INS45678')
    ])

    # Insert sample data into Providers
    cursor.executemany('''
    INSERT INTO providers (name, specialty, hospital) VALUES (?, ?, ?)
    ''', [
        ('Dr. Alice Brown', 'Cardiology', 'City Hospital'),
        ('Dr. Bob Miller', 'Orthopedics', 'Central Hospital'),
        ('Dr. Carol Lee', 'General Practice', 'Green Clinic'),
        ('Dr. David Wright', 'Dermatology', 'City Hospital'),
        ('Dr. Emily Clark', 'Pediatrics', 'Children Hospital')
    ])

    # Insert sample data into Claims
    cursor.executemany('''
    INSERT INTO claims (member_id, provider_id, claim_date, amount, status) VALUES (?, ?, ?, ?, ?)
    ''', [
        (1, 1, '2024-01-15', 1200.50, 'paid'),
        (2, 2, '2024-02-10', 900.00, 'denied'),
        (3, 3, '2024-03-05', 300.75, 'dending'),
        (4, 4, '2024-01-20', 1500.00, 'paid'),
        (5, 5, '2024-02-25', 750.25, 'paid')
    ])

    # Insert sample data into procedures
    cursor.executemany('''
    INSERT INTO procedures (claim_id, treatment_name, cost) VALUES (?, ?, ?)
    ''', [
        (1, 'Echocardiogram', 500.00),
        (1, 'Stress Test', 700.50),
        (2, 'Knee X-Ray', 300.00),
        (3, 'Annual Checkup', 150.75),
        (4, 'Skin Biopsy', 1000.00),
        (5, 'Child Vaccination', 750.25)
    ])

    # Insert sample data into Diagnosis
    cursor.executemany('''
    INSERT INTO diagnosis (claim_id, diagnosis_code, description) VALUES (?, ?, ?)
    ''', [
        (1, 'I20.0', 'Angina Pectoris'),
        (2, 'M17.11', 'Unilateral Primary Osteoarthritis of Knee'),
        (3, 'Z00.00', 'General Adult Medical Exam'),
        (4, 'L82.0', 'Seborrheic Keratosis'),
        (5, 'Z23', 'Encounter for Immunization')
    ])

    conn.commit()
    conn.close()
    print("Healthcare claims database setup complete.")

if __name__ == '__main__':
    create_database()
