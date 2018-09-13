# Directory functions

<pre>
dir_mod.<b>check_os()</b>
</pre>
> Confirms that operating system is Unix or Windows. If operating system is neither, raises exception. 

<ul>
<b>Note:</b> 
<br>
<code>gslab_make</code> only supports Unix or Windows. 
</ul>

<br>

<pre>
dir_mod.<b>clear_dir(</b><i>dir_list</i><b>)</b>
</pre>
> Clears all directories in list <code>dir_list</code> using system command. Safely clears symbolic links.

<ul>
<b>Example:</b>
<br>
<code>clear_dir(['dir1', 'dir2'])</code> clears directories 'dir1' and 'dir2'. 
<br>
<br>
<b>Notes:</b>
<br>
To clear a directory means to remove all contents of a directory. If the directory is nonexistent, the directory is created.
<br>
<br>
Directories can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
</ul>

<br>

<pre>
dir_mod.<b>unzip(</b><i>zip_path, output_dir</i><b>)</b>
</pre>
> Unzips file `zip_path` into directory `output_dir`.

<br>

<pre>
dir_mod.<b>zip_dir(</b><i>source_dir, zip_dest</i><b>)</b>
</pre>
> Zips directory `source_dir` into file `zip_dest`. 

<br>

# Logging functions

<pre>
write_logs.<b>set_option(</b><i>*default_paths</i><b>)</b>
</pre>
> Sets default paths. The following default paths can be changed:
>
> * `link_dir` = '../input/'
> 
>     * Default path for writing symbolic links to inputs. 
>
> * `temp_dir` = '../temp/'
> 
>     * Default path for writing temporary files.
>
> * `output_dir` = '../output/' 
> 
>     * Default path for writing Lyx documents. 
>     * Default path for finding outputs for logging.
>
> * `makelog` = '../log/make.log'
> 
>     * Default path for writing make log.
>
> * `output_statslog` = '../log/output_stats.log'
> 
>     * Default path for writing log containing output statistics.
>
> * `output_headslog` = '../log/output_heads.log'
> 
>     * Default path for writing log containing output headers.
>
> * `link_maplog` = '../log/link_map.log'
> 
>     * Default path for writing log containing link mappings.
>
> * `link_statslog` = '../log/link_stats.log'
> 
>     * Default path for writing log containing link statistics.
>
> * `link_headslog` = '../log/link_heads.log'
> 
>     * Default path for writing log containing link headers.	

<ul>
<b>Example:</b>
<br>
<code>set_option(makelog = 'file1')</code> changes the default make log path to 'file1'. All future functions will use 'file1' as the make log path. 
</ul>

<br>

<pre>
write_logs.<b>start_makelog(</b><i>makelog = '../log/make.log'</i><b>)</b>
</pre>
> Starts new make log at file `makelog`, recording start time. Sets start condition for make log to boolean `True`, which is needed by other functions to confirm make log exists.

<br>

<pre>
write_logs.<b>end_makelog(</b><i>makelog = '../log/make.log'</i><b>)</b>
</pre>
> Ends make log at file `makelog`, recording end time. 

<br>

<pre>
write_logs.<b>write_output_logs(</b><i> 
    output_dir = '../output/',
    output_statslog = '../log/output_stats.log', 
    output_headslog = '../log/output_heads.log', 
    recursive = float('inf')</i><b>
)</b>
</pre>
> Logs the following information for all files contained in directory `output_dir`:
>
> * File name (in file `output_statslog`)
>
> * Last modified (in file `output_statslog`)
>
> * File size (in file `output_statslog`)
>
> * File head (in file `output_headslog`)
>
> When walking through directory `output_dir`, float `recursive` determines level of depth to walk.

<br>

# Linking functions
<pre>
create_links.<b>create_links(</b><i>
    file_list, 
	link_dir = '../input/'</i>, 
	makelog = '../log/make.log'</i><b>
)</b> 
</pre>
> Create symbolic links using instructions contained in files of list `file_list`. Symbolic links are written in directory `link_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Example 1:</b>
<br>
<code>create_links(['file1', 'file2'])</code> uses files 'file1' and 'file2' to create symbolic links.
<br>
<br>
Suppose file 'file1' contained the following text:
<br>
</ul>
<code># Each line of this file should contain a symbolic link and target delimited by a tab</code>
<code># Lines beginning with # are ignored</code>
<code>symlink1    target1</code>
<code>symlink2    target2</code>
<ul>
Symbolic links <code>symlink1</code> and <code>symlink2</code> would be created in directory <code>link_dir</code>. Their targets would be <code>target1</code> and <code>target2</code>, respectively. 
<br>
<br>
<b>Notes:</b>
<br>
Files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Symbolic links and their targets can also be specified with the * shell pattern. The number of wildcards must be the same for both symbolic links and targets.
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>target1</code>
<br>
<code>target2</code>
<br>
<code>target3</code>
<br>
<br>
Specifying <code>symlink*   target*</code> in one of your files would create the following symbolic links in <code>link_dir</code>:
<br>
<code>symlink1</code>
<br>
<code>symlink2</code>
<br>
<code>symlink3</code>
</pre>
</ul>

<br>

# Link logging functions
<pre>
write_link_logs.<b>write_link_logs(</b><i>
    link_map, 
    link_statslog = '../log/link_stats.log', 
    link_headslog = '../log/link_heads.log', 
    link_maplog = '../log/link_map.log', 
    recursive = float('inf')</i><b>
)</b>
</pre>

> Logs the following information for files contained in all mappings of list `link_map` (returned by `create_links.create_links`):
> 
> * Mapping of symbolic links to targets (in file `link_maplog`)
>
> * Details on files contained in targets: 			
>
>     * File name (in file `link_statslog`)
>
>     * Last modified (infile `link_statslog`)
>
>     * File size (in file `link_statslog`)
>
>     * File head (in file `link_headslog`)
>
> When walking through targets, float `recursive` determines level of depth to walk.

<br> 

# Program functions

<pre>
run_program.<b>execute_command(</b><i>
    command, 
    osname = os.name, 
    shell = False, 
    makelog = '../log/make.log', 
    log = ''</i><b>
)</b>
</pre>
> Runs system command `command`, assuming operating system `osname` and shell execution boolean `shell`. Outputs are appended to make log file `makelog` and written to program log file `log`. Status messages are appended to make log `makelog`.
> 

<ul>
<b>Notes:</b> 
<br>
For more information on shell execution, see <a href = 'https://docs.python.org/2/library/subprocess.html#frequently-used-arguments'>here</a>.
<br>
<br>
To prevent appending outputs to make log, specify <code>makelog</code> = ''.
<br>
<br>
By default, program log is not written as <code>log</code> = ''.
<br>
<br>
<b>Notes:</b> 
<br>
<code>execute_command('ls', makelog = '', log = 'file')</code> executes the 'ls' command, writes outputs to program log 'file', but does not append status messages or outputs to make log.
</ul>

<br> 

#### Unless specified otherwise, the following program functions will use default settings to run your program. See the setting section below for more information.
<br>

<pre>
run_program.<b>run_stata(program, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.do'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_stata(program = 'script.do')</code>
</ul>


<br>

<pre>
run_program.<b>run_matlab(program, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.m'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_matlab(program = 'script.m')</code>
</ul>

<br>

<pre>
run_program.<b>run_perl(program, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.pl'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_perl(program = 'script.pl')</code>
</ul>


<br>

<pre>
run_program.<b>run_python(program, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.py'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_python(program = 'script.py')</code>
</ul>


<br>

<pre>
run_program.<b>run_mathematica(program, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.m'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_mathematica(program = 'script.m')</code>
</ul>


<br>

<pre>
run_program.<b>run_stat_transfer(program, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.stc'` or `'script.stcmd'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_stat_transfer(program = 'script.stc')</code>
</ul>


<br>

<pre>
run_program.<b>run_lyx(program, doctype = '', pdfout = '', *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.lyx'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_lyx(program = 'script.lyx')</code>
</ul>


<br>

<pre>
run_program.<b>run_r(program, options, *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.R'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_r(program = 'script.R')</code>
</ul>


<br>

<pre>
run_program.<b>run_sas(program, lst = '', *settings)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.sas'`. Status messages are appended to make log `makelog`.
<ul>
<b>Example:</b>
<br>
<code>run_sas(program = 'script.sas')</code>
</ul>


<br>

#### Settings

* `osname` : str
    * Name of OS. Defaults to `os.name`.

* `shell` : bool
    * For more information on shell execution, see <a href = 'https://docs.python.org/2/library/subprocess.html#frequently-used-arguments'>here</a>.

* `makelog` : str
    * Path of make log to append outputs. Defaults to '../log/make.log'. To prevent appending outputs to make log, set `makelog` = ''.

* `log` : str
    * Path of program log to write outputs. Defaults to '' (i.e., not written).

* `executable` : str
    * Executable to use for system command. Default executable depends on application.

    <pre>
    default_executables = {
        'posix': 
            {'stata'     : 'statamp',
             'matlab'    : 'matlab',
             'perl'      : 'perl',
             'python'    : 'python',
             'math'      : 'math',
             'st'        : 'st',
             'lyx'       : 'lyx',
             'r'         : 'Rscript',
             'sas'       : 'sas'},
        'nt': 
            {'stata'     : '%STATAEXE%',
             'matlab'    : 'matlab',
             'perl'      : 'perl',
             'python'    : 'python',
             'math'      : 'math',
             'st'        : 'st',
             'lyx'       : 'lyx',
             'r'         : 'Rscript',
             'sas'       : 'sas'}
    }
    </pre>

* `option` : str
    * Options for system command. Default option depends on application.

    <pre>
    default_options = {
        'posix': 
            {'stata'     : '-e',
             'matlab'    : '-nosplash -nodesktop',
             'perl'      : '',
             'python'    : '',
             'math'      : '-noprompt',
             'st'        : '',
             'lyx'       : '-e pdf2',
             'r'         : '--no-save',
             'sas'       : ''},
        'nt': 
            {'stata'     : '/e',
             'matlab'    : '-nosplash -minimize -wait',
             'perl'      : '',
             'python'    : '',
             'math'      : '-noprompt',
             'st'        : '',
             'lyx'       : '-e pdf2',
             'r'         : '--no-save',
             'sas'       : '-nosplash'}
    }
    </pre>

* `args`
    * Arguments for system command. Defaults to no arguments.