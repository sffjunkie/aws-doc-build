import argparse
import os
import re
import subprocess
import sys
import tempfile

# s, source-dir
# i, index-file
# d, data-dir
# m, metadata-file
# o, output-file
# c, css-file

p = argparse.ArgumentParser()
p.add_argument('-s', '--source-dir', help='Directory that contains the source files', default='doc_source')
p.add_argument('-d', '--data-dir', help='Pandoc data directory', default='pandoc_data')
p.add_argument('-m', '--metadata-file', help='Metadata file', default='document.yaml')
p.add_argument('-c', '--css-file', help='CSS file', default='epub.css')
p.add_argument('-o', '--output-file', help='Output file')
p.add_argument('index', help='Index file')


output_type = 'epub'
output_filename = os.path.join('..', '%s.%s' % (os.path.basename(os.path.dirname(os.path.abspath(__file__))), output_type))

md_re = re.compile('\(([\w\-_]+\.md)\)')
index_file = 'index.md'
metadata_file = os.path.join('..', 'document.yaml')
files_to_process = [metadata_file, index_file]
os.chdir('doc_source')
with open(index_file) as fp:
	for line in fp:
		fname = md_re.findall(line)
		for item in fname:
			files_to_process.append(os.path.join(item))

args = ['pandoc', '-o', output_filename, '--data-dir', 'pandoc_data']
if output_type != 'pdf':
	args.extend(['-t', output_type])

output_file = tempfile.NamedTemporaryFile(delete=False)
for fname in files_to_process:
	with open(fname, 'rb') as input_file:
		output_file.write(input_file.read(-1))
	output_file.write(b'\n\n')
output_file.close()

args.append(output_file.name)
subprocess.run(args)

os.remove(output_file.name)
