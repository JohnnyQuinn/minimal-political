# minimalpolitical.com

For the average American, their greatest impact they can have in politics is being an informed citizen and voting. In order to keep those in power accountable, we have to know what actions they take. For example, how they vote on bills. But getting access to voting records of particular politicians can be very mentally tasking and more stressful than it needs to be. **Minimal Political will empower average voters by offering effortless access to voting records of US lawmakers by presenting it in a simple, easily digestible way.** 

## Usage

![Demo Gif](minimal_political_demo_screen_cap.gif)

Search for any lawmakers in Congress that are currently in office and get their votes on the most recent votes in their respective chambers. 

## Road Map

### MVP:
* Be able to search through **all** the bills that the searched lawmaker has voted on
* Be able to click on the bills and display more information
* Update styling (colors, fonts, overall layout)
* display data on the lawmaker and the bills they voted on with simple visual data representation (graphs)

### Long Term:
* filter results of voting histories
* offer more access to data on Congress overall (senate's votes as a whole, etc)
* More data visualizations
* timelines (voting history, financial actions, etc)
* search for a particular bill 
* compare lawmakers/bills

## How it will be built
Using [ProPublica's Congress API](https://projects.propublica.org/api-docs/congress-api/), there is an abundance of data on Congress available. Right now all the data is being called and retrieved in the JS file. The data is stored in an array which can be easily navigated through. Using and displaying the data will continue to be done using the arrays from the API. In the near future, the data will be retrieved in the backend instead of in JS. 
