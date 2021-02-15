import subprocess
import os
import time
import shutil
from shutil import copyfile

#This project
from src.utils import filestruct
from src.utils import query_maker
from src.utils import file_maker

"data/2_after_particle_fiducial_cuts/ "



def process_root_files(root_macro,data_dir,output_dir):
    print("Processing root files for directory {}".format(data_dir))
    default_root_outname = "output_root_file.root"
    default_root_inname = "input_root_file.root"

    file_maker.make_dir(output_dir)

    data_list = os.listdir(data_dir)
    for count,file in enumerate(data_list):
        print("on file {} out of {}, named {}".format(count+1,len(data_list),file))
        copyfile(data_dir+file,default_root_inname)
        process = subprocess.Popen(['root','-b','-q', root_macro],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(r"STDOUT is {}".format(stdout))
        print("STDERR is {}".format(stderr))
        shutil.move(default_root_outname,output_dir+file.replace(".root","_DVEP.root"))
        time.sleep(0.05)
    os.remove(default_root_inname) #cleanup


if __name__ == "__main__":
    fs = filestruct.fs()

    data_dir = fs.base_dir+fs.data_dir+fs.data_2_dir+fs.data_basename 
    output_dir = fs.base_dir+fs.data_dir+fs.data_3_dir+fs.data_basename
    root_macro = fs.base_dir+fs.src_dir+fs.data_processing_formatting + fs.dvep_cut_dir+fs.root_macro_script

    process_root_files(root_macro,data_dir,output_dir)    

    
    

