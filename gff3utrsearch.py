import pandas as pd
import os

shellFile = '/Users/simonray/Dropbox/dropData/ensembl/extractSeq.sh'
sequenceFile = '/Users/simonray/Dropbox/dropData/ensembl/extractSeq.fa'
missing3UTRFile = '/Users/simonray/Dropbox/dropData/ensembl/missing3UTRs.txt'
fwSh = open(shellFile, "a+")
fwMs = open(missing3UTRFile, "a+")
dfGFFAll=pd.read_csv('/Users/simonray/Dropbox/dropData/ensembl/Homo_sapiens.GRCh38.102.chr.gff3', sep='\t', skiprows=33)
dfGFFAll.columns = ['chr', 'source', 'type', 'start', 'stop', 'score', 'strand', 'unk', 'attrib']

dfGenes = dfGFFAll[dfGFFAll['type']=='gene']


ensg=pd.DataFrame(pd.DataFrame(dfGenes.attrib.str.split(";", expand=True,)[0]).iloc[:,0].str.split(":", expand=True,)[1]).iloc[:,0].unique()
#ensg=['ENSG00000221983']
dfENSG=pd.DataFrame(ensg)

dfGFF3pUTRs=dfGFFAll[dfGFFAll['type']=='three_prime_UTR']
dfGFF3pUTRs.columns = ['chr', 'source', 'type', 'start', 'stop', 'score', 'strand', 'unk', 'attrib']
#dfENSGHits = dfGFFAll[(dfGFFAll['attrib'].str.contains('ENSG00000078808', na=False)) & (dfGFFAll['type']=='mRNA')]
for indexG, row in dfENSG.iterrows():
    #if indexG%100 == 0:
    #	print (indexG)

    ensgID = row.loc[0]
    df3UTR4Gene = pd.DataFrame(columns = ['chr', 'source', 'type', 'start', 'stop', 'score', 'strand', 'unk', 'attrib'])
    #df3UTR4Gene.columns = ['chr', 'source', 'type', 'start', 'stop', 'score', 'strand', 'unk', 'attrib']
    print("searching for mRNA transcripts for <" + str(indexG) + ":" + ensgID + ">" )

    dfENSGHits = dfGFFAll[(dfGFFAll['attrib'].str.contains(ensgID, na=False)) & (dfGFFAll['type']=='mRNA')]
    #print("-- found " + str(len(dfENSGHits)) + " hits")

    for indexT, ensgHit in dfENSGHits.iterrows():
        #ensgstr=pd.DataFrame(ensgHit['attrib'].str.split(";", expand=True,)[1]).iloc[:,0].to_string(index=False)
        enstID = ensgHit['attrib'].split(";")[0].split(":")[1]
        #print("----search for " + enstID + " in 3'UTR list")
        df3UTRHits = dfGFF3pUTRs[dfGFF3pUTRs['attrib'].str.contains(enstID, na=False)]
        #print("----found " + str(len(df3UTRHits)) + " hits" )
        df3UTR4Gene = df3UTR4Gene.append(df3UTRHits)


    print("----found a total of <" + str(len(df3UTR4Gene)) + "> 3'UTR transcripts")
    if len(df3UTR4Gene) == 0:
    	fwMs.write(ensgID + os.linesep)
    else:


	    leng = df3UTR4Gene['stop'].astype(float) - df3UTR4Gene['start'].astype(float)

	    df3UTR4Gene['length']=leng
	    #df3UTR4Gene.to_csv('/Users/simonray/Dropbox/dropData/ensembl/df3UTR4Gene.csv')
	    #print(df3UTR4Gene)
	    #print("+++++1")
	    #print(df3UTR4Gene.index.values.tolist())
	    #print("+++++2")
	    #for indexE, entry in  df3UTR4Gene.iterrows():
	    #	print(indexE, entry['attrib'])

	    #print("+++++3")
	    #print(df3UTR4Gene.loc[[1484413]])
	    #print("+++++4")
	    max_index = df3UTR4Gene['length'].idxmax()
	    #print(max_index)
	        #print(df3UTR4Gene.iloc[df3UTR4Gene['length'].idxmax()])
	    #print("+++++5")

	    max_row = df3UTR4Gene.loc[[max_index]]

	    refFAFile = '/Users/simonray/Dropbox/dropData/1KGenomes/reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa.gz'
	    #print('chr:' + max_row['chr'])
	    chrom = max_row['chr'].astype(int).to_string(index=False)

	    start = max_row['start'].astype(int).to_string(index=False)
	    stop = max_row['stop'].astype(int).to_string(index=False)
	    strand = max_row['strand'].to_string(index=False)

	    #print('stop:' + str(max_row['stop']))
	    #print('strand:' + max_row['strand'])

	    samtoolsCmd = 'samtools faidx ' + refFAFile +  ' chr' + chrom + ':'+ start + '-' + stop
	    if strand == '-':
	    	samtoolsCmd = samtoolsCmd + " -i"

	    samtoolsCmd = samtoolsCmd + " >> " + sequenceFile

	    #print(samtoolsCmd)
	    fwSh.write(samtoolsCmd + os.linesep)
	    #for indexE, entry in  df3UTR4Gene.iterrows():
	    #	enstID = entry['attrib'].split(";")[0].split(":")[1] + \
	    #		str(entry['start']) + "-" + str(entry['stop'])
	    #	print("------>" + enstID + "::" + str(entry['start']) + "-->" + str(entry['stop']) + "=" + str(entry['length']))


    #if indexG == 3:
    #    break


#samtools faidx refgenome.fa.gz chr19:3777973-3778182 (-i for reverse strand) if the fa file has been bgzip-ped


