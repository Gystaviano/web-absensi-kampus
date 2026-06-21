import streamlit as st
import pandas as pd
from datetime import date
from database import get_connection

def dashboard_admin():
    st.title("🛡️ Dashboard Admin")
    st.write("Kelola dan pantau data absensi mahasiswa di sini.")
    
    conn = get_connection()
    
    tab1, tab2 = st.tabs(["📋 Absensi Harian", "📊 Rekap Keseluruhan"])
    
    with tab1:
        st.subheader("Daftar Absensi Harian")
        hari_ini = st.date_input("Pilih Tanggal Absensi", date.today())
        
        query_harian = f"""
            SELECT a.tanggal as Tanggal, a.jam as Jam, s.nim as NIM, s.nama as Nama, a.status as Status
            FROM attendance a
            JOIN students s ON a.nim = s.nim
            WHERE a.tanggal = '{hari_ini}'
            ORDER BY a.jam DESC
        """
        df_harian = pd.read_sql_query(query_harian, conn)
        st.dataframe(df_harian, use_container_width=True)
        
        if not df_harian.empty:
            csv_harian = df_harian.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Harian ke CSV",
                data=csv_harian,
                file_name=f"absensi_harian_{hari_ini}.csv",
                mime="text/csv"
            )
            
    with tab2:
        st.subheader("Rekap Absensi Per Mahasiswa")
        
        # Hitung total hari absensi yang pernah berjalan di sistem
        total_hari_query = "SELECT COUNT(DISTINCT tanggal) FROM attendance"
        total_hari_aktif = pd.read_sql_query(total_hari_query, conn).iloc[0,0]
        
        query_rekap = """
            SELECT s.nim as NIM, s.nama as Nama, 
                   COUNT(a.id) as Total_Hadir
            FROM students s
            LEFT JOIN attendance a ON s.nim = a.nim AND a.status = 'Hadir'
            GROUP BY s.nim
        """
        df_rekap = pd.read_sql_query(query_rekap, conn)
        
        # Kalkulasi Total Tidak Hadir
        # Asumsi: Jika hari aktif = 5, dan Hadir = 3, maka Tidak Hadir = 2. 
        # Jika belum ada absensi sama sekali (hari aktif = 0), tidak hadir = 0
        if total_hari_aktif > 0:
            df_rekap['Total_Tidak_Hadir'] = total_hari_aktif - df_rekap['Total_Hadir']
        else:
            df_rekap['Total_Tidak_Hadir'] = 0
            
        st.dataframe(df_rekap, use_container_width=True)
        
        csv_rekap = df_rekap.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Rekap ke CSV",
            data=csv_rekap,
            file_name="rekap_absensi_mahasiswa.csv",
            mime="text/csv"
        )
        
    conn.close()