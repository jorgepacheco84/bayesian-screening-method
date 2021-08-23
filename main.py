import downloadData as download
import trainStan as trainModel
import plotVaccineEfficacy as plt

def main():
    # download and preparation of data
    download.downloadData()

    # compile and training the model
    trainModel.train()

    # plot the graph
    plt.plot()


if __name__ == "__main__":
    main()