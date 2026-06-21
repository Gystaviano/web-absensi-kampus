import streamlit as st
from datetime import datetime
from database import get_connection

def portal_mahasiswa():
    st.title("🎓 Portal Absensi Mahasiswa")
    st.write("Silakan login menggunakan NIM dan Nama lengkap Anda untuk melakukan absensi.")
    
    with st.form("form_absensi"):
        nim_input = st.text_input("Masukkan NIM").strip()
        nama_input = st.text_input("Masukkan Nama Lengkap").strip().upper() # Kapital otomatis
        
        submit_button = st.form_submit_button("Login & Absen Hadir")
        
        if submit_button:
            if not nim_input or not nama_input:
                st.warning("⚠️ NIM dan Nama tidak boleh kosong!")
                return
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Validasi Login
            cursor.execute("SELECT * FROM students WHERE nim = ? AND nama = ?", (nim_input, nama_input))
            student = cursor.fetchone()
            
            if student:
                now = datetime.now()
                tanggal = now.strftime("%Y-%m-%d")
                jam = now.strftime("%H:%M:%S")
                
                # Cek apakah sudah absen hari ini
                cursor.execute("SELECT * FROM attendance WHERE nim = ? AND tanggal = ?", (nim_input, tanggal))
                if cursor.fetchone():
                    st.error(f"❌ Maaf {student[1]}, Anda sudah melakukan absensi hari ini!")
                else:
                    # Insert absensi
                    cursor.execute(
                        "INSERT INTO attendance (nim, tanggal, jam, status) VALUES (?, ?, ?, ?)",
                        (nim_input, tanggal, jam, "Hadir")
                    )
                    conn.commit()
                    st.success(f"✅ Berhasil! Absensi atas nama **{student[1]}** tercatat pada jam {jam}.")
            else:
                st.error("⚠️ Gagal Login! Kombinasi NIM dan Nama tidak ditemukan di database.")
                
            conn.close()