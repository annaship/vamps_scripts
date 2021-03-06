#!/usr/bin/env python

"""
  create_counts_lookup.py


"""

import sys,os,io
import argparse
try:
    import pymysql as mysql
except ImportError:
    import MySQLdb as mysql
except:
    raise
import json
import shutil
import datetime
import socket
from collections import defaultdict

today     = str(datetime.date.today())


"""

"""


parser = argparse.ArgumentParser(description="")


def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

# def go_list(args):
# 
#     #
#     file_dids = []
# 
#     metadata_lookup = convert_keys_to_string(read_original_metadata())
#     (projects_by_did, project_id_lookup, project_lookup) = get_project_lookup(args) # from database
#     #print(project_lookup)
#     required_metadata_fields = get_required_metadata_fields(args)
#     #print('file_dids')
#     #print(metadata_lookup)  ## <-- lookup by did
#     
#     project_id_order = list(project_id_lookup.keys())
#     project_id_order.sort()
#     #metadata_dids = metadata_lookup.keys()
#     #
#    
#     failed_projects = []
#     no_req_data_found = 0
#     no_file_found = {}          # 2only for metadata BULK FILE: if did NOT found
#     mismatch_data = {}          # 1metadata mismatch between DATABASE and metadata BULK FILE
#     cust_rowcount_data = {}     # 4dataset count unequal between DATABASE custom metadata table and DATABASE datasets table
#     other_problem = {}
#     did_file_problem = {}       # 5did FILES: if taxcounts ={} or empty file present
#     did_file_problem_by_pid = defaultdict(list)
#     no_req_metadata = {}        # 3if no required metadata found in DATABASE
#     num_cust_rows = 0 
#     
#     
#         
#     for pid in project_id_order:
#         # go project by project
#         sql_dids =  "','".join(project_id_lookup[pid])
#         ds_count = len(project_id_lookup[pid]) 
#         q = "SELECT dataset_id, "+ ', '.join(required_metadata_fields) +" from required_metadata_info WHERE dataset_id in ('%s')" % (sql_dids)
#         if args.verbose:
#             print(q)
#         clean_project = True
#         num = 0
#         cur.execute(q)
#         numrows = cur.rowcount
#         if numrows == 0:
#             no_req_data_found += 1
#             #print(str(no_req_data_found)+') No Required metadata for project: '+str(project_lookup[pid])+' ('+str(pid)+')')
#             if pid not in no_req_metadata:
#                     no_req_metadata[pid] = project_lookup[pid]
#             continue
# 
#         for row in cur.fetchall():
#             did = str(row[0])
#             did_file1 = os.path.join(args.json_file_path, NODE_DATABASE+'--datasets_silva119', str(did)+'.json')
#             did_file2 = os.path.join(args.json_file_path, NODE_DATABASE+'--datasets_rdp2.6"',  str(did)+'.json')
#             did_file3 = os.path.join(args.json_file_path, NODE_DATABASE+'--datasets_generic',  str(did)+'.json')
#             
#             #if did == '3938':
#             if did not in metadata_lookup:
#                 if pid not in no_file_found:
#                     no_file_found[pid] = project_lookup[pid]
#                 clean_project = False
#             else:
#                 for i,item in enumerate(required_metadata_fields):
#                    
#                     if item in metadata_lookup[did]:
#                         db_val = str(row[i+1])
#                         if str(metadata_lookup[did][item]) != db_val :
#                             if args.verbose:
#                                 print('pid:'+str(pid) +' -- '+project_lookup[pid]+' -- did:' +did+'  no match-1 for `'+item+'`:',metadata_lookup[did][item],' - ',db_val)
#                             if pid not in mismatch_data:
#                                 mismatch_data[pid] = project_lookup[pid]
#                             clean_project = False
#                     else:
#                          if args.verbose:
#                             print('pid:'+str(pid) +' -- '+'--'+project_lookup[pid]+' -- did:' +did+' -- `'+item+'` item not found in req metadata file-1\n')
#                          if pid not in other_problem:
#                             other_problem[pid] = project_lookup[pid]
#                          clean_project = False
#             
#             try:
#                 #did_file = os.path.join(args.json_file_path, NODE_DATABASE+'--datasets_silva119', str(did)+'.json')
#                 fp = open(did_file1)
#                 file_data = json.load(fp)
#                 if not file_data or not file_data['taxcounts']:
#                     did_file_problem[pid] = project_lookup[pid] 
#                     did_file_problem_by_pid[str(pid)].append(str(did))
#                 fp.close()
#             except:
#                 did_file_problem[pid] = project_lookup[pid]
#                 if args.verbose:
#                     print('pid:'+str(pid) +' -- '+'--'+project_lookup[pid]+' -- did:' +did+' -- Could not open did file-1\n')
#         
#         
#         
#         custom_metadata_file = 'custom_metadata_'+str(pid)
#         
#         q1 = "SHOW fields from "+custom_metadata_file
#         q2 = "SELECT * from "+custom_metadata_file
# 
#         fields = []
#         try:
#             cur.execute(q1)
#             rows = cur.fetchall()
#             for row in rows:
#                 
#                 field = str(row[0])
#                 if field !=  custom_metadata_file+'_id' and field != 'dataset_id' and field != 'project_id':
#                     fields.append(field) # starts with idx 2
#             
#             if args.verbose:
#                 print(q2)
#             # query2 q2 = "SELECT * from "+custom_metadata_file
#             cur.execute(q2)
#             num_cust_rows = cur.rowcount
#             if num_cust_rows != ds_count:
#                 cust_rowcount_data[pid] = project_lookup[pid]
#             
#             rows = cur.fetchall()
#             for row in rows:
#                 did = str(row[1]) # first is custom_metadata_<pid>_id, second is did
#                 
#                 for i,item in enumerate(fields):
# 
#                     #print('pid:',pid,'did:',did, 'item:',item, metadata_lookup[did], project_lookup[pid])
#                     if item in metadata_lookup[did]:
#                         #print(item,i,'row',row)
#                         db_val = str(row[i+2])
# 
#                         if str(metadata_lookup[did][item]) != db_val:
#                             if args.verbose:
#                                 print('pid:'+str(pid) +' -- '+project_lookup[pid]+' -- did:' +did+'  no match-2 for `'+item+'`:',metadata_lookup[did][item],'!=',db_val)
#                             if pid not in mismatch_data:
#                                 mismatch_data[pid] = project_lookup[pid]
#                             clean_project = False
#                     else:
#                         if args.verbose:
#                             print( 'pid:'+str(pid) +' -- '+project_lookup[pid]+' -- did:' +did+' -- `'+item+'` item not found in cust metadata file-2\n')
#                         if pid not in other_problem:
#                             other_problem[pid] = project_lookup[pid]
#                         clean_project = False
#         except:
#             pass
#         #sys.exit()
#         #if not clean_project:
#         #      failed_projects.append('pid:'+str(pid)+' -- '+project_lookup[pid])
#     missing_seqs = {}
#     q2_base = "SELECT sequence_pdr_info_id from sequence_pdr_info where dataset_id in ('%s')"
#     if args.verbose:
#         print(q2_base)
#     if args.search_seqs:
#         print('Searching for sequences in sequence_pdr_info')        
#         for pid in project_id_order:
#             # go project by project
#             sql_dids =  "','".join(project_id_lookup[pid])
#             ds_count = len(project_id_lookup[pid]) 
#             q2 = q2_base % (sql_dids)                
#             clean_project = True
#             num = 0
#             cur.execute(q2)
#             numrows = cur.rowcount
#             if numrows == 0:
#                 missing_seqs[pid] = project_lookup[pid]
#                 if args.verbose:
#                     print('No sequences found::pid:'+str(pid) +' -- '+project_lookup[pid])
#         
#     print()
#     print('*'*60)
#     print('Failed projects:')
#     
#     print()
#     print('\t1) METADATA MIS-MATCHES BETWEEN BULK FILE AND DBASE (Assumes same for did file) (re-build should work):')
#     if not len(mismatch_data):
#         print('\t **Clean**')
#     else:
#         for pid in mismatch_data:
#             print('\t pid:',pid,' -- ',mismatch_data[pid])
#         print('\t PID List:',','.join([str(n) for n in mismatch_data.keys()]))
#     print()
#     print('\t2) NO DID FOUND IN METADATA BULK FILE (Assumes no did file found either) (re-build should work):')
#     if not len(no_file_found):
#         print('\t **Clean**')
#     else:
#         for pid in no_file_found:
#             print('\t pid:',pid,' -- ',no_file_found[pid])
#         print('\t PID List:',','.join([str(n) for n in no_file_found.keys()]))
#     print()
#     print('\t3) NO REQUIRED METADATA FOUND IN DATABASE (re-install project or add by hand -- re-build won\'t help):')
#     if not len(no_req_metadata):
#         print('\t **Clean**')
#     else:
#         for pid in no_req_metadata:
#             print('\t pid:',pid,' -- ',no_req_metadata[pid])
#         print('\t PID List:',','.join([str(n) for n in no_req_metadata.keys()]))
#     print()
#     print('\t4) DATABASE: Dataset count is different between `dataset` and `custom_metadata_xxx` tables (re-build won\'t help):')
#     if not len(cust_rowcount_data):
#         print('\t **Clean**')
#     else:
#         for pid in cust_rowcount_data:
#             print('\t pid:',pid,' -- ',cust_rowcount_data[pid])
#         print('\t PID List:',','.join([str(n) for n in cust_rowcount_data.keys()]))
#     print()
#     print('\t5) DID FILES: zero-length file or taxcounts={}:')
#     if not len(did_file_problem):
#         print('\t **Clean**')
#     else:
#         for pid in did_file_problem:
#             print('\t pid:',pid,' -- ',did_file_problem[pid])
#         print('\t PID List:',','.join([str(n) for n in did_file_problem.keys()]))
# 
#         if args.show_dids:
#             for pid, dids in did_file_problem_by_pid.items():
#                 print('\t pid: %s, dids: %s' % (pid, ', '.join(dids)))
#         
#     print()
#     print('\t6) OTHER (rare -- Possible DID mis-match or case difference for metadata -- re-build may or may not help):')
#     if not len(other_problem):
#         print('\t **Clean**')
#     else:
#         for pid in other_problem:
#             print('\t pid:',pid,' -- ',other_problem[pid])
#         print('\t PID List:',','.join([str(n) for n in other_problem.keys()]))
#     
#     print()
#     if args.search_seqs:
#         print('\t7) SEQUENCES (all-or-nothing: NO seqs found in `sequence_pdr_info` table):')
#         if not len(missing_seqs):
#             print('\t **Clean**')
#         else:
#             for pid in missing_seqs:
#                 print('\t pid:',pid,' -- ',missing_seqs[pid])
#             print('\t PID List:',','.join([str(n) for n in missing_seqs.keys()]))
#         print()
#     all_to_rebuild = list(other_problem.keys()) + list(mismatch_data.keys()) + list(no_file_found.keys()) + list(did_file_problem.keys()) 
#      
#     print("To rebuild: \ncd /groups/vampsweb/new_vamps_maintenance_scripts/; ./rebuild_vamps_files.py -host "+args.dbhost+" -pids '%s'; mail_done" % (", ".join(list(set(all_to_rebuild)))))    
#     print("Number of files that should be rebuilt:",len(other_problem)+len(mismatch_data)+len(no_file_found))
#     print('*'*60)
# 
# def read_original_metadata():
#     file_path = os.path.join(args.json_file_path,NODE_DATABASE+'--metadata.json')
#     try:
#         with open(file_path) as data_file:
#             data = json.load(data_file)
#     except:
#         print("could not read json file",file_path,'-Exiting')
#         sys.exit(1)
#     return data
# 
# 
# def get_required_metadata_fields(args):
#     q =  "SHOW fields from required_metadata_info"
#     cur.execute(q)
#     md_fields = []
#     fields_not_wanted = ['required_metadata_id','dataset_id','created_at','updated_at']
#     for row in cur.fetchall():
#         if row[0] not in fields_not_wanted:
#             md_fields.append(row[0])
#     return md_fields
# 
# def get_project_lookup(args):
#     q =  "SELECT dataset_id, dataset.project_id, project from project"
#     q += " JOIN dataset using(project_id) where project not like '%_Sgun' order by project"
# 
#     num = 0
#     cur.execute(q)
#    
#     projects_by_did = {}
#     project_id_lookup = {}
#     project_lookup = {}
# 
#     for row in cur.fetchall():
#         did = str(row[0])
#         pid = str(row[1])
#         pj  = row[2]
#         project_lookup[pid]  = pj
#         projects_by_did[did] = pj
#         if pid in project_id_lookup:
#             project_id_lookup[pid].append(str(did))
#         else:
#             project_id_lookup[pid] = [str(did)]
# 
#     return (projects_by_did, project_id_lookup, project_lookup)
def list_group_file_metadata_names():
    group_file = os.path.join(args.json_file_path,'vamps2--metadata.json')
    metadata_items = {}  # lookup
    with open(group_file) as f:
        data = json.load(f)
        for did in data:
            
            for mdname in data[did]:
                if mdname in metadata_items:
                    metadata_items[mdname].append(did)
                else:                
                    metadata_items[mdname] = [did]
    
    metadata_items_list = list(metadata_items.keys())
    metadata_items_list.sort(key=lambda y: y.lower()) # sorts case insensitive
    count = 0
    for mdname in metadata_items_list:
        print(mdname)
        count +=1
    print('Count=',count)
        
        
def search_group_file():
    group_file = os.path.join(args.json_file_path,'vamps2--metadata.json')
    print("Searching group_file...")
    dids = []
    with open(group_file) as f:
        data = json.load(f)
        for did in data:
            #print(data[did])
            if args.field_name in data[did]:
                print('did:',did,' field:',args.field_name,' val:',data[did][args.field_name])
                dids.append(did)
    if dids:
        q = "SELECT distinct project_id,project from dataset JOIN project using(project_id) WHERE dataset_id in (%s)"
        q = q % (','.join(dids))
        print("did list: (length:",str(len(dids))+')',sorted(dids))
        cur.execute(q)
        for row in cur.fetchall():
            print(row)
        
    else:
        print(args.field_name,'Not Found')
#
#
#
def search_single_files():
    dir_silva  = os.path.join(args.json_file_path,'vamps2--datasets_silva119')
    dir_rdp    = os.path.join(args.json_file_path,'vamps2--datasets_rdp2.6')
    dir_generic= os.path.join(args.json_file_path,'vamps2--datasets_generic')
    search_dirs = [dir_silva,dir_rdp,dir_generic]
    
    dids = []
    for dir in search_dirs:
        print("Searching single_files in:",dir)
        files = os.listdir(dir)
        for f in files:
            json_file = os.path.join(dir,f)
            did = f[:-5]
            with open(json_file) as fp:
                data = json.load(fp)
                if args.field_name in data['metadata']:
                    print("Found `"+args.field_name+"` in",json_file,"val=",data['metadata'][args.field_name])
                    dids.append(did)
                    
    if dids:
        q = "SELECT distinct project_id,project from dataset JOIN project using(project_id) WHERE dataset_id in (%s)"
        q = q % (','.join(dids))
        print("did list: (length:",str(len(dids))+')',sorted(dids))
        cur.execute(q)
        for row in cur.fetchall():
            print(row)
    else:
        print(args.field_name,'Not Found')
    
#
#
#
if __name__ == '__main__':

    myusage = """
    
    metadata_files_synchrony.py
    
        -host/--host        vampsdb, vampsdev    dbhost:  [Default: localhost]
        
        -v/--verbose    lots of talk          
        
        
        
        -json_file_path/--json_file_path
        
        -s/--search_where   choices=['group_file', 'single_files', 'database']  DEFAULT='' REQUIRED if not using -l
        -f/--field_name     to search for; DEFAULT='dataset_id'
        -l/--list   List metadata names from group file [TAKES PRECEDENCE over others]
    
    """

    parser.add_argument("-json_file_path", "--json_file_path",
                required=False,  action='store', dest = "json_file_path",  default='json',
                help="Not usually needed if -host is accurate")
    parser.add_argument("-host", "--host",
                required=False,  action='store', dest = "dbhost",  default='localhost',
                help="choices=['vampsdb','vampsdev','localhost']")
    parser.add_argument("-v", "--verbose",
                required=False,  action='store_true',  dest = "verbose",  default=False,
                help="")
    parser.add_argument("-s", "--search_where",
                required=False,  action='store',  choices=['group_file', 'single_files', 'database'], dest = "search_where",  default='group_file',
                help="group_file single_files, database")
    parser.add_argument("-f", "--field_name",
                required=False,  action='store',  dest = "field_name",  default='', 
                help="MetadataName to search for")
    parser.add_argument("-l", "--list",
                required=False,  action='store_true',  dest = "list",  default=False,
                help="List metadata from group file TAKES PRECEDENCE")
    if len(sys.argv[1:]) == 0:
        print(myusage)
        sys.exit()
    args = parser.parse_args()

    print(args)
    if args.dbhost == 'vamps' or args.dbhost == 'vampsdb' or args.dbhost == 'bpcweb8' :
        args.json_file_path = '/groups/vampsweb/vamps/nodejs/json'
        args.dbhost = 'vampsdb'
        args.NODE_DATABASE = 'vamps2'

    elif args.dbhost == 'vampsdev' or args.dbhost == 'bpcweb7':
        args.json_file_path = '/groups/vampsweb/vampsdev/nodejs/json'
        args.NODE_DATABASE = 'vamps2'
        args.dbhost = 'bpcweb7'
    elif args.dbhost == 'localhost' and (socket.gethostname() == 'Annas-MacBook.local' or socket.gethostname() == 'Annas-MacBook-new.local'):
        args.NODE_DATABASE = 'vamps2'
        args.dbhost = 'localhost'
    else:
        args.NODE_DATABASE = 'vamps_development'
        args.dbhost = 'localhost'
   

    if os.path.exists(args.json_file_path):
        print('Validated: json file path')
    else:
        print(myusage)
        print("Could not find json directory: '",args.json_file_path,"' Try adding -host to CL -Exiting")
        sys.exit(-1)
    print("\nARGS: dbhost  =",args.dbhost)
    print("ARGS: json_dir=",args.json_file_path)

    db = mysql.connect(host=args.dbhost, # your host, usually localhost
                             read_default_file="~/.my.cnf_node"  )
    cur = db.cursor()
    if args.NODE_DATABASE:
        NODE_DATABASE = args.NODE_DATABASE
    else:
        cur.execute("SHOW databases like 'vamps%'")
        dbs = []
        print(myusage)
        db_str = ''
        for i, row in enumerate(cur.fetchall()):
            dbs.append(row[0])
            db_str += str(i)+'-'+row[0]+';  '
        print(db_str)
        db_no = input("\nchoose database number: ")
        if int(db_no) < len(dbs):
            NODE_DATABASE = dbs[db_no]
        else:
            sys.exit("unrecognized number -- Exiting")

    print()
    cur.execute("USE "+NODE_DATABASE)

    
    searches = ['database','group_file','single_files']
    if args.list:
        list_group_file_metadata_names()
    else:
        if args.field_name == '':
            print(myusage)
            sys.exit()
        if args.search_where not in searches:
            print("search_where has to be one of:  'database', 'group_file', 'single_files'")
            sys.exit()
        if args.search_where == 'group_file':
            search_group_file()
        elif args.search_where == 'single_files':
            search_single_files()
        elif args.search_where == 'database':
            print("Searching the database is not coded yet!")
        else:
            pass
            
