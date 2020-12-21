#!/bin/bash 
echo $1
chr=$(echo $1)
echo $chr
awk '{split($2,a,":"); $2="6:"a[2]"_"a[3]"_"a[4]; print}' $3 > ${2}/all_impute2_awk_${1}.gen
sed -i "s/6:/$chr:/g" ${2}/all_impute2_awk_${1}.gen
head -10 ${2}/all_impute2_awk_${1}.gen
gzip ${2}/all_impute2_awk_${1}.gen 

mv ${2}/phased_data_${1}.ped.sample ${2}/all_impute2_awk_${1}.samples

bcftools convert --gensample2vcf ${2}/all_impute2_awk_${1} > ${2}/all_imputed_${1}.vcf

#sed "/#/d" ./Output/temp_dir/all_imputed.vcf > ./Output/temp_dir/all_imputed_nohash.vcf

#grep "#" ./Output/temp_dir/all_imputed.vcf > ./Output/temp_dir/all_imputed_header.vcf

#paste ./Output/temp_dir/all_imputed_nohash.vcf ./Output/temp_dir/rsidfile | awk '{print $1"\t"$2"\t"$9"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8}' > ./Output/temp_dir/all_imputed_rsid.vcf

#cat ./Output/temp_dir/all_imputed_header.vcf ./Output/temp_dir/all_imputed_rsid.vcf > ./Output/temp_dir/all_imputed_final.vcf

