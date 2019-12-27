use strict;
use warnings;
 
my $output = 'test/output/output.csv';
open(my $fh, '>', $output) or die "Could not open file '$output' $!";
print $fh join('\n', (1..10));
close $fh;
print 'Test script complete';