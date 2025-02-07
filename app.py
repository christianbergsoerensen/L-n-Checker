import matplotlib.pyplot as plt
import requests
import requests
import csv
import streamlit as st

def get_forbrugerprisindeks(months):
    url = "https://api.statbank.dk/v1/data/"

    
    info = {
        "table": "PRIS113",
        "format": "CSV",
        "variables": [
            {
            "code": "TID",
            "values": months  # Last x years + y months
            }
        ]
    }
    print(len(months))
    print(months)


    response = requests.post(url, json=info)

    if response.status_code == 200:
        csv_data = csv.reader(response.text.splitlines(),delimiter=";")
        content = []
        for row in csv_data:
            print(row)
            if row[1] == "INDHOLD":
                continue
            content.append(row[1])

        content = [float(value.replace(",",".")) for value in content]
        return content
    else:
        #no clue what went wrong
        print(f"Error: {response.status_code}, Message: {response.text}")
        exit()

def calculate_pay(start_pay,forbrugerprisindeks):
    
    
    updated_pay = [start_pay]

    month_accum = 0
    for i in range(1,len(forbrugerprisindeks)):
        inflation = (forbrugerprisindeks[i] - forbrugerprisindeks[i-1]) / forbrugerprisindeks[i-1]
        pay = updated_pay[i-1] * (1 + inflation)
        
        updated_pay.append(pay+month_accum)

    rounded = [round(x) for x in updated_pay]
    return rounded

def display(years,start_pay,actual_pay,expected_pay):
    plt.plot(years, expected_pay, label="Forventet Løn (Inflation)", linestyle="--", color="blue")
    plt.plot([years[0], years[-1]], [start_pay, actual_pay], label="Faktisk Løn", color="green", marker='o')
    print(years,expected_pay)
    plt.margins(x=0, y=0)
    #plt.xticks(years,rotation = 45)
    plt.legend()
    plt.xlabel("Årstal")
    plt.ylabel("Månedsløn")
    
    #cursor = mplcursors.cursor(hover=False)
    #cursor.connect("add", lambda sel: sel.annotation.set_text(f"{int(sel.target[0])} - {sel.target[1]:,.0f} kr."))
    st.pyplot(plt)

def get_int_from_month(month):
    match month:
        case "Januar":
            return 1
        case "Februar":
            return 2
        case "Marts":
            return 3
        case "April":
            return 4
        case "Maj":
            return 5
        case "Juni":
            return 6
        case "Juli":
            return 7
        case "August":
            return 8
        case "September":
            return 9
        case "Oktober":
            return 10
        case "November":
            return 11
        case "December":
            return 12
        case _:
            #impossible to reach
            print("Ugyldig måned")
            exit()


if __name__ == "__main__":
    st.title("Lønjustering ift. Inflation")
    start_year = st.number_input("Indtast startår", min_value=1980, max_value=2024, value=2014)
    months = [
    "Januar", "Februar", "Marts", "April", "Maj", "Juni",
    "Juli", "August", "September", "Oktober", "November", "December"]
    start_month = st.selectbox("Vælg startmåned:", months)
    start_pay = st.number_input("Indtast din startløn", min_value=0, value=30000)
    end_year = st.number_input("Indtast aktuelt år", min_value=1980, max_value=2024, value=2024)
    end_pay = st.number_input("Indtast aktuel løn", min_value=0, value=30000)
    
    

    #display(years,start_pay,actual_end_pay,expected_pay)
    if start_year > end_year:
        st.error("Startåret skal være mindre end det aktuelle år!")
    else:
        if st.button("Beregn"):
            start_month = get_int_from_month(start_month)

            months = [f"{start_year}M{0 if month < 10 else ''}{month}" for month in range(start_month, 13)]
            months = months + [f"{year}M{0 if month < 10 else ''}{month}" for year in range(start_year + 1, end_year + 1) for month in range(1,13)]

            forbrugerprisindeks = get_forbrugerprisindeks(months)
            expected_pay = calculate_pay(start_pay,forbrugerprisindeks)
            burde_loen = expected_pay[-1]
            st.write(f"Din løn burde være {burde_loen:,.2f} kr. i {end_year}. Din aktuelle løn er {abs(burde_loen - end_pay):,.2f} kr. for {'høj' if end_pay > burde_loen else 'lav'} ift. inflation.")

            months = [float(month.replace("M",".")) for month in months]
            display(months,start_pay,end_pay,expected_pay)

