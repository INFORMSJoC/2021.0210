# 2021.0210
[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)
# Satisficing Approach to On-Demand Ride-Matching

This archive is distributed in association with the [INFORMS Journal on Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

This repository contains supporting material for the paper "Satisficing Approach to On-Demand Ride-Matching" by D.L. Rong, X.Y. Sun, M.L. Zhang and S.C. H

## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2021.0210

https://doi.org/10.1287/ijoc.2021.0210.cd

Below is the BibTex for citing this snapshot of the respoitory.
```
@misc{Rong2024,
  author =        {D.L. Rong, X.Y. Sun, M.L. Zhang, and S.C. He},
  publisher =     {INFORMS Journal on Computing},
  title =         {{Satisficing Approach to On-Demand Ride-Matching}},
  year =          {2024},
  doi =           {10.1287/ijoc.2021.0210},
  url =           {https://github.com/INFORMSJoC/2021.0210},
  note =          {Available for download at https://github.com/INFORMSJoC/2021.0210},
}  
```

## Description
Online ride-hailing platforms have developed into an integral part of the transportation infrastructure in many countries. The primary task of a ride-hailing platform is to match trip requests to drivers in real time. Although both passengers and drivers prefer a prompt pickup to initiate their trips, it is often difficult to find a nearby driver for every passenger. If the driver is far from the pickup point, the passenger may cancel the trip while the driver is heading toward the pickup point. In order for the platform to be profitable, the trip cancellation rate must be maintained at a low level. In this paper, we propose a data-driven, computational efficient approach to ride-matching. We associate an adjustable pickup time target with each request and formulate an optimization problem to maximize the joint probability of all the pickup times meeting the respective targets. This formulation can be converted into a standard assignment problem, which can be solved within an $O(n^{3})$ time bound with $n$ being the number of trip requests to be matched. By adjusting pickup time targets individually, this approach can assign more high-value trip requests to nearby drivers, thus boosting the platform's revenue and still maintaining a low cancellation rate. In numerical experiments, the proposed approach outperforms several ride-matching policies that are widely used in practice.

## Data
In Section 5.1 of our paper, the original data set of a ride-hailing platform in China can be found in [https://www.biendata.xyz/competition/kdd_didi/](Data).

## Scripts
The folder contains the Python implementations of the numerical experiments. The codes are split into the following three folders.

* "Static" contains codes for numerical experiments on Static Matching.

* "Sequence" contains codes for numerical experiments on Sequential Matching.

* "Soon" contains codes for numerical experiments with Soon-to-be-Available Drivers.

## Details on implementation
In static matching experiments, parameters $N$ and $M$ respectively represent the number of drivers and trip requests entering the order-matching decision; $X\underline{}axis\underline{}max$ and $Y\underline{}axis\underline{}max$ limit the area of the matching region; $Alpha$ and $Percentile$ correspond to the preference exponent and the reference cancellation rate in each order’s pickup time target. $LB\underline{}waiting$ and $UB\underline{}waiting$ respond to the possible passengers’ waiting thresholds, and $LB\underline{}reward$ and $UB\underline{}reward$ correspond to potential trip values. $LB\underline{}minPerKm$ and $UB\underline{}minPerKm$ are the endpoint values of the empirical driving speed. 

 * In experiments to explore the influence of preference exponents, different model results can be obtained by iterating $Alpha$, as shown in Table 1.

 * In experiments with different pickup points and waiting thresholds, we adjust passengers' waiting thresholds with the parameters $LB\underline{}waiting$ and  $UB\underline{}waiting$. The dispersion of pickup points is controlled by model code. And the reference cancellation rate, e.g., parameter $Percentile$ can be set by reference to the results of the benchmark model.

 * In the peak/off-peak hours experiments, the peak-hour and off-peak hour driving speeds can be set by parameters $LB\underline{}minPerKm$ and $UB\underline{}minPerKm$.

In sequence matching experiments, parameter $T$ refers to the whole time horizon, $OPT\underline{}Interval$ is the time interval of each round of order-matching, $mu\underline{}Driver$ and $mu\underline{}Rider$ indicate respectively the arrival rate of available drivers and trip requests.

## Requirements
All optimization problems are solved using CPLEX via Python language.
