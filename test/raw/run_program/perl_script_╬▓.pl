use strict;
use warnings;
 
my $output = 'output/output.txt';
open(my $fh, '>', $output) or die "Could not open file '$output' $!";
print $fh join('\n', (1..10));
close $fh;
print 'Test script complete β';