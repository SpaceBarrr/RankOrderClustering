import string
import numpy as np
import pandas as pd

def column_optimisation(df: pd.DataFrame, machines: list, parts: list) -> tuple[pd.DataFrame, bool]:
    for part in parts:
        sum_col = 0
        for machine in machines:
            if df.loc[machine,part] == 1:
                machine_index = list(df.index.values)
                sum_power_index = machine_index.index(machine) + 1
                sum_col += 2**sum_power_index
        df.loc["Sum",part] = sum_col
    
    df.loc["Rank"] = df.loc["Sum"].rank(method="first")

    # add a dummy column to display the powers of two we are summing
    twos_powers = [2**(n+1) for n in range(len(machines))]
    twos_powers.extend([" "," "])
    df[" "] = twos_powers

    print(df,end="\n\n")
    df = df.drop(" ", axis=1)

    old_cols = list(df)
    new_columns = df.columns[df.loc[df.last_valid_index()].argsort()]
    df = df[new_columns]
    
    status = False
    if np.array_equal(old_cols, new_columns):
        status = True

    df = df.drop(["Sum","Rank"], axis=0)
    return df, status

def row_optimisation(df: pd.DataFrame, machines: list, parts: list) -> tuple[pd.DataFrame, bool]:
    for machine in machines:
        sum_row = 0
        for part in parts:
            if df.loc[machine,part] == 1:
                parts_index = list(df)
                sum_power_index = parts_index.index(part) + 1
                sum_row += 2**sum_power_index
        df.loc[machine,"Sum"] = sum_row

    df["Rank"] = df["Sum"].rank(method="first")

    # add a dummy row to display the powers of two we are summing
    twos_powers = [2**(n+1) for n in range(len(parts))]
    twos_powers.extend([" "," "])
    df.loc[" "] = twos_powers

    print(df,end="\n\n")
    df = df.drop(" ", axis=0)

    old_rows = list(df.index.values)
    df = df.sort_values("Sum")
    new_rows = list(df.index.values)

    status = False
    if np.array_equal(old_rows, new_rows):
        status = True

    df = df.drop(["Sum","Rank"], axis=1)
    return df, status

if __name__ == "__main__":
    print("Automated Rank Order Clustering")
    
    while True:
        num_parts = input("Enter the number of parts (letters): ")
        num_machines = input("Enter the number of machines (numbers): ")

        try:
            num_parts = int(num_parts)
            num_machines = int(num_machines)
        except ValueError:
            print("Non-integer detected. Please try again!\n")
            continue

        if num_parts < 1 or num_machines < 1:
            print("Number of machines & parts must be >1. Please try again!\n")
            continue
        break

    possible_machines = [machine + 1 for machine in range(num_machines)]
    possible_parts = list(string.ascii_uppercase)[:num_parts]

    part_machine_incidence_matrix = pd.DataFrame(0, index=possible_machines, columns=possible_parts)
    print(part_machine_incidence_matrix)

    for part in possible_parts:
        while True:
            machine_input = input(f"\nEnter machines for Part {part}, separated by a space: ")
            try:
                machine_list = [int(machine) for machine in machine_input.split()]
            except ValueError:
                print("You did not enter a valid number. Please try again!\n")
                continue

            for machine in machine_list:
                part_machine_incidence_matrix.loc[machine,part] = 1
            break

        print(part_machine_incidence_matrix)

    input("\nCreated part incidence matrix. Press enter to begin rank order clustering...")

    while True:
        part_machine_incidence_matrix, col_status = column_optimisation(part_machine_incidence_matrix, possible_machines, possible_parts)
        part_machine_incidence_matrix, row_status = row_optimisation(part_machine_incidence_matrix, possible_machines, possible_parts)
        
        if row_status and col_status:
            break

    print("Done!")
    print(part_machine_incidence_matrix)
    