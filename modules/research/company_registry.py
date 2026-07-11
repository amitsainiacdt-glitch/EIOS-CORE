def open_company_registry():
    print("\n" + "=" * 50)
    print("          COMPANY REGISTRY")
    print("=" * 50)

    companies = [
        "ANUP Engineering",
        "KPIT Technologies",
        "Coromandel International",
        "Shakti Pumps"
    ]

    for i, company in enumerate(companies, start=1):
        print(f"{i}. {company}")

    print("=" * 50)