import matplotlib.pyplot as plt
import requests
import requests
import csv

def get_forbrugerprisindeks(start_year, end_year = 2024):
    if start_year > end_year:
        exit()
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


if __name__ == "__main__":
    start_year = 2010
    end_year = 2024
    forbrugerprisindeks = get_forbrugerprisindeks(start_year,end_year)
    start_pay = 40_000
    updated_pay = calculate_pay(start_pay,forbrugerprisindeks)
    years = [start_year+i for i in range((end_year - start_year)+1)]

    plt.plot(years,updated_pay)
    plt.margins(x=0, y=0)
    plt.xticks(years,rotation = 45)

    plt.xlabel("Årstal")
    plt.ylabel("Månedsløn justeret ift. inflation")

    plt.show()
    print(forbrugerprisindeks) 
    print(updated_pay)



