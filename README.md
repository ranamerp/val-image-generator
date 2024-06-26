
# Valorant Post-Game Image
 Generation of Valorant Post-Game Stats.

![b2ab433e-3ac4-46d3-bc8f-1c147b04de07](https://raw.githubusercontent.com/ranamerp/val-image-generator/master/output/output.png)

## Usage

### Prerequisites
Python >= 3.7. To download Python, follow [these](https://github.com/PackeTsar/Install-Python/blob/master/README.md) instructions. 


### 1. Clone GitHub Repository
[Download](https://github.com/ranamerp/val-image-generator/archive/refs/heads/master.zip) or clone the repo:
```
git clone https://github.com/ranamerp/val-image-generator.git
```

### 2. Install Python packages
```cmd
python -m pip install -r requirements.txt
```

### 3. Set region
In `src/valorant_manager.py` change `Client(region="na")` to your region.

Valid regions are: `na, eu, latam, br, ap, kr, pbe`


### 4. Run
```cmd
python main.py
```

### 5. Adjust colors.
Colors and team names can be adjusted in the `colors.json` file. Team A is first-half attackers, and Team B is second-half attackers.
Images are outputted in `/output` with the file name being either output.png, or the matchid of the game.

Special thanks to colinhartigan, whose code makes up the majority of this project, and to Hendrik, who's API makes this code non-dependent on the in-game client.
