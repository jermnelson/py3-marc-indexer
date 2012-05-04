"""
 Creates a MARC records shards from a full MARC record
"""
import pymarc,sys,argparse

arg_parser = argparse.ArgumentParser(description='Index MARC records into Solr')
arg_parser.add_argument('filename',
                        nargs="+",
                        help="[filename] Name of MARC file to be shared")
arg_parser.add_argument('--shard_size',
                        nargs="+",
                        default=50000,
                        help="[shard_size] Size of shard, default is 50000")

def shard(shard_size,
          input_marc_filename):
    print("STARTING MARC Random test file generator")
    marc_file = pymarc.MARCReader(open(input_marc_filename,'rb'))
    root_path = input_marc_filename.split(".")[0]
    error_file = pymarc.MARCWriter(open('%s-error.mrc' % root_path,'wb'))
    all_marc_recs = []
    count = 1
    marc_output_filename = '%s-%sk-%sk.mrc' % (root_path,
                                               count,
                                               count+shard_size)
    marc_writer = pymarc.MARCWriter(open(marc_output_filename,'wb'))
    print("\tStart cycling through MARC file")
    try:
        for record in marc_file:
            if count%1000:
                sys.stderr.write(".")
            else:
                sys.stderr.write(str(count))
            if not count%shard_size:
                print("Attempted to create shard %s" % marc_output_filename)
                if marc_writer is not None:
                    marc_writer.close()
                marc_output_filename = '%s-%sk-%sk.mrc' % (root_path,
                                                           count,
                                                           count+shard_size)
                marc_writer = pymarc.MARCWriter(open(marc_output_filename))
                
            try:
                marc_writer.write(record)
            except:
                print("\tError %s writing record %s " % (sys.exc_info(),
                                                         count))
                try:
                    error_file.write(record)
                except:
                    print("Can't read/recorcd at count=%s" % count)
            count += 1
    except:
        print("Error writing record %s" % count)
##    if not marc_writer is None:
##        marc_writer.close()
    print("\tFinished cycling through MARC file, generating random output file")
    print("FINISHED MARC Random test file generator")

if __name__ == '__main__':
    args = arg_parser.parse_args()
    if 'shard_size' is args:
        SHARD_SIZE = args.shard_size
    else:
        SHARD_SIZE = 50000 # Default
        print("Using default shard_size of %s" % SHARD_SIZE)
    shard(SHARD_SIZE,args.filename[0])
    
        
                          
    



    
