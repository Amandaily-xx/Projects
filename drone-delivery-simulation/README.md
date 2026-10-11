# Drone Delivery Simulation

## Overview

This project is a Python-based simulation exploring when drone delivery could be a useful alternative to ground food delivery in Montreal.

The simulation compares estimated delivery times for drones and ground couriers under different conditions, including distance, traffic, road construction, and snow. It also considers operational constraints such as severe weather and maximum drone delivery range.

Rather than assuming drones are always faster, I wanted to explore **when drone delivery is feasible and when its time advantage makes it worth considering.**

## Motivation

I lived in Shenzhen, China, for 18 years before moving to Montreal for university. Drone delivery was an idea I became interested in while living in Shenzhen, and I started wondering whether something similar could work in Montreal.

After moving here, I noticed how different the delivery environment is. Many food couriers use bikes or e-bikes, and road construction, traffic, and especially Montreal's long winters can make deliveries more challenging. I've often wondered how these conditions affect delivery times, both for couriers and for customers waiting for their food.

However, I also realize that drone delivery comes with its own challenges. Drones need preparation time after an order is ready, have limited battery capacity and operating range, and may not be able to fly safely in severe weather. Montreal's winter conditions make these limitations particularly important.

This led me to a question: **Could drone delivery be a useful alternative in Montreal, and under what conditions would it actually make sense?**

I decided to start with a simplified Python simulation to explore this question before considering more realistic data and operational constraints.

## Research Question

> Under what conditions can drone delivery provide a meaningful time advantage over ground delivery while remaining operationally feasible?

## Results

The simulation evaluated 120 delivery scenarios using different combinations of distance, traffic, snow, and road construction.

### Main Results

| Metric | Result |
|---|---:|
| Total simulated scenarios | 120 |
| Drone delivery feasible | 60.0% |
| Drone delivery recommended overall | 57.5% |
| Drone recommended among feasible scenarios | 95.8% |

Under the current assumptions, drone delivery was feasible in 72 of the 120 scenarios. Among these feasible scenarios, drones were recommended in 69 cases.

### Why Was Drone Delivery Infeasible?

Of the 48 infeasible scenarios:

| Reason | Scenarios | Percentage |
|---|---:|---:|
| Heavy snow only | 24 | 50.0% |
| Exceeded maximum range only | 18 | 37.5% |
| Both constraints | 6 | 12.5% |

These results suggest that operational constraints play an important role in determining whether drone delivery can be considered.

### When Was Ground Delivery Preferred?

Interestingly, ground delivery was still preferred in three scenarios where drone delivery was feasible.

These scenarios shared several characteristics:

- Short delivery distances of 1–2 km
- Low traffic
- No road construction
- No snow or only light snow

In these cases, the drone's higher travel speed was not enough to overcome its fixed preparation time. When estimated delivery times were equal, the model recommended ground delivery.

## Key Findings

**1. Drone delivery is not always the better option.**

Although drones travel faster under the model's assumptions, ground delivery remains competitive for short-distance orders under favorable road conditions.

**2. Operational feasibility matters as much as delivery speed.**

Drones were recommended in 95.8% of feasible scenarios, but they were feasible in only 60% of all simulated scenarios. This suggests that distance and weather constraints are major limitations within the model.

**3. Ground-level delays can increase the potential advantage of drone delivery.**

Higher traffic levels, construction delays, and longer delivery distances generally increase the estimated time advantage of drones, provided drone delivery remains feasible.

## Limitations

This is an exploratory simulation rather than a validated real-world delivery model.

Several limitations should be considered:

- Delivery speeds and delay penalties are simplified assumptions rather than measurements from Montreal.
- The 120 scenarios are equally weighted and do not represent the actual frequency of delivery conditions.
- The model uses the same delivery distance for drones and ground couriers, although their real routes may differ.
- Drone feasibility is based only on snow severity and delivery distance. Other factors, such as wind, battery capacity, payload weight, airspace restrictions, and safe landing locations, are not modeled.
- Ground and drone delivery times do not account for every stage of the delivery process.
- The model focuses on delivery time rather than operating costs, environmental impacts, or safety outcomes.

Therefore, the results should be interpreted as patterns within the simulated scenarios, not predictions of actual drone delivery performance in Montreal.

## Next Steps

Future improvements could include:

- Building an interactive prototype where users can enter delivery conditions and compare recommendations.
- Incorporating historical Montreal weather data and road construction records.
- Testing how sensitive the results are to different speed, preparation-time, and range assumptions.
- Exploring additional operational constraints, such as wind conditions and battery capacity.

## Tools Used

- **Python:** Simulation logic and scenario generation
- **pandas:** Data manipulation and analysis
- **Matplotlib:** Data visualization