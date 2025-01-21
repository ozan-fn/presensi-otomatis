# Presensi Otomatis

Proyek ini adalah sistem presensi otomatis berbasis pengenalan wajah yang menggunakan teknologi pengolahan citra (image processing) dengan OpenCV dan dikembangkan menggunakan bahasa pemrograman Python.

## Persyaratan Sistem

Pastikan Anda telah menginstal perangkat berikut:

- Python 3.x
- Pustaka OpenCV
- Pustaka NumPy

## Instalasi

Ikuti langkah-langkah berikut untuk mengatur dan menjalankan proyek ini di sistem Anda:

1. **Clone repository**: 
    ```bash
    git clone https://github.com/ozan-fn/presensi-otomatis.git
    cd presensi-otomatis
    ```

2. **Buat virtual environment (opsional tetapi disarankan)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Pada Windows gunakan `venv\Scripts\activate`
    ```

3. **Instal dependensi**:
    ```bash
    pip install -r requirements.txt
    ```

    **Catatan**: Pastikan file `requirements.txt` mencakup pustaka-pustaka berikut:
    ```
    opencv-python
    numpy
    ```

## Menjalankan Proyek

Untuk menjalankan proyek ini, cukup jalankan perintah berikut:

```bash
python main.py
