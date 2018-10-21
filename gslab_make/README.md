# Logging functions

<b>The following functions are used to create a master log of activity (i.e., a <i>make log</i>) and to log information about output files. The logs are intended to facilitate the reproducibility of research.</b>

<br>

<pre>
write_logs.<b>start_makelog(</b><i>paths = {makelog: '../log/make.log'}</i><b>)</b>
</pre>
> Starts new make log at file `makelog`, recording start time. Sets start condition for make log to boolean `True`, which is needed by other functions to confirm make log exists.

<br>

<pre>
write_logs.<b>end_makelog(</b><i>paths = {makelog: '../log/make.log'}</i><b>)</b>
</pre>
> Ends make log at file `makelog`, recording end time. 

<br>

<pre>
write_logs.<b>log_files_in_output(</b><i> 
    paths = {
        output_dir: '../output/',
        output_statslog: '../log/output_stats.log', 
        output_headslog: '../log/output_heads.log', 
        makelog: '../log/make.log'
    }, 
    recursive = float('inf'),</i><b>
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
> When walking through directory `output_dir`, float `recursive` determines level of depth to walk. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>write_output_logs(recursive = 1)</code> will log information for all files contained in '../output/'.
<br>
<br>
<code>write_output_logs(recursive = 2)</code> will log information for all files contained in '../output/' and all files contained in any directories in '../output/.
<br>
<br>
<code>write_output_logs(recursive = inf(float))</code> will log information for all files contained in any level of '../output/'.
</ul>

<br>

# Linking functions

<b>The following function is used to create symbolic links to input files. Doing so avoids potential duplication of input files and any associated confusion.</b>

<br>

<pre>
create_links.<b>create_links(</b><i>
	paths = {
        link_dir: '../input/', 
	    makelog: '../log/make.log'
    }, 
    file_list</i><b>
)</b> 
</pre>
> Create symbolic links using instructions contained in files of list `file_list`. Symbolic links are written in directory `link_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create symbolic links should be formatted in the following way:
<br>
<code># Each line of instruction should contain a symbolic link and target delimited by a tab</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>symlink  target</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Symbolic links and their targets can also be specified with the * shell pattern. The number of wildcards must be the same for both symbolic links and targets.
<br>
<br>
<b>Example 1:</b>
<br>
<code>create_links(['file1', 'file2'])</code> uses instruction files 'file1' and 'file2' to create symbolic links.
<br>
<br>
Suppose instruction file 'file1' contained the following text:
<br>
<code>symlink1  target1</code>
<br>
<code>symlink2  target2</code>
<br>
<br>
Symbolic links <code>symlink1</code> and <code>symlink2</code> would be created in directory <code>link_dir</code>. Their targets would be <code>target1</code> and <code>target2</code>, respectively. 
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
Specifying <code>symlink*   target*</code> in one of your instruction files would create the following symbolic links in <code>link_dir</code>:
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

<b>The following function is used to log linking activity and information about input files. The logs are intended to facilitate the reproducibility of research.</b>

<br>

<pre>
write_link_logs.<b>write_link_logs(</b><i>
    paths = {
        link_statslog = '../log/link_stats.log', 
        link_headslog = '../log/link_heads.log', 
        link_maplog = '../log/link_map.log', 
        makelog = '../log/make.log'
    }, 
    link_map, 
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
> When walking through targets, float `recursive` determines level of depth to walk. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>write_link_logs(recursive = 1)</code> will log information for all link mappings and target files linked in '../input/'.
<br>
<br>
<code>write_link_logs(recursive = 2)</code> will log information for all link mappings, target files linked in '../input/', and files contained in target directories linked in '../input/'.
<br>
<br>
<code>write_link_logs(recursive = inf(float))</code> will log information for all link mappings, target files linked in '../input/', and files contained in any level of target directories linked in '../input/'.
</ul>

<br> 

# Program functions

<b>The following functions are used to run system commands or programs for certain applications.</b>

<br>

<pre>
run_program.<b>execute_command(</b><i>
    paths = {makelog: '../log/make.log'}, 
    command, 
    osname = os.name, 
    shell = False, 
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
<b>Example:</b> 
<br>
<code>execute_command(paths = {makelog: ''}, 'ls', log = 'file')</code> executes the 'ls' command, writes outputs to program log 'file', but does not append status messages or outputs to make log.
</ul>

<br> 

<b>Unless specified otherwise, the following program functions will use default settings to run your program. See the setting section below for more information.</b>

<br>

<pre>
run_program.<b>run_lyx(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    doctype = '', 
    pdfout = '', 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.lyx'`. Status messages are appended to make log `makelog`.
>
> LyX-specific settings:
>
> * `doctype` : str
>
>     * Type of LyX document. Takes either `handout` and `comments`. Defaults to no special document type.
>
> * `pdfout` : str
>
>     * Directory to write PDF. Defaults to '../output/' if no special document type, '../temp/' otherwise.
>

<ul>
<b>Example:</b>
<br>
<code>run_lyx(paths = {makelog: '../log/make.log'}, program = 'script.lyx')</code>
</ul>

<br>

<pre>
run_program.<b>run_mathematica(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.m'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_mathematica(paths = {makelog: '../log/make.log'}, program = 'script.m')</code>
</ul>

<br>

<pre>
run_program.<b>run_matlab(</b><i>
     paths = {makelog: '../log/make.log'}, 
     program, 
     *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.m'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_matlab(paths = {makelog: '../log/make.log'}, program = 'script.m')</code>
</ul>

<br>

<pre>
run_program.<b>run_perl(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.pl'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_perl(paths = {makelog: '../log/make.log'}, program = 'script.pl')</code>
</ul>

<br>

<pre>
run_program.<b>run_python(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.py'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_python(paths = {makelog: '../log/make.log'}, program = 'script.py')</code>
</ul>

<br>

<pre>
run_program.<b>run_r(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.R'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_r(paths = {makelog: '../log/make.log'}, program = 'script.R')</code>
</ul>

<br>

<pre>
run_program.<b>run_sas(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    lst = '', 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.sas'`. Status messages are appended to make log `makelog`.
>
> SAS-specific settings:
>
> * `lst` : str
>
>     * Path of program lst to write outputs. Defaults to '' (i.e., not written).
>

<ul>
<b>Example:</b>
<br>
<code>run_sas(paths = {makelog: '../log/make.log'}, program = 'script.sas')</code>
</ul>

<br>

<pre>
run_program.<b>run_stat_transfer(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program,
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.stc'` or `'script.stcmd'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_stat_transfer(paths = {makelog: '../log/make.log'}, program = 'script.stc')</code>
</ul>

<br>

<pre>
run_program.<b>run_stata(</b><i>
    paths = {makelog: '../log/make.log'}, 
    program, 
    *settings</i><b>
)</b>
</pre>
> Runs script `program` using system command, with script specified in the form of `'script.do'`. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>run_stata(paths = {makelog: '../log/make.log'}, program = 'script.do')</code>
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
            {'lyx'       : 'lyx',
             'perl'      : 'perl',
             'python'    : 'python',
             'math'      : 'math',
             'matlab'    : 'matlab',
             'r'         : 'Rscript',
             'sas'       : 'sas', 
             'st'        : 'st',
             'stata'     : 'statamp'},
        'nt': 
            {'lyx'       : 'lyx',
             'perl'      : 'perl',
             'python'    : 'python',
             'matlab'    : 'matlab',
             'math'      : 'math',
             'r'         : 'Rscript',
             'sas'       : 'sas', 
             'st'        : 'st',
             'stata'     : '%STATAEXE%'}
    }
    </pre>

* `option` : str
    * Options for system command. Default option depends on application.

    <pre>
    default_options = {
        'posix': 
            {'lyx'       : '-e pdf2',
             'perl'      : '',
             'python'    : '',
             'math'      : '-noprompt',
             'matlab'    : '-nosplash -nodesktop',
             'r'         : '--no-save',
             'st'        : '',
             'sas'       : '', 
             'stata'     : '-e'},
        'nt': 
            {'lyx'       : '-e pdf2',
             'perl'      : '',
             'python'    : '',
             'matlab'    : '-nosplash -minimize -wait',
             'math'      : '-noprompt',
             'r'         : '--no-save',
             'st'        : '',
             'sas'       : '-nosplash', 
             'stata'     : '/e'}
    }
    </pre>

* `args`
    * Arguments for system command. Defaults to no arguments.

# Directory functions

<b>The following functions are used to make modifications to a directory. Functions to check operating system, clear directories, and zip/unzip files are included.</b>

<br>

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