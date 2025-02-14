import pandas as pd


def add_conditions_to_df(df: pd.DataFrame, var_name: str, threshold: float, condition: str = "under"):
    if condition not in ["under", "over"]:
        condition = "under"

    var_name_df = var_name + "_" + condition + "_" + str(threshold)
    df[var_name_df] = df.temp_min.apply(
        lambda x: x < threshold if condition == "under" else x > threshold)
    prev_var_name = "prev_" + var_name + "_" + condition + "_" + str(threshold)
    df[prev_var_name] = False

    prev_value = False
    for idx, row in df.iterrows():
        df.loc[idx, prev_var_name] = prev_value
        prev_value = row[var_name_df]

    return df


def calculate_non_dependent_probability(df: pd.DataFrame, var_name: str, condition: bool):
    length_all = df.shape[0]
    length_condition = df[lambda x: x[var_name] == condition].shape[0]
    probability = length_condition / length_all
    return probability


def calculate_and_probability(df: pd.DataFrame, var_names: list[str], var_conditions: list[bool]):
    length_all = df.shape[0]
    length_condition = \
        df[lambda x: (x[var_names[0]] == var_conditions[0]) & (x[var_names[1]] == var_conditions[1])].shape[0]
    probability = length_condition / length_all
    return probability


def calculate_dependent_probability(df: pd.DataFrame, dependent_var: str, independent_var: str,
                                    dependent_var_condition: bool, independent_var_condition: bool):
    # P(A|B) = P(A u B) / P(B)
    and_probability = calculate_and_probability(df=df, var_names=[dependent_var, independent_var],
                                                var_conditions=[dependent_var_condition, independent_var_condition])
    independent_probability = calculate_non_dependent_probability(df=df, var_name=independent_var,
                                                                  condition=independent_var_condition)
    dependent_probability = and_probability / independent_probability
    return dependent_probability


if __name__ == "__main__":
    df_data_2023 = pd.read_csv(f"../data/weather_data_bielefeld_2023.csv")
    df_data_2023 = df_data_2023.rename(
        columns={"tavg": "temp_avg", "tmin": "temp_min", "tmax": "temp_max", "prcp": "precipitation",
                 "wspd": "wind_speed", "wdir": "wind_direction", "wpgt": "wind_peak_gust", "pres": "pressure",
                 "tsun": "time_sun"})

    dependent_var = "temp_min"
    independent_var = "temp_min"
    threshold_dependent_var = 0.0
    threshold_independent_var = 0.0
    condition_dependent_var = "under"
    condition_independent_var = "under"

    df_data_2023 = add_conditions_to_df(df=df_data_2023, var_name=dependent_var, threshold=threshold_dependent_var,
                                        condition=condition_dependent_var)

    dependent_var_name_cond = dependent_var + "_" + condition_dependent_var + "_" + str(threshold_dependent_var)
    independent_var_name_cond = "prev_" + dependent_var_name_cond

    print(calculate_non_dependent_probability(df=df_data_2023, var_name=dependent_var_name_cond, condition=True))
    print(calculate_and_probability(df=df_data_2023, var_names=[dependent_var_name_cond, independent_var_name_cond],
                                    var_conditions=[True, True]))
    print(calculate_dependent_probability(df=df_data_2023, dependent_var=dependent_var_name_cond,
                                          independent_var=independent_var_name_cond, dependent_var_condition=True,
                                          independent_var_condition=True))

    print("a")

