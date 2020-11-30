# import libraries
import requests
from bs4 import BeautifulSoup


def main():
    homeURL = 'https://geographic.org/streetview/germany/'
    homePage = requests.get(homeURL)
    homeSoup = BeautifulSoup(homePage.content, 'html.parser')
    mainList = homeSoup.select("div.listmain li a")
    file = open('streets.txt', 'a')
    for item in mainList:
        cityURL = homeURL + str(item['href'])
        cityPage = requests.get(cityURL)
        citySoup = BeautifulSoup(cityPage.content, 'html.parser')
        print(cityURL)
        centerFont = citySoup.select('div.table > center strong')
        centerFont = centerFont[0].get_text()

        isStreets = 'List of streets in'
        if isStreets in centerFont:  # some pages have streets immediately
            print("Street List Found at: " + cityURL)
            streetList = citySoup.select('div.listmain li')
            for street in streetList:
                streetText = street.get_text()
                file.write(streetText + '\n')

        else:
            cityList = citySoup.select('div.listmain li a')

            for city in cityList:
                distURL = cityURL.rstrip('index.html') + city['href']
                distPage = requests.get(distURL)
                distSoup = BeautifulSoup(distPage.content, 'html.parser')

                centerFont = distSoup.select('div.table > center strong')
                centerFont = centerFont[0].get_text()

                isStreets = 'List of streets in'
                if isStreets in centerFont:  # some pages have streets immediately
                    print("Street List Found at: " + distURL)
                    streetList = distSoup.select('div.listmain li')

                    for street in streetList:
                        streetText = street.get_text()
                        file.write(streetText + '\n')

                else:   # some require another iteration
                    localities = distSoup.select('div.listmain li a')
                    for local in localities:
                        localURL = distURL.rstrip('index.html') + local['href']
                        localPage = requests.get(localURL)
                        localSoup = BeautifulSoup(
                            localPage.content, 'html.parser')

                        print("Street List Found at: " + localURL)
                        streetList = localSoup.select('div.listmain li')
                        for street in streetList:
                            streetText = street.get_text()
                            file.write(streetText + '\n')
            exit()
    file.close()


if __name__ == "__main__":
    main()
