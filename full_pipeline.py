#! /projects/team-1/html/miniconda3/bin/python3.8 
import os
import shutil 
import db_util
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import blue 
from reportlab.lib.units import inch
from reportlab.lib.colors import red
import matplotlib.pyplot as plt
import subprocess
import re
import pandas as pd
import numpy as np
from multiprocessing import Pool
import time
def check_format(input_path,temp_dir):
	unknown=open(input_path,"r")
	header = unknown.readline()
	andMe_header = "# rsid"+"\t"+"chromosome"+"\t"+"position"+"\t"+"genotype"+"\n"
	if header.startswith("#AncestryDNA"):
		output=open(temp_dir+"/ancestry_known.tsv","w+")
		output.write(andMe_header)
		for line in unknown:
			line_split = line.split("\t")
			if len(line_split) == 5:
				if "rs" in line_split[0] and line_split[1] in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]:
					line_split[-2] =line_split[-2]+line_split[-1]
					line_split = line_split[:-1]
					if line_split[-1] =="00\n":
						line_split[-1]="--"+"\n" 
					line_join = "\t".join(line_split)
					output.write(line_join)
		output.close()
		return(temp_dir+"/ancestry_known.tsv")
			
	elif header.startswith("RSID,CHROM"):
		output=open(temp_dir+"/ftdna_known.tsv","w+")
		#header_split = header.split(",")
		#header_join = "\t".join(header_split)
		output.write(andMe_header)
		for line in unknown:
			line_split = line.split(",")
			#print(line_split)
			#print(line_split[0],line_split[1])
			#print(line_split[1])
			chr = line_split[1].rstrip("\"")
			chr = chr.lstrip("\"")
			if chr in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]:
				#print("here1")
				updated_list = []
				if "rs" in line_split[0]:
					for item in range(len(line_split)):
						if item != len(line_split)-1:
							p = (line_split[item])[1:]
							p = p[:-1]
						else:
							p = (line_split[item])[1:]
							p = p[:-2]
							p = p+"\n"
						#item = item.lstrip("\"")
						updated_list.append(p)
					#print("here")
					line_join = "\t".join(updated_list)
					output.write(line_join)
		output.close()
		return(temp_dir+"/ftdna_known.tsv")
	else:
		return(input_path)

	unknown.close()
		 
def modify_input(input_path,temp_dir, reference_dir,sample_name):

	tsv = open(input_path,"r")
	modify_tsv = open(temp_dir+"/modified.tsv","w+")
	for line in tsv:
		if "is" not in line:
			modify_tsv.write(line)
	tsv.close()
	modify_tsv.close()

	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/bcftools", "convert", "--tsv2vcf", temp_dir+"/modified.tsv", "-f", reference_dir+ "/Homo_sapiens.GRCh37.dna.primary_assembly.fa","-s", sample_name, "-Ov", "-o", temp_dir+"/blood_type.vcf"]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	print("moving to next step")
	vcf_file = open(temp_dir+"/blood_type.vcf","r")
	vcf_file_filtered = open(temp_dir+"/blood_type_filtered.vcf","w+")
	positions = []
	for line in vcf_file:
		line_split = line.split("\t")
		if line_split[0] in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]:
			if "rs" in line_split[2]:
				vcf_file_filtered.write(line)
		else:
			vcf_file_filtered.write(line)
	vcf_file.close()
	vcf_file_filtered.close()
	vcf_file = open(temp_dir+"/blood_type_filtered.vcf","r")
	vcf_file_filtered = open(temp_dir+"/blood_type_filtered_again.vcf","w+")
	for line in vcf_file:
		line_split = line.split("\t")
		if not line.startswith("#"):
			if line_split[3] != "." and line_split[4] != ".":
				vcf_file_filtered.write(line)
		else:
			vcf_file_filtered.write(line)
	vcf_file.close()
	vcf_file_filtered.close()
	return(temp_dir+"/blood_type_filtered_again.vcf")

def phase(input_path,temp_dir,reference_dir,chr,path_to_eagle):
	
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/bgzip",input_path]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/tabix",input_path+".gz"]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	cmd = [path_to_eagle, "--vcfTarget", input_path+".gz", "--vcfRef", reference_dir+"/ALL.chr"+str(chr)+".phase3.bcf.gz", "--geneticMapFile", reference_dir+"/genetic_map_hg19_withX.txt.gz", "--outPrefix", temp_dir+"/phased_data_"+str(chr), "--chrom",str(chr)]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	return(temp_dir+"/phased_data_"+str(chr)+".vcf.gz")

def convert_vcf_to_gen(input_path,temp_dir,chr):
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/vcftools", "--gzvcf", input_path, "--out", temp_dir+"/phased_data_"+str(chr), "--plink"]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	cmd = ["/projects/team-1/html/Tools/gtool", "-P", "--ped", temp_dir+"/phased_data_"+str(chr)+".ped", "--map", temp_dir+"/phased_data_"+str(chr)+".map", "--og", temp_dir+"/phased_data_"+str(chr)+".ped.gen"]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	return(temp_dir+"/phased_data_"+str(chr)+".ped.gen")

def impute(start,stop,input_path,temp_dir, reference_dir,count,chr):

	cmd = ["/projects/team-1/html/Tools/impute_v2.3.2_x86_64_static/impute2", "-m", reference_dir+"/genetic_map_chr"+str(chr)+"_combined_b37.txt", "-h", reference_dir+"/1000GP_Phase3_chr"+str(chr)+".hap.gz", "-l", reference_dir+"/1000GP_Phase3_chr"+str(chr)+".legend.gz", "-g", input_path, "-int",str(start),str(stop), "-Ne", "20000", "-o", temp_dir+"/imputed.chr"+str(chr)+"."+str(count)+"."+str(chr)+".phased.impute2", ">", "impute_log"+str(count)+".log", "2>&1"]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	#cmd = ["rm", "-r", "impute_log"+str(count)+".log"]
	#subprocess.call(cmd)

def impute2temp(input_path,temp_dir,chr):
	temp_output = open(temp_dir+"/all_impute2_filtered_"+str(chr),"w+")
	rsidfile = open(temp_dir+"/rsidfile_"+str(chr),"w+")
	print("here in impute to temp")
	with open(input_path,"r") as fh:
		for line in fh:
			#print(line)
			if line.startswith("--- rs"):
				temp_output.write(line)
				row = line.split(" ")
				row[1] = row[1].split(":")
				rsidfile.write(row[1][0] + "\t" +row[1][1] + "\n")
			if re.search("^[0-9]",line):
				row = line.split(" ")
				templine = "--- " + row[1] + ":" + row[2] + ":" + row[3] + ":" + row[4] + " " + row[2] + " " + row[3] + " " + row[4] + " " +row[5]+" "+row[6]+" "+row[7]+"\n"
				temp_output.write(templine)
				rsidfile.write(row[1]+ "\t" + row[2] + "\n")
	rsidfile.close()
	temp_output.close()
	cmd = "sed -i '/^$/d' "+temp_dir+"/all_impute2_filtered_"+str(chr) 
	os.popen(cmd)
	time.sleep(10)
	#subprocess.call(cmd)
	return(temp_dir+"/all_impute2_filtered_"+str(chr))

def impute2vcf(input_path,temp_dir,chr):

	cmd = ["/projects/team-1/html/null-project/temp2vcf.sh",str(chr),temp_dir,input_path]
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	return(temp_dir+"/all_imputed_"+str(chr)+".vcf")

def add_rsid(input_path,temp_dir,chr):
	hold_rs = {}
	rsidfile = open(temp_dir+"/rsidfile_"+str(chr),"r")
	for line in rsidfile:
		rs_id = line.split("\t")[0]
		chr_pos = line.split("\t")[1]
		#print(rs_id)
		chr_pos = chr_pos.rstrip("\n")
		#print(chr_pos)
		if chr_pos not in hold_rs:
			hold_rs[chr_pos] = rs_id
	rsidfile.close()
	
	vcf_file = open(temp_dir+"/all_imputed_"+str(chr)+".vcf","r")
	vcf_with_rs = open(temp_dir+"/all_imputed_rs_"+str(chr)+".vcf","w+")
	for line in vcf_file:
		if line.startswith(str(chr)):
			#print("past line starts with") 
			line_split = line.split("\t")
			#print(line_split[1])
			if line_split[1] in hold_rs:
				#print("pos in hold_rs")
				line_split[2] = hold_rs.get(line_split[1])
				new_line = "\t".join(line_split)
				vcf_with_rs.write(new_line)
		else:
			vcf_with_rs.write(line)
	vcf_file.close()
	vcf_with_rs.close()
	cmd = ["/projects/team-1/html/null-project/filter_out.sh",str(chr),temp_dir,input_path]
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	#cmd = ["grep","^#",temp_dir+"/all_imputed_rs.vcf",">",temp_dir+"/all_imputed_rs_filtered.vcf"]
	#subprocess.call(cmd)
	#cmd = "grep ^6 "+temp_dir+"/all_imputed_rs.vcf | awk '!seen[$3]++' >> "+temp_dir+"/all_imputed_rs_filtered.vcf"
	#os.popen(cmd)
	#time.sleep(10)
	return(temp_dir+"/all_imputed_rs_filtered_"+str(chr)+".vcf")
def combine_vcf_final(input_path_sample,input_path_ancestry,temp_dir,sample_name,chr,ancestry):
	rsidfile = open(temp_dir+"/rsidfile.txt","w+")
	cmd = ["cut", "-f", "3", input_path_sample]
	p = subprocess.Popen(cmd,stdout=rsidfile)
	out = p.communicate()
	rsidfile.close()
	ancestry_filtered = open(temp_dir+"/"+ancestry+"_"+chr+"_filtered.vcf","w+")
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/bcftools", "view", "--include", "ID==@"+temp_dir+"/rsidfile.txt", input_path_ancestry]
	p = subprocess.Popen(cmd,stdout=ancestry_filtered)
	out = p.communicate()
	ancestry_filtered.close()

	sample_vcf = open(input_path_sample,"r")
	ancestry_vcf = open(temp_dir+"/"+ancestry+"_"+chr+"_filtered.vcf","r")
	final_vcf = open(temp_dir+"/combine_"+chr+".vcf","w+")
	hold_sample_info = {}
	for line in sample_vcf:
		line_split=line.split("\t")
		if line_split[0] == chr:
			rsid = line_split[2]
			genotype = line_split[9]
			genotype = genotype.split(":")[0]
			if rsid not in hold_sample_info:
				hold_sample_info[rsid] = genotype
	for line in ancestry_vcf:
		line_split = line.split("\t")
		if line_split[0] == chr:
			if hold_sample_info.get(line_split[2]):
				line_split[-1] = line_split[-1].rstrip()
				line_split.append(hold_sample_info.get(line_split[2])+"\n")
				#print(line_split)
				final_line = "\t".join(line_split)
				final_vcf.write(final_line)		
		elif "#CHR" in line_split[0]:
			print("here")
			line_split[-1]=line_split[-1].rstrip()
			line_split.append(sample_name+"_"+sample_name+"\n")
			final_line = "\t".join(line_split)
			final_vcf.write(final_line)
		else:
			final_vcf.write(line)
	sample_vcf.close()
	ancestry_vcf.close()
	final_vcf.close()
	return(temp_dir+"/combine_"+chr+".vcf")

def convert_for_PRS(input_path,temp_dir,reference_path,output_path,chr):
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/bcftools", "sort", input_path,"-O","v","-o",temp_dir+"/all_imputed_sorted_"+str(chr)+".vcf"]
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate() 
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/plink2", "--vcf", temp_dir+"/all_imputed_sorted_"+str(chr)+".vcf", "--make-bed", "--out",temp_dir+"/all_imputed_"+str(chr)]
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/plink2", "--bfile", temp_dir+"/all_imputed_"+str(chr), "--maf", "0.05", "--mind", "0.1", "--geno", "0.1", "--hwe", "1e-6", "--make-just-bim", "--make-just-fam", "--out",temp_dir+"/all_imputed_filtered_"+str(chr)+".qc"]
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()
	
	if chr == 6:

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/chicken.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep",temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/chicken"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/childhood_ear_infections.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/childhood_ear_infections"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/mono.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/mono"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()
	
		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base",reference_path+"/strep_throat.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/strep_throat"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/mumps.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/mumps"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/tonsillectomy.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/tonsillectomy"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/plantar_warts.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/plantar_warts"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100","--base", reference_path+"/uti_frequency_6.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/uti"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05", "--clump-kb","100","--base", reference_path+"/pneumonia.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/pneumonia"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()
	
		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05", "--clump-kb","100","--base", reference_path+"/yeast_infections.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/yeast_infections"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05", "--clump-kb","100","--base", reference_path+"/positive_tb_test.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/positive_tb_test"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05", "--clump-kb","100","--base", reference_path+"/bacterial_meningitis.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/bacterial_meningitis"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/scarlet_fever.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/scarlet_fever"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/shingles.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "OR", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/shingles"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

	if chr == 3:
		cmd = ["/projects/team-1/html/miniconda3/envs/Renv/bin/Rscript", "/projects/team-1/html/Tools/PRSice.R", "--dir", "/projects/team-1/html/null-project/", "--prsice", "/projects/team-1/html/Tools/PRSice_linux", "--no-regress","--lower","1e-05","--clump-kb","100", "--base", reference_path+"/covid.assoc", "--target", temp_dir+"/all_imputed_"+str(chr), "--stat", "BETA", "--binary-target", "T", "--keep", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.fam", "--extract", temp_dir+"/all_imputed_filtered_"+str(chr)+".qc.bim", "--snp", "SNP", "--chr", "CHR", "--bp", "BP", "--A1", "A1", "--A2", "A2", "--pvalue", "P","--out",temp_dir+"/covid"]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()

def calculate_percentile(disease,ethnicity,temp_dir,reference_path,score,sample_name):
	file_path = temp_dir+"/"+reference_path
	if os.path.exists(file_path):
		output = temp_dir+"/"+sample_name+"_"+disease+".txt"
		print(file_path,score,output)
		cmd = ["/projects/team-1/html/miniconda3/envs/test_env/bin/Rscript","/projects/team-1/html/null-project/calculate_percentile.R",file_path,score,output]
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()
	
def PRS_to_percentile(temp_dir,ethnicity,sample_name):
	score =[]
	for filename in os.listdir(temp_dir):
		if "all_score" in filename and "updated" not in filename:
			print(filename)
			f = open(temp_dir+"/"+filename,"r")
			disease = filename.split(".")[0]
			output_prs = open(temp_dir+"/"+disease+".updated.all_score","w+")
			header = f.readline()
			#print(header)
			updated_header = header.split(" ")[:3]
			#print(updated_header)
			updated_header[2] = "PRScore"
			final_header = "\t".join(updated_header)+"\n"
			output_prs.write(final_header)
			for line in f:
				line = line.rstrip()
				line = line.rstrip(" ")
				if sample_name in line:
					updated_line = line.split(" ")
					#print(updated_line)
					final_line = updated_line[0]+"\t"+updated_line[1]+"\t"+updated_line[-1]+"\n"
					#print(final_line)
				else:
					updated_line = line.split(" ")
					#print(updated_line)
					final_line = updated_line[0]+"\t"+updated_line[1]+"\t"+updated_line[-1]+"\n"
					#print(final_line)
				#final_line = "\t".join(updated_line)+"\n"
				output_prs.write(final_line)
			f.close()
			output_prs.close()

	for filename in os.listdir(temp_dir):
		if "all_score" in filename and "updated" in filename:
			f = open(temp_dir+"/"+filename,"r")
			for line in f:
				if sample_name in line:
					#print(f.readline().split(" "))
					#print(line)
					score = (line.split("\t"))[2]
					print(score)
			f.close()
			disease = filename.split(".")[0]
			calculate_percentile(disease,ethnicity,temp_dir,filename,score,sample_name)
 
def blood_type_predict(input_path,temp_dir,reference_path,output_path,sample_name,chr):
	pos_arr = ["136132908", "136131322", "136131315" ]
	GT_dict = {}
	

	cmd =["mv",input_path,input_path+".tsv"]
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	out = p.communicate()

	with open(input_path+".tsv") as fh:
		for line in fh.readlines():
			#print(line)
			if line.split("\t")[0] == "9" and line.split("\t")[1] in pos_arr:
				print(line)
				o = {}
				o = set(o)
				if line.split("\t")[1] == '136132908':
					if len(line.split("\t")[4]) == 2:
						if (line.split("\t")[9].split(":")[0].split("/")[0]) == "0":
							o1 = (line.split("\t")[3])
						else:
							o1 = (line.split("\t")[4][1])
						if (line.split("\t")[9].split(":")[0].split("/")[1]) == "0":
							o2 = (line.split("\t")[3])
						else:
							o2 = (line.split("\t")[4][1])

					else:
						if (line.split("\t")[9].split(":")[0].split("/")[0]) == "0":
							 o1 = (line.split("\t")[3])
						else:
							o1 = (line.split("\t")[4])

						if (line.split("\t")[9].split(":")[0].split("/")[1]) == "0":
							o2 = (line.split("\t")[3])
						else:
							o2 = (line.split("\t")[4])

				else:
					if (line.split("\t")[9].split(":")[0].split("/")[0]) == "0":
						o1 = (line.split("\t")[3])
					else:
						o1 = (line.split("\t")[4])
					if (line.split("\t")[9].split(":")[0].split("/")[1]) == "0":
						o2 = (line.split("\t")[3])
					else:
						o2 = (line.split("\t")[4])
				o.add(o1 + "/" + o2)
				o.add(o2 + "/" + o1)
				print(o)
				GT_dict[line.split("\t")[1]] = o
	print(GT_dict)
	#logo = reference_path+"/logo.png"
	#im = Image(logo, 2*inch, 2*inch)
	
	output = open(output_path+"/"+sample_name+"blood_type.txt","w+")
	canvas = Canvas(output_path+"/"+sample_name+"blood_type.pdf")
	canvas.setFillColor(blue)
	canvas.setFont("Courier-Bold", 18)
	canvas.drawString(25, 700, "Blood Type Report")
	canvas.setFillColor(red)
	canvas.setFont("Courier-Bold", 16)
	arr = []
	df = pd.read_csv(reference_path+"/predict_blood_type_2.csv")
	for k,v in GT_dict.items():
		if len(v) == 2:
			for i in v:
				df1 = df[df[k] == i]
				arr.append(df1)
				print(arr)
			df = pd.concat([arr[0],arr[1]])
			arr = []
		else:
			for i in v:
				df1 = df[df[k] == i]
				arr.append(df1)
			df = pd.concat([arr[0]])
	
	if df['Blood type'].empty:
		output.write("not clear")
		canvas.drawString(25, 600, "not clear")
		print("here")
	else:
		blood_type="Blood type = " + df['Blood type'].tolist()[0]
		output.write(blood_type)
		canvas.drawString(25, 600, blood_type)
		if df['Blood type'].tolist()[0] == "O":
			print("O")
			canvas.drawString(25, 550, "Blood Type O has been associated with lower") 
			canvas.drawString(25, 500, "risk of severe Covid-19 progression please ")
			canvas.drawString(25, 450, "refer to our website for more information ")
			canvas.drawString(25, 400, "regarding this")
		if df['Blood type'].tolist()[0] == "AB":
			canvas.drawString(25, 550, "As of recent studies Blood Type AB has not")
			canvas.drawString(25, 500, "been associated with an increased or") 
			canvas.drawString(25, 450, "descreased risk of severe Covid-19 progression")
			print("AB")
		if df['Blood type'].tolist()[0] == "A":
			print("A")
			canvas.drawString(25, 550, "As of recent studies Blood Type A has been")
			canvas.drawString(25, 500, "associated with an increased risk of severe") 
			canvas.drawString(25, 450, "Covid-19 progression please refer to out ")
			canvas.drawString(25, 400, "website for more information")
		if df['Blood type'].tolist()[0] =="B":
			print("B")
			canvas.drawString(25, 550, "As of recent studies Blood Type B has not ")
			canvas.drawString(25, 500, "been associated with an increased or ")
			canvas.drawString(25, 450, "descreased risk of severe Covid-19 progression")
		if df['Blood type'].tolist()[0] =="B likely, A possible":
			print("B possible")
			canvas.drawString(25, 550, "From data could not pinpoint exact blood type")
			canvas.drawString(25, 500, "As of recent studies Blood Type B has not ")
			canvas.drawString(25, 450, "been associated with an increased or ")
			canvas.drawString(25, 400, "Covid-19 progression please refer to out ")
			canvas.drawString(25, 350, "website for more information")
	canvas.save()
	output.close()
def make_readable(sample_name, temp_dir):
	updated_filename = temp_dir+"/"+sample_name+".csv"
	updated_output = open(updated_filename,"w+")
	for filename in os.listdir(temp_dir):
		disease = (filename.split(".")[0]).split("_")[1:]
		disease_updated = " ".join(disease)
		#print(disease_updated)
		if sample_name in filename and filename != sample_name+".csv":
			print(disease)
			read_output = open(temp_dir+"/"+filename,"r")
			header_line=read_output.readline()
			print(header_line)
			score_line = read_output.readline()
			#print(score_line)
			#print(score_line.split("\""))
			score = ((score_line).split("\"")[2]).rstrip()
			fixed_score = str(int(float(score)*100))
			print(fixed_score)
			output_write = disease_updated+"\t"+fixed_score+"\n"
			updated_output.write(output_write)
	return(temp_dir+"/"+sample_name+".csv")
def donut_plot(input_path,output_path,sample_name):
	df = pd.read_csv(input_path, sep = '\t', header = None)
	np.random.seed(42)
	df2 = pd.DataFrame(np.random.randint(5, 10, (7, 3)), columns=['a', 'b', 'c'])
	df = df.transpose()
	new_header = df.iloc[0] #grab the first row for the header
	df = df[1:] #take the data less the header row
	df.columns = new_header
	df['']=int()
	df[' ']=int()
	print(df)

	fig, axes = plt.subplots(3,5, figsize=(10,5))
	axes = axes.flatten()
	i=0
	for ax, col in zip(axes[:len(axes)-2], df.columns):
		#print(list(df[col])[0])
		ax.pie([list(df[col])[0], 100-df[col]], wedgeprops=dict(width=.3), labels=[str(list(df[col])[0])+'%',''])
		ax.set(ylabel='', title=col.title(), aspect='equal')
		i+=1
	fig.delaxes(axes[13])
	fig.delaxes(axes[14])
	ax.legend(['Susceptibility'], title="Legend", loc="center left", bbox_to_anchor=(2, 0, 20, 1))  
	plt.savefig(output_path+"/"+sample_name+"_donut.pdf")
	#plt.show()

def f(input_path,output_path,ethnicity,job_id):
	output_path = output_path.rstrip("/")
	temp_dir = output_path+"/temp_dir"
	make_temp = "mkdir " + temp_dir
	os.system(make_temp)
	#pool = Pool(3)
	sample_name = input_path.split("/")[-1]
	sample_name = sample_name.split("_")[0]
	print(sample_name)
	path_to_eagle = "/projects/team-1/html/null-project/Tools/Eagle2/Eagle_v2.4.1/eagle"
	reference_path = "/projects/team-1/html/null-project/Reference"
	input_path = check_format(input_path, temp_dir)
	input_path = modify_input(input_path, temp_dir, reference_path,sample_name)
	input_path1 = phase(input_path,temp_dir,reference_path,6,path_to_eagle)
	input_path2 = phase(input_path,temp_dir,reference_path,9,path_to_eagle)
	input_path3 = phase(input_path,temp_dir,reference_path,3,path_to_eagle)
	input_path1 = convert_vcf_to_gen(input_path1,temp_dir,6)
	input_path2 = convert_vcf_to_gen(input_path2,temp_dir,9)
	input_path3 = convert_vcf_to_gen(input_path3,temp_dir,3)
	#sample_name = input_path.split("/")[-1]
	#sample_name = sample_name.split("_")[0]

	impute_list = [[7000000,8000000,input_path1,temp_dir,reference_path,1,6],[13000000,14000000,input_path1,temp_dir,reference_path,5,6],[14000001,15000000,input_path1,temp_dir,reference_path,6,6],[28000000,29000000,input_path1,temp_dir,reference_path,10,6],[29000001,30000000,input_path1,temp_dir,reference_path,11,6],[30000001,31000000,input_path1,temp_dir,reference_path,12,6],[31000001,32000000,input_path1,temp_dir,reference_path,13,6],[32000001,33000000,input_path1,temp_dir,reference_path,14,6],[33000001,34000000,input_path1,temp_dir,reference_path,15,6],[45000000,46000000,input_path1,temp_dir,reference_path,18,6],[48000000,49000000,input_path1,temp_dir,reference_path,21,6],[49000001,50000000,input_path1,temp_dir,reference_path,22,6],[50000001,51000000,input_path1,temp_dir,reference_path,23,6],[72000000,73000000,input_path1,temp_dir,reference_path,24,6],[96000000,97000000,input_path1,temp_dir,reference_path,24,6],[126000000,127000000,input_path1,temp_dir,reference_path,25,6],[150000000,151000000,input_path1,temp_dir,reference_path,28,6],[151000001,152000000,input_path1,temp_dir,reference_path,29,6]]
	
	#list(pool.starmap(impute, impute_list))
	for i in impute_list:
		impute(i[0],i[1],i[2],i[3],i[4],i[5],i[6])

	impute(135000000,137000000,input_path2,temp_dir,reference_path,7,9)

	impute_list = [[3000000,4000000,input_path3,temp_dir,reference_path,8,3],[8600000,8700000,input_path3,temp_dir,reference_path,9,3],[8700001,8800000,input_path3,temp_dir,reference_path,10,3],[45000000,46000000,input_path3,temp_dir,reference_path,11,3],[46000001,47000000,input_path3,temp_dir,reference_path,12,3],[61000000,62000000,input_path3,temp_dir,reference_path,13,3],[62000001,63000000,input_path3,temp_dir,reference_path,14,3],[119000000,120000000,input_path3,temp_dir,reference_path,15,3],[137000000,138000000,input_path3,temp_dir,reference_path,16,3],[148000000,149000000,input_path3,temp_dir,reference_path,17,3]]
	#list(pool.starmap(impute, impute_list))

	for i in impute_list:
		impute(i[0],i[1],i[2],i[3],i[4],i[5],i[6])

	cmd = "for i in "+ temp_dir+"/*6.phased.impute2; do cat $i >> "+temp_dir+"/all_impute2_6.gen ; done"
	os.popen(cmd)
	time.sleep(10)
	cmd = "for i in "+ temp_dir+"/*9.phased.impute2 ; do cat $i >> "+temp_dir+"/all_impute2_9.gen ; done"
	os.popen(cmd)
	time.sleep(10)
	cmd = "for i in "+ temp_dir+"/*3.phased.impute2 ; do cat $i >> "+temp_dir+"/all_impute2_3.gen ; done"
	os.popen(cmd)
	time.sleep(10)
	input_path1 = temp_dir+"/all_impute2_6.gen"
	input_path2 = temp_dir+"/all_impute2_9.gen"
	input_path3 = temp_dir+"/all_impute2_3.gen"
	input_path1 = impute2temp(input_path1,temp_dir,6)
	input_path2 = impute2temp(input_path2,temp_dir,9)
	input_path3 = impute2temp(input_path3,temp_dir,3)
	input_path1 = impute2vcf(input_path1,temp_dir,6)
	input_path2 = impute2vcf(input_path2,temp_dir,9)
	input_path3 = impute2vcf(input_path3,temp_dir,3)
	input_path1 = add_rsid(input_path1,temp_dir,6)
	input_path2 = add_rsid(input_path2,temp_dir,9)
	input_path3 = add_rsid(input_path3,temp_dir,3)
	input_path1 = combine_vcf_final(input_path1,reference_path+"/"+ethnicity+"/"+ethnicity+"_6.vcf",temp_dir,sample_name,str(6),ethnicity)
	input_path3 = combine_vcf_final(input_path3,reference_path+"/"+ethnicity+"/"+ethnicity+"_3.vcf",temp_dir,sample_name,str(3),ethnicity)
	convert_for_PRS(input_path1,temp_dir,reference_path,output_path,6)
	convert_for_PRS(input_path3,temp_dir,reference_path,output_path,3)
	PRS_to_percentile(temp_dir,ethnicity,sample_name)
	input_path = make_readable(sample_name,temp_dir)
	donut_plot(input_path,output_path,sample_name)
	blood_type_predict(temp_dir+"/all_imputed_rs_filtered_"+str(9)+".vcf",temp_dir,reference_path,output_path,sample_name,9)
	location = output_path+"/"
	dir = "temp_dir"
	path = os.path.join(location, dir)
	shutil.rmtree(path, ignore_errors=True)
	db_util.update_pipeline_status(job_id)
