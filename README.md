# Optimizing Champion Drafting in League of Legends: Predicting Counter Picks and Optimal Team Compositions Using Machine Learning

## Data source
Acquire data from the [RIOT Games API](https://developer.riotgames.com/) - this is the eventual plan, but for now we will use a [Kaggle dataset](https://www.kaggle.com/datasets/chuckephron/leagueoflegends)

## Plan for our data
The data will be sorted into roles, and then compared within those roles to the other champions within the same roles.

### Data Cleaning
Convert champions into numerical IDs
### Synergies
How often a champion wins with other champions
### Counters
How often a champion wins against other champions

### Modeling
Will use simple logistic regression to calculate probability of winning

## Project Structure

- main.py: Entry point, interacts with other files
- data_loader.py: Loads raw match data
- data_cleaning.py: Filters for draft-time information (Champions picks & Game results)
- features.py: Feature engineering and representations.