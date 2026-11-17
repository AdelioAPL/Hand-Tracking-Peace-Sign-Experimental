# Hand-Tracking-Peace-Sign-Experimental (Invisible Peace Gesture)

Projek sederhana Python: ketika Anda memperagakan pose peace (jari telunjuk & tengah terangkat), Anda akan menghilang dari kamera dan digantikan background ruangan.

> Developed with AntiGravity

## Cara Menjalankan

1. Clone repositori ini atau buka di folder projek:
   ```bash
   git clone https://github.com/AdelioAPL/Hand-Tracking-Peace-Sign-Experimental.git
   cd Hand-Tracking-Peace-Sign-Experimental
   ```

2. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
   *(Atau buat virtual environment terlebih dahulu: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`)*

3. Jalankan program:
   - **Linux / macOS**:
     ```bash
     python3 main.py
     ```
   - **Windows**:
     Klik ganda `run_windows.bat` atau jalankan:
     ```cmd
     python main.py
     ```

## Tombol Kontrol
- **`b`**: Tekan saat Anda menyingkir sebentar dari kamera untuk merekam latar belakang kosong yang bersih.
- **Pose Peace (✌️)**: Tunjukkan jari telunjuk & tengah ke kamera untuk menghilang.
- **`q`**: Keluar dari aplikasi.
