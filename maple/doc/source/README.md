
# MAPLE Introduction

MAPLE - Multi-purpose API Programming Language Extension

## Introduction


MAPLE has the following overarching goals:

1. Provide a common interface to multiple input/output methods for working with data including API, html, text, syslog, snmp, etc.
2. Enable these input/output methods to exchange information in real time or batch.
3. Where possible, maintain resiliency to updates to these input/output methods through intelligent adaptation.
4. Provide high level interfaces for non-programmers to access advanced input/output methods in a reusable fashion.
5. Enable fast onboard of new input/output methods.

MAPLE currently supports the FMC, AMP and ThreatGrid APIs with many others in development.

MAPLE currently offers two interfaces to supported input/output methods:

1. Programmatic with Python
2. MAPLE CLI - a configuration file type syntax allowing non-programmers to use MAPLE functionality.

Examples of using MAPLE with each interface will be given below.

## The MAPLE Object Model

---

### The "tree" object - MAPLE's top level controller object

The top level object for MAPLE is the "tree".  The tree provides the methods to instantiate and manage "leaf" objects (the specific input/output method interfaces).  The tree also provides helper methods common to all leaf types.

In future releases of MAPLE, the tree object will also provide translation services and multi-threaded leaf instance management.

Using Python a tree object is instantiated as follows:

***from maple.tree import MapleTree***
***tree=MapleTree(name=[tree_name],tree_dir=[file_path],logging_level=[logging_level])***

#### Tree Parameters
name: string, keyword, default=None - **Required**

    ​The name of this MAPLE tree.  The name is required and will be used to create a 
    working directory for the tree object.

tree_dir: string, keyword, default=None - **Required**

    ​The path to the desired location for the tree's working directory.
    Together with the tree name, will be used to create the tree's working 
    directory (e.g. tree_dir/name).

logging_level: string, keyword, default=INFO

    The desired logging level for the tree object (inherited by all leaf objects)

### The "leaf" object - MAPLEs input/output interface

The "leaf" object defines the native interface to the respective supported input/output methods.  The leaf object is instantiated and managed by the tree object.

Using Python, a leaf object is instantiated as follows:
```python
from maple.tree import MapleTree
# First get a tree object
maple_tree = MapleTree(logging_level='INFO', 
                       name='tree', 
                       tree_dir=r'C:\Users\rhindere\Documents\maple_working_dir')
# Now attach the leaf object...
leaf = \
	maple_tree.add_leaf_instance('[leaf_type]', name='[leaf_name]', [leaf specific keyword args])
```
#### Leaf Parameters
leaf_type: string, keyword, default=None - **Required**

    The text label for the leaf type. Currently one of; fmc, amp, tg (ThreatGrid).

name: string, keyword, default=None - **Required**

    The user defined name of the leaf instance. Together with the tree_dir, tree name, 
    will be used to create the leaf's working directory (e.g. leaf_dir/tree name/leaf name)

\[leaf specific keyword arguments passed to respective leaf object]: keyword

    "variable_name=variable_value"
	The leaf specific keywords required to instantiate and conduct leaf operations.  
	See specific leaf type for required and optional keyword arguments.

For a list of supported operations for each leaf, run maple_cli.py with the '-h' parameter.

### Currently supported leaf types

#### FMC REST API

MAPLE supports the FMC Rest API both for reading and writing.

MAPLE bases most FMC operations on the current API model as defined in the file named 'api-docs-fmcwithll.json' and obtained from the target FMC.  This file currently resides in the directory '/var/opt/CSCOpx/MDC/tomcat/vms/api/api-explorer/api'.  This file provides the API model to MAPLE:FMC which is used for many of the operations to derive urls, etc.  This file can be copied from the target FMC using scp and placed in a directory of the users choice.  The path to this file must be provided when the FMC leaf instance is instantiated.

##### FMC REST API - Instantiating an FMC leaf with Python

```python
from maple.tree import MapleTree
# First get a tree object
maple_tree = MapleTree(logging_level='INFO', 
                       name='tree', 
                       tree_dir=r'C:\Users\rhindere\Documents\maple_working_dir')
model_json_file= \
    r'C:\Users\rhindere\Documents\PycharmProjects\maple_project\maple\fmc\api-docs-fmcwithll.json'
FMC_leaf = \
	maple_tree.add_leaf_instance('fmc', name='fmc_leaf_1',
	json_file_path=model_json_file, FMC_host='10.1.101.39',
	FMC_username='rest_admin', FMC_password='C1sc0123', default_get_item_limit=200)
```

##### FMC Leaf Keyword Parameters (used in FMC leaf instantiation call)
json_file_path: string, keyword, default=None

    ​The path to the json model file.  This file is typically named 'api-docs-fmcwithll.json' and obtained from the 
    target FMC.  Typically resides in the directory /var/opt/CSCOpx/MDC/tomcat/vms/api/api-explorer/api'.  This file 
    provides the API model to MAPLE:FMC which is used for many of the operations to derive urls, etc.

FMC_host: string, keyword, default=None

    The ip address or fqdn of the FMC

FMC_port: integer, keyword, default=443

    The TCP/IP FMC management port

FMC_username: string, keyword, default=None

    The username for FMC

FMC_password: string, keyword, default=None

    The password for FMC

FMC_domain: string, keyword, default='Global'

    The target FMC domain.

API_path_delimiter: string, keyword, default='/'

    The default delimiter for the API path.

API_version: string, keyword, default='v1'

    The API version supported by the target FMC.

verify: boolean, keyword, default=False

    If True, verify the certificate.  If False disable verification.

default_get_item_limit: integer, keyword, default=400

    The default number of items to request in a GET request.

rpm_retries: integer, keyword, default=5

    The number of times to retry in response to a 429 error.

backoff_timer: integer, keyword, default=30

    The interval to wait between retry attempts

persist_responses: boolean, keyword, default=True

    If True, responses will be pickle persisted by url into the leaf's working directory.

restore_responses: boolean, keyword, default=False

    If True, pickled persistent responses will be restored prior to all other operations.

#### AMP REST API

MAPLE supports the AMP API for read/write.

At the time of writing, limited testing has been performed for write operations 

##### AMP REST API - Instantiating an AMP leaf with Python

```python
from maple.tree import MapleTree
# First get a tree object
maple_tree = MapleTree(logging_level='INFO', 
                       name='tree', 
                       tree_dir=r'C:\Users\rhindere\Documents\maple_working_dir')
# Now attach the AMP leaf...
AMP_leaf = maple_tree.add_leaf_instance('amp', name='amp_leaf_1',
                                        AMP_host='api.amp.cisco.com',
                                        AMP_API_client_ID='your_amp_client_id',
                                        AMP_API_key='your_amp_api_key',
                                        default_get_item_limit=200)
```

##### Parameters
AMP_host: string, keyword, default=None

    The ip address or fqdn of ThreatGrid

AMP_API_client_ID: string, keyword, default=None

    The AMP API client ID

AMP_API_key: string, keyword, default=None

    The AMP API key.

API_path_delimiter: string, keyword, default='/'

    The default delimiter for the API path.

API_version: string, keyword, default='v1'

    The API version supported by the target ThreatGrid.

verify: boolean, keyword, default=False

    If True, verify the certificate.  If False disable verification.

default_get_item_limit: integer, keyword, default=400

    The default number of items to request in a GET request.

rpm_retries: integer, keyword, default=5

    The number of times to retry in response to a 429 error.

backoff_timer: integer, keyword, default=30

    The interval to wait between retry attempts

persist_responses: boolean, keyword, default=True

    If True, responses will be pickle persisted by url into the leaf's working directory.

restore_responses: boolean, keyword, default=False

    If True, pickled persistent responses will be restored prior to all other operations.

#### ThreatGrid REST API

MAPLE supports the ThreatGrid API for read/write.

At the time of writing, limited testing has been performed for write operations 

##### ThreatGrid REST API - Instantiating an AMP leaf with Python

```python
from maple.tree import MapleTree
# First get a tree object
maple_tree = MapleTree(logging_level='INFO', 
                       name='tree', 
                       tree_dir=r'C:\Users\rhindere\Documents\maple_working_dir')
# Now attach the ThreatGrid leaf...
TG_leaf = maple_tree.add_leaf_instance(leaf_type='tg', name='tg_leaf_1',
                                       TG_host='panacea.threatgrid.com',
                                       TG_API_key='your_threatgrid_api_key',
                                       default_get_item_limit=200)
```

##### Parameters
TG_host: string, keyword, default=None

    The ip address or fqdn of ThreatGrid

TG_API_key: string, keyword, default=None

    The AMP API key.

API_path_delimiter: string, keyword, default='/'

    The default delimiter for the API path.

API_version: string, keyword, default='v1'

    The API version supported by the target ThreatGrid.

verify: boolean, keyword, default=False

    If True, verify the certificate.  If False disable verification.

default_get_item_limit: integer, keyword, default=400

    The default number of items to request in a GET request.

rpm_retries: integer, keyword, default=5

    The number of times to retry in response to a 429 error.

backoff_timer: integer, keyword, default=30

    The interval to wait between retry attempts

persist_responses: boolean, keyword, default=True

    If True, responses will be pickle persisted by url into the leaf's working directory.

restore_responses: boolean, keyword, default=False

    If True, pickled persistent responses will be restored prior to all other operations.

### MAPLE logging

MAPLE logs to "maple.log" located in tree_dir/tree_name

# MAPLE CLI

MAPLE CLI is a macro language interface for MAPLE.  It can be used to provide a simple macro language to peform MAPLE operations.

MAPLE CLI operations are defined using a combination of 3 input types:
1. Parameters passed to maple_cli.py on the command line.
2. Parameters stored in a parameters text file.
3. The operations config file which defines the actual MAPLE input/output operations.

MAPLE CLI parameters are primarily used for network connection and credential passing as well as some operational parameters such as file and directory paths.

## MAPLE Command Line Parameters
The following parameters can be passed to maple_cli.py either on the command line or in the parameters file:

Long form '-rest_admin_user' or short form '-rau', default='rest_admin'

    The REST admin user name configured in FMC

Long form '-rest_admin_password' or short form '-rap', default='C1sc0123'

    The REST admin user password configured in FMC

Long form '-operations_config_file' or short form '-ocf'

    The full path to the operations configuration file
Long form '-maple_working_dir' or short form '-mwd'

    The full path to the working directory for maple

### Passing parameters to MAPLE from a text file

maple_cli_parameters.txt

    File containing init parameters for maple_cli.  Edit this file to suit.  
    Username and password for FMC is in this file but you can remove them and pass instead on cli.  
    Edit for your own system if you choose to hard code them here.  Run maple_cli.py or 
    maple_cli.exe with -h to get a brief list of parameters and exposed operations.
    Pass this file as an argument to maple_cli and precede it with an @ symbol (enclosing 
    in quotes may be required one some OS types).  Example:
    
        maple_cli.py @maple_cli_parameters.txt

You can also pass any of the arguments in this file directly on the command line or use a combination of cli, file parameters. 

## The MAPLE operations configuration file

MAPLE CLI operations are defined in an "operations" configuration file.  This file is read by maple_cli to execute MAPLE operations.

Characteristics of the operations config file:

1. ​An INI config style file read by maple_cli.py to run API and utility functions. Example of this file below with inline comments:
2. Lines beginning with “RUN” are API or utility function calls.  RUN is always followed by an arbitrary unique label. RUN results are stored in a Python structure indexed by “RUN label”.
3. Anything enclosed in {} is a substitution.  In the example below, {tree$logging_level} will be substituted with the value in section “tree” and item “logging_level”.  When this construct appears before a set of parentheses, the substitution will be a class instance or class method stored in the respective section/item.
4. Anything preceded with “@” symbol will be substituted for the parameter of the same name in maple_cli_parameters.txt.
5. Comment out lines with a # symbol.

## MAPLE CLI output options - current support

The results can be displayed in a few different formats for now as follows:
1. output.tabbed_print

    Will dump the API responses to stdout.  Pipe to a file to save.
    
2. output.create_outline

    Will dump the results to an indented outline format suitable to import into Word or create mindmaps in “The Brain” or paste into MindManager.

3. output.create_pickle

    Creates a Python pickle file that can be reloaded for further processing.

4. output.pretty_print

    Uses the Python Pretty Print module to produce readable output of Python objects

## Example operations config file:

The following configurations file

```
#RH – section to define and create the top level object for MAPLE (the “tree” object).  Note “tree” is arbitrary and can be “foo” or whatever.  It is just a label.
[tree]
#RH – sets the logging level for MAPLE.  Log file is maple.log in default directory
logging_level=INFO
#RH – Instantiates the top level MAPLE object and stores the object reference to “RUN tree”. Since maple_working_dir is preceded by an '@', it will be replaced with
#the value passed either on the command line or in the parameters file.
RUN tree=MapleTree(name=mig_tree_1,tree_dir=@maple_working_dir,logging_level={tree$logging_level})
#RH – section to define and create the FMC leaf object for the MAPLE tree (the “leaf” object).  Note: 'leaf' is an arbitrary label.
[leaf:fmc_src]
host=10.1.101.40
domain=Global
type=fmc
name=fmc_mig_2
#RH – creates a substitution variable to hold the arguments for creating the leaf object.  Not necessary, only for readability
leaf_args=leaf_type={leaf:fmc_src$type},name={leaf:fmc_src$name},json_file_path=@model_json_file,FMC_host={leaf:fmc_src$host},FMC_username=@rest_admin_user,FMC_password=@rest_admin_password,FMC_domain={leaf:fmc_src$domain},restore_responses=False
#RH – adds the leaf instance for the FMC to the tree
RUN leaf={tree$RUN tree}.add_leaf_instance({leaf:fmc_src$leaf_args})
#RH – gets the domain id for the given domain
RUN domain_id={leaf:fmc_src$RUN leaf}.get_domain_id(domain={leaf:fmc_srcdomain})
[get]
# If security zones are to be migrated, the device records and physical interfaces need to be obtained due to json model anomalies in fmc
RUN dr = {leaf:fmc_srcRUN leaf}.get_all_items(url=devices/devicerecords)
# Get a list of all the device
RUN did = {leaf:fmc_srcRUN leaf}.query_json_field(query_field=items.id,json_to_query={get$RUN dr})
#Get all device records
#Run multiple get iterating over values in the device id list substituting each value in the list for ~id~
drs = devices/devicerecords/~id~
RUN drq = {leaf:fmc_srcRUN leaf}.query_with_list(query_url={get$drs},query_list={get$RUN did})
RUN pp_drq=output.pretty_print(_object={get$RUN drq})
#Get all physical interfaces for each device
#Run multiple get iterating over values in the device id list substituting each value in the list for ~id~
piu = devices/devicerecords/~id~/physicalinterfaces
RUN piq = {leaf:fmc_srcRUN leaf}.query_with_list(query_url={get$piu},query_list={get$RUN did})
RUN pp_piq=output.pretty_print(_object={get$RUN piq})
#Get the nat policies
RUN nat={leaf:fmc_srcRUN leaf}.walk_API_path_gets(url=policy/ftdnatpolicies)
RUN pp_nat=output.pretty_print(_object={get$RUN nat})
#Get the access policies
RUN ap={leaf:fmc_srcRUN leaf}.walk_API_path_gets(url=policy/accesspolicies)
RUN pp_ap=output.pretty_print(_object={get$RUN ap})
[leaf:fmc_1]
host=10.1.101.39
domain=Global
type=fmc
name=fmc_mig_1
leaf_args=leaf_type={leaf:fmc_1$type},name={leaf:fmc_1$name},json_file_path=@model_json_file,FMC_host={leaf:fmc_1$host},FMC_username=@rest_admin_user,FMC_password=@rest_admin_password,FMC_domain={leaf:fmc_1$domain},restore_responses=False
RUN leaf={tree$RUN tree}.add_leaf_instance({leaf:fmc_1$leaf_args})
RUN domain_id={leaf:fmc_1$RUN leaf}.get_domain_id(domain={leaf:fmc_1$domain})
[leaf]
RUN migrate = {leaf:fmc_1$RUN leaf}.or_migrate_config(source_config_path=mig_tree_1\\fmc_mig_2)
```

## MAPLE CLI Logging

MAPLE CLI logs to "maple_cli.log" in the directory where it is launched.