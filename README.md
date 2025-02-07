# Løn Beregner App

Dette er en Python-app, der beregner, hvad din løn "burde" være i forhold til inflation.
Man bliver "snydt" for nogle måneder, da den bruger forbrugerprisindeks'er for December, så hvis man f.eks. bliver ansat i februar, regner den ikke inflationen for februar-december det år. 

## Installation

1. Klon repository'et:
   - git clone https://github.com/christianbergsoerensen/L-n-Checker.git

2. (Valgfrit) Lav et virtual environment og aktiver det:
   - python3.10 -m venv .venv
   - .venv/Scripts/Activate

3. Installer nødvendige pakker:
   - pip install -r requirements.txt

4. Kør appen:
   - streamlit run app.py