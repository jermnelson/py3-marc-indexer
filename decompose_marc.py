__author__ = "Jeremy Nelson"
import os,pymarc,sys
try:
    import argparse
    arg_parser = argparse.ArgumentParser(description="Create individual records from MARC file")
    arg_parser.add_argument('filename',
                        nargs="+",
                        help="[filename] Name of MARC file")
except ImportError:
    import optparse
    arg_parser = optparse.OptionParser()
    arg_parser.add_option("-f","--file",dest="filename")

def save_individual_record(marc_record,shard_num):
    bib_number = marc_record['907']['a'][1:-1]
    path = os.path.join(os.path.abspath("."),
                        "shard{0}".format(shard_num),
                        "{0}.mrc".format(bib_number))
    marc_writer = pymarc.MARCWriter(open(path,'wb'))
    marc_writer.write(marc_record)
    marc_writer.close()

def process_file(marc_file,shard_size):
    shard_num = -1
    counter = 0
    marc_reader = pymarc.MARCReader(open(marc_file,"rb"),utf8_handling="ignore")
    error_record = open(os.path.join(os.path.abspath("."),"errors.txt"),"w")
    for record in marc_reader:
        try:
            if not counter%shard_size:
                shard_num += 1
                os.mkdir(os.path.join(os.path.abspath("."),
                                      "shard{0}".format(shard_num)))

            if counter%1000:
                sys.stderr.write(".")
            else:
                sys.stderr.write(str(counter))
            save_individual_record(record,shard_num)
            counter += 1
        except:
            error_record.write("Error %s at count %s\n" % (sys.exc_info()[0],
                                                           counter))
    error_record.close()


if __name__ == '__main__':
    args = arg_parser.parse_args()
    if hasattr(args,"filename"):
        process_file(args.filename[0],50000)
    else:
        process_file(args[0].filename,50000)
