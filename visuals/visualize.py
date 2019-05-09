import json
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint as pprint
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

SENSE_SCORE_THRESHOLD = 3.55


def readData(fileName):
    """
    TweetID	Tweets	Normalised Valence	Normalised Strength	 Valence	Strength Sense-Score
    """
    allJsonData = []
    with open("{}.json".format(fileName), "r") as jsonFile:
        allJsonData = json.load(jsonFile)
    return allJsonData


def cleanData(jsonData):
    finalData = {}
    for data in jsonData:
        if data["Sense-Score"] < SENSE_SCORE_THRESHOLD or data["TweetID"] == "6":
            continue
        else:
            finalData[data["TweetID"]] = data
    return finalData


def getTweetValenceAndStrength(jsonData):
    """
    This function returns the normalised valence and strength of the data.
    """
    listOfValence = []
    listOfStrength = []
    for ind in jsonData.keys():
        data = jsonData[ind]
        tweetId = data["TweetID"]
        strength = data["Normalised Strength"]
        valence = data["Normalised Valence"]
        listOfValence.append(valence)
        listOfStrength.append(strength)
        # print(
        #     "tweetID: {0}, index:{1}, tweet:{2} valence:{3}, str:{4}".format(
        #         tweetId, ind, data["Tweets"], valence, strength
        #     )
        # )
    return listOfValence, listOfStrength


def getDifference(ogDataAll, bestDataAll, worstDataAll, fromNormalised=True):
    """
    Get the og data, find the corresponding data for higher and lower
    Therefore having the relative difference in the data
    Now we can plot the relative difference rather than the absolute values.
    """
    positiveShiftsInValence = []
    positiveShiftsInStrength = []
    negativeShiftsInValence = []
    negativeShiftsInStrength = []

    ExtractValence = "Normalised Valence" if fromNormalised else "Valence"
    ExtractStrength = "Normalised Strength" if fromNormalised else "Strength"

    for val in ogDataAll.keys():
        ogData = ogDataAll[val]
        bestData = bestDataAll[val]
        worstData = worstDataAll[val]

        ogValence = ogData[ExtractValence]
        bestValence = bestData[ExtractValence]
        worstValence = worstData[ExtractValence]

        pos_val = bestValence - ogValence
        neg_val = ogValence - worstValence

        ogStrength = ogData[ExtractStrength]
        bestStrength = bestData[ExtractStrength]
        worstStrength = worstData[ExtractStrength]

        pos_str = bestStrength - ogStrength
        neg_str = ogStrength - worstStrength

        if pos_val == 0 or neg_val == 0 or pos_str == 0 or neg_str == 0:
            print("0 found, at {}".format(val))

        positiveShiftsInStrength.append(pos_str)
        negativeShiftsInStrength.append(neg_str)

        positiveShiftsInValence.append(pos_val)
        negativeShiftsInValence.append(neg_val)
        # print(
        #     "id:{0}\npositiveValence:{1}\nnegativeValence:{2}\npositiveStrength:{3}\nnegativeStrength:{4}\n".format(
        #         val, pos_val, neg_val, pos_str, neg_str
        #     )
        # )

    dictOfChanges = {}
    dictOfChanges["positive_valence"] = positiveShiftsInValence
    dictOfChanges["negative_valence"] = negativeShiftsInValence
    dictOfChanges["positive_strength"] = positiveShiftsInStrength
    dictOfChanges["negative_strength"] = negativeShiftsInStrength
    return dictOfChanges


def display2DAbsolute(ogTweets, bestTweets, worstTweets):
    ogVal, ogStr = getTweetValenceAndStrength(ogTweets)
    bestVal, bestStr = getTweetValenceAndStrength(bestTweets)
    worstVal, worstStr = getTweetValenceAndStrength(worstTweets)

    rangeOfValenceValues = np.arange(-2.2, +2.5, 0.5)
    rangeOfStrengthValues = rangeOfValenceValues[:]
    rangeOfLabels = sorted(ogTweets.keys())

    sizeVal = 15
    plt.figure(1)
    plt.scatter(ogVal, ogStr, label="original", color="blue", s=sizeVal, marker="o")
    plt.scatter(bestVal, bestStr, label="best", color="green", s=sizeVal, marker="x")
    plt.scatter(worstVal, worstStr, label="worst", color="red", s=sizeVal, marker="s")

    for i, txt in enumerate(rangeOfLabels):
        plt.annotate("{0}".format(txt), (ogVal[i], ogStr[i]))
        plt.annotate("{0}".format(txt), (bestVal[i], bestStr[i]))
        plt.annotate("{0}".format(txt), (worstVal[i], worstStr[i]))
        plt.plot([], [], " ", label="{0} = Sentence {0}".format(txt))
    plt.hlines(0.0, -2.0, 2.0, linestyles="dashed")
    plt.vlines(0.0, -2.0, 2.0, linestyles="dashed")
    plt.xticks(rangeOfValenceValues)
    plt.yticks(rangeOfStrengthValues)
    plt.ylabel("Strength/Arousal")
    plt.xlabel("Happines-Sadness/Valence")
    plt.title("Absolute values of the Valence/Arousal scale")
    plt.legend()
    plt.show()


def display2DRelative(
    positive_valence, negative_valence, positive_strength, negative_strength
):
    rangeOfValenceValues = np.arange(-2.2, +2.5, 0.5)
    rangeOfStrengthValues = rangeOfValenceValues[:]
    rangeOfLabels = sorted(ogTweets.keys())  # list(range(1, 13))

    sizeVal = 15
    plt.figure(1)
    plt.scatter(
        positive_valence,
        positive_strength,
        label="PositiveMeasure",
        color="blue",
        s=sizeVal,
    )

    plt.scatter(
        negative_valence,
        negative_strength,
        label="NegativeMeasure",
        color="green",
        s=sizeVal,
    )

    for i, txt in enumerate(rangeOfLabels):
        plt.annotate(txt, (positive_valence[i], positive_strength[i]))
        plt.annotate(txt, (negative_valence[i], negative_strength[i]))

    plt.hlines(0.0, -2.5, 2.5, linestyles="dashed")
    plt.vlines(0.0, -2.5, 2.5, linestyles="dashed")
    plt.xticks(rangeOfValenceValues)
    plt.yticks(rangeOfStrengthValues)
    plt.title("RELATIVE differences plotted!")
    plt.ylabel("Arousal / Strength")
    plt.xlabel("Valence")
    plt.legend()
    plt.show()

    return


def plotLinearRegressionAtDifferences(ogData, bestData, worstData):
    diff = getDifference(ogData, bestData, worstData)

    xs_pos = diff["positive_valence"]
    ys_pos = diff["positive_strength"]
    xs_neg = diff["negative_valence"]
    ys_neg = diff["negative_strength"]

    rangeOfLabels = range(0, len(ogData.keys()))

    slope_pos, intercept_pos, r_value_pos, p_value_pos, std_err_pos = stats.linregress(
        xs_pos, ys_pos
    )
    ys_posForLine = [intercept_pos + (slope_pos * val) for val in xs_pos]
    plt.scatter(xs_pos, ys_pos, color="blue", label="Positive Shift", marker="o")
    plt.plot(
        xs_pos, ys_posForLine, "r", label="positiveLine", color="blue", linewidth=1.0
    )

    slope_neg, intercept_neg, r_value_neg, p_value_neg, std_err_neg = stats.linregress(
        xs_neg, ys_neg
    )
    ys_negForLine = [intercept_neg + (slope_neg * val) for val in xs_neg]
    plt.scatter(xs_neg, ys_neg, color="red", label="Negative Shift", marker="x")
    plt.plot(
        xs_neg, ys_negForLine, "r", label="negativeLine", color="red", linewidth=1.0
    )

    for i, txt in enumerate(rangeOfLabels):
        plt.annotate(txt, (xs_pos[i], ys_pos[i]))
        plt.annotate(txt, (xs_neg[i], ys_neg[i]))

    plt.hlines(0.0, -2.0, 2.0, linestyles="dashed")
    plt.vlines(0.0, -2.0, 2.0, linestyles="dashed")
    plt.title("Trends in Differences Plotted")
    plt.xlabel("Valence")
    plt.ylabel("Arousal or Strength")
    plt.legend()
    plt.show()

    return


def plotLinearRegressionLines(ogData, bestData, worstData):

    ogVal, ogStr = getTweetValenceAndStrength(ogData)
    bestVal, bestStr = getTweetValenceAndStrength(bestData)
    worstVal, worstStr = getTweetValenceAndStrength(worstData)

    ysForOg = linearRegressionLines(ogData)
    ysForBest = linearRegressionLines(bestData)
    ysForWorst = linearRegressionLines(worstData)

    lineWidth = 1.0
    plt.scatter(ogVal, ogStr, color="blue", label="originalSentences")
    plt.plot(
        ogVal, ysForOg, "r", label="originalLine", color="blue", linewidth=lineWidth
    )

    plt.scatter(bestVal, bestStr, color="green", label="best sentences")
    plt.plot(
        bestVal, ysForBest, "r", label="best_Line", color="green", linewidth=lineWidth
    )

    plt.scatter(worstVal, worstStr, color="red", label="worst sentences")
    plt.plot(
        worstVal, ysForWorst, "r", label="worst_Line", color="red", linewidth=lineWidth
    )

    plt.hlines(0.0, -2.5, 2.5, linestyles="dashed")
    plt.vlines(0.0, -2.5, 2.5, linestyles="dashed")
    plt.title("Linear Regression Lines")
    plt.xlabel("Valence")
    plt.ylabel("Arousal/Strength")
    plt.legend()
    plt.show()


def linearRegressionLines(data):
    val, strength = getTweetValenceAndStrength(data)

    slope, intercept, r_value, p_value, std_err = stats.linregress(val, strength)
    ysForLine = [intercept + (slope * val) for val in val]

    return ysForLine


def displayOnlyStrength(ogData, bestData, worstData):
    _, originalStrength = getTweetValenceAndStrength(ogData)
    _, bestStr = getTweetValenceAndStrength(bestData)
    _, worstStr = getTweetValenceAndStrength(worstData)
    zerosList = [0] * len(ogData.keys())

    for i in range(0, len(zerosList)):
        plt.scatter(originalStrength[i], [i], color="blue", marker="o")
        plt.scatter(bestStr[i], [i], color="green", marker="x")
        plt.scatter(worstStr[i], [i], color="red", marker="s")
    for i, txt in enumerate(range(0, len(ogData.keys()))):
        plt.annotate(txt, (originalStrength[i], i))
        plt.annotate(txt, (bestStr[i], i))
        plt.annotate(txt, (worstStr[i], i))
    plt.plot([], [], label="Original Sentence", marker="o", color="blue")
    plt.plot([], [], label="Best Sentence", marker="x", color="green")
    plt.plot([], [], label="Worst Sentence", marker="s", color="red")
    plt.hlines(4.0, -2.5, 2.5, linestyles="dashed")
    plt.xlabel("Strength")
    plt.title("Only Strength")
    plt.ylabel("Sentences groups")
    plt.legend()
    plt.show()

    return


def displayOnlyValence(ogData, bestData, worstData):
    originalValence, _ = getTweetValenceAndStrength(ogData)
    bestVal, _ = getTweetValenceAndStrength(bestData)
    worstVal, _ = getTweetValenceAndStrength(worstData)
    zerosList = [0] * len(ogData.keys())

    for i in range(0, len(zerosList)):
        plt.scatter(originalValence[i], [i], color="blue", marker="o")
        plt.scatter(bestVal[i], [i], color="green", marker="x")
        plt.scatter(worstVal[i], [i], color="red", marker="s")

    for i, txt in enumerate(range(0, len(ogData.keys()))):
        plt.annotate(txt, (originalValence[i], i))
        plt.annotate(txt, (bestVal[i], i))
        plt.annotate(txt, (worstVal[i], i))
    plt.plot([], [], label="Original Sentence", marker="o", color="blue")
    plt.plot([], [], label="Best Sentence", marker="x", color="green")
    plt.plot([], [], label="Worst Sentence", marker="s", color="red")
    plt.hlines(4.0, -2.5, 2.5, linestyles="dashed")
    plt.xlabel("Valence")
    plt.title("Only valence displayed")
    plt.ylabel("Different Sentence Groups")
    plt.legend()
    plt.show()

    return


ogTweets = cleanData(readData("originalTweets"))
bestTweets = cleanData(readData("bestTweets"))
worstTweets = cleanData(readData("worstTweets"))


# display2DAbsolute(ogTweets, bestTweets, worstTweets)

diff = getDifference(ogTweets, bestTweets, worstTweets)
# display2DRelative(
#     diff["positive_valence"],
#     diff["negative_valence"],
#     diff["positive_strength"],
#     diff["negative_strength"],
# )


# displayOnlyValence(ogTweets, bestTweets, worstTweets)
# displayOnlyStrength(ogTweets, bestTweets, worstTweets)

# plotLinearRegressionLines(ogTweets, bestTweets, worstTweets)
plotLinearRegressionAtDifferences(ogTweets, bestTweets, worstTweets)
