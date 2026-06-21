import streamlit as st
from database import init_db
from attendance import portal_mahasiswa
from report import dashboard_admin

# Konfigurasi halaman dasar Streamlit
st.set_page_config(page_title="Sistem Absensi", page_icon="🏫", layout="centered")

def main():
    # Inisialisasi Database setiap kali aplikasi berjalan
    init_db()
    
    st.sidebar.title("🗂️ Navigasi")
    pilihan_menu = st.sidebar.radio("Pilih Akses:", ["Mahasiswa", "Admin"])
    
    if pilihan_menu == "Mahasiswa":
        portal_mahasiswa()
        
    elif pilihan_menu == "Admin":
        st.sidebar.markdown("---")
        # Keamanan sederhana menggunakan session_state Streamlit
        if "admin_logged_in" not in st.session_state:
            st.session_state["admin_logged_in"] = False
            
        if not st.session_state["admin_logged_in"]:
            st.sidebar.write("🔒 Silakan Login Admin")
            password = st.sidebar.text_input("Password", type="password")
            
            # Ganti password sesuai keinginan (saat ini: admin123)
            if st.sidebar.button("Login Admin"):
                if password == "a1a2a3":
                    st.session_state["admin_logged_in"] = True
                    st.rerun() # Refresh halaman agar masuk
                else:
                    st.sidebar.error("Password Salah!")
        else:
            if st.sidebar.button("Logout"):
                st.session_state["admin_logged_in"] = False
                st.rerun()
            
            dashboard_admin()

if __name__ == "__main__":
    main()