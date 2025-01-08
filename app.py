from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# Definisikan logika fuzzy
kualitas_bahan = ctrl.Antecedent(np.arange(0, 101, 1), 'kualitas_bahan')
jenis_bahan = ctrl.Antecedent(np.arange(0, 101, 1), 'jenis_bahan')
ukuran = ctrl.Antecedent(np.arange(0, 101, 1), 'ukuran')
harga_jual = ctrl.Consequent(np.arange(0, 101, 1), 'harga_jual')

# Definisi himpunan fuzzy
kualitas_bahan['tipis'] = fuzz.trimf(kualitas_bahan.universe, [0, 0, 30])
kualitas_bahan['sedang'] = fuzz.trimf(kualitas_bahan.universe, [20, 35, 50])
kualitas_bahan['tebal'] = fuzz.trimf(kualitas_bahan.universe, [40, 100, 100])

jenis_bahan['katun'] = fuzz.trimf(jenis_bahan.universe, [0, 0, 40])
jenis_bahan['jeans'] = fuzz.trimf(jenis_bahan.universe, [30, 50, 70])
jenis_bahan['sweater'] = fuzz.trimf(jenis_bahan.universe, [60, 100, 100])

ukuran['kecil'] = fuzz.trimf(ukuran.universe, [0, 0, 40])
ukuran['sedang'] = fuzz.trimf(ukuran.universe, [30, 50, 70])
ukuran['besar'] = fuzz.trimf(ukuran.universe, [60, 100, 100])

harga_jual['murah'] = fuzz.trimf(harga_jual.universe, [0, 0, 50])
harga_jual['sedang'] = fuzz.trimf(harga_jual.universe, [30, 50, 70])
harga_jual['mahal'] = fuzz.trimf(harga_jual.universe, [60, 100, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['katun'] & ukuran['kecil'], harga_jual['murah'])
rule2 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['katun'] & ukuran['sedang'], harga_jual['murah'])
rule3 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['katun'] & ukuran['besar'], harga_jual['murah'])
rule4 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['jeans'] & ukuran['kecil'], harga_jual['murah'])
rule5 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['jeans'] & ukuran['sedang'], harga_jual['sedang'])
rule6 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['jeans'] & ukuran['besar'], harga_jual['sedang'])
rule7 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['sweater'] & ukuran['kecil'], harga_jual['sedang'])
rule8 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['sweater'] & ukuran['sedang'], harga_jual['sedang'])
rule9 = ctrl.Rule(kualitas_bahan['tipis'] & jenis_bahan['sweater'] & ukuran['besar'], harga_jual['sedang'])
rule10 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['katun'] & ukuran['kecil'], harga_jual['murah'])
rule11 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['katun'] & ukuran['sedang'], harga_jual['sedang'])
rule12 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['katun'] & ukuran['besar'], harga_jual['sedang'])
rule13 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['jeans'] & ukuran['kecil'], harga_jual['sedang'])
rule14 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['jeans'] & ukuran['sedang'], harga_jual['sedang'])
rule15 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['jeans'] & ukuran['besar'], harga_jual['mahal'])
rule16 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['sweater'] & ukuran['kecil'], harga_jual['sedang'])
rule17 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['sweater'] & ukuran['sedang'], harga_jual['mahal'])
rule18 = ctrl.Rule(kualitas_bahan['sedang'] & jenis_bahan['sweater'] & ukuran['besar'], harga_jual['mahal'])
rule19 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['katun'] & ukuran['kecil'], harga_jual['sedang'])
rule20 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['katun'] & ukuran['sedang'], harga_jual['mahal'])
rule21 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['katun'] & ukuran['besar'], harga_jual['mahal'])
rule22 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['jeans'] & ukuran['kecil'], harga_jual['mahal'])
rule23 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['jeans'] & ukuran['sedang'], harga_jual['mahal'])
rule24 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['jeans'] & ukuran['besar'], harga_jual['mahal'])
rule25 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['sweater'] & ukuran['kecil'], harga_jual['mahal'])
rule26 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['sweater'] & ukuran['sedang'], harga_jual['mahal'])
rule27 = ctrl.Rule(kualitas_bahan['tebal'] & jenis_bahan['sweater'] & ukuran['besar'], harga_jual['mahal'])

harga_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19,
    rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27
])
harga_simulasi = ctrl.ControlSystemSimulation(harga_ctrl)

@app.route('/', methods=['GET', 'POST'])
def index():
    harga_hasil = None
    if request.method == 'POST':
        # Ambil input dari form
        kualitas = int(request.form['kualitas_bahan'])
        jenis = int(request.form['jenis_bahan'])
        ukuran_input = int(request.form['ukuran'])

        # Jalankan logika fuzzy
        harga_simulasi.input['kualitas_bahan'] = kualitas
        harga_simulasi.input['jenis_bahan'] = jenis
        harga_simulasi.input['ukuran'] = ukuran_input
        harga_simulasi.compute()

        harga_hasil = harga_simulasi.output['harga_jual']

    return render_template('index.html', harga_jual=harga_hasil)

if __name__ == '__main__':
    app.run(debug=True)