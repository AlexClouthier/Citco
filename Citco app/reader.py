import csv
from scholarly import scholarly

if __name__ == "__main__":
    awardees=set()
    done=set()
    with open('NSERC_Awards/NSERC_Results_CS.csv', newline='') as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            awardees.add(f"{row['Awards List']}")
    
    print(len(awardees))
    file=open("citationCount.csv", "w")
    file.write("Name,Citations,\n")
    count=0
    for people in awardees:
        count+=1
        if count%100==0:
            print(f"Through {count}")
        search=scholarly.search_author(people)
        auth=next(search, None)
        if auth is not None:
            author=scholarly.fill(auth)
            citations=author.get('citedby',0)
            file.write(f"\"{people}\", {citations}\n")
    file.close()