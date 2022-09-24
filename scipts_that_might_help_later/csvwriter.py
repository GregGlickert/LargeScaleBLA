import csv

def tone(tstart):
     with open('inputs/tone_spikes.csv', 'a', newline='') as f1:
        writer = csv.writer(f1)
        
        for i in range(0, 505, 50):
            writer.writerow([ str(tstart + i) + " 'tone' 0"])
        
def shock(tstart):
     with open('inputs/shock_spikes.csv', 'a', newline='') as f2:
        writer = csv.writer(f2)
        
        for i in range(0, 105, 5):
            writer.writerow([str(tstart + i) + " 'shock' 0"])
        
def toneANDshock(tstart):
    tshock = tstart + 400
    
    tone(tstart)
    shock(tshock)
    
def main():
    
    time = 500 #in milliseconds
    #Background Phase --- Just Poisson
    
    #Sensitizaiton Phase
    for i in range(0,15):
        tone(time)
        shock(time + 1750) #shock occurs in pause between tones
        time = time + 1500 #3500 ms between each tone (4000 including 500 ms tone duration)
    
    print(time)
    
    #Conditioning Phase
    time = time + 0 #conditioning occurs 0 second after sensitization
    for i in range(0,10):
        toneANDshock(time)
        time = time + 4000
        
    #Extinction Phase 1
    time = time + 36000 #extinction phase 1 occurs 40 seconds after conditioning (3.5 seconds accounted for above)
    for i in range(0,30):
        tone(time)
        time = time + 4000
    
    #Extinction Phase 2
    time = time + 836000 #extinction phase 2 occurs 840 seconds after conditioning (3.5 seconds accounted for above)
    for i in range(0,30):
        tone(time)
        time = time + 4000
    
    print(time)
    
    
    
if __name__=="__main__":
    main()
