import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# 1. MODEL ASSUMPTIONS
# =========================================================

MAX_DRONE_RANGE = 6
DRONE_PREPARATION_TIME = 3
GROUND_SPEED_KMH = 20
DRONE_SPEED_KMH = 40  


# Ground delivery assumptions:
# Traffic: low +0 min, medium +5 min, high +10 min
# Construction: +5 min
# Snow: none +0 min, light +3 min, moderate +8 min, heavy +15 min

# Drone delivery assumptions:
# Snow: none +0 min, light +2 min, moderate +5 min
# Heavy snow: drone infeasible
# Distance > 6 km: drone infeasible


# =========================================================
# 2. CORE SIMULATION FUNCTIONS
# =========================================================

# time = distance / speed
def calculate_ground_time(distance_km, traffic_level, construction, snow_level):

    time_hours = distance_km / GROUND_SPEED_KMH
    ground_time_minutes = time_hours * 60  # convert to minutes

    if traffic_level == "medium":
        ground_time_minutes += 5
    elif traffic_level == "high":
        ground_time_minutes += 10

    if construction:
        ground_time_minutes += 5

    if snow_level == "light":
        ground_time_minutes += 3
    elif snow_level == "moderate":
        ground_time_minutes += 8
    elif snow_level == "heavy":
        ground_time_minutes += 15

    return ground_time_minutes


# since drone will not start delivering right after the order is done,
# we need to consider the preparation and setup time for drone 
# e.x. put the order inside the drone, check the battery...
def calculate_drone_time(distance_km, snow_level):

    time_hours = distance_km / DRONE_SPEED_KMH
    drone_time_minutes = time_hours * 60 + DRONE_PREPARATION_TIME

    if snow_level == "light":
        drone_time_minutes += 2
    elif snow_level == "moderate":
        drone_time_minutes += 5

    return drone_time_minutes

# very heavy snow -> not feasible for drone delivery
def is_drone_feasible(distance_km, snow_level):
    if snow_level == "heavy":
        return False
    if distance_km > MAX_DRONE_RANGE:
        return False
    return True


# want to know the reason why drone delivery was infeasible
def get_infeasibility_reason(distance_km, snow_level):

    if snow_level == "heavy" and distance_km > MAX_DRONE_RANGE:
        return "heavy snow + range"
    
    elif snow_level == "heavy":
        return "heavy snow"

    elif distance_km > MAX_DRONE_RANGE:
        return "range" 

    return "feasible"


# compare delivery times & recommendation
def compare_delivery(distance_km, traffic_level, construction, snow_level):

    ground_time = calculate_ground_time(distance_km, traffic_level, construction, snow_level)

    drone_time = calculate_drone_time(distance_km, snow_level)

    feasible = is_drone_feasible(distance_km, snow_level)

    if feasible:
        time_saved = ground_time - drone_time
        

        if drone_time < ground_time:
            recommendation = "drone"

        else:
            recommendation = "ground"
    
    else:
        time_saved = None
        recommendation = "ground"

    # a dictionary to store the results
    return {
        "distance": distance_km,
        "traffic": traffic_level,
        "snow": snow_level,
        "construction": construction,
        "ground_time": ground_time,
        "drone_time": drone_time,
        "drone_feasible": feasible,
        "time_saved": time_saved,
        "recommendation": recommendation,
        "infeasibility_reason": get_infeasibility_reason(distance_km, snow_level)
    }


# =========================================================
# 3. GENERATE SIMULATION SCENARIOS
# =========================================================

# compare_delivery(4,"high",True,"heavy")
distances = [1, 2, 4, 6, 8]
traffic_levels = ["low", "medium", "high"]
snow_levels = ["none", "light", "moderate", "heavy"]
construction_options = [False, True]

results = []

for distance in distances:
    for traffic in traffic_levels:
        for snow in snow_levels:
            for construction in construction_options:
                result = compare_delivery(distance, traffic, construction, snow)
                results.append(result)



# =========================================================
# 4. PREPARE DATA
# =========================================================

# Convert simulation results into a DataFrame
df = pd.DataFrame(results)

# Give traffic and snow their natural severity order
df["traffic"] = pd.Categorical(
    df["traffic"],
    categories=["low", "medium", "high"],
    ordered=True
)

df["snow"] = pd.Categorical(
    df["snow"],
    categories=["none", "light", "moderate", "heavy"],
    ordered=True
)

feasible_df = df[df["drone_feasible"] == True]


infeasible_df = df[df["drone_feasible"] == False]

# =========================================================
# 5. MAIN SIMULATION RESULTS
# =========================================================

# Q1: How often is drone delivery recommended overall?
drone_recommended_pct = ((df["recommendation"] == "drone").mean() * 100)

# Q2: How often is drone delivery feasible?
drone_feasible_pct = (df["drone_feasible"].mean() * 100)

# Q3: When drone delivery is feasible, how often is it recommended?
drone_recommended_when_feasible_pct = (
    (feasible_df["recommendation"] == "drone").mean() * 100
)

print("\n===== MAIN SIMULATION RESULTS =====")

print(
    f"Drone recommended overall: "
    f"{drone_recommended_pct:.1f}%"
)

print(
    f"Drone feasible: "
    f"{drone_feasible_pct:.1f}%"
)

print(
    f"Drone recommended when feasible: "
    f"{drone_recommended_when_feasible_pct:.1f}%"
)


# =========================================================
# 6. FACTOR ANALYSIS
# =========================================================

# Traffic
traffic_analysis = (
    feasible_df.groupby("traffic", observed=True)["time_saved"].mean())


# Distance
distance_analysis = (
    feasible_df.groupby("distance")["time_saved"].mean())


# Snow
# Only analyze scenarios where drone delivery is feasible
snow_analysis = (
    feasible_df.groupby("snow", observed=True)["time_saved"].mean())


print("\n===== TRAFFIC ANALYSIS =====")
print(traffic_analysis)

print("\n===== DISTANCE ANALYSIS =====")
print(distance_analysis)

print("\n===== SNOW ANALYSIS =====")
print(snow_analysis)


# =========================================================
# 7. FEASIBILITY ANALYSIS
# =========================================================

reason_pct = (
    infeasible_df["infeasibility_reason"]
    .value_counts(normalize=True) * 100)


print("\n===== INFEASIBILITY ANALYSIS =====")
print(reason_pct)


# Find cases where drone is feasible,
# but ground delivery is still preferred
ground_better_df = feasible_df[feasible_df["recommendation"] == "ground"]

print("\n===== GROUND BETTER DESPITE DRONE FEASIBILITY =====")

print(
    ground_better_df[
        [   "distance",
            "traffic",
            "snow",
            "construction",
            "ground_time",
            "drone_time",
            "time_saved"
        ]
    ]
)

# ===== MAIN SIMULATION RESULTS =====
# Drone recommended overall: 57.5%
# Drone feasible: 60.0%
# Drone recommended when feasible: 95.8%

# Of the scenarios where drone delivery was infeasible, 50% were caused by severe snow, 37.5% by range limitations, and 12.5% violated both constraints.

# =========================================================
# 8. VISUALIZATION
# =========================================================


traffic_analysis.plot(kind="bar")
plt.title("Average Drone Time Saved by Traffic Level")
plt.xlabel("Traffic Level")
plt.ylabel("Average Time Saved (minutes)")
plt.show()


distance_analysis.plot(kind="line", marker="o")
plt.title("Average Drone Time Saved by Distance")
plt.xlabel("Delivery Distance (km)")
plt.ylabel("Average Time Saved (minutes)")
plt.show()
