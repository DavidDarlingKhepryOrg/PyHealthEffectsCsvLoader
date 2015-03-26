# -*- coding: utf-8 -*-

import codecs
import csv
import os
import sys
import time
import urllib.request

# specify the blended and sorted output file full path
blendedSortedOutFile = '/home/fracking/ChemicalToxicities/Chemical_Toxicities_Blended_Sorted.csv' 
blendedGroupedOutFile = '/home/fracking/ChemicalToxicities/Chemical_Toxicities_Blended_Grouped.csv'
blendedNumericOutFile = '/home/fracking/ChemicalToxicities/Chemical_Toxicities_Blended_Flattened_Numeric.csv' 
blendedBooleanOutFile = '/home/fracking/ChemicalToxicities/Chemical_Toxicities_Blended_Flattened_Boolean.csv' 

# maximum rows to read
# per URL to be processed
# 0 equivalent to 'unlimited' rows
maxRowsPerFile = 0

# number of seconds
# to sleep between
# URL fetches to prevent
# DoSing the source website
sleepInterval = 1
    
# define a list
# for the values
# to be sorted later
listOfValues = []

# build a list of URLs to be downloaded and processed

urls = []
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=recognized&all_p=t&full_hazard_name=Cancer")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=recognized&all_p=t&full_hazard_name=Developmental%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=recognized&all_p=t&full_hazard_name=Reproductive%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Cancer")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Cardiovascular%20or%20Blood%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Developmental%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Endocrine%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Gastrointestinal%20or%20Liver%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Immunotoxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Kidney%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Musculoskeletal%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Neurotoxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Reproductive%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Respiratory%20Toxicity")
urls.append("http://scorecard.goodguide.com/health-effects/chemicals.csv?which=suspected&all_p=t&full_hazard_name=Skin%20or%20Sense%20Organ%20Toxicity")

# build a dictionary of translations from the source
# files' values to what the database wants to utilize

xlations = {}
xlations['cancer'] = 'cancer'
xlations['developmental toxicity'] = 'developmental'
xlations['reproductive toxicity'] = 'reproductive'
xlations['cardiovascular or blood toxicity'] = 'cardiovascular blood'
xlations['developmental toxicity'] = 'developmental'
xlations['endocrine toxicity'] = 'endocrine'
xlations['gastrointestinal or liver toxicity'] = 'gastrointestinal liver'
xlations['immunotoxicity'] = 'immunotoxicity'
xlations['kidney toxicity'] = 'kidney'
xlations['musculoskeletal toxicity'] = 'musculoskeletal'
xlations['neurotoxicity'] = 'neurotoxicity'
xlations['reproductive toxicity'] = 'reproductive'
xlations['respiratory toxicity'] = 'respiratory'
xlations['skin or sense organ toxicity'] = 'skin sense'

# build a list of health effects in alphabetical order to be
# used when creating the flattened boolean and numeric output rows

listEffects = sorted(xlations.values())


def main():

    # obtain any command-line arguments
    # overriding any values set so far
    nextArg = ""
    for argv in sys.argv:
        if nextArg != "":
            if nextArg == "blendedSortedOutFile":
                blendedSortedOutFile = argv
            if nextArg == "maxRowsPerFile":
                maxRowsPerFile = int(argv)
            if nextArg == "sleepInterval":
                sleepInterval = int(argv)
            nextArg = ""
        else:
            if argv.lower() == "--blendedsortedoutfile":
                nextArg = "blendedSortedOutFile"
            if argv.lower() == "--maxrowsperfile":
                nextArg = "maxRowsPerFile"
            if argv.lower() == "--sleepinterval":
                nextArg = "sleepInterval"
                
    outputBlendedSortedFile()
    outputBlendedGroupedFile()
    outputBlendedFlattenedFiles()
    
    return


def outputBlendedSortedFile():
    
    # initialize the destination file's header row

    values = ['tox_cas_edf_id','tox_chemical_name','tox_references','tox_toxicity','tox_category']
    
    # open the destination file
    
    with open(blendedSortedOutFile,'w',newline='') as csvOutput:
        
        # instantiate the CSV writer with comma delimiters and minimal quoting using double-quotes
        
        csvWriter = csv.writer(csvOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        # output the destination
        # file's header row values
        csvWriter.writerow(values)
        values.clear()
    
        # url-by-url
        for url in urls:
            
            sys.stdout.write('Processing: ' + url + os.linesep)
        
            # derive the "category" and "toxicity" values
            category = url.split('?which=')[1].split('&')[0].lower()
            toxicity = urllib.parse.unquote(url).split('&full_hazard_name=')[1].lower()
            
            # translate the toxicity value
            # to one more suited for reporting
            try:
                toxicity = xlations[toxicity]
            except KeyError:
                toxicity = '*Toxicity [' + toxicity + '] translation not found*'
            
            # using the URL in question,
            # open an input stream for reading
            csvStream = urllib.request.urlopen(url)
            csvReader = csv.reader(codecs.iterdecode(csvStream, 'utf-8'))
    
            # initialize row counter
            rows = 0
            
            # line-by-line
            for line in csvReader:
                # if the line has
                # has the proper
                # number of items
                if len(line) == 3:
    
                    # increment row counter
                    rows += 1
                    
                    # if data row, i.e.,
                    # ignore the header row
                    if rows > 1:
                        
                        # build up the values list
                        values.append(line[1])
                        values.append(line[0])
                        values.append(line[2])
                        values.append(toxicity)
                        values.append(category)
                        
                        # append these values to the sorting list
                        # for later output to the destination file
                        listOfValues.append(values.copy())
                        
                        #clear the values list
                        values.clear()
                        
                        # output desired number
                        # of rows per input file
                        if maxRowsPerFile > 0 and rows > maxRowsPerFile:
                            break
    
            # close the input stream
            csvStream.close()
            
            # sleep for 5 seconds
            # to avoid DoSing the website
            time.sleep(sleepInterval)

        # output the rows now ordered
        # on the value of the CASRNs
        for row in sorted(listOfValues):
            csvWriter.writerow(row)        
        
    return

    
def outputBlendedGroupedFile():

    key = None
    name = None
    toxRecognized = []
    toxSuspected = []

    # initialize the destination file's header row

    values = ['tox_cas_edf_id','tox_chemical_name','tox_recognized','tox_suspected']
    
    # open the destination file
    
    with open(blendedGroupedOutFile,'w',newline='') as csvOutput:
        
        # instantiate the CSV writer with comma delimiters and minimal quoting using double-quotes
        
        csvWriter = csv.writer(csvOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        # output the destination
        # file's header row values
        csvWriter.writerow(values)
    
        # output the rows now ordered
        # on the value of the CASRNs
        for row in sorted(listOfValues):
            
            if key == None:
                key = row[0]
                name = row[1]
                
            if key != row[0]:
                csvWriter.writerow([key,name,','.join(sorted(toxRecognized)),','.join(sorted(toxSuspected))])
                key = row[0]
                name = row[1]
                toxRecognized.clear()
                toxSuspected.clear()
    
            if row[4] == 'recognized':
                toxRecognized.append(row[3])
            else:
                toxSuspected.append(row[3])

        csvWriter.writerow([key,name,','.join(sorted(toxRecognized)),','.join(sorted(toxSuspected))])
                
    return


def outputBlendedFlattenedFiles():

    key = None
    name = None
    toxRecognized = []
    toxSuspected = []

    # initialize the destination files' header row
    values = []
    booleanColNames = 'tox_cas_edf_id,tox_chemical_name,tox_category,tox_cancer,tox_cardiovascular_blood,tox_developmental,tox_endocrine,tox_gastrointestinal_liver,tox_immunotoxicity,tox_kidney,tox_musculoskeletal,tox_neurotoxicity,tox_reproductive,tox_respiratory,tox_skin_sense'    
    booleanColHeader = booleanColNames.split(',')
    numericColNames = 'tox_cas_edf_id,tox_chemical_name,tox_recognized,tox_recognized_cancer,tox_recognized_cardio_blood,tox_recognized_developmental,tox_recognized_endocrine,tox_recognized_gastro_liver,tox_recognized_immunotoxicity,tox_recognized_kidney,tox_recognized_musculoskeletal,tox_recognized_neurotoxicity,tox_recognized_reproductive,tox_recognized_respiratory,tox_recognized_skin_sense,tox_suspected,tox_suspected_cancer,tox_suspected_cardio_blood,tox_suspected_developmental,tox_suspected_endocrine,tox_suspected_gastro_liver,tox_suspected_immunotoxicity,tox_suspected_kidney,tox_suspected_musculoskeletal,tox_suspected_neurotoxicity,tox_suspected_reproductive,tox_suspected_respiratory,tox_suspected_skin_sense'    
    numericColHeader = numericColNames.split(',')
    
    # open the destination files
    
    csvBooleanFile = open(blendedBooleanOutFile,'w',newline='')
    csvNumericFile = open(blendedNumericOutFile,'w',newline='')
    
    csvBooleanWriter = csv.writer(csvBooleanFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvNumericWriter = csv.writer(csvNumericFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # output the destination
    # files' header row values
    csvBooleanWriter.writerow(booleanColHeader)
    csvNumericWriter.writerow(numericColHeader)
    
    # output the rows now ordered
    # on the value of the CASRNs
    for row in sorted(listOfValues):
        
        if key == None:
            key = row[0]
            name = row[1]
            
        if key != row[0]:

            booleanRecognizedEffects,numericRecognizedEffects,booleanRecognizedEffectsFound,numericRecognizedEffectsFound = getEffectsValues(toxRecognized)
            booleanSuspectedEffects,numericSuspectedEffects,booleanSuspectedEffectsFound,numericSuspectedEffectsFound = getEffectsValues(toxSuspected)
            
            if booleanRecognizedEffectsFound == 'true':
                values.clear()
                values = [key, name]
                values.append('recognized')
                values.extend(booleanRecognizedEffects)
                csvBooleanWriter.writerow(values)
            
            if booleanSuspectedEffectsFound == 'true':
                values.clear()
                values = [key, name]
                values.append('suspected')
                values.extend(booleanSuspectedEffects)
                csvBooleanWriter.writerow(values)

            values.clear()
            values = [key, name]
            values.append(numericRecognizedEffectsFound)
            values.extend(numericRecognizedEffects)
            values.append(numericSuspectedEffectsFound)
            values.extend(numericSuspectedEffects)
            csvNumericWriter.writerow(values)

            key = row[0]
            name = row[1]
            toxRecognized.clear()
            toxSuspected.clear()

        if row[4] == 'recognized':
            toxRecognized.append(row[3])
        else:
            toxSuspected.append(row[3])

    booleanRecognizedEffects,numericRecognizedEffects,booleanRecognizedEffectsFound,numericRecognizedEffectsFound = getEffectsValues(toxRecognized)
    booleanSuspectedEffects,numericSuspectedEffects,booleanSuspectedEffectsFound,numericSuspectedEffectsFound = getEffectsValues(toxSuspected)
    
    if booleanRecognizedEffectsFound == 'true':
        values.clear()
        values = [key, name]
        values.append('recognized')
        values.extend(booleanRecognizedEffects)
        csvBooleanWriter.writerow(values)
    
    if booleanSuspectedEffectsFound == 'true':
        values.clear()
        values = [key, name]
        values.append('suspected')
        values.extend(booleanSuspectedEffects)
        csvBooleanWriter.writerow(values)

    values.clear()
    values = [key, name]
    values.append(numericRecognizedEffectsFound)
    values.extend(numericRecognizedEffects)
    values.append(numericSuspectedEffectsFound)
    values.extend(numericSuspectedEffects)
    csvNumericWriter.writerow(values)
    
    # close the destination files
    csvBooleanFile.close()
    csvNumericFile.close()

    return
    

def getEffectsValues(effectsFound):
    
    booleanEffects = []
    numericEffects = []
    booleanEffectsFound = 'false'
    numericEffectsFound = '0'
    
    for effect in listEffects:
        if effect in effectsFound:
            booleanEffects.append('true')
            numericEffects.append('1')
            booleanEffectsFound = 'true'
            numericEffectsFound = '1'
        else:
            booleanEffects.append('false')
            numericEffects.append('0')

    return booleanEffects, numericEffects, booleanEffectsFound, numericEffectsFound


# -------------------------------------------------------------------------
# execute the "main" method
# -------------------------------------------------------------------------

if __name__ == "__main__":
    main()
