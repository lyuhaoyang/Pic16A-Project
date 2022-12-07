import numpy 
import pandas as pd
import random
from sklearn.linear_model import LinearRegression


def get_column_correlation(dataframe, cols):
    """"Obtain correlation for each of the 2 columns passed in arguments
        Args:
             cols: column names for a data frame which you want to obtain correlations with, a list
             dataframe: the dataframe to retrieve columns
        Returns:
             scripts about the correlation between each of the 2 columns
    
    """
    if not isinstance(dataframe, pd.core.frame.DataFrame):
            raise TypeError("dataframe should be an instance of Python Dataframe")
    #get number of columns
    n = len(cols) 
    output=""
    # iterate to obtain correlation value
    for i in range(n):
        # to avoid redundacy, j starts after i
        for j in range(i,n):
           
            if i != j:
                #obtain correlation
                corr = numpy.corrcoef(dataframe[cols[i]],dataframe[cols[j]])
                #update the output string
                output=output+"The correlation between "+str(cols[i])+" and "+str(cols[j])+" is "+str(numpy.round(corr[0,1], 2))+".\n"

    print(output)

    
    

def normed_error(dataframe, column_name, L, p):
    '''predict the L-p norm error between predicted values and dataframe values
       Args:
            dataframe: the input dataframe for comparison
            column_name: the specific column for comparison
            L: list of predicted values
            p: L-p norm
    '''
    
    s=dataframe.shape
    if s[0]!=len(L): #input list and the dataframe should have the same length
        raise ValueError("input size doesn't match")
    sum=0
    for i in range(s[0]):
        sum=sum+abs(dataframe.iloc[i][column_name]-L[i])^p #iterate to get the total sum of error
    
    return sum^(1/p)

def linear_regression(basketball):
    '''
    Create and train a linear regression model to predict the "BARTHAG" attribute with the inputs "W","ADJOE", and "ADJDE". 
    Args:
        basketball: a dataframe containing all basketball teams for a given year. 
    Returns:
         lr: a trained linear regression model
    '''
    
    lr = LinearRegression()
    # structure the "basketball" data into X and y variable
    train_X = basketball[["W","ADJOE","ADJDE"]]
    train_y = basketball["BARTHAG"]
    lr.fit(train_X, train_y) # train the model
        
    return lr


def march_madness(basketball):
    '''
    Simulates a march madness tournament. Prints out winners of each (4) region and the overall winner.
    Extracts the team from each conference and the next top 32 teams given newIndex column. Runs a 64-team
    tournament (with some degree of randomness).
    Args:
        basketball: a basketball object containing all basketball teams for a given year. 
            Must include newIndex and conference columns.
    '''
    if not isinstance(basketball, pd.core.frame.DataFrame):
            raise TypeError("dataframe should be an instance of Python Dataframe")
    
    # get the top newIndex from each conference
    confNewIndex = basketball.groupby('CONF')['newIndex'].max()
    # add the teams that match the values found in confNewIndex
    autoQual = basketball.loc[basketball['newIndex'].isin(confNewIndex)]
    # add the next 32 highest teams not already qualified
    nonAutoQual = basketball[~basketball["TEAM"].isin(autoQual["TEAM"])][:32]
    # combine two lists sorted by newIndex
    tournTeams = pd.concat([autoQual, nonAutoQual]).sort_values(by='newIndex', ascending=False)

    # assign seeds
    west = basketball_team(tournTeams.iloc[::4].reset_index(drop = True))
    east = basketball_team(tournTeams.iloc[1::4].reset_index(drop = True))
    north = basketball_team(tournTeams.iloc[2::4].reset_index(drop = True))
    south = basketball_team(tournTeams.iloc[3::4].reset_index(drop = True))

    # simulate regional games
    northWinner = north.simulate_regional_games()
    southWinner = south.simulate_regional_games()
    eastWinner = east.simulate_regional_games()
    westWinner = west.simulate_regional_games()
    
    print(f'Final Four Teams: {northWinner["TEAM"]}, {southWinner["TEAM"]}, {eastWinner["TEAM"]}, {westWinner["TEAM"]}')
    
    # creates another basketball object with the four region winners
    finalFour = basketball_team(pd.concat([northWinner, southWinner, eastWinner, westWinner], axis=1).T)
    
    marchMadnessWinner = finalFour.play_final_four()
    
    print(f'\n\nThe winner of March Madness is:\n-------------------\n{marchMadnessWinner}!!!\n-------------------')
    
    
class basketball_team(pd.DataFrame):
    
    def obtain_average_team(self):
        '''obtain the data for an average team according to data
        '''
        d={}
        n=self.shape[1]
        for i in range(2,n): ## CHANGED FROM 3 to 2
            d[self.columns[i]]=self[self.columns[i]].mean()
        d["CONF"]="N/A"
        d["TEAM"]="avg_team"
        d["W"]=self["W"].mean() ####Changed FROM RK TO W
        return d
            
        
    def play_weighted_games(self, index1, index2):
        ''' plays a game using the score of two teams with random chance.
        Args:
            index1: the row index of team 1 in the basketball object (int)
            index2: the row index of team 2 in the basketball object (int)
        Returns:
            team1/team2: the basketball object (row) of the winning basketball team
        '''
        team1 = self.iloc[index1]
        team2 = self.iloc[index2]
        
        games_played = 100
        winning_indexes = random.choices([1, 0], weights=[team1["newIndex"], team2["newIndex"]], k=games_played)
        
        if sum(winning_indexes) > games_played/2:
            return team1
        else:
            return team2
        
    
    def simulate_regional_games(self):
        ''' Simulates a single region of a march madness tournament. Basketball object must
        be 16 teams (the amount of teams in a single region)
        Returns:
            simulation.iloc[0]: a basketball object that is one row (the winner of the region)
        '''
        if len(self)!=16:
            raise ValueError("Region must have 16 seeds")
        
        simulation = self
        num_of_games_per_round = [8, 4, 2, 1]
        
        # for number of games in the round
        for curr_round_games in num_of_games_per_round:
            # for the highest seed in the number of games this round
            for team1index in range(curr_round_games):
                # set the seed of the opposing team
                team2index = (curr_round_games*2-1) - team1index
                # simulate the game between two teams
                game_winner = simulation.play_weighted_games(team1index, team2index)
                
                # assign the winner as the higher seed and drop the losing team
                simulation.iloc[team1index] = game_winner
                simulation.drop(team2index, inplace=True)
                
        return simulation.iloc[0]
    
    
    def play_final_four(self):
        '''
        Simulates a final four tournament. Takes 4 teams (the winners of each region) and outputs
        a single overall winner. Basketball object must have only 4 teams.
        Returns:
            A string of the name of the team that won the final four
        '''
        if len(self)!=4:
            raise ValueError("Final Four must have 4 teams")
        
        simulation = basketball_team(self.reset_index(drop = True))
        
        simulation.iloc[0] = simulation.play_weighted_games(0, 1)
        simulation.iloc[1] = simulation.play_weighted_games(2, 3)
        
        winner = simulation.play_weighted_games(0, 1)
        
        return winner["TEAM"]
