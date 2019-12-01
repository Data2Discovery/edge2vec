from __future__ import print_function

import pandas as pd
import os

dir_edge = "edges/"

files_edge = \
	['geneCellularComponent.tsv', 'targetFamily.tsv', 'pathwayGene.tsv', \
	 'goRegulates.tsv', 'phenotypeCategory.tsv', 'goComponentOf.tsv', \
	 'geneGene.tsv', 'compoundIndication.tsv', 'goInstanceOf.tsv', \
	 'pathwayCompound.tsv', 'isaEC.tsv', 'geneDisease.tsv', \
	 'geneBiologicalProcess.tsv', 'pathwayCellularComponent.tsv', \
	 'compoundAdverseEffect.tsv', 'canonicalTarget.tsv', \
	 'compoundSimilarity.tsv', 'geneEC.tsv', 'geneTissue.tsv', \
	 'compoundGene.tsv', 'targetDarkness.tsv', 'pathwayContainsPathway.tsv', \
	 'geneMolecularFunction.tsv', 'goHasPart.tsv', 'isaPhenotype.tsv']

index = {"vertice": 0, "edge_type": 0}
vertices = {}
edge_types = {}
edge_df = []

def process_vertice(item, hashmap, index, type_str):
	if item in hashmap:
		ret_id = hashmap[item]
	else:
		hashmap[item] = index[type_str]
		ret_id = index[type_str]
		index[type_str] += 1
	return ret_id

def process_edges(dir_edge, file_name):
	file_name = dir_edge + file_name
	edge_df = pd.read_csv(file_name, sep="\t", header=0)
	edge_df = edge_df[[':START_ID', ':END_ID', ':TYPE']]

	edge_df[":START_ID"] = edge_df[":START_ID"].apply(
		lambda x: process_vertice(x, vertices, index, "vertice"))

	edge_df[":END_ID"] = edge_df[":END_ID"].apply(
		lambda x: process_vertice(x, vertices, index, "vertice"))

	edge_df[":TYPE"] = edge_df[":TYPE"].apply(
		lambda x: process_vertice(x, edge_types, index, "edge_type"))

	return edge_df

for file in files_edge:
	edge_df.append(process_edges(dir_edge, file))

whole_pd = pd.concat(edge_df)
length = whole_pd.shape[0]

data_file = "data.csv"
file_write = open(data_file, "a")

for i in range(length):
	line = "%d %d %d %d\n" % (whole_pd.iloc[i][0], whole_pd.iloc[i][1], whole_pd.iloc[i][2], i)
	file_write.write(line)

file_write.close()

vertice_file = "vertice_list.tsv"
file_write = open(vertice_file, "a")

for key, val in vertices.items():
	line = "%s\t%d\n" % (key, val)
	file_write.write(line)

file_write.close()

edge_file = "edge_list.tsv"
file_write = open(edge_file, "a")

for key, val in edge_types.items():
	line = "%s\t%d\n" % (key, val)
	file_write.write(line)

file_write.close()
