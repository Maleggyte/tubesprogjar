from flask import Flask, render_template, jsonify
import requests
import threading
import time
import signal
import sys

app = Flask(__name__)

websites = [
    {"nama_perguruan": "Universitas Aisyah Pringsewu", "wilayah": "Lampung", "url": "http://www.aisyahuniversity.ac.id/"},
    {"nama_perguruan": "Universitas Muhammadiyah Lampung", "wilayah": "Lampung", "url": "http://www.uml.ac.id"},
    {"nama_perguruan": "Universitas Bina Darma", "wilayah": "Sumatera Selatan", "url": "http://www.binadarma.ac.id/"},
    {"nama_perguruan": "Institut Informatika Dan Bisnis Darmajaya", "wilayah": "Lampung", "url": "http://www.darmajaya.ac.id/profile/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Hukum PERTIBA Pangkalpinang", "wilayah": "Bangka Belitung", "url": "http://stihpertiba.ac.id"},
    {"nama_perguruan": "Institut Teknologi dan Bisnis (ITBis) Lembah Dempo", "wilayah": "Sumatera Selatan", "url": "http://www.lembahdempo.ac.id"},
    {"nama_perguruan": "Universitas Katolik Musi Charitas", "wilayah": "Sumatera Selatan", "url": "http://www.ukmc.ac.id"},
    {"nama_perguruan": "STMIK Pringsewu", "wilayah": "Lampung", "url": "http://www.stmikpringsewu.ac.id"},
    {"nama_perguruan": "STMIK Tunas Bangsa Bandar Lampung", "wilayah": "Lampung", "url": "http://www.stmiktb.com"},
    {"nama_perguruan": "Universitas Muhammadiyah Pringsewu", "wilayah": "Lampung", "url": "http://www.umpri.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Pertiba", "wilayah": "Bangka Belitung", "url": "http://www.stiepertiba.ac.id"},
    {"nama_perguruan": "STISIPOL Candradimuka", "wilayah": "Sumatera Selatan", "url": "http://stisipolcandradimuka.ac.id/"},
    {"nama_perguruan": "STIE IBEK Pangkalpinang Bangka", "wilayah": "Bangka Belitung", "url": "http://www.stie-ibek.ac.id/web/"},
    {"nama_perguruan": "Universitas Sang Bumi Ruwa Jurai", "wilayah": "Lampung", "url": "http://www.saburai.ac.id"},
    {"nama_perguruan": "Institut Teknologi dan Bisnis Diniyyah Lampung", "wilayah": "Lampung", "url": "http://www.instidla.ac.id"},
    {"nama_perguruan": "Akademi Manajemen Belitung", "wilayah": "Bangka Belitung", "url": "http://amb.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Sosial dan Ilmu Politik Pahlawan 12", "wilayah": "Sumatera Selatan", "url": "http://stisipolp12.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Kesehatan Abdurahman Palembang", "wilayah": "Sumatera Selatan", "url": "http://stikesabdurahman.ac.id"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Kesehatan Adila Di Kota Bandar Lampung", "wilayah": "Lampung", "url": "http://stikes.adila.ac.id"},
    {"nama_perguruan": "Stikes Pondok Pesantren Assanadiyah Palembang", "wilayah": "Sumatera Selatan", "url": "http://assanadiyah.ponpes.id"},
    {"nama_perguruan": "Universitas Tridinanti", "wilayah": "Sumatera Selatan", "url": "http://univ-tridinanti.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Teknologi Pagaralam", "wilayah": "Sumatera Selatan", "url": "http://sttpagaralam.ac.id/"},
    {"nama_perguruan": "Akademi Analis Kesehatan Harapan Bangsa Bengkulu", "wilayah": "Bengkulu", "url": "http://aakharapanbangsa.ac.id"},
    {"nama_perguruan": "Universitas Muhammadiyah Palembang", "wilayah": "Sumatera Selatan", "url": "http://www.um-palembang.ac.id/"},
    {"nama_perguruan": "AKBID Tunas Harapan Bangsa Palembang", "wilayah": "Sumatera Selatan", "url": "http://www.akbidthb.ac.id"},
    {"nama_perguruan": "Universitas Muhammadiyah Palembang", "wilayah": "Sumatera Selatan", "url": "http://www.um-palembang.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Pertanian (Stiper) Belitang", "wilayah": "Sumatera Selatan", "url": "http://www.stiperbelitang.ac.id/"},
    {"nama_perguruan": "STIKES 'Aisyiyah Palembang", "wilayah": "Sumatera Selatan", "url": "http://stikes-aisyiyah-palembang.ac.id/"},
    {"nama_perguruan": "Universitas Bandar Lampung", "wilayah": "Lampung", "url": "http://ubl.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Abdi Nusa", "wilayah": "Sumatera Selatan", "url": "http://stieabdinusa.blogspot.com/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Rahmaniyah Sekayu", "wilayah": "Sumatera Selatan", "url": "http://www.stier.ac.id/"},
    {"nama_perguruan": "STMIK Dian Cipta Cendikia Kotabumi", "wilayah": "Lampung", "url": "http://dcckotabumi.ac.id/"},
    {"nama_perguruan": "Universitas Malahayati", "wilayah": "Lampung", "url": "http://malahayati.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Teologi Injili di Palembang", "wilayah": "Sumatera Selatan", "url": "http://www.sttipal.ac.id"},
    {"nama_perguruan": "STKIP Muhammadiyah Pagaralam", "wilayah": "Sumatera Selatan", "url": "http://stkipm-pagaralam.ac.id"},
    {"nama_perguruan": "Universitas Muhammadiyah Bengkulu", "wilayah": "Bengkulu", "url": "http://umb.ac.id"},
    {"nama_perguruan": "Akademi Keperawatan Kesdam II Sriwijaya", "wilayah": "Sumatera Selatan", "url": "http://akperkesdam2sriwijaya.ac.id/"},
    {"nama_perguruan": "Institut Sains Dan Bisnis (Isb) Atma Luhur", "wilayah": "Bangka Belitung", "url": "http://www.atmaluhur.ac.id/"},
    {"nama_perguruan": "Akademi Farmasi Cendikia Farma Husada", "wilayah": "Sumatera Selatan", "url": "http://lms.akfarcefada.ac.id/"},
    {"nama_perguruan": "Akademi Keperawatan Pangkalpinang", "wilayah": "Bangka Belitung", "url": "http://akperpangkalpinang.ac.id"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Kesehatan Bina Husada Palembang", "wilayah": "Sumatera Selatan", "url": "http://binahusada.ac.id/"},
    {"nama_perguruan": "Politeknik Akamigas Palembang", "wilayah": "Sumatera Selatan", "url": "http://poliakamigasplg.ac.id/"},
    {"nama_perguruan": "Universitas Sumatera Selatan", "wilayah": "Sumatera Selatan", "url": "http://uss.ac.id"},
    {"nama_perguruan": "Sekolah Tinggi Teknologi Nusantara Lampung", "wilayah": "Lampung", "url": "http://www.sttnlampung.ac.id"},
    {"nama_perguruan": "STMIK Dharma Wacana", "wilayah": "Lampung", "url": "http://www.stmikdharmawacana.ac.id"},
    {"nama_perguruan": "Universitas Indo Global Mandiri", "wilayah": "Sumatera Selatan", "url": "http://www.uigm.ac.id"},
    {"nama_perguruan": "Universitas Muhammadiyah Metro", "wilayah": "Lampung", "url": "http://ummetro.ac.id/"},
    {"nama_perguruan": "Akademi Kebidanan Manna", "wilayah": "Sumatera Selatan", "url": "http://www.akbidmanna.ac.id"},
    {"nama_perguruan": "Akademi Komunitas Industri Pertambangan Bukit Asam", "wilayah": "Sumatera Selatan", "url": "http://akipba.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi dan Bisnis Prana Putra", "wilayah": "Sumatera Selatan", "url": "http://www.stiebipranaputra.ac.id"},
    {"nama_perguruan": "Universitas PGRI Palembang", "wilayah": "Sumatera Selatan", "url": "http://univpgri-palembang.ac.id"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Hukum Rahmaniyah Sekayu", "wilayah": "Sumatera Selatan", "url": "http://stihura.ic.id"},
    {"nama_perguruan": "STIKESMAS Abdi Nusa Palembang", "wilayah": "Sumatera Selatan", "url": "http://stikesmasabdinusaplg.ac.id/"},
    {"nama_perguruan": "Universitas Teknokrat Indonesia", "wilayah": "Lampung", "url": "http://teknokrat.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Serelo Lahat", "wilayah": "Sumatera Selatan", "url": "http://stieserelo.ac.id/"},
    {"nama_perguruan": "Universitas Muhammadiyah Jakarta", "wilayah": "Jakarta", "url": "http://pmb.umj.ac.id"},
    {"nama_perguruan": "Universitas Baturaja", "wilayah": "Sumatera Selatan", "url": "http://unbara.ac.id"},
    {"nama_perguruan": "Universitas Tulang Bawang", "wilayah": "Lampung", "url": "http://utb.ac.id/v2/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Gentiaras", "wilayah": "Sumatera Selatan", "url": "http://stie.gentiaras.ac.id/"},
    {"nama_perguruan": "Universitas Bina Darma", "wilayah": "Sumatera Selatan", "url": "http://www.binadarma.ac.id/"},
    {"nama_perguruan": "Akademi Kebidanan Wahana Husada", "wilayah": "Sumatera Selatan", "url": "http://akbidwahana.ac.id"},
    {"nama_perguruan": "Universitas Pat Petulai", "wilayah": "Sumatera Selatan", "url": "http://upprl.ac.id/"},
    {"nama_perguruan": "Universitas IBA Palembang", "wilayah": "Sumatera Selatan", "url": "http://web.iba.ac.id/"},
    {"nama_perguruan": "STMIK Dharma Wacana Metro Lampung", "wilayah": "Lampung", "url": "http://www.stmikdharmawacana.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Hukum Serasan", "wilayah": "Sumatera Selatan", "url": "http://www.stihserasan.ac.id"},
    {"nama_perguruan": "Universitas Dehasen Bengkulu", "wilayah": "Bengkulu", "url": "http://unived.ac.id"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Kesehatan Mitra Adiguna", "wilayah": "Lampung", "url": "http://stikesmitraadiguna.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Kesehatan (STIKES) Citra Delima Bangka", "wilayah": "Bangka Belitung", "url": "http://www.stikescitradelima.ac.id"},
    {"nama_perguruan": "STIK Siti Khadijah Palembang", "wilayah": "Sumatera Selatan", "url": "http://stik-sitikhadijah.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Prabumulih", "wilayah": "Sumatera Selatan", "url": "http://stieprabumulih.ac.id"},
    {"nama_perguruan": "Universitas Palembang", "wilayah": "Sumatera Selatan", "url": "http://unpal.ac.id"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Ekonomi Al-Madani", "wilayah": "Lampung", "url": "http://www.almadani.ac.id"},
    {"nama_perguruan": "Universitas Bina Insan", "wilayah": "Sumatera Selatan", "url": "http://univbinainsan.ac.id/"},
    {"nama_perguruan": "Akademi Kebidanan Budi Mulia Palembang", "wilayah": "Sumatera Selatan", "url": "http://budimulia.ac.id/"},
    {"nama_perguruan": "Sekolah Tinggi Ilmu Teknik Serasan", "wilayah": "Sumatera Selatan", "url": "http://www.stitserasan.ac.id/"},
    {"nama_perguruan": "Akademi Kebidanan An Nur Husada Walisongo", "wilayah": "Sumatera Selatan", "url": "http://annur.ac.id"},
    {"nama_perguruan": "STIKES Adila", "wilayah": "Lampung", "url": "http://www.stikes.adila.ac.id"},
    {"nama_perguruan": "Universitas Muhammadiyah Bangka Belitung", "wilayah": "Bangka Belitung", "url": "http://unmuhbabel.ac.id"},
    {"nama_perguruan": "STIH Muhammadiyah Kalianda", "wilayah": "Lampung", "url": "http://stihmuhammadiyahkalianda.ac.id"},
    {"nama_perguruan": "Universitas Nahdlatul Ulama Lampung", "wilayah": "Lampung", "url": "http://unulampung.ac.id"},
    {"nama_perguruan": "Politeknik Sekayu", "wilayah": "Sumatera Selatan", "url": "http://polsky.ac.id"},
    {"nama_perguruan": "Universitas Mitra Indonesia", "wilayah": "Lampung", "url": "http://www.umitra.ac.id/"},
    {"nama_perguruan": "STIKES Sapta Bakti", "wilayah": "Bengkulu", "url": "http://stikessaptabakti.ac.id/"},
    {"nama_perguruan": "Universitas Ratu Samban", "wilayah": "Bengkulu", "url": "http://unras.ac.id/"}
]





results = {site['url']: {"nama_perguruan": site['nama_perguruan'], "wilayah": site['wilayah'], "status": "Unknown"} for site in websites}
stop_thread = False

def get_status_description(status_code):
    if status_code // 100 == 2:
        return "Success"
    elif status_code // 100 == 3:
        return "Redirection"
    elif status_code // 100 == 4:
        return "Client Error"
    elif status_code // 100 == 5:
        return "Server Error"
    else:
        return "Unknown Status"

def check_website_status():
    global stop_thread
    while not stop_thread:
        for site in websites:
            url = site["url"]
            try:
                response = requests.get(url, timeout=5)
                status_description = get_status_description(response.status_code)
                results[url] = {"nama_perguruan": site["nama_perguruan"], "wilayah": site["wilayah"], "status": f"{response.status_code} ({status_description})"}
            except requests.RequestException:
                results[url] = {"nama_perguruan": site["nama_perguruan"], "wilayah": site["wilayah"], "status": "Website invalid"}
        time.sleep(30)

@app.route('/')
def index():
    return render_template('index.html', results=results)

@app.route('/status')
def status():
    return jsonify(results)

def signal_handler(sig, frame):
    global stop_thread
    print('Exiting...')
    stop_thread = True
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=check_website_status)
    thread.start()
    app.run(debug=True, use_reloader=False)
