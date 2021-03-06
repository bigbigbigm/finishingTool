import os
import alignerRobot
import IORobot
import houseKeeper

# ## 0) Preprocess by removing embedded contigs (I: contigs.fasta ; O : noEmbed.fasta)



def removeEmbedded(folderName , mummerLink):
    print "removeEmbedded"
    
    thres = 10
    
    command= r'''perl -pe 's/>[^\$]*$/">Seg" . ++$n ."\n"/ge' ''' + folderName + "raw_reads.fasta > " + folderName  + houseKeeper.globalReadName
    os.system(command)

    command= r'''perl -pe 's/>[^\$]*$/">Seg" . ++$n ."\n"/ge' ''' + folderName + "contigs.fasta > " + folderName  + houseKeeper.globalContigName
    os.system(command)


    if True:
        alignerRobot.useMummerAlignBatch(mummerLink, folderName, [["self", houseKeeper.globalContigName, houseKeeper.globalContigName, ""]], houseKeeper.globalParallel)
        # alignerRobot.useMummerAlign(mummerLink, folderName, "self", "contigs.fasta", "contigs.fasta")
        # outputName, referenceName, queryName, specialName
    
    dataList = alignerRobot.extractMumData(folderName, "selfOut")
    
    dataList = alignerRobot.transformCoor(dataList)
    
    lenDic = IORobot.obtainLength(folderName, houseKeeper.globalContigName)
    
    removeList = []
    for eachitem in dataList:
        match1, match2, name1, name2 = eachitem[4], eachitem[5], eachitem[7], eachitem[8]
        
        if name1 != name2:
            l1, l2 = lenDic[name1], lenDic[name2]
            
            if abs(l1 - match1) < thres and abs(l2 - match2) > thres:
                removeList.append(name1)
            elif abs(l1 - match1) > thres and abs(l2 - match2) < thres:
                removeList.append(name2)
            elif abs(l1 - match1) < thres and abs(l2 - match2) < thres:
                print "Both shortembedd", eachitem
                
    
    
    nameList = []
    for eachitem in lenDic:
        nameList.append(eachitem)

    print len(nameList)
    
    for eachitem in removeList:
        if eachitem in nameList:
            nameList.remove(eachitem)
    print len(nameList)
    
    IORobot.putListToFileO(folderName, houseKeeper.globalContigName, "noEmbed", nameList)
    