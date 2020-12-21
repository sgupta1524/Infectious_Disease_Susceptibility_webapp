#! /projects/team-1/html/miniconda3/bin/python3.8
 
import os 
import full_pipeline
import subprocess

#cmd = ["./activate_conda.sh"]
#subprocess.call(cmd)

#full_pipeline.PRS_to_percentile("/projects/team-1/html/Test_Pipeline/Output","AFR","overlap23")
#full_pipeline.add_rsid("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_imputed_3.vcf","/projects/team-1/html/Test_Pipeline/Output/temp_dir",3)

#full_pipeline.combine_vcf_final("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_imputed_rs_filtered_3.vcf","/projects/team-1/html/Test_Pipeline/Reference/EUR/EUR_3.vcf","/projects/team-1/html/Test_Pipeline/Output/temp_dir","hu706427",str(3),"EUR")
#full_pipeline.f("/projects/team-1/html/Test_Pipeline/Input/3925_report.tsv","/projects/team-1/html/Test_Pipeline/Output",1,"EUR")
#full_pipeline.impute2vcf("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_impute2_filtered_3","/projects/team-1/html/Test_Pipeline/Output/temp_dir",3)
#full_pipeline.check_format("/projects/team-1/html/Test_Pipeline/Input/3925_report.tsv","/projects/team-1/html/Test_Pipeline/Output/temp_dir")
#full_pipeline.convert_for_PRS("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_imputed_rs_filtered.vcf","/projects/team-1/html/Test_Pipeline/Output/temp_dir","/projects/team-1/html/Test_Pipeline/Reference")

#full_pipeline.add_rsid("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_imputed.vcf","/projects/team-1/html/Test_Pipeline/Output/temp_dir")

#full_pipeline.PRS_to_percentile("/projects/team-1/html/Test_Pipeline/Output","EUR","/projects/team-1/html/Test_Pipeline/Reference","hkytest")

#cmd = ["conda","deactivate","test_env"]
#subprocess.call(cmd)

#full_pipeline.impute2vcf("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_impute2_filtered_6","/projects/team-1/html/Test_Pipeline/Output/temp_dir",6)
#full_pipeline.impute2vcf("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_impute2_filtered_9","/projects/team-1/html/Test_Pipeline/Output/temp_dir",9)

#full_pipeline.add_rsid("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_imputed_6.vcf","/projects/team-1/html/Test_Pipeline/Output/temp_dir",6)
#full_pipeline.add_rsid("/projects/team-1/html/Test_Pipeline/Output/temp_dir/all_imputed_9.vcf","/projects/team-1/html/Test_Pipeline/Output/temp_dir",9)

full_pipeline.blood_type_predict("/projects/team-1/html/null-project/Output/25202012130009475/temp_dir/all_imputed_rs_filtered_9.vcf","/projects/team-1/html/null-project/Output/25202012130009475/temp_dir","/projects/team-1/html/null-project/Reference","/projects/team-1/html/null-project/Output/25202012130009475", "hkytest",9)

#full_pipeline.make_readable("hu706427","/projects/team-1/html/Test_Pipeline/Output")
#full_pipeline.donut_plot("/projects/team-1/html/Test_Pipeline/Output/temp_dir/hu553F31.csv","/projects/team-1/html/Test_Pipeline/Output/","hu553F31")
