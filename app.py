import matplotlib.pyplot as plt
import requests
import requests
import csv
import mplcursors
import streamlit as st

def get_forbrugerprisindeks(start_year, end_year = 2024):
    url = "https://api.statbank.dk/v1/data/"

    # No data for 2025 yet.
    years = [f"{year}M12" for year in range(start_year, end_year + 1)]
    info = {
        "table": "PRIS113",
        "format": "CSV",
        "variables": [
            {
            "code": "TID",
            "values": years  # Last x years
            }
        ]
    }

    response = requests.post(url, json=info)

    if response.status_code == 200:
        csv_data = csv.reader(response.text.splitlines(),delimiter=";")
        content = []
        for row in csv_data:
            if row[1] == "INDHOLD":
                continue
            content.append(row[1])

        content = [float(value.replace(",",".")) for value in content]
        return content
    else:
        #no clue what went wrong
        print(f"Error: {response.status_code}, Message: {response.text}")
        exit()

def calculate_pay(start_pay, forbrugerprisindeks):
    #assume that the start_pay corresponds to the first year in forbrugerprisindeks
    updated_pay = [start_pay]
    
    for i in range(1,len(forbrugerprisindeks)):
        inflation = (forbrugerprisindeks[i] - forbrugerprisindeks[i-1]) / forbrugerprisindeks[i-1]
        pay = updated_pay[i-1] * (1 + inflation)
        updated_pay.append(pay)

    rounded = [round(x) for x in updated_pay]
    return rounded

def display(years,start_pay,actual_pay,expected_pay):
    plt.plot(years, expected_pay, label="Forventet Løn (Inflation)", linestyle="--", color="blue")
    plt.plot([2014, 2024], [start_pay, actual_pay], label="Faktisk Løn", color="green", marker='o')

    plt.margins(x=0, y=0)
    plt.xticks(years,rotation = 45)
    plt.legend()
    plt.xlabel("Årstal")
    plt.ylabel("Månedsløn")
    
    cursor = mplcursors.cursor(hover=False)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{int(sel.target[0])} - {sel.target[1]:,.0f} kr."))
    st.pyplot(plt)


if __name__ == "__main__":
    st.title("Lønjustering ift. Inflation")
    start_year = st.number_input("Indtast startår", min_value=1980, max_value=2024, value=2014)
    start_pay = st.number_input("Indtast din startløn", min_value=0, value=30000)
    end_year = st.number_input("Indtast aktuelt år", min_value=1980, max_value=2024, value=2024)
    end_pay = st.number_input("Indtast aktuel løn", min_value=0, value=30000)
    
    years = [start_year+i for i in range((end_year - start_year)+1)]

    #display(years,start_pay,actual_end_pay,expected_pay)
    if start_year >= end_year:
        st.error("Startåret skal være mindre end det aktuelle år!")
    else:
        if st.button("Beregn"):
            forbrugerprisindeks = get_forbrugerprisindeks(start_year,end_year)
            expected_pay = calculate_pay(start_pay,forbrugerprisindeks)
            burde_loen = expected_pay[-1]
            st.write(f"Din løn burde være {burde_loen:,.2f} kr. i {end_year}. Din aktuelle løn er {abs(burde_loen - end_pay):,.2f} kr. for {'høj' if end_pay > burde_loen else 'lav'} ift. inflation.")

            display(years,start_pay,end_pay,expected_pay)

