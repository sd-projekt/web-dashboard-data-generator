import time
from fastapi.encoders import isoformat
from mongo_helper_functions import *
from random import uniform
import datetime

parameterDict = { # Format: [Value, min, max, unit]
    "inverter": [["temperature", 50, 80, "°C"], ["v_zk", 60, 450, "V"], ["error_state", 0, 0, ""], ["target_torque", 0, 150, "Nm"]],
    "motor": [["temperature", 50, 80, "°C"], ["rpm", 0, 3000, "min^(-1)"]],
    "c6": [["error_state", 0, 0, ""], ["control_state", 0, 0, ""]],
    "accumulator": [["voltage_hv", 400, 600, "V"], ["voltage_lv", 17, 25, "V"], ["current_hv", 0, 133, "A"], ["lowest_cell_voltage", 2.25, 3.5, "V"], ["soc", 60, 80, "%"], ["contactor_state", 0, 0, ""]],
    "drivecontroller": [["statemachine_state", 0, 0, ""]],
    "pedals": [["brake", 0, 100, "%"], ["accelerator", 0, 100, "%"]],
    "steering_angle": [["value", -180, 180, "°"]],
    "spring_travel": [["value_fr", 45, 60, "mm"], ["value_rr", 45, 60, "mm"], ["value_rl", 45, 60, "mm"], ["value_fl", 45, 60, "mm"]],
    "velocity": [["value_fr", 0, 110, "km/h"], ["value_rr", 0, 110, "km/h"], ["value_rl", 0, 110, "km/h"], ["value_fl", 0, 110, "km/h"]],
    "acceleration": [["value_fr", -5, 5, "m/s^2"], ["value_rr", -5, 5, "m/s^2"], ["value_rl", -5, 5, "m/s^2"], ["value_fl", -5, 5, "m/s^2"]]
}

def generate_entries():
    # Create the connection
    databaseClient = connect_to_mongodb()
    
    for category in parameterDict:
        # Now, we have selected each category, which corresponds to an appropriate db
        categoryDB = select_db(databaseClient, category)

        for parameter in parameterDict[category]:
            # Now, we have selected each available parameter for each respective category
            parameterName : str = parameter[0]
            parameterCol = select_col(categoryDB, parameterName)

            # Generate a new document for the collection
            minParameterValue = parameter[1]
            maxParameterValue = parameter[2]
            parameterUnit = parameter[3]
            # Compute value with two decimal places
            currentParameterValue = round(uniform(minParameterValue, maxParameterValue), 2)
            # Generate display name: No underscores, starts with a capital letter
            parameterDisplayName = parameterName.replace("_", " ").capitalize()
            # Generate category: No underscores, starts with a capital letter
            parameterCategory = category.replace("_", " ").capitalize()
            # Generate timestamp
            parameterTimestamp = datetime.datetime.now().isoformat()
            # Final document
            currentDocument = { "displayName": parameterDisplayName, "category": parameterCategory, "value": currentParameterValue, "unit": parameterUnit, "timestamp": parameterTimestamp}

            # Insert document into db
            parameterCol.insert_one(currentDocument)

def main():
    while True:
        generate_entries()
        time.sleep(0.5)


if __name__ == "__main__":
    main()