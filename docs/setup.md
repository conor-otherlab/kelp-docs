# Setup

## First Time Install

Run the commands below to get the dev environment set up. Dependencies should all be in the `setup-dev.sh` script, but be aware that some debugging might be needed to fix missing elements if there's been any drift since the last time `setup-dev.sh` has been updated.

``` bash
# Install the basic dependencies 
sudo apt install build-essential git

# Install github command line (https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
        && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y

# Login to github & clone the repo
gh auth login
gh repo clone otherlab/kelp

# Run the setup script to install rest of dependencies and set up docker containers
cd kelp
./tools/setup-dev.sh
```

## Building Software

Most build tasks are managed with the top-level Makefile, take a read through it to see how it works & what it can do.

``` bash
# Most useful make targets

make arduanchorbot  	# Builds the autopilot firmware, binary is kelp/ardupilot/build/navigator/bin/anchorbot
make qgroundcontrol 	# Builds AnchorbotQGroundControl.AppImage
make blueos-anchorbot 	# Builds & deploys docker container with additional software running on companion computer
make docs 				# Serves a local copy of this documentation
make sitl 				# Builds simulation version of the ardupilot firmware & starts SITL simulation (needs QGC & gazebo sim already running to work)
```
## Updating Dependencies

Ardupilot and QGroundControl are both included as [git subtrees](https://docs.github.com/en/get-started/using-git/about-git-subtree-merges). To update them to later versions, use `git subtree pull`, for example the command to upgrade ardusub to 4.1.1 was `git subtree pull -P ardupilot ardupilot ArduSub-4.1.1 --squash`. If submodules are updated, you will need to update the top-level .gitmodules by hand, since subtrees don't cooperate with recursive submodules. Upgrades haven't always gone smoothly, it's not recommended unless there are compelling reasons. 

## Steam Deck

SteamOS is an Arch-based linux distribution that runs the QGroundControl appimage without too much trouble. Copy `AnchorbotQGroundControl.Appimage` and `tools/setup-deck.sh` to a SD card, move it over to the deck, then install dependencies using the terminal in desktop mode (instructions [here](https://help.steampowered.com/en/faqs/view/671A-4453-E8D2-323C)):

``` bash
# Open terminal in the sd card folder (open in files, right click, "Open Terminal Here")

# set a user password (if you haven't already)
passwd

# run setup script
./setup-dev.sh
```

After installation, add QGroundControl to the steam library (right click on icon, then "Add to Steam"), and you can launch directly from game mode instead of booting desktop mode.


## Topside & Network

The ROV can be controlled either from a Linux laptop with a gamepad or a steam deck (recommended). Our custom fork of QGroundControl is right now only tested on Linux, but a should build on Windows if necessary. Whatever controls the ROV needs a static IP of `192.168.2.1`, which is automatically assigned to the steam deck through the router but can be set through the wifi settings on Ubuntu if a laptop is used. Any additional computers connected to the wifi will get assigned DHCP addresses, and will not work as control computers.

The topside box contains a raspberry pi that can eventually be used for live data analysis & statistics. See `topside/` and `data/src/dashboard` for current progress if that gets picked up in the future.

### GS Network Diagram
``` mermaid	
%%{init: {'theme':'neutral'}}%%
graph LR
	subgraph ROV
		navigator["Blue Robotics Navigator<br/>192.168.2.2"]
        dvl["Waterlinked DVL A50<br/>192.168.2.95"]
        switch["Blue Robotics Ethernet Switch"]
		fxti1[ROV FXTI]
	end

	subgraph groundstation
		fxti2[Topside FXTI]
		router["Teltonika RUT951<br/>Router & Cell Modem<br/>192.168.2.3"]
		rpi["RPi Groundstation<br/>192.168.2.5"]
	end

	ugps["Waterlinked UGPS G2 <br/> 192.168.2.94"]
	deck["Steam Deck <br/> 192.168.2.1"]

	navigator --- switch
    dvl --- switch
    switch --- fxti1
    fxti1 --- Tether --- fxti2
    ugps --- fxti2
    fxti2 --- router
    rpi --- router
    router --- deck
 ```

