#!/usr/bin/perl -w
use strict;

my $usage = "usage: ./total_bp.pl <features>\n";
die $usage unless @ARGV == 1;

my ($feature)=@ARGV;
open(PARA,$feature) || die "can not open the file $feature\n";;

my $total_bp = 0;
while(<PARA>)
{
    chomp;
    my $l_now = $_;
    if($l_now =~ /^chr\w+\s+(\d+)\s+(\d+)/){
	if(abs($2-$1) >= 3){
	    $total_bp += ($2 - $1 +1);
	}
    }
}

print "$feature 's total bps = $total_bp\n";
