
from scipy.stats.qmc import LatinHypercube

from Utils import TestCase as TC
from Utils.functions import read_json, get_digits

from ModelValidation.SampleCDF import invCDF

def gen_mc_spread(
        test_case: TC.TestCase,
        n: int,
        active_variables = None,
        rng_seed = 1) -> list[TC.TestCase]:

    assert n > 0, "Must have at least 1 monte carlo case."
    assert test_case.case_type == TC.CASE_TYPE.mc_parent, "Must be monte carlo parent to generate child cases."
    assert test_case.status in [TC.STATUS.proposed, TC.STATUS.failure], "Must have not already generated child cases."

    # Read in the cubric config json file
    cubrc_config = read_json("000_Config/cubrc.json")
    potential_random_variables = cubrc_config["flow_conditions"]["potential_random_variables"]

    # Record the lists of active and inactive variables
    if active_variables is None:
        active_variables = potential_random_variables
    inactive_variables = []
    for random_variable in potential_random_variables:
        if random_variable not in active_variables:
            inactive_variables.append(random_variable)

    # Read in cubrc flow condition uncertainty
    var = []
    for name in active_variables:
        var.append(cubrc_config["flow_conditions"]["variance"][name])

    # Read in test case conditions
    mean = []
    for name in active_variables:
        mean.append(test_case[name])

    # Generate pseudorandom distribution
    LHS = LatinHypercube(d=len(active_variables), rng=rng_seed)
    p = LHS.random(n=n)
    X = invCDF(p, mean, var)

    # Create child cases and assign random values.
    child_cases = [None] * n
    max_digits = get_digits(n+1)
    for i in range(0, n):
        name = f"{test_case.name}_child_#{'0'*(max_digits-get_digits(i+1))}{i+1}"
        case = TC.TestCase(name, TC.CASE_TYPE.mc_child, 0, test_case.mesh)
        for j in range(0, len(active_variables)):
            case[active_variables[j]] = X[i,j]
        for k in range(0, len(inactive_variables)):
            case[inactive_variables[k]] = test_case[inactive_variables[k]]
        child_cases[i] = case

    test_case.status = TC.STATUS.success
    return child_cases



if __name__ == "__main__":
    test_case = TC.TestCase("ExampleParent", TC.CASE_TYPE.mc_parent, TC.STATUS.proposed, 0)
    test_case["mach"] = 0
    test_case["reynolds"] = 0
    test_case["stanton"] = 0
    test_case["attack_angle"] = 0
    child_list = gen_mc_spread(test_case, n = 10)

    path = "001_PrerequisiteData/gen_mc_spread.csv"
    TC.setup_csv(path)
    TC.append_case_to_csv(test_case, path)
    TC.append_case_to_csv(child_list, path)
    TC.update_case_in_csv(test_case, path)
