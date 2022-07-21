#python3 make_annot_bed.py gencode.v19.annotation.gtf |sortBed >hg19_annot.bed


python3 metaplot.py ../../5.peak/m6A-100ng-HEK293.cs.bed ./hg19_annot.bed >m6A-100ng-HEK293.dist_measure.tsv
python3 metaplot.py ../../5.peak/m6A-100pg-HEK293.cs.bed ./hg19_annot.bed >m6A-100pg-HEK293.dist_measure.tsv
python3 metaplot.py ../../5.peak/m6A-10ng-HEK293.cs.bed ./hg19_annot.bed >m6A-10ng-HEK293.dist_measure.tsv
python3 metaplot.py ../../5.peak/m6A-1ug-HEK293.cs.bed ./hg19_annot.bed >m6A-1ug-HEK293.dist_measure.tsv



