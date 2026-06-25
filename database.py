import sqlite3

DB_NAME = "sistem_absensi.db"

def get_connection():
    # check_same_thread=False penting untuk Streamlit dan SQLite
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Membuat tabel students
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            nim TEXT PRIMARY KEY,
            nama TEXT NOT NULL
        )
    ''')
    
    # Membuat tabel attendance
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT,
            tanggal TEXT,
            jam TEXT,
            status TEXT,
            FOREIGN KEY (nim) REFERENCES students (nim)
        )
    ''')
    
    # Daftar 25 Mahasiswa dari foto (Seed Data)
    students_data = [
        ('15250536', 'ABDUL MUKHTAR AZKA'), ('15250232', 'ABDULLAH AZZAHIDI'),
        ('15250208', 'AKBAR ARDIANSYAH'), ('15250170', 'KHAYNA MAULIDYA ARIESTA'),
        ('15250570', 'ARDIKA PRAMUDIYA PUTRA'), ('15250038', 'ARLY AZMI HARRIS'),
        ('15250161', 'ARRIVAL MUKHAMMAD RAIHAN ATVYSSSA'), ('15250199', 'BAYU ZIKRIANSYAH'),
        ('15251020', 'DZAKY NAUFAL FAUZAN'), ('15250454', 'EVIANA SIHOMBING'),
        ('15250273', 'FAUZAN NAJIB'), ('15250718', 'TRISNO WIBOWO'),
        ('15250055', 'ANDI'), ('15251220', 'LINDA WULAN SARI'),
        ('15250095', 'LUKMAN FIRDAUS'), ('15250741', 'MUHAMAD RAIHAN DWI SAPUTRA'),
        ('15250274', 'MUHAMMAD DIKA SYAH PUTRA'), ('15250937', 'MUHAMMAD SHEFA DIAZ PUTRA'),
        ('15250669', 'NAUFAL PASYA ALDRI'), ('15250400', 'NUR RACHMA RAMADHANI'),
        ('15251129', 'PUTRA MUHAMMAD PASHA'), ('15250213', 'RAFIF MUHAMMAD ANWAR'),
        ('15250455', 'REIFAN ARYA PRATAMA'), ('15250201', 'SEPTIAN SYAHRUR RAMADHAN'), ('15250210', 'FINA ZANUAR DWI TARUNA')
    ]
    
    # Cek apakah data sudah ada agar tidak di-insert berulang kali
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO students (nim, nama) VALUES (?, ?)", students_data)
        
    conn.commit()
    conn.close()
