echo Compute the Character Set.. 
unicharset_extractor.exe jgm.font.exp0.box 
mftraining -F font_properties -U unicharset -O jgm.unicharset jgm.font.exp0.tr 


echo Clustering.. 
cntraining.exe jgm.font.exp0.tr 

echo Rename Files.. 
rename normproto jgm.normproto 
rename inttemp jgm.inttemp 
rename pffmtable jgm.pffmtable 
rename shapetable jgm.shapetable  

echo Create Tessdata.. 
combine_tessdata.exe jgm. 

echo. & pause