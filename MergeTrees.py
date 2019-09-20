#!/usr/bin/env python
# coding: utf-8

import ROOT
import os


    
def MergeROOTFiles(files):
    guideFile = files[0]
    
    if type(guideFile) in (ROOT.TDirectoryFile, ROOT.TFile):
        if type(guideFile) == ROOT.TDirectoryFile:
            mergedDirectory = ROOT.TDirectoryFile(guideFile.GetName(), guideFile.GetName())
        else:
            mergedDirectory = ROOT.TFile(outputFileName, "RECREATE")
        
        mergedDirectory.cd()
        keys = guideFile.GetListOfKeys()
        
        for key in keys:
            name = key.GetName()
            subFiles = [file.Get(name) for file in files]
            mergedSubFile = MergeROOTFiles(subFiles)
            
            # MergedROOTFiles will return None if it encounters a file type it has not
            # been designed to handle
            if mergedSubFile:
                # Incase the sub file is itself a directory which has been cd'd to
                mergedDirectory.cd()
                mergedSubFile.Write()
        
        return mergedDirectory

        
    elif type(guideFile) == ROOT.TTree:
        treeList = ROOT.TList()
        for file in files:
            treeList.Add(file)
        mergedTree = ROOT.TTree.MergeTrees(treeList)
        return mergedTree
    
    
    elif type(guideFile) in (ROOT.TH1F, ROOT.TH2F, ROOT.TH1D, ROOT.TH2D):
        histoList = ROOT.TList()
        sumHisto = guideFile
        
        xMin = sumHisto.GetXaxis().GetXmin()
        xMax = sumHisto.GetXaxis().GetXmax()
        
        # Excludes guide file to avoid double counting
        for histo in files[1:]:
            # Slightly hacky. Technically loses data, since bins are not neccesarily alligned, but
            # in practice the limits are very close anyway, so its good enough for a rough analysis.
            histo.GetXaxis().SetLimits(xMin, xMax)
            histoList.Add(histo)
        
        sumHisto.Merge(histoList)
        
        if "Pull" in guideFile.GetName():
            sumHisto.Fit("gaus")
        
        return sumHisto
        

        
# Returns the number of files are available for merging
def GetNumOfFiles(runDirect):
    foundFile = True
    i = 0
    
    while foundFile:
        filePath = f"{runDirect}/run{i}/histograms.root"
        if os.path.exists(filePath):
            i+=1
        else:
            foundFile = False
    
    return i
        


runDirect = "TopRuns"
outputFileName = "Merged.root"
    
numberOfFiles = GetNumOfFiles(runDirect)
            
files = []
for i in range(numberOfFiles):
    filePath = f"{runDirect}/run{i}/histograms.root"
    file = ROOT.TFile(filePath)
    files.append(file)

mergedFile = MergeROOTFiles(files)
mergedFile.Write()
keys = mergedFile.GetListOfKeys()
names = [key.GetName() for key in keys]
mergedFile.Close()



