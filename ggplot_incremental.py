        snvPlotFile = os.path.join(resultFolder, basename + "__"+ self.md5string + ".png")
        snvPlotTitle = basename 
        dfPlot = dfSNV.loc[:, ['nt']]
        dfT1 = dfSNV.filter(regex=("^snvplot"))
        print(dfT1.iloc[1])

        dfPlot=dfPlot.join(dfSNV.filter(regex=("^snvplot")).astype(int))
        
        #with open(plotFileAsCSV, "w") as csvPlotFile:
            
        #if len(cmds) > 0:
        #    with open(shellFile, 'w') as shfile:
        #        for cmd in cmds:
        #            print(cmd, file=shfile)       
        
        print(list(dfPlot.columns))
        
        logging.info(INDENT*'-' + "--plotting")
        p = (p9.ggplot(data=dfPlot) + p9.labs(title=self.projectID) + p9.xlab(self.XVAR) + p9.xlab(self.YVAR))       
        bamFile=1
        for inputFile in self.inputFiles:
            p = p + p9.geom_point(data=dfPlot, 
                                mapping=p9.aes(list(dfPlot.columns)[0], list(dfPlot.columns)[bamFile]),
                                alpha=0.1, size=0.25) + p9.scale_color_gradient(low="blue", high="red")
            bamFile+=1
            pass

        p.save(filename = snvPlotFile, height=self.PLOTHEIGHT, width=self.PLOTWIDTH, units = self.PLOTUNITS, dpi=self.PLOTDPI)   
