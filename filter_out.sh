#!/usr/bin/bash

grep ^# ${2}/all_imputed_rs_${1}.vcf > ${2}/all_imputed_rs_filtered_${1}.vcf
grep ^$1 ${2}/all_imputed_rs_${1}.vcf | awk '!seen[$3]++' >> ${2}/all_imputed_rs_filtered_${1}.vcf


