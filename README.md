# Curation Station
Recommendation engine that creates (or appends) a spotify playlist from a growing RDS database of independent/DIY artists.

The goal is to allow people to find new music that is similar to popular artists around the same genre neighborhood.

Although this is a work in progress, the sample json file still works with the functions.py and curation_station.py scripts.

**Current State**:

The database is not up and running yet, and might not be for a couple weeks. By October 23rd, there will be a functional web app available that creates a recommendation playlist based on genres, and the recommendations will come from a local json file and also the spotify API. I'm currently trying to use a Markov Chain Monte Carlo Gibbs sampling to find a cluster of genres that have the highest probability of being neighbors to user's input (list of genres), which will be the core of the recommendation engine.

**Coming soon**:

Frontend GUI for collaborative filtering. This will allow people to login with their Spotify account and start making playlists.

Dashboard and jupyter notebook outlining the process of this project.
