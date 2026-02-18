# Acoustic Impact Localization

Determines the impact point on a surface using acoustic sensor triangulation. Six sensors detect the impact sound at different times; the algorithm computes the exact impact coordinates by solving a nonlinear least-squares problem.

## How It Works

1. **Sensors** are placed at known positions around the surface
2. An impact produces a sound wave that reaches each sensor at a different time
3. Time differences between sensors create a system of nonlinear equations
4. `scipy.optimize.least_squares` finds the impact point (x, y), measurement accuracy, and effective sound speed

## Algorithm

The solver minimizes the residuals between observed and predicted time differences:

```
Δt_predicted(i) = dist(impact, sensor_i) / v_sound
residual(i) = Δt_observed(i) - Δt_predicted(i)
```

The unknowns are: impact position (x, y), time offset, and sound propagation speed in the material.

## Visualization

The script produces a matplotlib plot showing:
- Sensor positions (blue dots)
- True impact point (red cross)
- Computed impact point (green circle)
- Accuracy radius

## Usage

```bash
python impact.py
```

## Tech Stack

`Python` `NumPy` `SciPy` `Matplotlib`

## Requirements

```
pip install -r requirements.txt
```
