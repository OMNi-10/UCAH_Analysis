import csv
from enum import Enum
from operator import truediv

from Utils.UncertainValue import UncertainValue
from Utils.functions import read_json


class CASE_TYPE(Enum):
    cfd_result = 1
    mc_parent = 2
    mc_child = 3
    cubrc_experiment = 4

class STATUS(Enum):
    proposed = 0
    in_progress = 1
    success = 2
    failure = 3

class MESH(Enum):
    example_mesh = 0

class TestCase:
    # --- Identifying info ---
    name: str
    case_type: CASE_TYPE
    status:    STATUS
    mesh:      MESH

    # --- Nondimensional Test Conditions ---
    mach:     float
    reynolds: float
    # pressure_coefficient: float
    stanton: float
    attack_angle: float  # radians
    sideslip_angle:  float  # radians

    # --- CFD Test Conditions ---
    """
    Mach
    Alpha
    Beta
    VX
    VY
    VZ
    Temp
    Density
    Pressure
    Viscosity
    Speed of sound
    Velocity
    """

    # --- Test Results ---
    body_x_force: float | UncertainValue
    body_y_force: float | UncertainValue
    body_z_force: float | UncertainValue

    body_x_moment: float | UncertainValue
    body_y_moment: float | UncertainValue
    body_z_moment: float | UncertainValue

    point_pressures: list[float] | list[UncertainValue]
    point_heat_flux: list[float] | list[UncertainValue]

    # --- Nondimensional Results ---
    lift_coefficient: float | UncertainValue
    drag_coefficient: float | UncertainValue
    side_coefficient: float | UncertainValue

    pitch_coefficient: float | UncertainValue
    yaw_coefficient:   float | UncertainValue
    roll_coefficient:  float | UncertainValue


    point_stanton_numbers: list[float] | list[UncertainValue]

    def __init__(self, name: str, case_type: int|CASE_TYPE, status: int|STATUS, mesh: int|MESH):
        self.name = name
        if type(case_type) == int:
            self.case_type = CASE_TYPE(case_type)
        else:
            self.case_type = case_type

        if type(status) == int:
            self.status = STATUS(status)
        else:
            self.status = status

        if type(mesh) == int:
            self.mesh = MESH(mesh)
        else:
            self.mesh = mesh

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def format_for_csv(self) -> list:
        file_config = read_json("Config/file_handling.json")
        header_names = file_config["header_variables"]

        data = []
        for variable in header_names:
            data.append(self[variable])
        return data


def case_in_csv(test_cases: TestCase, path: str, skip_header: bool = True) -> dict[TestCase, int]:
    if type(test_cases) == TestCase:
        test_cases = [test_cases]

    names = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader)
        for row in reader:
            names.append(row[0])

    locations = {}
    for case in test_cases:
        if case.name in names:
            locations[case] = names.index(case.name)
    return locations

def setup_csv(path: str):
    file_config = read_json("Config/file_handling.json")
    header = file_config["header_variables"]
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def append_case_to_csv(test_cases: TestCase | list[TestCase], path: str) -> list[TestCase]:
    if type(test_cases) == TestCase:
        test_cases = [test_cases]

    data = []
    skipped_cases = []
    for case in test_cases:
        if case_in_csv(case, path):
            print(f"WARNING: skipped {case.name}, already exists")
            continue
        data.append(case.format_for_csv())

    with open(path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    return skipped_cases


def update_case_in_csv(test_cases: TestCase|list[TestCase], path: str):
    if type(test_cases) == TestCase:
        test_cases = [test_cases]

    data = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)


    for case in test_cases:
        present = case_in_csv(case, path)
        if not present:
            print(f"WARNING: skipped {case.name}, does not exist")
            continue
        index = present[case]
        data[index] = case.format_for_csv()
    pass

def remove_case_from_csv(test_cases: TestCase|list[TestCase], path: str):
    pass
