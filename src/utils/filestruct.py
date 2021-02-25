import pandas as pd
from icecream import ic

class fs:
	def __init__(self):
		self.base_dir = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/"  
		self.fonts_dir = "src/data_analysis_plotting/picture_tools/fonts/"
		self.src_dir = "src/"
		self.data_processing_formatting = "data_processing_formatting/"
		self.dvep_cut_dir = "hipo_root_cuts/dvep_cutter/"
		self.data_2_dir = "2_after_particle_fiducial_cuts/"
		self.data_3_dir = "3_after_DVEP_cuts/"
		self.data_4_dir = "4_uprooted_txts/"
		self.pandas_dir = "5_pickled_pandas/"
		self.data_dir = "data/"


		self.output_dir =  "output/"
		self.t_dep_dir = "t_dependence_hists/"
		self.phi_dep_dir = "phi_1d_hists/"
		self.t_vs_phi = "t_vs_phi_2d_hists/"
		self.xb_ranges_clas61 = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.7,0.85,1]
		self.q2_ranges_clas61 =  [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,7.0,8.0,9.0,12.0]
		self.t_ranges_clas61 =  [0.09,0.15,0.2,0.3,0.4,0.6,1,1.5,2,3,4.5,6]
		self.xb_ranges_clas6 = [0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.99]
		self.q2_ranges_clas6 =  [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,12.0]
		self.t_ranges_clas6 =  [0.09,0.15,0.2,0.3,0.4,0.6,1,1.5,2,3,4.5,6]

		self.xb_ranges_clas6_14 = [0,0.10,0.15,0.20,0.25,0.30,0.38,0.48,0.58,0.68,0.78,1,1.2]
		self.q2_ranges_clas6_14 =  [0,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.6,5.5,6.5,7.5,8.5,9.5,10.5,11.5]
		self.t_ranges_clas6_14 =  [0,0.09,0.15,0.2,0.3,0.4,0.6,1,1.5,2,3,4.5]#,6,10]
		self.phi_ranges_clas6_14 = [0,18,36,54,72,90,108,126,144,162,180,198,216,234,252,270,288,306,324,342,360]

		self.xb_ranges_test =  [0,0.3,0.5,1.0]
		self.q2_ranges_test =  [1.0,5.0,12.0]
		self.t_ranges_test =  [0.09,0.3,6]
		self.default_2iter_dir = "output/2iter/"
		self.test_run_dir = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
		self.phi_fits_pkl_name = "phi_fit_vals_14.pkl"
		self.phi_fits_pkl_name_corrected = "phi_fit_vals_14_corrected.pkl"
		self.raw_data_dir = "/mnt/d/CLAS12Data/"
		self.lund_event_pandas_headers = ["run","event","luminosity","helicity","Ebeam","Eprime","q2","xb","t","phi"]

		self.lund_dir = "lund_files/"
		self.lund_pandas_filtered = "lund_pandas_filtered/"
		self.evented_lund_pandas = "lund_pandas_with_kinematics/"
		self.binned_lund_pandas = "lund_pandas_binned/"
		self.filtered_lunds = "filtered_lunds/"
		self.raw_lunds = "raw_lunds/"
		self.lund_outputs = "lund_outputs/"
		self.counted_pickled_out_name = "counted_4D_out.pkl"
		self.lund_out_2d = "lund_2d_coverage/"
		self.lund_out_3d = "lund_3d_coverage/"
		self.lund_out_4d = "lund_4d_coverage/"
		self.lund_out_stitched = "stitched_lund_coverages/"

		self.whole_data_pkl_name = "full_dataset_pickle.pkl"
		self.data_outs = "data_outputs/data_out_stitched/"

		### ADJUST THESE PARAMETERS TO PROCESS DIFFERENT DATA
		self.root_macro_script = "dvpip_cutterFD.C"
		
		#self.data_basename = "sims100k/"
		self.data_basename =  "F18_Inbending_FD_SangbaekSkim_0_20210205/" #"testpi01Ksim/"
		#self.data_basename = "sim_100k_test/"
		#self.lund_test_run = "q2_100k_test/"
		#self.lund_test_run = "q2_w_cut_200k/" 
		#self.lund_test_run = "higherq2_test/" 
		self.lund_test_run = "testpi0sim1K/"
		self.real_dataset_full_pandas = "full_df_pickle-174_20210205_08-46-50.pkl"

		self.f18_inbending_total_lumi = 5.511802214933477e+40

		