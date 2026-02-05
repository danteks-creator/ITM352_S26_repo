url = input("enter a full url:   ")

closed_url = url.replace("https://", "")

print("closed url: ", closed_url)

parts = closed_url.split(",")

domain = parts[1]
print("domain: ", domain)

#we might get a trailing/character, so we need to remove it. 
TLD = parts[2]
TLD_clean = TLD.strip("/")
print("top level domain: ", TLD_clean)
