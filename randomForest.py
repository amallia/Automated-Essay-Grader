import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor


class randomForestRegression(object):
    """Use random forest regression model to train the data and make predictions on the validation data"""
    
    def __init__(self, trainingFileName, validationFileName, validationScoreFileName):
       self.trainingFileName = trainingFileName
       self.validationFileName = validationFileName
       self.validationScoreFileName = validationScoreFileName


    def readTrainingValidationData(self):
        """Read training data and validation data from files"""
        try:
            trainingData = pd.read_csv(self.trainingFileName)
        except Exception, e:
            print "Cannot open the training data due to the exception:", e
            raise e

        try:
            validationData = pd.read_csv(self.validationFileName)
        except Exception, e:
            print "Cannot open the validation data due to the exception:", e
            raise e

        return trainingData, validationData


    def readVaidationScores(self, essaySetNumber):
        """Read validation scores from file"""
        
        try:
            score = open(self.validationScoreFileName, "rb")
            scoreData = pickle.load(score)
        except Exception, e:
            print "Cannot open the validation scores data due tp the exception:", e
            raise e
        return scoreData[essaySetNumber-1]


    def randomForestRegressionModel(self, essaySetNumber):
        """Train the random forest model using the training data"""
        trainingData, validationData = self.readTrainingValidationData()
        validationScore = self.readVaidationScores(essaySetNumber)
        trainingScore = trainingData["score"]
        trainingData = trainingData.drop("score", 1)
       
        # train model
        clf = RandomForestRegressor()
        clf = clf.fit(trainingData, trainingScore)
       
        # make predictions
        predictScores = clf.predict(validationData)
        predictScores = map(round, predictScores)
        
        return predictScores


if __name__ == '__main__':
    rf = randomForestRegression("essaySet1.csv", "validEssaySet1.csv", "validationScores.pkl")
    print rf.randomForestRegressionModel(1)
