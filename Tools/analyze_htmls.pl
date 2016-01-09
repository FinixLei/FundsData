our @dir_set = ();
our %total_hash = ();

sub get_files($) {
    ($dir) = @_;
    
    opendir(DIR,$dir) || die "Can not open $dir. $!\n";    
    my @all_entries = grep(!/^\.\.?$/,readdir(DIR));
    closedir(DIR);

    foreach my $entry (@all_entries) {
        $entry=join('/',($dir,$entry));
        
        if(-d $entry) {
            push(@dir_set, $entry);
        } 
        elsif(-f $entry) {
            read_file($entry);
        }
    }
    
    my $size = @dir_set; 
    if ($size != 0) {
        my $dir_entry = pop(@dir_set);
        get_files($dir_entry);
    }
}

sub read_file($) {
    ($PathName) = @_;
    
    my $year = '????'; 
    if ($PathName =~ /.+?\/(\d{4})-\d{2}-\d{2}_.+/) {
        $year = $1;
    }
    
    open(FILEHANDLE, $PathName) || die "Can't open $PathName: $@.";
    my @content = <FILEHANDLE>;
    close(FILEHANDLE);
    
    my $size = @content;
    my $hit_flag = 0;
    my $i = 0;
    
    while ($i < $size) {
        my $line = $content[$i];
        chomp($line);
        
        my ($date, $id, $title, $value);
        
        if ($line =~ /^\s*\<tr\>\s*/) {  # <tr>
            if ($content[$i + 2] =~ /\s*\<td.*?\>(.+)\<\/td\>/) {
                $date = "${year}-$1";
            } else {
                $i += 2;
                next;
            }
            if ($content[$i + 3] =~ /\s*\<td.*?\>(\d+)\<\/td\>/) {
                $id = $1;
            } else {
                $i += 3;
                next;
            }
            if ($content[$i + 4] =~ /\s*\<td.*?\>.*?title=\"(.+?)的历史收益情况\".+?\<\/td\>/) {
                $title = $1;
            } else {
                $i += 4;
                next;
            }
            if ($content[$i + 5] =~ /\s*\<td.*?\>(.+)\<\/td\>/) {
                $value = $1;
            } else {
                $i += 5;
                next;
            }
            
            $hit_flag = 1;
            $i += 6;
        } else {
            $hit_flag = 0;
            $i++;
        }
        
        if ($hit_flag) {
            if (exists $total_hash{$id}) {
                $total_hash{$id}{$date} = $value;
            } else {
                my %temp_hash = ();
                $total_hash{$id} = \%temp_hash;
                $total_hash{$id}{'title'} = $title;
                $total_hash{$id}{$date} = $value;
            }
        }
    }
}

sub print_total_hash() {
    print "{\n";
    
    foreach my $key (sort keys %total_hash) {
        print '"', ${key},'": {', "\n";
        
        if (exists $total_hash{$key}{'title'}) {
            print '    "title": "', $total_hash{$key}{'title'}, '",', "\n";
        }
        
        foreach my $date (sort keys $total_hash{$key}) {
            if ($date != 'title') {
                print '    "', ${date}, '": ', $total_hash{$key}{$date}, ",\n";
            }
        }
        print "},\n";
    }
    
    print "}\n";
}

##### Main Body #####

get_files("/tmp/FundsData/web_pages");
print_total_hash();
