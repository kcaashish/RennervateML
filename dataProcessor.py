import csv

# from statistics import median


def save_ear(ear_list, mar_list, filename, person):
    # if not os.path.exists(f"{filename}.csv"):
    #     with open(f"{filename}.csv", mode="w") as train_file:
    #         file_write = csv.writer(
    #             train_file, delimiter=",", quoting=csv.QUOTE_MINIMAL
    #         )
    #         file_write.writerow(ear_list)
    #         file_write.writerow(mar_list)
    # else:
    with open(
        f"{filename}_mear_PA{person}.csv", mode="a"
    ) as file:  # change P3 in the file name with PA1, PA2 and so on for different person's video
        file_write = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        file_write.writerow(ear_list)
        file_write.writerow(mar_list)

    # with open(f"{filename}_mar.csv", mode="a") as file:
    #     file_write = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    #     file_write.writerow(mar_list)


def processingCSV(filename):
    cleanedMAR = []
    cleanedEAR = []

    if filename == "Drowsy":
        status = 1
    else:
        status = 0

    with open(f"{filename}_mear.csv", mode="r") as file:
        csv_read = csv.reader(file, delimiter=",")
        count = 0

        for row in csv_read:
            # print(count)
            if row != []:
                mearList = []

                for item in row:
                    mearList.append(float(item))
                # print(mearList)

                # if count % 2 == 0:
                #     medMEar.append(status)
                #     # print(medMEar)
                #     finalCSV(filename, medMEar)
                #     medMEar.clear()

                # taking min/max value from 5 data
                for x in range(0, len(mearList) + 1, 5):
                    if len(mearList) - x >= 5:
                        minimum = round(
                            min(
                                mearList[x],
                                mearList[x + 1],
                                mearList[x + 2],
                                mearList[x + 3],
                                mearList[x + 4],
                            ),
                            2,
                        )
                        maximum = round(
                            max(
                                mearList[x],
                                mearList[x + 1],
                                mearList[x + 2],
                                mearList[x + 3],
                                mearList[x + 4],
                            ),
                            2,
                        )

                        if status == 1 and count % 2 == 0:
                            cleanedEAR.append(minimum)
                        elif status == 0 and count % 2 == 1:
                            cleanedMAR.append(minimum)
                        elif status == 1 and count % 2 == 1:
                            cleanedMAR.append(maximum)
                        elif status == 0 and count % 2 == 0:
                            cleanedEAR.append(maximum)

                count += 1
                mearList.clear()

                if count % 2 == 0:
                    print(cleanedEAR)
                    print(cleanedMAR)
                    cleanCSV(filename, cleanedEAR, cleanedMAR)
                    cleanedEAR.clear()
                    cleanedMAR.clear()


def cleanCSV(filename, cleanedEAR, cleanedMAR):
    with open(f"{filename}_mear_cleaned.csv", mode="a") as file:
        file_write = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        file_write.writerow(cleanedEAR)
        file_write.writerow(cleanedMAR)


def main():
    processingCSV("Drowsy")
    processingCSV("NotDrowsy")


if __name__ == "__main__":
    main()
