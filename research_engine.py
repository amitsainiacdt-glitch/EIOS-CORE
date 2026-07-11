def start():
    print("=" * 60)
    print("EIOS RESEARCH ENGINE")
    print("=" * 60)

    print("1. Business Quality")
    print("2. Management")
    print("3. Moat")
    print("4. Financial Quality")
    print("5. Valuation")
    print("6. Final Verdict")

    choice = input("\nChoose Research Step: ")

    if choice == "1":
        print("\nBusiness Quality Analysis Started...")

    elif choice == "2":
        print("\nManagement Analysis Started...")

    elif choice == "3":
        print("\nMoat Analysis Started...")

    elif choice == "4":
        print("\nFinancial Quality Analysis Started...")

    elif choice == "5":
        print("\nValuation Analysis Started...")

    elif choice == "6":
        print("\nGenerating Final EIOS Verdict...")

    else:
        print("\nInvalid Selection")