#This code generate the MCOP graph based on our modeling in Appendix
#about V-PCC, where the dependancy between geometry map and attribute map
#is constructed first by conduct a measurement study (not included in the paper),
#then analyzed through a mathematical modeling effort
#We only used the basic observations of VPCC model, that is
#the P frame depends on I frame
#the attribute map will be invalid witout receiving the depth map
#attribute map P frame can be dropped from sometimes(as HEVC decoder has a error concealing,
#which works fine on attribute map stream)
#This code work together with our QUIC server based on quic-go
#And a NAL splitter written in C++, which first recognize the NAL byte barrier
#Then split a whole chunk of V-PCC bin file into NALs,
#before actively dropping some NALs
#We also implemented a NAL assembler at receiver-side, who can reassemble the BIN file
#from frames by filling the dropped frames with zero content placeholders.
