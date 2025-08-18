# Ck3-HistroryGrabber
Two simple Python scripts for total conversions that automatically generates clean, ready-to-use title and province history stubs from your landed_titles.txt.

Features:

Parses kingdoms, duchies, and counties in order of appearance.

Outputs neatly structured blocks like:


k_example = {

}


d_example = {

}


c_example = {

}


Keeps titles grouped under their correct kingdom and duchy.

Designed to work directly with a raw landed_titles text or any similar file.

Paste content of landed titles or empire hierrchy title within input file (00_Input.txt) and run either of the .py files 

The scripts will do its thing and results will be printed to the output file (00_Output.txt).


Perfect for quickly scaffolding title history files without manually typing every block.



Requires python to be able to run
