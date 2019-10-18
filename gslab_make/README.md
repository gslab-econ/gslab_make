

# Linking functions

<b>The following functions are used to create symbolic links to source files. Doing so avoids potential duplication of source files and any associated confusion. In the case of modules dedicated to LyX documents, there is a optional function to copy source files instead of creating symbolic links so that users without </b><code>gslab_make</code><b> can still manually compile.</b>

<br>

<pre>
move_sources.<b>link_inputs(</b><i>
    paths = {
        input_dir,
        makelog,
    }, 
    file_list, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Create symbolic links using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Defaults to no string formatting. Symbolic links are written in directory `input_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create symbolic links (destinations) from targets (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>link_inputs(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create symbolic links.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Symbolic links <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['input_dir']</code>. Their targets would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following symbolic links in <code>paths['input_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

<pre>
move_sources.<b>link_externals(</b><i>
    paths = {
        external_dir,
        makelog,
    }, 
    file_list, 
    path_mappings</i><b>
)</b> 
</pre>
> Create symbolic links using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Symbolic links are written in directory `external_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create symbolic links (destinations) from targets (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>link_externals(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create symbolic links.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Symbolic links <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['external_dir']</code>. Their targets would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following symbolic links in <code>paths['external_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

<pre>
move_sources.<b>copy_inputs(</b><i>
    paths = {
        input_dir,
        makelog,
    }, 
    file_list, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Create copies using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Defaults to no string formatting. Copies are written in directory `input_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create copies (destinations) from orginals (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>copy_inputs(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create copies.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Copies <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['input_dir']</code>. Their originals would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following copies in <code>paths['input_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

<pre>
move_sources.<b>copy_externals(</b><i>
    paths = {
        external_dir,
        makelog,
    }, 
    file_list, 
    path_mappings = {}</i><b>
)</b> 
</pre>
> Create copies using instructions contained in files of list `file_list`. Instructions are string formatted using dictionary `path_mappings`. Defaults to no string formatting. Copies are written in directory `external_dir`. Status messages are appended to make log `makelog`.

<ul>
<b>Notes:</b>
<br>
Instruction files on how to create copies (destinations) from orginals (sources) should be formatted in the following way:
<br>
<code># Each line of instruction should contain a destination and source delimited by a `|`</code>
<br>
<code># Lines beginning with # are ignored</code>
<br>
<code>destination | source</code>
<br>
<br>
Instruction files can be specified with the * shell pattern (see <a href = 'https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html'>here</a>).
<br>
<br>
Destinations and their sources can also be specified with the * shell pattern. The number of wildcards must be the same for both destinations and sources.
<br>
<br>
<b>Example 1:</b>
<br>
<code>copy_externals(paths, ['file1', 'file2'])</code> uses instruction files <code>'file1'</code> and <code>'file2'</code> to create copies.
<br>
<br>
Suppose instruction file <code>'file1'</code> contained the following text:
<br>
<code>destination1 | source1</code>
<br>
<code>destination2 | source2</code>
<br>
<br>
Copies <code>destination1</code> and <code>destination1</code> would be created in directory <code>paths['external_dir']</code>. Their originals would be <code>source1</code> and <code>source2</code>, respectively. 
<br>
<br>
<b>Example 2:</b>
<br>
Suppose you have the following targets:
<br>
<code>source1</code>
<br>
<code>source2</code>
<br>
<code>source3</code>
<br>
<br>
Specifying <code>destination* | source*</code> in one of your instruction files would create the following copies in <code>paths['external_dir']</code>:
<br>
<code>destination1</code>
<br>
<code>destination2</code>
<br>
<code>destination3</code>
</pre>
</ul>

<br>

# Source logging functions

<b>The following function is used to log linking/copying activity and information about source files. The logs are intended to facilitate the reproducibility of research.</b>

<br>

<pre>
write_source_logs.<b>write_source_logs(</b><i>
    paths = {
        source_statslog,
        source_headslog, 
        source_maplog,
        makelog,
    }, 
    move_map, 
    depth = float('inf')</i><b>
)</b>
</pre>

> Logs the following information for files contained in all mappings of list `move_map` (returned by `move_sources.link_inputs`, `move_sources.copy_inputs`, `move_sources.link_externals`):
> 
> * Mapping of symbolic links/copies to sources (in file `source_maplog`)
>
> * Details on files contained in sources:          
>
>     * File name (in file `source_statslog`)
>
>     * Last modified (in file `source_statslog`)
>
>     * File size (in file `source_statslog`)
>
>     * File head (in file `source_headslog`)
>
> When walking through sources, float `depth` determines level of depth to walk. Status messages are appended to make log `makelog`.

<ul>
<b>Example:</b>
<br>
<code>write_source_logs(paths, move_map, depth = 1)</code> will log information for all source files listed in <code>move_map</code>.
<br>
<br>
<code>write_source_logs(paths, move_map, depth = 2)</code> will log information for all source files listed in <code>move_map</code>, and all files contained in any source directories listed in <code>move_map</code>.
<br>
<br>
<code>write_source_logs(paths, move_map, depth = float('inf'))</code> will log information for all source files listed in <code>move_map</code>, and all files contained in any level of source directories listed in <code>move_map</code>.
</ul>

<br> 



