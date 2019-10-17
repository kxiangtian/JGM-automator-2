echo Run Tesseract for Training.. 
tesseract.exe JGM.font.exp0.tif JGM.font.exp0 nobatch box.train 

echo Compute the Character Set.. 
unicharset_extractor.exe JGM.font.exp0.box 
mftraining -F font_properties -U unicharset -O JGM.unicharset JGM.font.exp0.tr 


echo Clustering.. 
cntraining.exe JGM.font.exp0.tr 

echo Rename Files.. 
rename normproto JGM.normproto 
rename inttemp JGM.inttemp 
rename pffmtable JGM.pffmtable 
rename shapetable JGM.shapetable  

echo Create Tessdata.. 
combine_tessdata.exe JGM. 

echo. & pause