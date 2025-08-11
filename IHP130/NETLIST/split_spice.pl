#!/bin/perl
#
# usage
# perl split_spice.pl spice.sp

open(IN, "$ARGV[0]") || die "cannot open file $ARGV[0], die\n";

my @INA=<IN>;

my $write_flag = 0;
for(my $i=0; $i<=$#INA; $i++){
	my $line      = $INA[$i];
	my $line_next = $INA[$i+1];
	my $lib_name;
	
	if($line =~ /\* Library name/){
  	$write_flag = 1;
		my @sparray = split(/ /,$line_next);
		chomp($sparray[3]);
		my $ofile = $sparray[3].".spi";
		open(OUT, ">$ofile") || die "cannot open file $ofile, die\n";
		printf("$sparray[0]\n");
		printf("$sparray[1]\n");
		printf("$sparray[2]\n");
		printf("file $ofile is opened\n");
	}
	if($write_flag == 1){
		printf OUT ($line);	
	}
	if($line =~ /\* End of subcircuit definition./){
  	$write_flag = 0;
		close(OUT);
		printf("file $ofile is closed\n");
	}
}

