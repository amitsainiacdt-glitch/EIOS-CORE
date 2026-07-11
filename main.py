from companies import anup
from companies import kpit
from companies import coromandel
import research_engine

print("=" * 60)
print("EIOS - Everest Investment Operating System")
print("=" * 60)

print("1. ANUP Engineering")
print("2. KPIT Technologies")
print("3. Coromandel International")
print("4. Research Engine")
print("5. Exit")

choice = input("\nSelect Option: ")

if choice == "1":
    anup.show()

elif choice == "2":
    kpit.show()

elif choice == "3":
    coromandel.show()

elif choice == "4":
    research_engine.start()

elif choice == "5":
    print("Goodbye Amit!")

else:
    print("Invalid Selection")