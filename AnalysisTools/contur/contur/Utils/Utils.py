import os
def mkoutdir(outdir):
    "Function to make output directories"
    if not os.path.exists(outdir):
        try:
            os.makedirs(outdir)
        except:
            msg = "Can't make output directory '%s'" % outdir
            raise Exception(msg)
    if not os.access(outdir, os.W_OK):
        msg = "Can't write to output directory '%s'" % outdir
        raise Exception(msg)

def writeOutputHier(output, h):
    "Choose output file name and dir"
    hparts = h.strip("/").split("/")
    ana = "ANALYSIS"
    # if opts.HIER_OUTPUT:
    outdir = os.path.join('.', ana)
    #     ana = "_".join(hparts[:-1]) if len(hparts) > 1 else "ANALYSIS"
    #     outdir = os.path.join(opts.OUTDIR, ana)
    #     outfile = '%s.dat' % hparts[-1]
    # else:
    #     outdir = opts.OUTDIR
    #     outfile = '%s.dat' % "_".join(hparts)
    # # outdir = opts.OUTDIR
    # # outfile=output
    mkoutdir(outdir)
    outfilepath = os.path.join(outdir, output)
    f = open(outfilepath, 'w')
    for item in output:
        f.write(str(item) + "\n")
    #f.write(output)
    f.close()

def writeOutput(output, h):
    mkoutdir("ANALYSIS")
    f = open("./ANALYSIS/"+h, 'w')
    for item in output:
        f.write(str(item) + "\n")
    f.close()


