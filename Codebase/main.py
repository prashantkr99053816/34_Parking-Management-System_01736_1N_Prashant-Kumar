import json
import os
import re
import math

# Parking Management System
TOTAL_SLOTS = 5
FILE_NAME = "parking.txt"

RATES = {
    "car": 20,
    "bike": 10
}

# Create five empty parking slots
def create_slots():
    return [None] * TOTAL_SLOTS


# Load parking data from file
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

                if isinstance(data, list) and len(data) == TOTAL_SLOTS:
                    return data

        except (json.JSONDecodeError, OSError):
            print("Could not read saved data. Starting with empty parking.")

    return create_slots()


# Save parking data to file
def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(slots, file, indent=4)


# Validate vehicle number
def validate_vehicle(vehicle):
    pattern = r"^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{1,4}$"
    return re.fullmatch(pattern, vehicle) is not None


# Find vehicle in parking
def find_vehicle(vehicle):
    for i in range(TOTAL_SLOTS):
        if slots[i] is not None:
            if slots[i]["vehicle"] == vehicle:
                return i
    return -1


# Vehicle entry function
def entry():
    vehicle = input("Enter vehicle number: ").strip().upper()

    if not validate_vehicle(vehicle):
        print("Invalid vehicle number.")
        return

    if find_vehicle(vehicle) != -1:
        print(f"Vehicle {vehicle} is already parked.")
        return

    vehicle_type = input("Enter vehicle type (car/bike): ").strip().lower()

    if vehicle_type not in RATES:
        print("Invalid type. Enter car or bike.")
        return

    for i in range(TOTAL_SLOTS):
        if slots[i] is None:

            slots[i] = {
                "vehicle": vehicle,
                "type": vehicle_type
            }

            save_data()

            print(
                f"Vehicle {vehicle} parked in slot {i + 1}."
            )

            print(f"Slots free: {TOTAL_SLOTS - sum(s is not None for s in slots)}")
            return

    print("Parking lot is full!")


# Vehicle exit function
def exit_vehicle():
    vehicle = input("Enter vehicle number: ").strip().upper()

    index = find_vehicle(vehicle)

    if index == -1:
        print(f"Vehicle {vehicle} not found.")
        return

    # Get parking hours
    try:
        hours = float(input("Enter parking hours: "))

        if not math.isfinite(hours) or hours <= 0:
            print("Invalid hours. Enter a positive number.")
            return

    except ValueError:
        print("Invalid hours. Please enter a number.")
        return

    # Calculate parking fee
    charged_hours = max(1, math.ceil(hours))

    vehicle_type = slots[index]["type"]

    rate = RATES[vehicle_type]

    fee = charged_hours * rate

    print(f"Hours charged: {charged_hours} (minimum/rounded up)")
    print(f"Fee: Rs. {fee}")

    # Free the parking slot
    slots[index] = None

    save_data()

    print(f"Slot {index + 1} is now free.")


# Display parking status
def status():
    free_slots = 0

    print("\n------ PARKING STATUS ------")

    for i in range(TOTAL_SLOTS):

        if slots[i] is None:
            print(f"Slot {i + 1}: Empty")
            free_slots += 1

        else:
            vehicle = slots[i]["vehicle"]
            vehicle_type = slots[i]["type"]

            print(
                f"Slot {i + 1}: {vehicle} ({vehicle_type})"
            )

    print("----------------------------")
    print(f"Slots free: {free_slots} of {TOTAL_SLOTS}")
    print(f"Slots occupied: {TOTAL_SLOTS - free_slots}")


# Main menu
slots = load_data()

def main():

    while True:

        print("\n==============================")
        print("   PARKING MANAGEMENT SYSTEM")
        print("==============================")

        print("1. Entry")
        print("2. Exit")
        print("3. Status")
        print("4. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            entry()

        elif choice == "2":
            exit_vehicle()

        elif choice == "3":
            status()

        elif choice == "4":
            print("Thank you for using Parking Management System!")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3 or 4.")


# Run the program
if __name__ == "__main__":
     main()
