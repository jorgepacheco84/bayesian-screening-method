import downloadData as download
import trainStan as trainModel
import plotVaccineEfficacy as plt

def main():
    # download and preparation of data
    download.downloadData()

    # compile and training the model
    #trainModel.train()

    # plot the graph by split variable
    plt.plot('epidemiologicalWeek')
    plt.plot('ageGroup')


if __name__ == "__main__":
    main()